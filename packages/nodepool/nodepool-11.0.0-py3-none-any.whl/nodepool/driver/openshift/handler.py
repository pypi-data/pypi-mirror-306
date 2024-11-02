# Copyright 2018 Red Hat
# Copyright 2023 Acme Gating, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import math
import logging

from kazoo import exceptions as kze

from nodepool import exceptions
from nodepool.zk import zookeeper as zk
from nodepool.driver import NodeRequestHandler
from nodepool.driver.utils import NodeLauncher, QuotaInformation


class OpenshiftLauncher(NodeLauncher):
    def __init__(self, handler, node, provider_config, provider_label):
        super().__init__(handler, node, provider_config)
        self.label = provider_label
        self._retries = provider_config.launch_retries

    def _launchLabel(self):
        self.log.debug("Creating resource")
        project = "%s-%s" % (self.handler.pool.name, self.node.id)
        self.node.external_id = self.handler.manager.createProject(
            self.node, self.handler.pool.name, project, self.label,
            self.handler.request)
        self.zk.storeNode(self.node)

        resource = self.handler.manager.prepareProject(project)
        if self.label.type == "pod":
            self.handler.manager.createPod(
                self.node, self.handler.pool.name,
                project, self.label.name, self.label, self.handler.request)
            self.handler.manager.waitForPod(project, self.label.name)
            resource['pod'] = self.label.name
            self.node.connection_type = "kubectl"
            self.node.interface_ip = self.label.name
        else:
            self.node.connection_type = "project"

        self.node.state = zk.READY
        self.node.python_path = self.label.python_path
        self.node.shell_type = self.label.shell_type
        # NOTE: resource access token may be encrypted here
        self.node.connection_port = resource
        pool = self.handler.provider.pools.get(self.node.pool)
        self.node.resources = self.handler.manager.quotaNeededByLabel(
            self.node.type[0], pool).get_resources()
        self.node.cloud = self.provider_config.context
        self.zk.storeNode(self.node)
        self.log.info("Resource %s is ready", project)

    def launch(self):
        attempts = 1
        while attempts <= self._retries:
            try:
                self._launchLabel()
                break
            except kze.SessionExpiredError:
                # If we lost our ZooKeeper session, we've lost our node lock
                # so there's no need to continue.
                raise
            except Exception as e:
                if attempts <= self._retries:
                    self.log.exception(
                        "Launch attempt %d/%d failed for node %s:",
                        attempts, self._retries, self.node.id)
                # If we created an instance, delete it.
                if self.node.external_id:
                    self.handler.manager.cleanupNode(self.node.external_id)
                    self.handler.manager.waitForNodeCleanup(
                        self.node.external_id)
                    self.node.external_id = None
                    self.node.interface_ip = None
                    self.zk.storeNode(self.node)
                if 'exceeded quota' in str(e).lower():
                    self.log.info("%s: quota exceeded", self.node.id)
                    raise exceptions.QuotaException("Quota exceeded")
                if attempts == self._retries:
                    raise
                attempts += 1


class OpenshiftNodeRequestHandler(NodeRequestHandler):
    log = logging.getLogger("nodepool.driver.openshift."
                            "OpenshiftNodeRequestHandler")

    def __init__(self, pw, request):
        super().__init__(pw, request)
        self._threads = []

    @property
    def alive_thread_count(self):
        count = 0
        for t in self._threads:
            if t.is_alive():
                count += 1
        return count

    def imagesAvailable(self):
        return True

    def launchesComplete(self):
        '''
        Check if all launch requests have completed.

        When all of the Node objects have reached a final state (READY or
        FAILED), we'll know all threads have finished the launch process.
        '''
        if not self._threads:
            return True

        # Give the NodeLaunch threads time to finish.
        if self.alive_thread_count:
            return False

        node_states = [node.state for node in self.nodeset]

        # NOTE: It's very important that NodeLauncher always sets one of
        # these states, no matter what.
        if not all(s in (zk.READY, zk.FAILED, zk.ABORTED)
                   for s in node_states):
            return False

        return True

    def hasRemainingQuota(self, ntype):
        '''
        Checks if the predicted quota is enough for an additional node of type
        ntype.

        :param ntype: node type for the quota check
        :return: True if there is enough quota, False otherwise
        '''
        needed_quota = self.manager.quotaNeededByLabel(ntype, self.pool)

        # Calculate remaining quota which is calculated as:
        # quota = <total nodepool quota> - <used quota> - <quota for node>
        cloud_quota = self.manager.estimatedNodepoolQuota()
        cloud_quota.subtract(
            self.manager.estimatedNodepoolQuotaUsed())
        cloud_quota.subtract(needed_quota)
        self.log.debug("Predicted remaining provider quota: %s",
                       cloud_quota)

        if not cloud_quota.non_negative():
            return False

        # Now calculate pool specific quota. Values indicating no quota default
        # to math.inf representing infinity that can be calculated with.
        args = dict(cores=getattr(self.pool, 'max_cores', None),
                    instances=self.pool.max_servers,
                    ram=getattr(self.pool, 'max_ram', None))
        args.update(self.pool.max_resources)
        pool_quota = QuotaInformation(**args, default=math.inf)
        pool_quota.subtract(
            self.manager.estimatedNodepoolQuotaUsed(self.pool))
        self.log.debug("Current pool quota: %s" % pool_quota)
        pool_quota.subtract(needed_quota)
        self.log.debug("Predicted remaining pool quota: %s", pool_quota)

        return pool_quota.non_negative()

    def launch(self, node):
        label = self.pool.labels[node.type[0]]
        thd = OpenshiftLauncher(self, node, self.provider, label)
        thd.start()
        self._threads.append(thd)
