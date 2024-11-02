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

import base64
import logging
import math
import urllib3
import time

from kubernetes import client as k8s_client

from nodepool import exceptions, stats
from nodepool.driver import Provider
from nodepool.driver.kubernetes import handler
from nodepool.driver.utils import QuotaInformation, QuotaSupport
from nodepool.driver.utils import NodeDeleter
from nodepool.driver.utils_k8s import get_client

urllib3.disable_warnings()


class KubernetesProvider(Provider, QuotaSupport):
    log = logging.getLogger("nodepool.driver.kubernetes.KubernetesProvider")

    def __init__(self, provider, *args):
        super().__init__()
        self.provider = provider
        self._zk = None
        self._statsd = stats.get_client()
        self.ready = False
        _, _, self.k8s_client, self.rbac_client = get_client(
            self.log, provider.context, k8s_client.RbacAuthorizationV1Api)
        self.namespace_names = set()
        for pool in provider.pools.values():
            self.namespace_names.add(pool.name)

    def start(self, zk_conn):
        self.log.debug("Starting")
        self._zk = zk_conn
        if self.ready or not self.k8s_client or not self.rbac_client:
            return
        self.ready = True

    def stop(self):
        self.log.debug("Stopping")
        self.ready = False

    def idle(self):
        pass

    def listNodes(self):
        servers = []

        class FakeServer:
            def __init__(self, namespace, valid_names):
                self.id = namespace.metadata.name
                self.name = namespace.metadata.name
                self.metadata = {}

                if [True for valid_name in valid_names
                    if namespace.metadata.name.startswith("%s-" % valid_name)]:
                    node_id = namespace.metadata.name.split('-')[-1]
                    try:
                        # Make sure last component of name is an id
                        int(node_id)
                        self.metadata = namespace.metadata.labels
                    except Exception:
                        # Probably not a managed namespace, let's skip metadata
                        pass

            def get(self, name, default=None):
                return getattr(self, name, default)

        if self.ready:
            for namespace in self.k8s_client.list_namespace().items:
                servers.append(FakeServer(namespace, self.namespace_names))
        return servers

    def labelReady(self, name):
        # Labels are always ready
        return True

    def join(self):
        pass

    def cleanupLeakedResources(self):
        '''
        Delete any leaked server instances.

        Remove any servers found in this provider that are not recorded in
        the ZooKeeper data.
        '''

        for server in self.listNodes():
            meta = server.get('metadata', {})

            if 'nodepool_provider_name' not in meta:
                continue

            if meta['nodepool_provider_name'] != self.provider.name:
                # Another launcher, sharing this provider but configured
                # with a different name, owns this.
                continue

            if not self._zk.getNode(meta['nodepool_node_id']):
                self.log.warning(
                    "Deleting leaked instance %s (%s) in %s "
                    "(unknown node id %s)",
                    server.name, server.id, self.provider.name,
                    meta['nodepool_node_id']
                )
                self.cleanupNode(server.id)
                if self._statsd:
                    key = ('nodepool.provider.%s.leaked.nodes'
                           % self.provider.name)
                    self._statsd.incr(key)

    def startNodeCleanup(self, node):
        t = NodeDeleter(self._zk, self, node)
        t.start()
        return t

    def cleanupNode(self, server_id):
        if not self.ready:
            return
        self.log.debug("%s: removing namespace" % server_id)
        delete_body = {
            "apiVersion": "v1",
            "kind": "DeleteOptions",
            "propagationPolicy": "Background"
        }
        try:
            self.k8s_client.delete_namespace(server_id, body=delete_body)
            self.log.info("%s: namespace removed" % server_id)
        except Exception:
            # TODO: implement better exception handling
            self.log.exception("Couldn't remove namespace %s" % server_id)

    def waitForNodeCleanup(self, server_id):
        for retry in range(300):
            try:
                self.k8s_client.read_namespace(server_id)
            except Exception:
                break
            time.sleep(1)

    def createNamespace(
            self, node, pool, label, request, restricted_access=False
    ):
        name = node.id
        namespace = "%s-%s" % (pool, name)
        user = "zuul-worker"

        self.log.debug("%s: creating namespace" % namespace)

        k8s_labels = self._getK8sLabels(label, node, pool, request)

        # Create the namespace
        ns_body = {
            'apiVersion': 'v1',
            'kind': 'Namespace',
            'metadata': {
                'name': namespace,
                'labels': k8s_labels,
            }
        }
        proj = self.k8s_client.create_namespace(ns_body)
        node.external_id = namespace

        # Create the service account
        sa_body = {
            'apiVersion': 'v1',
            'kind': 'ServiceAccount',
            'metadata': {'name': user}
        }
        self.k8s_client.create_namespaced_service_account(namespace, sa_body)

        secret_body = {
            'apiVersion': 'v1',
            'kind': 'Secret',
            'type': 'kubernetes.io/service-account-token',
            'metadata': {
                'name': user,
                'annotations': {
                    'kubernetes.io/service-account.name': user
                }
            }
        }
        self.k8s_client.create_namespaced_secret(namespace, secret_body)

        # Wait for the token to be created
        for retry in range(30):
            secret = self.k8s_client.read_namespaced_secret(user, namespace)
            ca_crt = None
            token = None
            if secret.data:
                token = secret.data.get('token')
                ca_crt = secret.data.get('ca.crt')
                if token and ca_crt:
                    token = base64.b64decode(
                        token.encode('utf-8')).decode('utf-8')
            if token and ca_crt:
                break
            time.sleep(1)
        if not token or not ca_crt:
            raise exceptions.LaunchNodepoolException(
                "%s: couldn't find token for secret %s" %
                (namespace, secret))

        # Create service account role
        all_verbs = ["create", "delete", "get", "list", "patch",
                     "update", "watch"]
        if restricted_access:
            role_name = "zuul-restricted"
            role_body = {
                'kind': 'Role',
                'apiVersion': 'rbac.authorization.k8s.io/v1',
                'metadata': {
                    'name': role_name,
                },
                'rules': [{
                    'apiGroups': [""],
                    'resources': ["pods"],
                    'verbs': ["get", "list"],
                }, {
                    'apiGroups': [""],
                    'resources': ["pods/exec"],
                    'verbs': all_verbs
                }, {
                    'apiGroups': [""],
                    'resources': ["pods/logs"],
                    'verbs': all_verbs
                }, {
                    'apiGroups': [""],
                    'resources': ["pods/portforward"],
                    'verbs': all_verbs
                }]
            }
        else:
            role_name = "zuul"
            role_body = {
                'kind': 'Role',
                'apiVersion': 'rbac.authorization.k8s.io/v1',
                'metadata': {
                    'name': role_name,
                },
                'rules': [{
                    'apiGroups': [""],
                    'resources': ["pods", "pods/exec", "pods/log",
                                  "pods/portforward", "services",
                                  "endpoints", "crontabs", "jobs",
                                  "deployments", "replicasets",
                                  "configmaps", "secrets"],
                    'verbs': all_verbs,
                }]
            }
        self.rbac_client.create_namespaced_role(namespace, role_body)

        # Give service account admin access
        role_binding_body = {
            'apiVersion': 'rbac.authorization.k8s.io/v1',
            'kind': 'RoleBinding',
            'metadata': {'name': 'zuul-role'},
            'roleRef': {
                'apiGroup': 'rbac.authorization.k8s.io',
                'kind': 'Role',
                'name': role_name,
            },
            'subjects': [{
                'kind': 'ServiceAccount',
                'name': user,
                'namespace': namespace,
            }],
            'userNames': ['system:serviceaccount:%s:zuul-worker' % namespace]
        }
        self.rbac_client.create_namespaced_role_binding(
            namespace, role_binding_body)

        resource = {
            'name': proj.metadata.name,
            'namespace': namespace,
            'host': self.k8s_client.api_client.configuration.host,
            'skiptls': not self.k8s_client.api_client.configuration.verify_ssl,
            'token': token,
            'user': user,
        }

        if not resource['skiptls']:
            resource['ca_crt'] = ca_crt

        self.log.info("%s: namespace created" % namespace)
        return resource

    def createPod(self, node, pool, label, request):
        if label.spec:
            pod_body = self.getPodBodyCustom(node, pool, label, request)
        else:
            pod_body = self.getPodBodyNodepool(node, pool, label, request)
        resource = self.createNamespace(node, pool, label, request,
                                        restricted_access=True)
        namespace = resource['namespace']
        self.k8s_client.create_namespaced_pod(namespace, pod_body)

        for retry in range(300):
            pod = self.k8s_client.read_namespaced_pod(label.name, namespace)
            if pod.status.phase == "Running":
                break
            self.log.debug("%s: pod status is %s", namespace, pod.status.phase)
            time.sleep(1)
        if retry == 299:
            raise exceptions.LaunchNodepoolException(
                "%s: pod failed to initialize (%s)" % (
                    namespace, pod.status.phase))
        resource["pod"] = label.name
        node.host_id = pod.spec.node_name
        return resource

    def getPodBodyCustom(self, node, pool, label, request):
        k8s_labels = self._getK8sLabels(label, node, pool, request)
        k8s_annotations = {}
        if label.annotations:
            k8s_annotations.update(label.annotations)

        pod_body = {
            'apiVersion': 'v1',
            'kind': 'Pod',
            'metadata': {
                'name': label.name,
                'labels': k8s_labels,
                'annotations': k8s_annotations,
            },
            'spec': label.spec,
            'restartPolicy': 'Never',
        }

        return pod_body

    def getPodBodyNodepool(self, node, pool, label, request):
        container_body = {
            'name': label.name,
            'image': label.image,
            'imagePullPolicy': label.image_pull,
            'command': ["/bin/sh", "-c"],
            'args': ["while true; do sleep 30; done;"],
            'env': label.env,
        }

        requests = {}
        limits = {}
        if label.cpu:
            requests['cpu'] = int(label.cpu)
        if label.memory:
            requests['memory'] = '%dMi' % int(label.memory)
        if label.storage:
            requests['ephemeral-storage'] = '%dM' % int(label.storage)
        if label.cpu_limit:
            limits['cpu'] = int(label.cpu_limit)
        if label.memory_limit:
            limits['memory'] = '%dMi' % int(label.memory_limit)
        if label.storage_limit:
            limits['ephemeral-storage'] = '%dM' % int(label.storage_limit)
        if label.gpu_resource and label.gpu:
            requests[label.gpu_resource] = '%.2f' % label.gpu
            limits[label.gpu_resource] = '%.2f' % label.gpu
        resources = {}
        if requests:
            resources['requests'] = requests
        if limits:
            resources['limits'] = limits

        if resources:
            container_body['resources'] = resources
        if label.volume_mounts:
            container_body['volumeMounts'] = label.volume_mounts
        if label.privileged is not None:
            container_body['securityContext'] = {
                'privileged': label.privileged,
            }

        spec_body = {
            'containers': [container_body]
        }

        if label.node_selector:
            spec_body['nodeSelector'] = label.node_selector
        if label.scheduler_name:
            spec_body['schedulerName'] = label.scheduler_name
        if label.volumes:
            spec_body['volumes'] = label.volumes

        k8s_labels = self._getK8sLabels(label, node, pool, request)
        k8s_annotations = {}
        if label.annotations:
            k8s_annotations.update(label.annotations)

        pod_body = {
            'apiVersion': 'v1',
            'kind': 'Pod',
            'metadata': {
                'name': label.name,
                'labels': k8s_labels,
                'annotations': k8s_annotations,
            },
            'spec': spec_body,
            'restartPolicy': 'Never',
        }

        return pod_body

    def getRequestHandler(self, poolworker, request):
        return handler.KubernetesNodeRequestHandler(poolworker, request)

    def getProviderLimits(self):
        # TODO: query the api to get real limits
        return QuotaInformation(
            cores=math.inf,
            instances=math.inf,
            ram=math.inf,
            default=math.inf)

    def quotaNeededByLabel(self, ntype, pool):
        provider_label = pool.labels[ntype]
        resources = {}
        if provider_label.cpu:
            resources["cores"] = provider_label.cpu
        if provider_label.memory:
            resources["ram"] = provider_label.memory
        if provider_label.storage:
            resources["ephemeral-storage"] = provider_label.storage
        if provider_label.gpu and provider_label.gpu_resource:
            resources[provider_label.gpu_resource] = provider_label.gpu
        resources.update(provider_label.extra_resources)
        return QuotaInformation(instances=1, **resources)

    def unmanagedQuotaUsed(self):
        # TODO: return real quota information about quota
        return QuotaInformation()

    def _getK8sLabels(self, label, node, pool, request):
        k8s_labels = {}
        if label.labels:
            k8s_labels.update(label.labels)

        for k, v in label.dynamic_labels.items():
            try:
                k8s_labels[k] = v.format(request=request.getSafeAttributes())
            except Exception:
                self.log.exception("Error formatting tag %s", k)

        k8s_labels.update({
            'nodepool_node_id': node.id,
            'nodepool_provider_name': self.provider.name,
            'nodepool_pool_name': pool,
            'nodepool_node_label': label.name,
        })

        return k8s_labels
