# Copyright (C) 2014 OpenStack Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import math
import time
import fixtures
import mock
import socket
import testtools

from nodepool import tests
import nodepool.exceptions
from nodepool.zk import zookeeper as zk
from nodepool.zk.components import PoolComponent
from nodepool.driver.statemachine import StateMachineProvider
from nodepool.driver.fake import adapter as fakeadapter
from nodepool.nodeutils import iterate_timeout
import nodepool.launcher
from nodepool.version import get_version_string

from kazoo import exceptions as kze


class TestLauncher(tests.DBTestCase):
    log = logging.getLogger("nodepool.TestLauncher")

    def setUp(self):
        super().setUp()

        StateMachineProvider.MINIMUM_SLEEP = 0.1
        StateMachineProvider.MAXIMUM_SLEEP = 1

    def test_node_assignment(self):
        '''
        Successful node launch should have unlocked nodes in READY state
        and assigned to the request.
        '''
        configfile = self.setup_config('node_no_min_ready.yaml')
        self.useBuilder(configfile)
        image = self.waitForImage('fake-provider', 'fake-image')
        self.assertEqual(image.username, 'fake-username')

        nodepool.launcher.LOCK_CLEANUP = 1
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label')
        req.tenant_name = 'tenant-1'
        req.requestor = 'unit-test'
        self.zk.storeNodeRequest(req)

        req = self.waitForNodeRequest(req)
        self.assertEqual(req.state, zk.FULFILLED)

        self.assertNotEqual(req.nodes, [])
        for node_id in req.nodes:
            node = self.zk.getNode(node_id)
            self.assertEqual(node.allocated_to, req.id)
            self.assertEqual(node.state, zk.READY)
            self.assertIsNotNone(node.launcher)
            self.assertEqual(node.cloud, 'fake')
            self.assertEqual(node.region, 'fake-region')
            self.assertEqual(node.az, "az1")
            self.assertEqual(node.username, "fake-username")
            self.assertEqual(node.connection_type, 'ssh')
            self.assertEqual(node.connection_port, 22)
            self.assertEqual(node.python_path, '/usr/bin/python3')
            self.assertEqual(node.tenant_name, 'tenant-1')
            self.assertEqual(node.requestor, 'unit-test')
            p = "{path}/{id}".format(
                path=self.zk._imageUploadPath(image.image_name,
                                              image.build_id,
                                              image.provider_name),
                id=image.id)
            self.assertEqual(node.image_id, p)
            resources = {
                'cores': 4,
                'instances': 1,
                'ram': 8192,
            }
            self.assertEqual(node.resources, resources)

            # We check the "cloud" side attributes are set from nodepool side
            provider = pool.getProviderManager('fake-provider')
            cloud_node = provider.adapter._getServer(node.external_id)
            self.assertEqual(
                cloud_node['metadata']['nodepool_provider_name'],
                'fake-provider')
            self.assertEqual(cloud_node['metadata']['nodepool_pool_name'],
                             'main')
            self.assertEqual(cloud_node['metadata']['prop1'], 'foo')
            self.assertEqual(cloud_node['metadata']['dynamic-tenant'],
                             'Tenant is tenant-1')

            self.zk.lockNode(node, blocking=False)
            self.zk.unlockNode(node)

        # Verify the cleanup thread removed the lock
        self.assertIsNotNone(
            self.zk.kazoo_client.exists(self.zk._requestLockPath(req.id))
        )
        self.zk.deleteNodeRequest(req)
        self.waitForNodeRequestLockDeletion(req.id)
        self.assertReportedStat('nodepool.nodes.ready', value='1', kind='g')
        self.assertReportedStat('nodepool.nodes.building', value='0', kind='g')
        self.assertReportedStat('nodepool.label.fake-label.nodes.ready',
                                value='1', kind='g')

        # Verify that we correctly initialized unused label stats to 0
        self.assertReportedStat('nodepool.label.fake-label2.nodes.building',
                                value='0', kind='g')
        self.assertReportedStat('nodepool.label.fake-label2.nodes.testing',
                                value='0', kind='g')
        self.assertReportedStat('nodepool.label.fake-label2.nodes.ready',
                                value='0', kind='g')
        self.assertReportedStat('nodepool.label.fake-label2.nodes.in-use',
                                value='0', kind='g')
        self.assertReportedStat('nodepool.label.fake-label2.nodes.used',
                                value='0', kind='g')
        self.assertReportedStat('nodepool.label.fake-label2.nodes.hold',
                                value='0', kind='g')
        self.assertReportedStat('nodepool.label.fake-label2.nodes.deleting',
                                value='0', kind='g')
        self.assertReportedStat('nodepool.label.fake-label2.nodes.failed',
                                value='0', kind='g')
        self.assertReportedStat('nodepool.label.fake-label2.nodes.init',
                                value='0', kind='g')
        self.assertReportedStat('nodepool.label.fake-label2.nodes.aborted',
                                value='0', kind='g')

        hostname = socket.gethostname()
        # Only check for presence since other threads could have
        # outstanding requests and we don't know the value.
        self.assertReportedStat(f'nodepool.launcher.{hostname}.zk'
                                '.client.connection_queue')
        self.assertReportedStat(f'nodepool.launcher.{hostname}.zk'
                                '.node_cache.event_queue',
                                value='0', kind='g')
        self.assertReportedStat(f'nodepool.launcher.{hostname}.zk'
                                '.node_cache.playback_queue',
                                value='0', kind='g')
        self.assertReportedStat(f'nodepool.launcher.{hostname}.zk'
                                '.request_cache.event_queue',
                                value='0', kind='g')
        self.assertReportedStat(f'nodepool.launcher.{hostname}.zk'
                                '.request_cache.playback_queue',
                                value='0', kind='g')
        self.assertReportedStat(f'nodepool.launcher.{hostname}.zk'
                                '.image_cache.event_queue',
                                value='0', kind='g')
        self.assertReportedStat(f'nodepool.launcher.{hostname}.zk'
                                '.image_cache.playback_queue',
                                value='0', kind='g')

    def test_node_assignment_order(self):
        """Test that nodes are assigned in the order requested"""
        configfile = self.setup_config('node_many_labels.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')

        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        self.waitForNodes('fake-label1')
        self.waitForNodes('fake-label2')
        self.waitForNodes('fake-label3')
        self.waitForNodes('fake-label4')

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label3')
        req.node_types.append('fake-label1')
        req.node_types.append('fake-label4')
        req.node_types.append('fake-label2')
        self.zk.storeNodeRequest(req)

        req = self.waitForNodeRequest(req)
        self.assertEqual(req.state, zk.FULFILLED)
        self.assertEqual(4, len(req.nodes))
        nodes = []
        for node_id in req.nodes:
            nodes.append(self.zk.getNode(node_id))
        self.assertEqual(nodes[0].type, ['fake-label3'])
        self.assertEqual(nodes[1].type, ['fake-label1'])
        self.assertEqual(nodes[2].type, ['fake-label4'])
        self.assertEqual(nodes[3].type, ['fake-label2'])
        self.assertEqual(nodes[0].python_path, 'auto')

    def _test_node_assignment_at_quota(self,
                                       config,
                                       max_cores=100,
                                       max_instances=20,
                                       max_ram=1000000,
                                       max_volumes=100,
                                       max_volume_gb=1000000):
        '''
        Successful node launch should have unlocked nodes in READY state
        and assigned to the request. This should be run with a quota that
        fits for two nodes.
        '''

        # patch the cloud with requested quota
        def fake_get_quota():
            return (max_cores, max_instances, max_ram)

        def fake_get_volume_quota():
            return (max_volumes, max_volume_gb)

        self.useFixture(fixtures.MockPatchObject(
            fakeadapter.FakeAdapter.fake_cloud, '_get_quota',
            fake_get_quota
        ))
        self.useFixture(fixtures.MockPatchObject(
            fakeadapter.FakeAdapter.fake_cloud, '_get_volume_quota',
            fake_get_volume_quota
        ))

        configfile = self.setup_config(config)
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')

        nodepool.launcher.LOCK_CLEANUP = 1
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        client = pool.getProviderManager('fake-provider').adapter._getClient()

        req1 = zk.NodeRequest()
        req1.state = zk.REQUESTED
        req1.node_types.append('fake-label')
        req1.node_types.append('fake-label')
        self.zk.storeNodeRequest(req1)

        self.log.debug("Waiting for 1st request %s", req1.id)
        req1 = self.waitForNodeRequest(req1, (zk.FULFILLED,))
        self.assertEqual(len(req1.nodes), 2)

        # Mark the first request's nodes as in use so they won't be deleted
        # when we pause. Locking them is enough.
        req1_node1 = self.zk.getNode(req1.nodes[0])
        req1_node2 = self.zk.getNode(req1.nodes[1])
        self.zk.lockNode(req1_node1, blocking=False)
        self.zk.lockNode(req1_node2, blocking=False)

        # One of the things we want to test is that if we spawn many
        # node launches at once, we do not deadlock while the request
        # handler pauses for quota.  To ensure we test that case,
        # pause server creation until we have accepted all of the node
        # requests we submit.  This will ensure that we hold locks on
        # all of the nodes before pausing so that we can validate they
        # are released.
        req2 = zk.NodeRequest()
        req2.state = zk.REQUESTED
        req2.node_types.append('fake-label')
        req2.node_types.append('fake-label')
        self.zk.storeNodeRequest(req2)
        req2 = self.waitForNodeRequest(req2, (zk.PENDING,))

        # At this point, we should have already created two servers for the
        # first request, and the request handler has accepted the second node
        # request but paused waiting for the server count to go below quota.
        # Wait until there is a paused request handler and check if there
        # are exactly two servers
        pool_worker = pool.getPoolWorkers('fake-provider')
        while not pool_worker[0].paused_handlers:
            time.sleep(0.1)
        self.assertEqual(len(client._server_list), 2)

        # Mark the first request's nodes as USED, which will get them deleted
        # and allow the second to proceed.
        self.log.debug("Marking first node as used %s", req1.id)
        req1_node1.state = zk.USED
        self.zk.storeNode(req1_node1)
        self.zk.unlockNode(req1_node1)
        self.waitForNodeDeletion(req1_node1)

        # To force the sequential nature of what we're testing, wait for
        # the 2nd request to get a node allocated to it now that we've
        # freed up a node.
        self.log.debug("Waiting for node allocation for 2nd request")
        done = False
        while not done:
            for n in self.zk.nodeIterator():
                if n.allocated_to == req2.id:
                    done = True
                    break

        self.log.debug("Marking second node as used %s", req1.id)
        req1_node2.state = zk.USED
        self.zk.storeNode(req1_node2)
        self.zk.unlockNode(req1_node2)
        self.waitForNodeDeletion(req1_node2)

        self.log.debug("Deleting 1st request %s", req1.id)
        self.zk.deleteNodeRequest(req1)
        self.waitForNodeRequestLockDeletion(req1.id)

        req2 = self.waitForNodeRequest(req2, (zk.FULFILLED,))
        self.assertEqual(len(req2.nodes), 2)

    def test_node_assignment_at_pool_quota_cores(self):
        self._test_node_assignment_at_quota(
            config='node_quota_pool_cores.yaml')

    def test_node_assignment_at_pool_quota_instances(self):
        self._test_node_assignment_at_quota(
            config='node_quota_pool_instances.yaml')

    def test_node_assignment_at_pool_quota_ram(self):
        self._test_node_assignment_at_quota(
            config='node_quota_pool_ram.yaml')

    def test_node_assignment_at_pool_quota_volumes(self):
        self._test_node_assignment_at_quota(
            config='node_quota_pool_volumes.yaml')

    def test_node_assignment_at_pool_quota_volume_gb(self):
        self._test_node_assignment_at_quota(
            config='node_quota_pool_volume_gb.yaml')

    def _test_node_assignment_at_tenant_quota(self, config):
        configfile = self.setup_config(config)
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')

        nodepool.launcher.LOCK_CLEANUP = 1
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        # wait for min-ready nodes if configured
        # node requests must be deferred when at tenant quota even if there
        # are ready nodes available
        min_ready = pool.config.labels['fake-label'].min_ready
        if min_ready:
            self.waitForNodes('fake-label', min_ready)

        # request some nodes for tenant-1 which has a limit
        req1_tenant1 = zk.NodeRequest()
        req1_tenant1.state = zk.REQUESTED
        req1_tenant1.tenant_name = 'tenant-1'
        req1_tenant1.node_types.append('fake-label')
        req1_tenant1.node_types.append('fake-label')
        self.zk.storeNodeRequest(req1_tenant1)

        # request some more nodes for tenant-1 which is now at quota
        req2_tenant1 = zk.NodeRequest()
        req2_tenant1.state = zk.REQUESTED
        req2_tenant1.tenant_name = 'tenant-1'
        req2_tenant1.node_types.append('fake-label')
        req2_tenant1.node_types.append('fake-label')
        self.zk.storeNodeRequest(req2_tenant1)

        # request more nodes for tenant-2 which has no limit
        req3_tenant2 = zk.NodeRequest()
        req3_tenant2.state = zk.REQUESTED
        req3_tenant2.tenant_name = 'tenant-2'
        req3_tenant2.node_types.append('fake-label')
        req3_tenant2.node_types.append('fake-label')
        req3_tenant2.node_types.append('fake-label')
        req3_tenant2.node_types.append('fake-label')
        self.zk.storeNodeRequest(req3_tenant2)

        # nodes for req1 should be fulfilled right away
        self.log.debug("Waiting for 1st request %s", req1_tenant1.id)
        req1_tenant1 = self.waitForNodeRequest(req1_tenant1, (zk.FULFILLED,))
        self.assertEqual(len(req1_tenant1.nodes), 2)

        # also nodes from req2 (another thenant) should be fulfilled
        self.log.debug("Waiting for 2nd request %s", req3_tenant2.id)
        req1_tenant2 = self.waitForNodeRequest(req3_tenant2, (zk.FULFILLED,))
        self.assertEqual(len(req1_tenant2.nodes), 4)

        # Mark the first request's nodes as in use so they won't be deleted
        # when we pause. Locking them is enough.
        req1_node1 = self.zk.getNode(req1_tenant1.nodes[0])
        req1_node2 = self.zk.getNode(req1_tenant1.nodes[1])
        self.zk.lockNode(req1_node1, blocking=False)
        self.zk.lockNode(req1_node2, blocking=False)

        # nodes from req3 should stay in reuqested state until req1 nodes
        # are removed
        self.log.debug("Waiting for 3rd request %s", req2_tenant1.id)
        req2_tenant1 = self.waitForNodeRequest(req2_tenant1, (zk.REQUESTED,))
        self.assertEqual(len(req2_tenant1.nodes), 0)

        # mark nodes from req1 as used and have them deleted
        for node in (req1_node1, req1_node2):
            node.state = zk.USED
            self.zk.storeNode(node)
            self.zk.unlockNode(node)
            self.waitForNodeDeletion(node)

        # now the 3rd request (tenant-1) should be fulfilled
        self.log.debug("Waiting for 3rd request %s", req2_tenant1.id)
        req2_tenant1 = self.waitForNodeRequest(req2_tenant1, (zk.FULFILLED,))
        self.assertEqual(len(req2_tenant1.nodes), 2)

    def test_node_assignment_at_tenant_quota_cores(self):
        self._test_node_assignment_at_tenant_quota(
            'node_quota_tenant_cores.yaml')
        self.assertReportedStat('nodepool.tenant_limits.tenant-1.cores',
                                value='8', kind='g')

    def test_node_assignment_at_tenant_quota_instances(self):
        self._test_node_assignment_at_tenant_quota(
            'node_quota_tenant_instances.yaml')
        self.assertReportedStat('nodepool.tenant_limits.tenant-1.instances',
                                value='2', kind='g')

    def test_node_assignment_at_tenant_quota_ram(self):
        self._test_node_assignment_at_tenant_quota(
            'node_quota_tenant_ram.yaml')
        self.assertReportedStat('nodepool.tenant_limits.tenant-1.ram',
                                value='16384', kind='g')

    def test_node_assignment_at_tenant_quota_volumes(self):
        self._test_node_assignment_at_tenant_quota(
            'node_quota_tenant_volumes.yaml')
        self.assertReportedStat('nodepool.tenant_limits.tenant-1.volumes',
                                value='2', kind='g')

    def test_node_assignment_at_tenant_quota_volume_gb(self):
        self._test_node_assignment_at_tenant_quota(
            'node_quota_tenant_volume_gb.yaml')
        self.assertReportedStat('nodepool.tenant_limits.tenant-1.volume-gb',
                                value='20', kind='g')

    def test_node_assignment_at_tenant_quota_min_ready(self):
        self._test_node_assignment_at_tenant_quota(
            'node_quota_tenant_min_ready.yaml')
        self.assertReportedStat('nodepool.tenant_limits.tenant-1.instances',
                                value='2', kind='g')

    def test_node_assignment_at_cloud_cores_quota(self):
        self._test_node_assignment_at_quota(config='node_quota_cloud.yaml',
                                            max_cores=8,
                                            # check that -1 and inf work for no
                                            # quota
                                            max_instances=-1,
                                            max_ram=math.inf)

    def test_node_assignment_at_cloud_instances_quota(self):
        self._test_node_assignment_at_quota(config='node_quota_cloud.yaml',
                                            max_cores=math.inf,
                                            max_instances=2,
                                            max_ram=math.inf)

    def test_node_assignment_at_cloud_ram_quota(self):
        self._test_node_assignment_at_quota(config='node_quota_cloud.yaml',
                                            max_cores=math.inf,
                                            max_instances=math.inf,
                                            max_ram=2 * 8192)

    def test_node_assignment_at_cloud_volumes_quota(self):
        self._test_node_assignment_at_quota(
            config='node_quota_cloud_volumes.yaml',
            max_volumes=2)

    def test_node_assignment_at_cloud_volume_gb_quota(self):
        self._test_node_assignment_at_quota(
            config='node_quota_cloud_volumes.yaml',
            max_volume_gb=20)

    def test_decline_at_quota(self):
        '''test that a provider at quota continues to decline requests'''

        # patch the cloud with requested quota
        def fake_get_quota():
            return (math.inf, 1, math.inf)
        self.useFixture(fixtures.MockPatchObject(
            fakeadapter.FakeAdapter.fake_cloud, '_get_quota',
            fake_get_quota
        ))

        configfile = self.setup_config('node_quota_tenant_instances.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')

        nodepool.launcher.LOCK_CLEANUP = 1
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        req1 = zk.NodeRequest()
        req1.state = zk.REQUESTED
        req1.node_types.append('fake-label')
        self.zk.storeNodeRequest(req1)

        self.log.debug("Waiting for 1st request %s", req1.id)
        req1 = self.waitForNodeRequest(req1, (zk.FULFILLED,))
        self.assertEqual(len(req1.nodes), 1)

        # Mark the first request's nodes as in use so they won't be deleted
        # when we pause. Locking them is enough.
        req1_node1 = self.zk.getNode(req1.nodes[0])
        self.zk.lockNode(req1_node1, blocking=False)

        req2 = zk.NodeRequest()
        req2.state = zk.REQUESTED
        req2.node_types.append('fake-label')
        self.zk.storeNodeRequest(req2)
        self.log.debug("Waiting for 2nd request %s", req2.id)
        req2 = self.waitForNodeRequest(req2, (zk.PENDING,))

        req3 = zk.NodeRequest()
        req3.state = zk.REQUESTED
        req3.node_types.append('invalid-label')
        self.zk.storeNodeRequest(req3)
        self.log.debug("Waiting for 3rd request %s", req3.id)
        req3 = self.waitForNodeRequest(req3, (zk.FAILED,))

        # Make sure req2 is still pending.
        req2 = self.waitForNodeRequest(req2, (zk.PENDING,))

    def test_over_quota(self, config='node_quota_cloud.yaml'):
        '''
        This tests what happens when a cloud unexpectedly returns an
        over-quota error.

        '''
        # Start with an instance quota of 2
        max_cores = math.inf
        max_instances = 2
        max_ram = math.inf

        # patch the cloud with requested quota
        def fake_get_quota():
            nonlocal max_cores, max_instances, max_ram
            return (max_cores, max_instances, max_ram)
        self.useFixture(fixtures.MockPatchObject(
            fakeadapter.FakeAdapter.fake_cloud, '_get_quota',
            fake_get_quota
        ))

        configfile = self.setup_config(config)
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')

        nodepool.launcher.LOCK_CLEANUP = 1
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        client = pool.getProviderManager('fake-provider').adapter._getClient()

        # Wait for a single node to be created
        req1 = zk.NodeRequest()
        req1.state = zk.REQUESTED
        req1.node_types.append('fake-label')
        self.log.debug("Adding first request")
        self.zk.storeNodeRequest(req1)
        req1 = self.waitForNodeRequest(req1)
        self.assertEqual(req1.state, zk.FULFILLED)

        # Lock this node so it appears as used and not deleted
        req1_node = self.zk.getNode(req1.nodes[0])
        self.zk.lockNode(req1_node, blocking=False)

        # Now, reduce the quota so the next node unexpectedly
        # (according to nodepool's quota estimate) fails.
        max_instances = 1

        # Request a second node; this request should pause the handler.
        req2 = zk.NodeRequest()
        req2.state = zk.REQUESTED
        req2.node_types.append('fake-label')
        self.log.debug("Adding second request")
        self.zk.storeNodeRequest(req2)

        pool_worker = pool.getPoolWorkers('fake-provider')
        while not pool_worker[0].paused_handlers:
            time.sleep(0.1)

        # The handler is paused now and the request should be in state PENDING
        req2 = self.waitForNodeRequest(req2, zk.PENDING)
        self.assertEqual(req2.state, zk.PENDING)

        # Now free up the first node
        self.log.debug("Marking first node as used %s", req1.id)
        req1_node.state = zk.USED
        self.zk.storeNode(req1_node)
        self.zk.unlockNode(req1_node)
        self.waitForNodeDeletion(req1_node)

        # After the first node is cleaned up the second request should be
        # able to fulfill now.
        req2 = self.waitForNodeRequest(req2)
        self.assertEqual(req2.state, zk.FULFILLED)

        self.assertEqual(len(client._server_list), 1)

    def test_fail_request_on_launch_failure(self):
        '''
        Test that provider launch error fails the request.
        '''
        configfile = self.setup_config('node_launch_retry.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')

        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        manager = pool.getProviderManager('fake-provider')
        manager.adapter.createServer_fails = 2

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label')
        self.zk.storeNodeRequest(req)

        req = self.waitForNodeRequest(req)
        self.assertEqual(0, manager.adapter.createServer_fails)
        self.assertEqual(req.state, zk.FAILED)
        self.assertNotEqual(req.declined_by, [])

    def test_fail_request_on_launch_timeout(self):
        '''
        Test that provider launch timeout fails the request.
        '''
        configfile = self.setup_config('node_launch_timeout.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')

        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        manager = pool.getProviderManager('fake-provider')
        client = pool.getProviderManager('fake-provider').adapter._getClient()
        client._create_server_timeout = 2

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label')
        self.zk.storeNodeRequest(req)

        req = self.waitForNodeRequest(req)
        self.assertEqual(0, manager.adapter.createServer_fails)
        self.assertEqual(req.state, zk.FAILED)
        self.assertNotEqual(req.declined_by, [])

    def test_az_change_recover(self):
        '''
        Test that nodepool recovers from az change in the cloud.
        '''
        configfile = self.setup_config('node_az_change.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')

        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label')
        self.zk.storeNodeRequest(req)

        req = self.waitForNodeRequest(req)
        self.assertEqual(req.state, zk.FULFILLED)

        # now change the azs in the cloud
        cloud = pool.getProviderManager('fake-provider').adapter._getClient()
        cloud._azs = ['new-az1', 'new-az2']

        # Do a second request. This will fail because the cached azs are not
        # available anymore.
        # TODO(tobiash): Ideally we should already be able to already recover
        # this request.
        req2 = zk.NodeRequest()
        req2.state = zk.REQUESTED
        req2.node_types.append('fake-label')
        self.zk.storeNodeRequest(req2)
        req2 = self.waitForNodeRequest(req2)
        self.assertEqual(req2.state, zk.FAILED)

        # Create a third request to test that nodepool successfully recovers
        # from a stale az cache.
        req3 = zk.NodeRequest()
        req3.state = zk.REQUESTED
        req3.node_types.append('fake-label')
        self.zk.storeNodeRequest(req3)
        req3 = self.waitForNodeRequest(req3)
        self.assertEqual(req3.state, zk.FULFILLED)

        node = self.zk.getNode(req3.nodes[0])
        self.assertIn(node.az, ['new-az1', 'new-az2'])

    def test_fail_minready_request_at_capacity(self):
        '''
        A min-ready request to a provider that is already at capacity should
        be declined.
        '''
        configfile = self.setup_config('node_min_ready_capacity.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        # Get an initial node ready
        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append("fake-label")
        self.zk.storeNodeRequest(req)
        req = self.waitForNodeRequest(req)
        self.assertEqual(req.state, zk.FULFILLED)

        # Now simulate a min-ready request
        min_ready_req = zk.NodeRequest()
        min_ready_req.state = zk.REQUESTED
        min_ready_req.node_types.append("fake-label")
        min_ready_req.requestor = "NodePool:min-ready"
        self.zk.storeNodeRequest(min_ready_req)
        min_ready_req = self.waitForNodeRequest(min_ready_req)
        self.assertEqual(min_ready_req.state, zk.FAILED)
        self.assertNotEqual(min_ready_req.declined_by, [])

    def test_invalid_image_fails(self):
        '''
        Test that an invalid image declines and fails the request.
        '''
        configfile = self.setup_config('node.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append("zorky-zumba")
        self.zk.storeNodeRequest(req)

        req = self.waitForNodeRequest(req)
        self.assertEqual(req.state, zk.FAILED)
        self.assertNotEqual(req.declined_by, [])

    def test_node(self):
        """Test that an image and node are created"""
        configfile = self.setup_config('node.yaml')
        builder = self.useBuilder(configfile)
        image = self.waitForImage('fake-provider', 'fake-image')
        self.assertEqual(image.username, 'zuul')

        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        provider = (builder._upload_workers[0]._config.
                    provider_managers['fake-provider'])
        cloud_image = provider.adapter._findImage(image.external_id)
        self.assertEqual(
            cloud_image._kw.get('diskimage_metadata'), 'diskimage')
        self.assertEqual(
            cloud_image._kw.get('provider_metadata'), 'provider')

        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].provider, 'fake-provider')
        self.assertEqual(nodes[0].type, ['fake-label'])
        self.assertEqual(nodes[0].username, 'zuul')
        self.assertNotEqual(nodes[0].host_keys, [])
        self.assertEqual(nodes[0].attributes,
                         {'key1': 'value1', 'key2': 'value2'})

    def test_node_metadata(self):
        """Test that node metadata is set"""
        configfile = self.setup_config('node.yaml')
        self.useBuilder(configfile)
        image = self.waitForImage('fake-provider', 'fake-image')
        self.assertEqual(image.username, 'zuul')

        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        nodes = self.waitForNodes('fake-label')

        self.assertEqual(len(nodes), 1)

        # We check the "cloud" side attributes are set from nodepool side
        provider = pool.getProviderManager('fake-provider')
        cloud_node = provider.adapter._getServer(nodes[0].external_id)
        self.assertEqual(
            cloud_node['metadata']['nodepool_provider_name'],
            'fake-provider')
        self.assertEqual(cloud_node['metadata']['nodepool_pool_name'], 'main')
        self.assertEqual(cloud_node['metadata']['prop1'], 'foo')
        self.assertEqual(cloud_node['metadata']['dynamic-tenant'],
                         'Tenant is None')

    def test_node_network_cli(self):
        """Same as test_node but using connection-type network_cli"""
        configfile = self.setup_config('node-network_cli.yaml')
        self.useBuilder(configfile)
        image = self.waitForImage('fake-provider', 'fake-image')
        self.assertEqual(image.username, 'zuul')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        nodes = self.waitForNodes('fake-label')

        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].provider, 'fake-provider')
        self.assertEqual(nodes[0].type, ['fake-label'])
        self.assertEqual(nodes[0].username, 'zuul')
        self.assertNotEqual(nodes[0].host_keys, [])
        self.assertEqual(nodes[0].attributes,
                         {'key1': 'value1', 'key2': 'value2'})

    def test_node_host_key_checking_false(self):
        """Test that images and nodes are created"""
        configfile = self.setup_config('node-host-key-checking.yaml')
        self.useBuilder(configfile)
        image = self.waitForImage('fake-provider', 'fake-image')
        self.assertEqual(image.username, 'zuul')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        label1_nodes = self.waitForNodes('fake-label')
        label2_nodes = self.waitForNodes('fake-label2')

        self.assertEqual(len(label1_nodes), 1)
        self.assertEqual(label1_nodes[0].provider, 'fake-provider')
        self.assertEqual(label1_nodes[0].type, ['fake-label'])
        self.assertEqual(label1_nodes[0].username, 'zuul')
        # We have no host_keys because pool.host-key-checking is False.
        self.assertEqual(label1_nodes[0].host_keys, [])

        self.assertEqual(len(label2_nodes), 1)
        self.assertEqual(label2_nodes[0].provider, 'fake-provider2')
        self.assertEqual(label2_nodes[0].type, ['fake-label2'])
        self.assertEqual(label2_nodes[0].username, 'zuul')
        # We have no host_keys because label.host-key-checking is False.
        self.assertEqual(label2_nodes[0].host_keys, [])

    def test_multiple_launcher(self):
        """Test that an image and node are created with 2 launchers"""
        # nodepool-builder needs access to both providers to upload images
        configfile = self.setup_config('node_two_provider.yaml')
        self.useBuilder(configfile)
        # Validate we have images in both providers
        image1 = self.waitForImage('fake-provider', 'fake-image')
        self.assertEqual(image1.username, 'zuul')
        image2 = self.waitForImage('fake-provider2', 'fake-image')
        self.assertEqual(image2.username, 'zuul')
        # Start up first launcher
        configfile1 = self.setup_config('node.yaml')
        pool1 = self.useNodepool(configfile1, watermark_sleep=1)
        self.startPool(pool1)
        # Start up second launcher
        configfile2 = self.setup_config('node_second_provider.yaml')
        pool2 = self.useNodepool(configfile2, watermark_sleep=1)
        self.startPool(pool2)

        # We don't need to check which provider launched the min-ready, just
        # that one was launched.
        nodes = self.waitForNodes('fake-label', 1)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].type, ['fake-label'])
        self.assertEqual(nodes[0].username, 'zuul')
        self.assertNotEqual(nodes[0].host_keys, [])

    def test_node_request_provider(self):
        """Test that a node request for a specific provider is honored"""
        configfile = self.setup_config('node_two_provider.yaml')
        self.useBuilder(configfile)
        # Validate we have images in both providers
        self.waitForImage('fake-provider', 'fake-image')
        self.waitForImage('fake-provider2', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        self.waitForNodes('fake-label', 1)

        req1 = zk.NodeRequest()
        req1.state = zk.REQUESTED
        req1.provider = 'fake-provider'
        req1.node_types.append('fake-label')
        self.zk.storeNodeRequest(req1)

        req2 = zk.NodeRequest()
        req2.state = zk.REQUESTED
        req2.provider = 'fake-provider2'
        req2.node_types.append('fake-label')
        self.zk.storeNodeRequest(req2)

        req1 = self.waitForNodeRequest(req1)
        self.assertEqual(req1.state, zk.FULFILLED)
        self.assertEqual(len(req1.nodes), 1)
        node = self.zk.getNode(req1.nodes[0])
        self.assertEqual(node.provider, 'fake-provider')

        req2 = self.waitForNodeRequest(req2)
        self.assertEqual(req2.state, zk.FULFILLED)
        self.assertEqual(len(req2.nodes), 1)
        node = self.zk.getNode(req2.nodes[0])
        self.assertEqual(node.provider, 'fake-provider2')

    def test_node_request_invalid_provider(self):
        """Test that a node request for a missing provider is handled"""
        configfile = self.setup_config('node_two_provider.yaml')
        self.useBuilder(configfile)
        # Validate we have images in both providers
        self.waitForImage('fake-provider', 'fake-image')
        self.waitForImage('fake-provider2', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        self.waitForNodes('fake-label', 1)

        req1 = zk.NodeRequest()
        req1.state = zk.REQUESTED
        req1.provider = 'missing-provider'
        req1.node_types.append('fake-label')
        self.zk.storeNodeRequest(req1)

        req1 = self.waitForNodeRequest(req1)
        self.assertEqual(req1.state, zk.FULFILLED)
        self.assertEqual(len(req1.nodes), 1)
        self.zk.getNode(req1.nodes[0])

    def test_node_request_provider_label_mismatch(self):
        """Test that a node request for a specific provider is only honored
        when the requested labels are supported."""
        configfile = self.setup_config('node.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        self.waitForNodes('fake-label', 1)

        # Create a dummy launcher with a different set of supported labels
        # than what we are going to request.
        hostname = socket.gethostname()
        dummy_component = PoolComponent(
            self.zk.client, hostname,
            version=get_version_string())
        dummy_component.content.update({
            'id': 'dummy',
            'provider_name': 'other-provider',
            'supported_labels': ['other-label'],
            'state': dummy_component.RUNNING,
        })
        dummy_component.register()

        # Node request for a specific provider that doesn't support the
        # requested node type.
        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.provider = 'other-provider'
        req.node_types.append('fake-label')
        self.zk.storeNodeRequest(req)

        req = self.waitForNodeRequest(req)
        self.assertEqual(req.state, zk.FULFILLED)
        self.assertEqual(len(req.nodes), 1)
        self.zk.getNode(req.nodes[0])
        dummy_component.unregister()

    def test_node_boot_from_volume(self):
        """Test that an image and node are created from a volume"""
        configfile = self.setup_config('node_boot_from_volume.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        nodes = self.waitForNodes('fake-label')

        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].provider, 'fake-provider')
        self.assertEqual(nodes[0].type, ['fake-label'])

    def test_disabled_label(self):
        """Test that a node is not created with min-ready=0"""
        configfile = self.setup_config('node_disabled_label.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        self.assertEqual([], self.zk.getNodeRequests())
        self.assertEqual([], self.zk.getNodes())

    def test_node_net_name(self):
        """Test that a node is created with proper net name"""
        configfile = self.setup_config('node_net_name.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        label1_nodes = self.waitForNodes('fake-label1')
        label2_nodes = self.waitForNodes('fake-label2')

        self.assertEqual(len(label1_nodes), 1)
        self.assertEqual(len(label2_nodes), 1)

        # ipv6 address unavailable
        self.assertEqual(label1_nodes[0].provider, 'fake-provider')
        self.assertEqual(label1_nodes[0].public_ipv4, 'fake')
        self.assertEqual(label1_nodes[0].public_ipv6, '')
        self.assertEqual(label1_nodes[0].interface_ip, 'fake')
        self.assertEqual(label1_nodes[0].host_id, 'fake')

        # ipv6 address available
        self.assertEqual(label2_nodes[0].provider, 'fake-provider')
        self.assertEqual(label2_nodes[0].public_ipv4, 'fake')
        self.assertEqual(label2_nodes[0].public_ipv6, 'fake_v6')
        self.assertEqual(label2_nodes[0].interface_ip, 'fake_v6')
        self.assertEqual(label2_nodes[0].host_id, 'fake_host_id')

    def test_node_security_group(self):
        """Test that an image and node are created with sec_group specified"""
        configfile = self.setup_config('node_security_group.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        nodes = self.waitForNodes('fake-label')
        nodes_def_sg = self.waitForNodes('fake-label2')
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].provider, 'fake-provider')
        self.assertEqual(len(nodes_def_sg), 1)
        self.assertEqual(nodes_def_sg[0].provider, 'fake-provider')
        client = pool.getProviderManager('fake-provider').adapter._getClient()
        for server in client._server_list:
            if server.id == nodes[0].external_id:
                self.assertEqual(server.security_groups, ['fake-sg'])
            elif server.id == nodes_def_sg[0].external_id:
                self.assertEqual(server.security_groups, [])

    def test_node_flavor_name(self):
        """Test that a node is created with a flavor name"""
        configfile = self.setup_config('node_flavor_name.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].provider, 'fake-provider')
        self.assertEqual(nodes[0].type, ['fake-label'])

    def test_node_vhd_image(self):
        """Test that a image and node are created vhd image"""
        configfile = self.setup_config('node_vhd.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].provider, 'fake-provider')
        self.assertEqual(nodes[0].type, ['fake-label'])

    def test_node_vhd_and_qcow2(self):
        """Test label provided by vhd and qcow2 images builds"""
        configfile = self.setup_config('node_vhd_and_qcow2.yaml')
        self.useBuilder(configfile)
        p1_image = self.waitForImage('fake-provider1', 'fake-image')
        p2_image = self.waitForImage('fake-provider2', 'fake-image')

        # We can't guarantee which provider would build the requested
        # nodes, but that doesn't matter so much as guaranteeing that the
        # correct image type is uploaded to the correct provider.
        self.assertEqual(p1_image.format, "vhd")
        self.assertEqual(p2_image.format, "qcow2")

    def test_dib_upload_fail(self):
        """Test that an image upload failure is contained."""
        configfile = self.setup_config('node_upload_fail.yaml')
        self.useBuilder(configfile, num_uploaders=2)
        self.waitForImage('fake-provider2', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        nodes = self.waitForNodes('fake-label', 2)
        self.assertEqual(len(nodes), 2)
        total_nodes = sum(1 for _ in self.zk.nodeIterator())
        self.assertEqual(total_nodes, 2)
        self.assertEqual(nodes[0].provider, 'fake-provider2')
        self.assertEqual(nodes[0].type, ['fake-label'])
        self.assertEqual(nodes[0].username, 'zuul')
        self.assertEqual(nodes[1].provider, 'fake-provider2')
        self.assertEqual(nodes[1].type, ['fake-label'])
        self.assertEqual(nodes[1].username, 'zuul')

    def test_node_az(self):
        """Test that an image and node are created with az specified"""
        configfile = self.setup_config('node_az.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].provider, 'fake-provider')
        self.assertEqual(nodes[0].az, 'az1')

    def test_node_ipv6(self):
        """Test that ipv6 existence either way works fine."""
        configfile = self.setup_config('node_ipv6.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider1', 'fake-image')
        self.waitForImage('fake-provider2', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        label1_nodes = self.waitForNodes('fake-label1')
        label2_nodes = self.waitForNodes('fake-label2')

        self.assertEqual(len(label1_nodes), 1)
        self.assertEqual(len(label2_nodes), 1)

        # ipv6 address available
        self.assertEqual(label1_nodes[0].provider, 'fake-provider1')
        self.assertEqual(label1_nodes[0].public_ipv4, 'fake')
        self.assertEqual(label1_nodes[0].public_ipv6, 'fake_v6')
        self.assertEqual(label1_nodes[0].interface_ip, 'fake_v6')
        self.assertEqual(label1_nodes[0].host_id, 'fake_host_id')

        # ipv6 address unavailable
        self.assertEqual(label2_nodes[0].provider, 'fake-provider2')
        self.assertEqual(label2_nodes[0].public_ipv4, 'fake')
        self.assertEqual(label2_nodes[0].public_ipv6, '')
        self.assertEqual(label2_nodes[0].interface_ip, 'fake')
        self.assertEqual(label2_nodes[0].host_id, 'fake')

    def test_node_delete_success(self):
        configfile = self.setup_config('node.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)
        self.assertEqual(zk.READY, nodes[0].state)
        self.assertEqual('fake-provider', nodes[0].provider)
        nodes[0].state = zk.DELETING
        self.zk.storeNode(nodes[0])

        # Wait for this one to be deleted
        self.waitForNodeDeletion(nodes[0])

        # Wait for a new one to take it's place
        new_nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(zk.READY, new_nodes[0].state)
        self.assertEqual('fake-provider', new_nodes[0].provider)
        self.assertNotEqual(nodes[0], new_nodes[0])

    def test_node_delete_DELETED_success(self):
        """Test we treat a node in DELETING state as deleted"""
        configfile = self.setup_config('node.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)
        self.assertEqual(zk.READY, nodes[0].state)
        self.assertEqual('fake-provider', nodes[0].provider)

        # Get fake cloud record and set status to DELETING
        manager = pool.getProviderManager('fake-provider')
        for instance in manager.adapter._client._server_list:
            if instance.id == nodes[0].external_id:
                instance['status'] = 'DELETED'
                break

        nodes[0].state = zk.DELETING
        self.zk.storeNode(nodes[0])

        # Wait for this one to be deleted
        self.waitForNodeDeletion(nodes[0])

        api_record_remains = False
        for instance in manager.adapter._listServers():
            if instance['id'] == nodes[0].external_id:
                api_record_remains = True
                break
        self.assertTrue(api_record_remains)

        # Wait for a new one to take it's place
        new_nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(zk.READY, new_nodes[0].state)
        self.assertEqual('fake-provider', new_nodes[0].provider)
        self.assertNotEqual(nodes[0], new_nodes[0])

    def test_node_launch_retries(self):
        configfile = self.setup_config('node_launch_retry.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        manager = pool.getProviderManager('fake-provider')
        manager.adapter.createServer_fails = 2

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label')
        self.zk.storeNodeRequest(req)

        req = self.waitForNodeRequest(req)
        self.assertEqual(req.state, zk.FAILED)

        # retries in config is set to 2, so 2 attempts to create a server
        self.assertEqual(0, manager.adapter.createServer_fails)

    def _node_launch_keyscan_failure(self, count, result):
        # Test that a keyscan failure causes a retry
        counter = 0

        orig_advance = nodepool.driver.statemachine.NodescanRequest.advance

        def handler(*args, **kw):
            nonlocal counter, count
            counter += 1
            if counter <= count:
                raise nodepool.exceptions.ConnectionTimeoutException()
            return orig_advance(*args, **kw)

        self.useFixture(fixtures.MonkeyPatch(
            'nodepool.driver.statemachine.NodescanRequest.advance',
            handler))
        configfile = self.setup_config('node_no_min_ready.yaml')

        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')

        req1 = zk.NodeRequest()
        req1.state = zk.REQUESTED
        req1.node_types.append('fake-label')
        self.zk.storeNodeRequest(req1)

        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        req1 = self.waitForNodeRequest(req1)
        self.assertEqual(req1.state, result)

    def test_node_launch_keyscan_failure(self):
        # Test that a keyscan failure causes a retry
        self._node_launch_keyscan_failure(1, zk.FULFILLED)

    def test_node_launch_keyscan_failure_retry(self):
        # Test that a keyscan failure eventually fails after
        # exhausting retries
        self._node_launch_keyscan_failure(4, zk.FAILED)

    def test_node_launch_keyscan_failure_console_log(self):
        log_count = 0

        def fake_get_server_console(name_or_id):
            nonlocal log_count
            log_count += 1
            return f"TEST CONSOLE LOG {log_count}\nSECOND LINE {log_count}"

        with self.assertLogs("nodepool.StateMachineNodeLauncher.fake-provider",
                             level="INFO") as logs:
            self.useFixture(fixtures.MockPatchObject(
                fakeadapter.FakeAdapter.fake_cloud, '_get_server_console',
                fake_get_server_console
            ))
            self._node_launch_keyscan_failure(4, zk.FAILED)

            # Max attempts is 3 so there should be one console log for each
            # attempt
            self.assertEqual(log_count, 3)

            check_lines = {
                "TEST CONSOLE LOG 1",
                "SECOND LINE 1",
                "TEST CONSOLE LOG 2",
                "SECOND LINE 2",
                "TEST CONSOLE LOG 3",
                "SECOND LINE 3",
            }

            for line in logs.output:
                for c in check_lines:
                    if line.endswith(c):
                        check_lines.remove(c)
                        break

            self.assertFalse(check_lines)

    def test_node_launch_with_broken_znodes(self):
        """Test that node launch still works if there are broken znodes"""
        # Create a znode without type
        znode = zk.Node()
        znode.provider = 'fake-provider'
        znode.pool = 'main'
        znode.external_id = 'fakeid'
        znode.state = zk.READY

        # Create znode without pool
        self.zk.storeNode(znode)
        znode = zk.Node()
        znode.provider = 'fake-provider'
        znode.type = ['fake-label']
        znode.external_id = 'fakeid'
        znode.state = zk.READY
        self.zk.storeNode(znode)

        configfile = self.setup_config('node_launch_retry.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label')
        self.zk.storeNodeRequest(req)

        req = self.waitForNodeRequest(req)
        self.assertEqual(req.state, zk.FULFILLED)

    def test_node_launch_retries_with_external_id(self):
        configfile = self.setup_config('node_launch_retry.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        manager = pool.getProviderManager('fake-provider')
        manager.adapter.createServer_fails_with_external_id = 2

        # Stop the DeletedNodeWorker so we can make sure the fake znode that
        # is used to delete the failed servers is still around when requesting.
        # the second node.
        pool._delete_thread.stop()
        time.sleep(1)

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label')
        self.zk.storeNodeRequest(req)

        req = self.waitForNodeRequest(req)
        self.assertEqual(req.state, zk.FAILED)

        # retries in config is set to 2, so 2 attempts to create a server
        self.assertEqual(
            0, manager.adapter.createServer_fails_with_external_id)

        # Request another node to check if nothing is wedged
        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label')
        self.zk.storeNodeRequest(req)

        req = self.waitForNodeRequest(req)
        self.assertEqual(req.state, zk.FULFILLED)

    def test_node_delete_failure(self):
        def fail_delete(self, name):
            raise RuntimeError('Fake Error')

        self.useFixture(fixtures.MockPatchObject(
            fakeadapter.FakeAdapter, '_deleteServer', fail_delete))

        configfile = self.setup_config('node.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)

        self.zk.lockNode(nodes[0], blocking=False)

        pm = pool.getProviderManager('fake-provider')
        node_deleter = pm.startNodeCleanup(nodes[0])
        node_deleter.join()

        # Make sure our old node is in delete state, even though delete failed
        deleted_node = self.zk.getNode(nodes[0].id)
        self.assertIsNotNone(deleted_node)
        self.assertEqual(deleted_node.state, zk.DELETING)

        # Make sure we have a new, READY node
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].provider, 'fake-provider')

    def test_node_delete_error(self):
        def error_delete(self, name):
            # Set ERROR status instead of deleting the node
            self._client._server_list[0].status = 'ERROR'

        self.useFixture(fixtures.MockPatchObject(
            fakeadapter.FakeAdapter, '_deleteServer', error_delete))

        configfile = self.setup_config('node_delete_error.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        # request a node
        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label')
        self.zk.storeNodeRequest(req)
        self.log.debug("Wait for request")
        req = self.waitForNodeRequest(req)
        self.assertEqual(req.state, zk.FULFILLED)

        self.assertEqual(len(req.nodes), 1)

        # remove the node from db
        self.log.debug("deleting node %s", req.nodes[0])
        node = self.zk.getNode(req.nodes[0])
        self.zk.deleteNode(node)

        # wait the cleanup thread to kick in
        time.sleep(5)
        # Make sure it shows up as leaked
        manager = pool.getProviderManager('fake-provider')
        instances = list(manager.adapter.listInstances())
        self.assertEqual(1, len(instances))

    def test_leaked_node(self):
        """Test that a leaked node is deleted"""
        configfile = self.setup_config('leaked_node.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        self.log.debug("Waiting for initial pool...")
        nodes = self.waitForNodes('fake-label')
        self.log.debug("...done waiting for initial pool.")

        # Make sure we have a node built and ready
        self.assertEqual(len(nodes), 1)
        manager = pool.getProviderManager('fake-provider')
        servers = manager.adapter._listServers()
        self.assertEqual(len(servers), 1)

        # Delete the node from ZooKeeper, but leave the instance
        # so it is leaked.
        self.log.debug("Delete node db record so instance is leaked...")
        self.zk.deleteNode(nodes[0])
        self.log.debug("...deleted node db so instance is leaked.")

        # Wait for nodepool to replace it
        self.log.debug("Waiting for replacement pool...")
        new_nodes = self.waitForNodes('fake-label')
        self.log.debug("...done waiting for replacement pool.")
        self.assertEqual(len(new_nodes), 1)

        # Wait for the instance to be cleaned up
        self.waitForInstanceDeletion(manager, nodes[0].external_id)

        # Make sure we end up with only one server (the replacement)
        servers = manager.adapter._listServers()
        self.assertEqual(len(servers), 1)
        self.assertReportedStat(
            'nodepool.provider.fake-provider.leaked.instances',
            value='1', kind='c')

    def test_max_ready_age(self):
        """Test a node with exceeded max-ready-age is deleted"""
        configfile = self.setup_config('node_max_ready_age.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        self.log.debug("Waiting for initial pool...")
        nodes = self.waitForNodes('fake-label')
        self.log.debug("...done waiting for initial pool.")

        # Wait for the instance to be cleaned up
        manager = pool.getProviderManager('fake-provider')
        self.waitForInstanceDeletion(manager, nodes[0].external_id)

    def test_max_hold_age(self):
        """Test a held node with exceeded max-hold-age is deleted"""
        configfile = self.setup_config('node_max_hold_age.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        self.log.debug("Waiting for initial pool...")
        nodes = self.waitForNodes('fake-label')
        self.log.debug("...done waiting for initial pool.")
        node = nodes[0]
        self.log.debug("Holding node %s..." % node.id)
        # hold the node
        self.zk.lockNode(node, blocking=False)
        node.state = zk.HOLD
        node.comment = 'testing'
        self.zk.storeNode(node)
        self.zk.unlockNode(node)
        znode = self.zk.getNode(node.id)
        self.log.debug("Node %s in state '%s'" % (znode.id, znode.state))
        # Wait for the instance to be cleaned up
        manager = pool.getProviderManager('fake-provider')
        self.waitForInstanceDeletion(manager, node.external_id)

    def test_hold_expiration_no_default(self):
        """Test a held node is deleted when past its operator-specified TTL,
        no max-hold-age set"""
        configfile = self.setup_config('node_max_hold_age_no_default.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        self.log.debug("Waiting for initial pool...")
        nodes = self.waitForNodes('fake-label')
        self.log.debug("...done waiting for initial pool.")
        node = nodes[0]
        self.log.debug("Holding node %s..." % node.id)
        # hold the node
        self.zk.lockNode(node, blocking=False)
        node.state = zk.HOLD
        node.comment = 'testing'
        node.hold_expiration = 1
        self.zk.storeNode(node)
        self.zk.unlockNode(node)
        znode = self.zk.getNode(node.id)
        self.log.debug("Node %s in state '%s'" % (znode.id, znode.state))
        # Wait for the instance to be cleaned up
        manager = pool.getProviderManager('fake-provider')
        self.waitForInstanceDeletion(manager, node.external_id)

    def test_hold_expiration_str_type(self):
        """Test a held node is deleted when past its operator-specified TTL,
        even when the type is bad"""
        configfile = self.setup_config('node_max_hold_age_no_default.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        self.log.debug("Waiting for initial pool...")
        nodes = self.waitForNodes('fake-label')
        self.log.debug("...done waiting for initial pool.")
        node = nodes[0]
        self.log.debug("Holding node %s..." % node.id)
        # hold the node
        self.zk.lockNode(node, blocking=False)
        node.state = zk.HOLD
        node.comment = 'testing'
        node.hold_expiration = '1'
        self.zk.storeNode(node)
        self.zk.unlockNode(node)
        znode = self.zk.getNode(node.id)
        self.log.debug("Node %s in state '%s'" % (znode.id, znode.state))
        # Wait for the instance to be cleaned up
        manager = pool.getProviderManager('fake-provider')
        self.waitForInstanceDeletion(manager, node.external_id)

    def test_hold_expiration_bad_type_coercion(self):
        """Test a held node uses default expiration value when type is bad"""
        configfile = self.setup_config('node_max_hold_age_no_default.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        self.log.debug("Waiting for initial pool...")
        nodes = self.waitForNodes('fake-label')
        self.log.debug("...done waiting for initial pool.")
        node = nodes[0]
        self.log.debug("Holding node %s..." % node.id)
        # hold the node
        self.zk.lockNode(node, blocking=False)
        node.state = zk.HOLD
        node.comment = 'testing'
        node.hold_expiration = 'notanumber'
        self.zk.storeNode(node)
        self.zk.unlockNode(node)
        znode = self.zk.getNode(node.id)
        self.log.debug("Node %s in state '%s'" % (znode.id, znode.state))
        self.assertEqual(znode.hold_expiration, 0)

    def test_hold_expiration_lower_than_default(self):
        """Test a held node is deleted when past its operator-specified TTL,
        with max-hold-age set in the configuration"""
        configfile = self.setup_config('node_max_hold_age_2.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        self.log.debug("Waiting for initial pool...")
        nodes = self.waitForNodes('fake-label', 2)
        self.log.debug("...done waiting for initial pool.")
        node_custom = nodes[0]
        # TODO make it a fraction of fixture's max-hold-age
        hold_expiration = 2
        node = nodes[1]
        self.log.debug("Holding node %s... (default)" % node.id)
        self.log.debug("Holding node %s...(%s seconds)" % (node_custom.id,
                                                           hold_expiration))
        # hold the nodes
        self.zk.lockNode(node, blocking=False)
        node.state = zk.HOLD
        node.comment = 'testing'
        self.zk.storeNode(node)
        self.zk.unlockNode(node)
        self.zk.lockNode(node_custom, blocking=False)
        node_custom.state = zk.HOLD
        node_custom.comment = 'testing hold_expiration'
        node_custom.hold_expiration = hold_expiration
        self.zk.storeNode(node_custom)
        self.zk.unlockNode(node_custom)
        znode = self.zk.getNode(node.id)
        self.log.debug("Node %s in state '%s'" % (znode.id, znode.state))
        znode_custom = self.zk.getNode(node_custom.id)
        self.log.debug("Node %s in state '%s'" % (znode_custom.id,
                                                  znode_custom.state))
        # Wait for the instance to be cleaned up
        manager = pool.getProviderManager('fake-provider')
        self.waitForInstanceDeletion(manager, node_custom.external_id)
        # control node should still be held
        held_nodes = [n for n in self.zk.nodeIterator() if n.state == zk.HOLD]
        self.assertTrue(any(n.id == node.id for n in held_nodes),
                        held_nodes)
        # finally, control node gets deleted
        self.waitForInstanceDeletion(manager, node.external_id)

    def test_hold_expiration_higher_than_default(self):
        """Test a held node is deleted after max-hold-age seconds if the
        operator specifies a larger TTL"""
        configfile = self.setup_config('node_max_hold_age_2.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        self.log.debug("Waiting for initial pool...")
        nodes = self.waitForNodes('fake-label', 2)
        self.log.debug("...done waiting for initial pool.")
        node_custom = nodes[0]
        # Make hold expiration much larger than max hold age.
        hold_expiration = 180
        node = nodes[1]
        self.log.debug("Holding node %s... (default)" % node.id)
        self.log.debug("Holding node %s...(%s seconds)" % (node_custom.id,
                                                           hold_expiration))
        # hold the nodes
        self.zk.lockNode(node, blocking=False)
        node.state = zk.HOLD
        node.comment = 'testing'
        self.zk.storeNode(node)
        self.zk.unlockNode(node)
        self.zk.lockNode(node_custom, blocking=False)
        node_custom.state = zk.HOLD
        node_custom.comment = 'testing hold_expiration'
        node_custom.hold_expiration = hold_expiration
        self.zk.storeNode(node_custom)
        self.zk.unlockNode(node_custom)
        znode = self.zk.getNode(node.id)
        self.log.debug("Node %s in state '%s'" % (znode.id, znode.state))
        znode_custom = self.zk.getNode(node_custom.id)
        self.log.debug("Node %s in state '%s'" % (znode_custom.id,
                                                  znode_custom.state))
        # Wait for the instance to be cleaned up
        manager = pool.getProviderManager('fake-provider')
        self.waitForInstanceDeletion(manager, node.external_id)

        # The custom node should be deleted as well but it may be slightly
        # delayed after the other node. Because of that we have defined a much
        # higher hold time than the max hold age. So we can give nodepool a few
        # extra seconds to clean it up and still validate that the max hold
        # age is not violated.
        for _ in iterate_timeout(10, Exception, 'assert custom_node is gone'):
            try:
                held_nodes = [n for n in self.zk.nodeIterator(cached=False)
                              if n.state == zk.HOLD]
                self.assertEqual(0, len(held_nodes), held_nodes)
                break
            except AssertionError:
                # node still listed, retry
                pass

    def test_label_provider(self):
        """Test that only providers listed in the label satisfy the request"""
        configfile = self.setup_config('node_label_provider.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        self.waitForImage('fake-provider2', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].provider, 'fake-provider2')

    def _create_pending_request(self):
        req = zk.NodeRequest()
        req.state = zk.PENDING
        req.requestor = 'test_nodepool'
        req.node_types.append('fake-label')
        self.zk.storeNodeRequest(req)

        # Create a node that is allocated to the request, but not yet assigned
        # within the NodeRequest object
        node = zk.Node()
        node.state = zk.READY
        node.type = 'fake-label'
        node.public_ipv4 = 'fake'
        node.provider = 'fake-provider'
        node.pool = 'main'
        node.allocated_to = req.id
        self.zk.storeNode(node)

        return (req, node)

    def test_lost_requests(self):
        """Test a request left pending is reset and satisfied on restart"""
        (req, node) = self._create_pending_request()

        configfile = self.setup_config('node_lost_requests.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        req = self.waitForNodeRequest(req, (zk.FULFILLED,))
        # Since our config file has min-ready=0, we should be able to re-use
        # the previously assigned node, thus making sure that the cleanup
        # code reset the 'allocated_to' field.
        self.assertIn(node.id, req.nodes)

    def test_node_deallocation(self):
        """Test an allocated node with a missing request is deallocated"""
        node = zk.Node()
        node.state = zk.READY
        node.type = 'fake-label'
        node.public_ipv4 = 'fake'
        node.provider = 'fake-provider'
        node.allocated_to = "MISSING"
        self.zk.storeNode(node)

        configfile = self.setup_config('node_lost_requests.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.useBuilder(configfile)
        self.startPool(pool)

        while True:
            node = self.zk.getNode(node.id)
            if not node.allocated_to:
                break

    def test_multiple_pools(self):
        """Test that an image and node are created"""
        configfile = self.setup_config('multiple_pools.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        lab1 = self.waitForNodes('fake-label1')
        lab2 = self.waitForNodes('fake-label2')

        self.assertEqual(len(lab1), 1)
        self.assertEqual(lab1[0].provider, 'fake-provider')
        self.assertEqual(lab1[0].type, ['fake-label1'])
        self.assertEqual(lab1[0].az, 'az1')
        self.assertEqual(lab1[0].pool, 'pool1')

        self.assertEqual(len(lab2), 1)
        self.assertEqual(lab2[0].provider, 'fake-provider')
        self.assertEqual(lab2[0].type, ['fake-label2'])
        self.assertEqual(lab2[0].az, 'az2')
        self.assertEqual(lab2[0].pool, 'pool2')

    def test_unmanaged_image(self):
        """Test node launching using an unmanaged image"""
        configfile = self.setup_config('node_unmanaged_image.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)

        self.startPool(pool)
        manager = pool.getProviderManager('fake-provider')
        manager.adapter.IMAGE_CHECK_TIMEOUT = 1
        manager.adapter._client.create_image(name="fake-image")
        manager.adapter._client.create_image(name="fake-image-windows")
        manager.adapter._client.create_image(name="fake-image-windows-port")

        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)
        self.assertIsNone(nodes[0].username)
        self.assertEqual(nodes[0].python_path, '/usr/bin/python3')
        self.assertEqual(nodes[0].shell_type, 'csh')

        nodes = self.waitForNodes('fake-label-windows')
        self.assertEqual(len(nodes), 1)
        self.assertEqual('zuul', nodes[0].username)
        self.assertEqual('winrm', nodes[0].connection_type)
        self.assertEqual(5986, nodes[0].connection_port)
        self.assertEqual(nodes[0].host_keys, [])
        self.assertEqual(nodes[0].python_path, 'auto')
        self.assertIsNone(nodes[0].shell_type)

        nodes = self.waitForNodes('fake-label-arbitrary-port')
        self.assertEqual(len(nodes), 1)
        self.assertEqual('zuul', nodes[0].username)
        self.assertEqual('winrm', nodes[0].connection_type)
        self.assertEqual(1234, nodes[0].connection_port)
        self.assertEqual(nodes[0].host_keys, [])
        self.assertEqual(nodes[0].python_path, 'auto')
        self.assertIsNone(nodes[0].shell_type)

    def test_unmanaged_image_provider_name(self):
        """
        Test node launching using an unmanaged image referencing the
        image name as known by the provider.
        """
        configfile = self.setup_config('unmanaged_image_provider_name.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)

        self.startPool(pool)
        manager = pool.getProviderManager('fake-provider')
        manager.adapter.IMAGE_CHECK_TIMEOUT = 1
        manager.adapter._client.create_image(name="provider-named-image")

        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)

    def test_unmanaged_image_provider_id(self):
        """
        Test node launching using an unmanaged image referencing the
        image ID as known by the provider.
        """
        configfile = self.setup_config('unmanaged_image_provider_id.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        self.log.debug("Waiting for node")
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)

    def test_paused_gets_declined(self):
        """Test that a paused request, that later gets declined, unpauses."""

        # First config has max-servers set to 2
        configfile = self.setup_config('pause_declined_1.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        # Create a request that uses all capacity (2 servers)
        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label')
        req.node_types.append('fake-label')
        self.zk.storeNodeRequest(req)
        req = self.waitForNodeRequest(req)
        self.assertEqual(req.state, zk.FULFILLED)
        self.assertEqual(len(req.nodes), 2)

        # Now that we have 2 nodes in use, create another request that
        # requests two nodes, which should cause the request to pause.
        req2 = zk.NodeRequest()
        req2.state = zk.REQUESTED
        req2.node_types.append('fake-label')
        req2.node_types.append('fake-label')
        self.zk.storeNodeRequest(req2)
        req2 = self.waitForNodeRequest(req2, (zk.PENDING,))

        # Second config decreases max-servers to 1
        self.replace_config(configfile, 'pause_declined_2.yaml')

        # Because the second request asked for 2 nodes, but that now exceeds
        # max-servers, req2 should get declined now, and transition to FAILED
        req2 = self.waitForNodeRequest(req2, (zk.FAILED,))
        self.assertNotEqual(req2.declined_by, [])

    def test_node_auto_floating_ip(self):
        """Test that auto-floating-ip option works fine."""
        configfile = self.setup_config('node_auto_floating_ip.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider1', 'fake-image')
        self.waitForImage('fake-provider2', 'fake-image')
        self.waitForImage('fake-provider3', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        label1_nodes = self.waitForNodes('fake-label1')
        label2_nodes = self.waitForNodes('fake-label2')
        label3_nodes = self.waitForNodes('fake-label3')

        self.assertEqual(1, len(label1_nodes))
        self.assertEqual(1, len(label2_nodes))
        self.assertEqual(1, len(label3_nodes))

        # auto-floating-ip: False
        self.assertEqual('fake-provider1', label1_nodes[0].provider)
        self.assertEqual('', label1_nodes[0].public_ipv4)
        self.assertEqual('', label1_nodes[0].public_ipv6)
        self.assertEqual('fake', label1_nodes[0].interface_ip)

        # auto-floating-ip: True
        self.assertEqual('fake-provider2', label2_nodes[0].provider)
        self.assertEqual('fake', label2_nodes[0].public_ipv4)
        self.assertEqual('', label2_nodes[0].public_ipv6)
        self.assertEqual('fake', label2_nodes[0].interface_ip)

        # auto-floating-ip: default value
        self.assertEqual('fake-provider3', label3_nodes[0].provider)
        self.assertEqual('fake', label3_nodes[0].public_ipv4)
        self.assertEqual('', label3_nodes[0].public_ipv6)
        self.assertEqual('fake', label3_nodes[0].interface_ip)

    def test_secure_file(self):
        """Test using secure.conf file"""
        configfile = self.setup_config('secure_file_config.yaml')
        securefile = self.setup_secure('secure_file_secure.yaml')
        self.useBuilder(configfile, securefile=securefile)
        image = self.waitForImage('fake-provider', 'fake-image')
        pool = self.useNodepool(
            configfile,
            secure_conf=securefile,
            watermark_sleep=1)
        self.startPool(pool)

        fake_image = pool.config.diskimages['fake-image']
        self.assertIn('REG_PASSWORD', fake_image.env_vars)
        self.assertEqual('secret', fake_image.env_vars['REG_PASSWORD'])

        zk_servers = pool.config.zookeeper_servers
        expected = (f'{self.zookeeper_host}:{self.zookeeper_port}'
                    f'{self.zookeeper_chroot}')
        self.assertEqual(expected, zk_servers)

        self.assertEqual(image.username, 'zuul')
        nodes = self.waitForNodes('fake-label')

        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].provider, 'fake-provider')
        self.assertEqual(nodes[0].type, ['fake-label'])
        self.assertEqual(nodes[0].username, 'zuul')
        self.assertNotEqual(nodes[0].host_keys, [])

    def test_provider_removal(self):
        """Test that removing a provider stops the worker thread"""
        configfile = self.setup_config('launcher_two_provider.yaml')
        self.useBuilder(configfile)
        pool = self.useNodepool(configfile, watermark_sleep=.5)
        self.startPool(pool)
        self.waitForNodes('fake-label')
        self.assertEqual(2, len(pool._pool_threads))

        # We should have two pool workers registered
        self.assertEqual(2, len(self.zk.getRegisteredPools()))

        self.replace_config(configfile, 'launcher_two_provider_remove.yaml')

        # Our provider pool thread count should eventually be reduced to 1
        for _ in iterate_timeout(10, Exception,
                                 'provider pool threads to reduce to 1'):
            try:
                self.assertEqual(1, len(pool._pool_threads))
                break
            except AssertionError:
                pass

        # We should have one pool worker registered
        self.assertEqual(1, len(self.zk.getRegisteredPools()))

    def test_failed_provider(self):
        """Test that broken provider doesn't fail node requests."""
        configfile = self.setup_config('launcher_two_provider_max_1.yaml')
        self.useBuilder(configfile)
        # Steady state at images available.
        self.waitForImage('fake-provider', 'fake-image')
        self.waitForImage('fake-provider2', 'fake-image')

        pool = self.useNodepool(configfile, watermark_sleep=.5)
        self.startPool(pool)

        # We have now reached steady state and can manipulate the system to
        # test failing cloud behavior.

        # Make two requests so that the next requests are paused.
        # Note we use different provider specific labels here to avoid
        # a race where a single provider fulfills both of these initial
        # requests.

        # fake-provider
        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label2')
        self.zk.storeNodeRequest(req)
        req = self.waitForNodeRequest(req, zk.FULFILLED)

        # fake-provider2
        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label3')
        self.zk.storeNodeRequest(req)
        req = self.waitForNodeRequest(req, zk.FULFILLED)

        nodes = map(pool.zk.getNode, pool.zk.getNodes())
        provider1_first = None
        provider2_first = None
        for node in nodes:
            if node.provider == 'fake-provider2':
                provider2_first = node
            elif node.provider == 'fake-provider':
                provider1_first = node

        # Mark the nodes as being used so they won't be deleted at pause.
        # Locking them is enough.
        self.zk.lockNode(provider1_first, blocking=False)
        self.zk.lockNode(provider2_first, blocking=False)

        # Next two requests will go pending one for each provider.
        req1 = zk.NodeRequest()
        req1.state = zk.REQUESTED
        req1.node_types.append('fake-label')
        self.zk.storeNodeRequest(req1)
        req1 = self.waitForNodeRequest(req1, zk.PENDING)

        req2 = zk.NodeRequest()
        req2.state = zk.REQUESTED
        req2.node_types.append('fake-label')
        self.zk.storeNodeRequest(req2)
        req2 = self.waitForNodeRequest(req2, zk.PENDING)

        # Delete node attached to provider2 this will cause provider2 to
        # fulfill the request it had pending.
        provider2_first.state = zk.DELETING
        self.zk.storeNode(provider2_first)
        self.zk.unlockNode(provider2_first)
        self.waitForNodeDeletion(provider2_first)

        while True:
            # Wait for provider2 node to be created. Also find the request
            # that was not fulfilled. This is the request that fake-provider
            # is pending on.
            req = self.zk.getNodeRequest(req1.id)
            if req.state == zk.FULFILLED:
                final_req = req2
                break
            req = self.zk.getNodeRequest(req2.id)
            if req.state == zk.FULFILLED:
                final_req = req1
                break

        provider2_second = None
        nodes = map(pool.zk.getNode, pool.zk.getNodes())
        for node in nodes:
            if (node and node.provider == 'fake-provider2' and
                    node.state == zk.READY):
                provider2_second = node
                break

        # Now delete the new node we had provider2 build. At this point,
        # the only provider with any requests is fake-provider.
        provider2_second.state = zk.DELETING
        self.zk.storeNode(provider2_second)

        # Set provider1 runHandler to throw exception to simulate a
        # broken cloud. Note the pool worker instantiates request handlers on
        # demand which is why we have a somewhat convoluted monkey patch here.
        # We must patch deep enough in the request handler that
        # despite being paused fake-provider will still trip over this code.
        pool_worker = pool.getPoolWorkers('fake-provider')[0]
        request_handler = pool_worker.request_handlers[0]

        def raise_KeyError(node):
            raise KeyError('fake-provider')

        request_handler.launch = raise_KeyError

        # Delete instance in fake-provider. This should cause provider2
        # to service the request that was held pending by fake-provider.
        provider1_first.state = zk.DELETING
        self.zk.storeNode(provider1_first)
        self.zk.unlockNode(provider1_first)

        # Request is fulfilled by provider 2
        req = self.waitForNodeRequest(final_req)
        self.assertEqual(req.state, zk.FULFILLED)
        self.assertEqual(1, len(req.declined_by))
        self.assertIn('fake-provider-main', req.declined_by[0])

    def test_disabled_provider(self):
        '''
        A request should fail even with a provider that is disabled by
        setting max-servers to 0. Because we look to see that all providers
        decline a request by comparing the declined_by request attribute to
        the list of registered launchers, this means that each must attempt
        to handle it at least once, and thus decline it.
        '''
        configfile = self.setup_config('disabled_provider.yaml')
        self.useBuilder(configfile)
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label')
        self.zk.storeNodeRequest(req)

        req = self.waitForNodeRequest(req)
        self.assertEqual(req.state, zk.FAILED)

    def test_broken_provider(self):
        '''
        If a provider has a broken config, it should not be started, and
        any requests for it should be declined/failed.  Other
        providers should be started and should be able to fulfill
        requests.
        '''
        configfile = self.setup_config('broken_provider_config.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        manager = pool.getProviderManager('good-provider')
        manager.adapter._client.create_image(name="good-image")

        good_req = zk.NodeRequest()
        good_req.state = zk.REQUESTED
        good_req.node_types.append('good-label')
        self.zk.storeNodeRequest(good_req)

        broken_req = zk.NodeRequest()
        broken_req.state = zk.REQUESTED
        broken_req.node_types.append('broken-label')
        self.zk.storeNodeRequest(broken_req)

        good_req = self.waitForNodeRequest(good_req)
        broken_req = self.waitForNodeRequest(broken_req)
        self.assertEqual(good_req.state, zk.FULFILLED)
        self.assertEqual(broken_req.state, zk.FAILED)

    def test_provider_wont_wedge(self):
        '''
        A provider should not wedge itself when it is at (1) maximum capacity
        (# registered nodes == max-servers), (2) all of its current nodes are
        not being used, and (3) a request comes in with a label that it does
        not yet have available. Normally, situation (3) combined with (1)
        would cause the provider to pause until capacity becomes available,
        but because of (2), it never will and we would wedge the provider.
        '''
        configfile = self.setup_config('wedge_test.yaml')
        self.useBuilder(configfile)
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        # Wait for fake-label1 min-ready request to be fulfilled, which will
        # put us at maximum capacity with max-servers of 1.
        label1_nodes = self.waitForNodes('fake-label1')
        self.assertEqual(1, len(label1_nodes))

        # Now we submit a request for fake-label2, which is not yet available.
        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label2')
        self.zk.storeNodeRequest(req)

        # The provider should pause here to handle the fake-label2 request.
        # But because the fake-label1 node is not being used, and will never
        # be freed because we are paused and not handling additional requests,
        # the pool worker thread should recognize that and delete the unused
        # fake-label1 node for us. It can then fulfill the fake-label2 request.
        self.waitForNodeDeletion(label1_nodes[0])
        req = self.waitForNodeRequest(req)
        self.assertEqual(req.state, zk.FULFILLED)

    def test_launcher_registers_config_change(self):
        '''
        Launchers register themselves and some config info with ZooKeeper.
        Validate that a config change will propogate to ZooKeeper.
        '''
        configfile = self.setup_config('launcher_reg1.yaml')
        self.useBuilder(configfile)
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        self.waitForNodes('fake-label')
        launcher_pools = self.zk.getRegisteredPools()
        self.assertEqual(1, len(launcher_pools))

        # the fake-label-unused label should not appear
        self.assertEqual({'fake-label'},
                         set(launcher_pools[0].supported_labels))

        self.replace_config(configfile, 'launcher_reg2.yaml')

        # we should get 1 additional label now
        while (set(launcher_pools[0].supported_labels) !=
               {'fake-label', 'fake-label2'}):
            time.sleep(1)
            launcher_pools = self.zk.getRegisteredPools()

    @mock.patch('nodepool.driver.statemachine.'
                'StateMachineNodeLauncher.launch')
    def test_launchNode_session_expired(self, mock_launch):
        '''
        Test ZK session lost during launch().
        '''
        mock_launch.side_effect = kze.SessionExpiredError()

        # use a config with min-ready of 0
        configfile = self.setup_config('node_launch_retry.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        pool.cleanup_interval = 60
        self.startPool(pool)

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label')
        self.zk.storeNodeRequest(req)

        # A session loss during node launch should at least try to set the
        # request state to FAILED (in a non-test scenario, it may actually
        # be missing).
        req = self.waitForNodeRequest(req, states=(zk.FAILED,))
        self.assertEqual(1, mock_launch.call_count)

        # Any znodes created for the request should eventually get deleted.
        while self.zk.countPoolNodes('fake-provider', 'main'):
            time.sleep(0)

    @mock.patch('nodepool.driver.statemachine.'
                'StateMachineProvider.invalidateQuotaCache')
    def test_launchNode_node_fault_message(self, mock_invalidatequotacache):
        '''
        Test failed launch can get detailed node fault info if available.
        '''
        fake_client = fakeadapter.FakeLaunchAndGetFaultCloud()

        def get_fake_client(*args, **kwargs):
            return fake_client

        self.useFixture(fixtures.MockPatchObject(
            fakeadapter.FakeAdapter, '_getClient',
            get_fake_client))

        configfile = self.setup_config('node_launch_retry.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        pool.cleanup_interval = 60
        self.startPool(pool)

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label')
        self.zk.storeNodeRequest(req)

        # We expect the request to go PENDING and pause here because the
        # wait_for_server() defined in FakeLaunchAndGetFaultCloud should fail
        # and set the fault.message attribute on the server. When the code in
        # launch() catches this failure, it looks for the string 'quota' inside
        # this server attribute and makes the call to invalideQuotaCache()
        # based on the presence of that string and a QuotaException is raised,
        # causing request handling to pause.
        self.waitForNodeRequest(req, (zk.PENDING,))
        pool_worker = pool.getPoolWorkers('fake-provider')
        while not pool_worker[0].paused_handlers:
            time.sleep(0.1)
        self.assertTrue(mock_invalidatequotacache.called)

    def test_launchNode_delete_error(self):
        '''
        Test that the launcher keeps trying to spawn a node in case of a
        delete error
        '''
        fake_client = fakeadapter.FakeLaunchAndDeleteFailCloud(
            times_to_fail=1)

        def get_fake_client(*args, **kwargs):
            return fake_client

        self.useFixture(fixtures.MockPatchObject(
            fakeadapter.FakeAdapter, '_getClient',
            get_fake_client))

        configfile = self.setup_config('node_launch_retry.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label')
        self.zk.storeNodeRequest(req)

        req = self.waitForNodeRequest(req)

        # The deletion of the node can be delayed so wait for it.
        while True:
            if fake_client.delete_success:
                break
            time.sleep(0.1)
        self.assertTrue(fake_client.launch_success)
        self.assertEqual(fake_client.times_to_fail_delete,
                         fake_client.times_failed_delete)
        self.assertEqual(fake_client.times_to_fail_launch,
                         fake_client.times_failed_launch)
        self.assertEqual(req.state, zk.FULFILLED)
        self.assertEqual(len(req.nodes), 1)

    @mock.patch('nodepool.driver.NodeRequestHandler.poll')
    def test_handler_poll_session_expired(self, mock_poll):
        '''
        Test ZK session lost during handler poll() removes handler.
        '''
        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label')
        self.zk.storeNodeRequest(req)

        # We need to stop processing of this request so that it does not
        # re-enter request handling, so we can then verify that it was
        # actually removed from request_handlers in the final assert of
        # this test.
        def side_effect():
            req.state = zk.FAILED
            # Intentionally ignore that it is already locked.
            self.zk.storeNodeRequest(req)
            raise kze.SessionExpiredError()

        mock_poll.side_effect = side_effect

        # use a config with min-ready of 0
        configfile = self.setup_config('node_launch_retry.yaml')
        self.useBuilder(configfile)

        # Wait for the image to exist before starting the launcher, else
        # we'll decline the request.
        self.waitForImage('fake-provider', 'fake-image')

        pool = self.useNodepool(configfile, watermark_sleep=1)
        pool.cleanup_interval = 60
        self.startPool(pool)

        # Wait for request handling to occur
        while not mock_poll.call_count:
            time.sleep(.1)

        # Note: The launcher is not setting FAILED state here, but our mock
        # side effect should be doing so. Just verify that.
        req = self.waitForNodeRequest(req)
        self.assertEqual(zk.FAILED, req.state)

        # A session loss during handler poll should at least remove the
        # request from active handlers. The session exception from our first
        # time through poll() should handle removing the request handler.
        # And our mock side effect should ensure it does not re-enter
        # request handling before we check it.
        for _ in iterate_timeout(10, Exception,
                                 'request_handlers to reach zero count'):
            try:
                self.assertEqual(0, len(
                    pool._pool_threads["fake-provider-main"].request_handlers))
                break
            except AssertionError:
                pass

    def test_exception_causing_decline_of_paused_request(self):
        """
        Test that a paused request, that later gets declined because of
        an exception (say, thrown from a provider operation), unpauses
        and removes the request handler.
        """

        # First config has max-servers set to 2
        configfile = self.setup_config('pause_declined_1.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        # Create a request that uses all capacity (2 servers)
        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label')
        req.node_types.append('fake-label')
        self.zk.storeNodeRequest(req)
        req = self.waitForNodeRequest(req)
        self.assertEqual(req.state, zk.FULFILLED)
        self.assertEqual(len(req.nodes), 2)

        # Now that we have 2 nodes in use, create another request that
        # requests two nodes, which should cause the request to pause.
        req2 = zk.NodeRequest()
        req2.state = zk.REQUESTED
        req2.node_types.append('fake-label')
        req2.node_types.append('fake-label')
        self.zk.storeNodeRequest(req2)
        req2 = self.waitForNodeRequest(req2, (zk.PENDING,))

        # Force an exception within the run handler.
        pool_worker = pool.getPoolWorkers('fake-provider')
        while not pool_worker[0].paused_handlers:
            time.sleep(0.1)
        for rh in pool_worker[0].paused_handlers:
            rh.hasProviderQuota = mock.Mock(
                side_effect=Exception('mock exception')
            )

        # The above exception should cause us to fail the paused request.
        req2 = self.waitForNodeRequest(req2, (zk.FAILED,))
        self.assertNotEqual(req2.declined_by, [])

        # The exception handling should make sure that we unpause AND remove
        # the request handler.
        while pool_worker[0].paused_handlers:
            time.sleep(0.1)
        self.assertEqual(0, len(pool_worker[0].request_handlers))

    def test_ignore_provider_quota_false(self):
        '''
        Test that a node request get fulfilled with ignore-provider-quota set
        to false.
        '''

        # Set max-cores quota value to 0 to force "out of quota". Note that
        # the fake provider checks the number of instances during server
        # creation to decide if it should throw an over quota exception,
        # but it doesn't check cores.
        def fake_get_quota():
            return (0, 20, 1000000)
        self.useFixture(fixtures.MockPatchObject(
            fakeadapter.FakeAdapter.fake_cloud, '_get_quota',
            fake_get_quota
        ))

        configfile = self.setup_config('ignore_provider_quota_false.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')

        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        # Create a request with ignore-provider-quota set to false that should
        # fail because it will decline the request because "it would exceed
        # quota".
        self.log.debug("Submitting request with ignore-provider-quota False")
        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label')
        self.zk.storeNodeRequest(req)
        req = self.waitForNodeRequest(req)
        self.assertEqual(req.state, zk.FAILED)

    def test_ignore_provider_quota_true(self):
        '''
        Test that a node request get fulfilled with ignore-provider-quota set
        to true.
        '''

        # Set max-cores quota value to 0 to force "out of quota". Note that
        # the fake provider checks the number of instances during server
        # creation to decide if it should throw an over quota exception,
        # but it doesn't check cores.
        def fake_get_quota():
            return (0, 20, 1000000)
        self.useFixture(fixtures.MockPatchObject(
            fakeadapter.FakeAdapter.fake_cloud, '_get_quota',
            fake_get_quota
        ))

        configfile = self.setup_config('ignore_provider_quota_true.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')

        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        # Create a request with ignore-provider-quota set to true that should
        # pass regardless of the lack of cloud/provider quota.
        self.replace_config(configfile, 'ignore_provider_quota_true.yaml')

        self.log.debug(
            "Submitting an initial request with ignore-provider-quota True")
        req1 = zk.NodeRequest()
        req1.state = zk.REQUESTED
        req1.node_types.append('fake-label')
        self.zk.storeNodeRequest(req1)
        req1 = self.waitForNodeRequest(req1)
        self.assertEqual(req1.state, zk.FULFILLED)

        # Lock this node so it appears as used and not deleted
        req1_node = self.zk.getNode(req1.nodes[0])
        self.zk.lockNode(req1_node, blocking=False)

        # Request a second node; this request should pause the handler
        # due to the pool set with max-servers: 1
        req2 = zk.NodeRequest()
        req2.state = zk.REQUESTED
        req2.node_types.append('fake-label')
        self.log.debug(
            "Submitting a second request with ignore-provider-quota True"
            "but with a full max-servers quota.")
        self.zk.storeNodeRequest(req2)

        pool_worker = pool.getPoolWorkers('fake-provider')
        while not pool_worker[0].paused_handlers:
            time.sleep(0.1)

        # The handler is paused now and the request should be in state PENDING
        req2 = self.waitForNodeRequest(req2, zk.PENDING)
        self.assertEqual(req2.state, zk.PENDING)

        # Now free up the first node
        self.log.debug("Marking first node as used %s", req1.id)
        req1_node.state = zk.USED
        self.zk.storeNode(req1_node)
        self.zk.unlockNode(req1_node)
        self.waitForNodeDeletion(req1_node)

        # After the first node is cleaned up the second request should be
        # able to fulfill now.
        req2 = self.waitForNodeRequest(req2)
        self.assertEqual(req2.state, zk.FULFILLED)

        # Lock this node so it appears as used and not deleted
        req2_node = self.zk.getNode(req2.nodes[0])
        self.zk.lockNode(req2_node, blocking=False)

        # Now free up the second node
        self.log.debug("Marking second node as used %s", req2.id)
        req2_node.state = zk.USED
        self.zk.storeNode(req2_node)
        self.zk.unlockNode(req2_node)
        self.waitForNodeDeletion(req2_node)

        # Request a 2 node set; this request should fail
        # due to the provider only being able to fulfill
        # a single node at a time.
        req3 = zk.NodeRequest()
        req3.state = zk.REQUESTED
        req3.node_types.append('fake-label')
        req3.node_types.append('fake-label')
        self.log.debug(
            "Submitting a third request with ignore-provider-quota True"
            "for a 2-node set which the provider cannot fulfill.")
        self.zk.storeNodeRequest(req3)

        req3 = self.waitForNodeRequest(req3)
        self.assertEqual(req3.state, zk.FAILED)

    def test_ignore_provider_quota_true_with_provider_error(self):
        '''
        Tests that quota errors returned from the provider when allocating a
        node are correctly handled and retried. The node request should be
        retried until there is sufficient quota to satisfy it.
        '''
        max_instances = 0

        def fake_get_quota():
            nonlocal max_instances
            return (100, max_instances, 1000000)

        self.useFixture(fixtures.MockPatchObject(
            fakeadapter.FakeAdapter.fake_cloud, '_get_quota',
            fake_get_quota
        ))

        configfile = self.setup_config('ignore_provider_quota_true.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')

        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        # Create a request with ignore-provider-quota set to true that should
        # pass regardless of the lack of cloud/provider quota.
        self.replace_config(configfile, 'ignore_provider_quota_true.yaml')

        self.log.debug(
            "Submitting an initial request with ignore-provider-quota True")
        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label')
        self.zk.storeNodeRequest(req)

        self.waitForAnyNodeInState(zk.ABORTED)

        self.assertReportedStat(
            'nodepool.launch.provider.fake-provider.error.quota')
        self.assertReportedStat(
            'nodepool.launch.error.quota')

        # Bump up the quota to allow the provider to allocate a node
        max_instances = 1
        req = self.waitForNodeRequest(req)
        self.assertEqual(req.state, zk.FULFILLED)

    def test_multiple_paused_requests(self):
        """Test that multiple paused requests are fulfilled in order."""
        max_instances = 0

        def fake_get_quota():
            nonlocal max_instances
            return (100, max_instances, 1000000)

        self.useFixture(fixtures.MockPatchObject(
            fakeadapter.FakeAdapter.fake_cloud, '_get_quota',
            fake_get_quota
        ))

        req1 = zk.NodeRequest()
        req1.state = zk.REQUESTED
        req1.node_types.append('fake-label')
        self.zk.storeNodeRequest(req1)

        req2 = zk.NodeRequest()
        req2.state = zk.REQUESTED
        req2.node_types.append('fake-label')
        self.zk.storeNodeRequest(req2)

        configfile = self.setup_config('ignore_provider_quota_true.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')

        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        self.waitForAnyNodeInState(zk.ABORTED)

        pool_worker = pool.getPoolWorkers('fake-provider')
        while not len(pool_worker[0].paused_handlers) == 2:
            time.sleep(0.1)

        # Bump up the quota to allow the provider to allocate a node
        max_instances = 1
        req1 = self.waitForNodeRequest(req1)
        self.assertEqual(req1.state, zk.FULFILLED)

        req2 = self.waitForNodeRequest(req2, zk.PENDING)

        # Release the node allocated to the first request
        req1_node = self.zk.getNode(req1.nodes[0])
        self.zk.lockNode(req1_node, blocking=False)

        req1_node.state = zk.USED
        self.zk.storeNode(req1_node)
        self.zk.unlockNode(req1_node)
        self.waitForNodeDeletion(req1_node)

        self.waitForNodeRequest(req2, zk.FULFILLED)

    def test_request_order(self):
        """Test that requests are handled in sorted order"""
        configfile = self.setup_config('node_no_min_ready.yaml')
        self.useBuilder(configfile)
        image = self.waitForImage('fake-provider', 'fake-image')
        self.assertEqual(image.username, 'fake-username')

        req1 = zk.NodeRequest()
        req1.state = zk.REQUESTED
        req1.node_types.append('fake-label')
        req1.relative_priority = 2
        self.zk.storeNodeRequest(req1)

        req2 = zk.NodeRequest()
        req2.state = zk.REQUESTED
        req2.node_types.append('fake-label')
        req2.relative_priority = 1
        self.zk.storeNodeRequest(req2)

        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        req2 = self.waitForNodeRequest(req2)
        self.assertEqual(req2.state, zk.FULFILLED)
        req1 = self.waitForNodeRequest(req1)
        self.assertEqual(req1.state, zk.FULFILLED)

        self.assertTrue(req2.id > req1.id)
        self.assertTrue(req2.state_time < req1.state_time)

    def test_request_order_missing_label(self):
        """Test that requests that can be be fulfilled are prioritized over
        requests that need to be rejected (based on the request labels).
        """
        configfile = self.setup_config('node_no_min_ready.yaml')
        self.useBuilder(configfile)
        image = self.waitForImage('fake-provider', 'fake-image')
        self.assertEqual(image.username, 'fake-username')

        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        # Request with a higher relative priority coming in first, but
        # requesting a label that is not available.
        req1 = zk.NodeRequest()
        req1.state = zk.REQUESTED
        req1.node_types.append('not-available')
        req1.relative_priority = 1
        self.zk.storeNodeRequest(req1)

        # Later request with a lower relative priority, but a valid label
        # which should be handled first.
        req2 = zk.NodeRequest()
        req2.state = zk.REQUESTED
        req2.node_types.append('fake-label')
        req2.relative_priority = 2
        self.zk.storeNodeRequest(req2)

        req2 = self.waitForNodeRequest(req2)
        self.assertEqual(req2.state, zk.FULFILLED)
        req1 = self.waitForNodeRequest(req1)
        self.assertEqual(req1.state, zk.FAILED)

        # Verify that we created the node for req2 before we declined
        # req1.  This asserts that the request were processed in the
        # correct (reversed) order.
        req2_node = self.zk.getNode(req2.nodes[0], cached=False)
        self.assertGreater(req1.stat.mtime, req2_node.stat.ctime)
        self.assertGreater(req2.id, req1.id)

    def test_empty_node_deleted(self):
        """Test that empty nodes are deleted by the cleanup thread"""
        configfile = self.setup_config('node.yaml')

        # Create empty node
        path = "%s" % self.zk._nodePath("12345")
        self.log.debug("node path %s", path)
        self.zk.kazoo_client.create(path, makepath=True)
        self.assertTrue(self.zk.kazoo_client.exists(path))

        pool = self.useNodepool(configfile, watermark_sleep=1)
        pool.cleanup_interval = .1
        self.startPool(pool)

        while self.zk.kazoo_client.exists(path):
            time.sleep(.1)

    def test_leaked_port_cleanup(self):
        configfile = self.setup_config('node.yaml')
        self.useBuilder(configfile)
        pool = self.useNodepool(configfile, watermark_sleep=1)
        pool.cleanup_interval = 1
        self.startPool(pool)
        self.waitForNodes('fake-label')

        manager = pool.getProviderManager('fake-provider')
        down_ports = manager.adapter._listPorts(status='DOWN')
        self.assertEqual(2, len(down_ports))
        self.log.debug("Down ports: %s", down_ports)

        # Second config decreases cleanup interval to 2 seconds
        self.replace_config(configfile, 'cleanup-port.yaml')
        oldmanager = manager
        manager = pool.getProviderManager('fake-provider')
        for _ in iterate_timeout(10, Exception, 'assert config updated'):
            try:
                self.assertNotEqual(manager, oldmanager)
                break
            except AssertionError:
                # config still hasn't updated, retry
                manager = pool.getProviderManager('fake-provider')

        for _ in iterate_timeout(4, Exception, 'assert ports are cleaned'):
            try:
                down_ports = manager.adapter._listPorts(status='DOWN')
                self.assertEqual(0, len(down_ports))
                break
            except AssertionError:
                # ports not cleaned up yet, retry
                pass

        self.assertReportedStat(
            'nodepool.provider.fake-provider.leaked.ports',
            value='2', kind='c')

    def test_deleteRawNode_exception(self):
        configfile = self.setup_config('node.yaml')
        self.useBuilder(configfile)
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        nodes = self.waitForNodes('fake-label')
        self.assertEqual(1, len(nodes))

        # We want the first call to deleteRawNode() to fail, but subsequent
        # ones to succeed, so we store a pointer to the actual method so we
        # can reset it at the point we want to really delete.
        real_method = zk.ZooKeeper.deleteRawNode
        zk.ZooKeeper.deleteRawNode = mock.Mock(
            side_effect=Exception('mock exception'))

        # This call should leave the node in the DELETED state
        with testtools.ExpectedException(Exception):
            self.zk.deleteNode(nodes[0])

        node = self.zk.getNode(nodes[0].id, cached=False)
        self.assertEqual(zk.DELETED, node.state)

        # Ready for the real delete now
        zk.ZooKeeper.deleteRawNode = real_method
        self.waitForNodeDeletion(node)

    def test_provider_priority(self):
        """Test provider priorities"""
        configfile = self.setup_config('priority.yaml')
        self.useBuilder(configfile)
        self.waitForImage('low-provider', 'fake-image')
        self.waitForImage('high-provider', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        # The first request should be handled by the highest priority
        # provider (high-provider; priority 1)
        req1 = zk.NodeRequest()
        req1.state = zk.REQUESTED
        req1.node_types.append('fake-label')
        self.zk.storeNodeRequest(req1)
        req1 = self.waitForNodeRequest(req1)
        self.assertEqual(req1.state, zk.FULFILLED)
        self.assertEqual(len(req1.nodes), 1)
        node1 = self.zk.getNode(req1.nodes[0])
        self.assertEqual(node1.provider, 'high-provider')

        # The second request should also be handled by the highest
        # priority provider, but since it has max-servers=1, this
        # request should be paused, which will cause the provider to
        # be paused.
        req2 = zk.NodeRequest()
        req2.state = zk.REQUESTED
        req2.node_types.append('fake-label')
        self.zk.storeNodeRequest(req2)
        req2 = self.waitForNodeRequest(req2, (zk.PENDING,))
        self.assertEqual(req2.state, zk.PENDING)

        # The third request should be handled by the low priority
        # provider now that the high provider is paused.
        req3 = zk.NodeRequest()
        req3.state = zk.REQUESTED
        req3.node_types.append('fake-label')
        self.zk.storeNodeRequest(req3)
        req3 = self.waitForNodeRequest(req3)
        self.assertEqual(req3.state, zk.FULFILLED)
        self.assertEqual(len(req3.nodes), 1)
        node3 = self.zk.getNode(req3.nodes[0])
        self.assertEqual(node3.provider, 'low-provider')

    def test_requests_by_provider_stats(self):
        configfile = self.setup_config('node_two_providers_two_labels.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        self.waitForImage('fake-provider2', 'fake-image')

        nodepool.launcher.LOCK_CLEANUP = 1
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label')
        req.requestor = 'unit-test'
        self.zk.storeNodeRequest(req)

        req = self.waitForNodeRequest(req)
        self.assertEqual(req.state, zk.FULFILLED)

        req2 = zk.NodeRequest()
        req2.state = zk.REQUESTED
        req2.node_types.append('fake-label2')
        req2.requestor = 'unit-test'
        self.zk.storeNodeRequest(req2)

        req2 = self.waitForNodeRequest(req2)
        self.assertEqual(req2.state, zk.FULFILLED)

        self.assertReportedStat(
            'nodepool.'
            'provider.'
            'fake-provider.'
            'pool.'
            'main.'
            'addressable_requests',
            value='1', kind='g')
        self.assertReportedStat(
            'nodepool.'
            'provider.'
            'fake-provider2.'
            'pool.'
            'main.'
            'addressable_requests',
            value='2', kind='g')
