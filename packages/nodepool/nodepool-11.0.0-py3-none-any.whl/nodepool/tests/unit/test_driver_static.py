# Copyright (C) 2017 Red Hat
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
import mock
import os

from nodepool import config as nodepool_config
from nodepool import tests
from nodepool.zk import zookeeper as zk
from nodepool.cmd.config_validator import ConfigValidator


class TestDriverStatic(tests.DBTestCase):
    log = logging.getLogger("nodepool.TestDriverStatic")

    def test_static_validator(self):
        config = os.path.join(os.path.dirname(tests.__file__),
                              'fixtures', 'config_validate',
                              'static_error.yaml')
        validator = ConfigValidator(config)
        ret = validator.validate()
        self.assertEqual(ret, 1)

    def test_static_config(self):
        configfile = self.setup_config('static.yaml')
        config = nodepool_config.loadConfig(configfile)
        self.assertIn('static-provider', config.providers)
        config2 = nodepool_config.loadConfig(configfile)
        self.assertEqual(config, config2)

    def test_static_basic(self):
        '''
        Test that basic node registration works.
        '''
        configfile = self.setup_config('static-basic.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        self.log.debug("Waiting for node pre-registration")
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)

        self.assertEqual(nodes[0].state, zk.READY)
        self.assertEqual(nodes[0].provider, "static-provider")
        self.assertEqual(nodes[0].pool, "main")
        self.assertEqual(nodes[0].launcher, "static driver")
        self.assertEqual(nodes[0].type, ['fake-label'])
        self.assertEqual(nodes[0].hostname, 'fake-host-1')
        self.assertEqual(nodes[0].interface_ip, 'fake-host-1')
        self.assertEqual(nodes[0].username, 'zuul')
        self.assertEqual(nodes[0].connection_port, 22022)
        self.assertEqual(nodes[0].connection_type, 'ssh')
        self.assertEqual(nodes[0].host_keys, ['ssh-rsa FAKEKEY'])
        self.assertEqual(nodes[0].attributes,
                         {'key1': 'value1', 'key2': 'value2'})
        self.assertEqual(nodes[0].python_path, 'auto')
        self.assertIsNone(nodes[0].shell_type)
        self.assertEqual(nodes[0].slot, 0)

    def test_static_reuse(self):
        '''
        Test that static nodes are reused without benefit of the
        cleanup worker
        '''
        configfile = self.setup_config('static-basic.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        # Make sure the cleanup worker doesn't run.
        pool.cleanup_interval = 600
        self.startPool(pool)

        self.log.debug("Waiting for node pre-registration")
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(nodes[0].slot, 0)

        nodes[0].state = zk.USED
        self.zk.storeNode(nodes[0])

        self.log.debug("Waiting for node to be re-available")
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(nodes[0].slot, 0)

    def test_static_python_path(self):
        '''
        Test that static python-path works.
        '''
        configfile = self.setup_config('static-python-path.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        self.log.debug("Waiting for node pre-registration")
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(nodes[0].python_path, "/usr/bin/python3")
        self.assertEqual(nodes[0].slot, 0)

        nodes[0].state = zk.USED
        self.zk.storeNode(nodes[0])

        self.log.debug("Waiting for node to be re-available")
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(nodes[0].python_path, "/usr/bin/python3")
        self.assertEqual(nodes[0].slot, 0)

    def test_static_multiname(self):
        '''
        Test that multi name node (re-)registration works.
        '''
        configfile = self.setup_config('static-multiname.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        self.log.debug("Waiting for node pre-registration")
        nodes = self.waitForNodes('fake-label', 1)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].state, zk.READY)
        self.assertEqual(nodes[0].username, 'zuul')
        self.assertEqual(nodes[0].slot, 0)

        nodes = self.waitForNodes('other-label', 1)
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].state, zk.READY)
        self.assertEqual(nodes[0].username, 'zuul-2')
        self.assertEqual(nodes[0].slot, 0)

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.tenant_name = 'tenant-1'
        req.node_types.append('fake-label')
        self.zk.storeNodeRequest(req)
        req = self.waitForNodeRequest(req, zk.FULFILLED)
        node = self.zk.getNode(req.nodes[0])
        self.zk.lockNode(node)
        node.state = zk.USED
        self.zk.storeNode(node)

        self.zk.unlockNode(node)
        self.waitForNodeDeletion(node)

        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)

        registered_labels = {n.type[0] for n in self.zk.nodeIterator()}
        self.assertEqual(registered_labels, {'fake-label', 'other-label'})

    def test_static_unresolvable(self):
        '''
        Test that basic node registration works.
        '''
        configfile = self.setup_config('static-unresolvable.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        self.log.debug("Waiting for node pre-registration")
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)

        self.assertEqual(nodes[0].state, zk.READY)
        self.assertEqual(nodes[0].provider, "static-provider")
        self.assertEqual(nodes[0].pool, "main")
        self.assertEqual(nodes[0].launcher, "static driver")
        self.assertEqual(nodes[0].type, ['fake-label'])
        self.assertEqual(nodes[0].hostname, 'fake-host-1')
        self.assertEqual(nodes[0].interface_ip, 'fake-host-1')
        self.assertEqual(nodes[0].username, 'zuul')
        self.assertEqual(nodes[0].connection_port, 22022)
        self.assertEqual(nodes[0].connection_type, 'ssh')
        self.assertEqual(nodes[0].host_keys, ['ssh-rsa FAKEKEY'])
        self.assertEqual(nodes[0].slot, 0)

    def test_static_node_increase(self):
        '''
        Test that adding new nodes to the config creates additional nodes.
        '''
        configfile = self.setup_config('static-basic.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        self.log.debug("Waiting for initial node")
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].slot, 0)

        self.log.debug("Waiting for additional node")
        self.replace_config(configfile, 'static-2-nodes.yaml')
        nodes = self.waitForNodes('fake-label', 2)
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].slot, 0)
        self.assertEqual(nodes[1].slot, 0)

    def test_static_node_decrease(self):
        '''
        Test that removing nodes from the config removes nodes.
        '''
        configfile = self.setup_config('static-2-nodes.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        self.log.debug("Waiting for initial nodes")
        nodes = self.waitForNodes('fake-label', 2)
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].slot, 0)
        self.assertEqual(nodes[1].slot, 0)

        self.log.debug("Waiting for node decrease")
        self.replace_config(configfile, 'static-basic.yaml')
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].hostname, 'fake-host-1')
        self.assertEqual(nodes[0].slot, 0)

    def test_static_parallel_increase(self):
        '''
        Test that increasing max-parallel-jobs creates additional nodes.
        '''
        configfile = self.setup_config('static-basic.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        self.log.debug("Waiting for initial node")
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].slot, 0)

        self.log.debug("Waiting for additional node")
        self.replace_config(configfile, 'static-parallel-increase.yaml')
        nodes = self.waitForNodes('fake-label', 2)
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].slot, 0)
        self.assertEqual(nodes[1].slot, 1)

    def test_static_parallel_decrease(self):
        '''
        Test that decreasing max-parallel-jobs deletes nodes.
        '''
        configfile = self.setup_config('static-parallel-increase.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        self.log.debug("Waiting for initial nodes")
        nodes = self.waitForNodes('fake-label', 2)
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].slot, 0)
        self.assertEqual(nodes[1].slot, 1)

        self.log.debug("Waiting for node decrease")
        self.replace_config(configfile, 'static-basic.yaml')
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].slot, 0)

    def test_static_node_update(self):
        '''
        Test that updates a static node on config change.
        '''
        configfile = self.setup_config('static-basic.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        self.log.debug("Waiting for initial node")
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)

        self.log.debug("Waiting for new label")
        self.replace_config(configfile, 'static-update.yaml')
        nodes = self.waitForNodes('fake-label2')
        self.assertEqual(len(nodes), 1)
        self.assertIn('fake-label', nodes[0].type)
        self.assertIn('fake-label2', nodes[0].type)
        self.assertEqual(nodes[0].username, 'admin')
        self.assertEqual(nodes[0].connection_port, 5986)
        self.assertEqual(nodes[0].connection_type, 'winrm')
        self.assertEqual(nodes[0].host_keys, [])
        self.assertEqual(nodes[0].slot, 0)

    def test_static_node_update_startup(self):
        '''
        Test that updates a static node on config change at startup.
        '''
        configfile = self.setup_config('static-basic.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        self.log.debug("Waiting for initial node")
        nodes = self.waitForNodes('fake-label')

        pool.stop()
        configfile = self.setup_config('static-multilabel.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        self.log.debug("Waiting for new label")
        nodes = self.waitForNodes('fake-label2')
        self.assertEqual(len(nodes), 1)
        # Check that the node was updated and not re-created
        self.assertEqual(nodes[0].id, "0000000000")
        self.assertIn('fake-label', nodes[0].type)
        self.assertIn('fake-label2', nodes[0].type)
        self.assertEqual(nodes[0].slot, 0)

    def test_static_multilabel(self):
        configfile = self.setup_config('static-multilabel.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        nodes = self.waitForNodes('fake-label')
        self.assertIn('fake-label', nodes[0].type)
        self.assertIn('fake-label2', nodes[0].type)
        self.assertEqual(nodes[0].slot, 0)

    def test_static_handler(self):
        configfile = self.setup_config('static.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(nodes[0].slot, 0)
        self.waitForNodes('fake-concurrent-label', 2)

        node = nodes[0]
        self.log.debug("Marking first node as used %s", node.id)
        node.state = zk.USED
        self.zk.storeNode(node)
        self.waitForNodeDeletion(node)

        self.log.debug("Waiting for node to be re-available")
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].slot, 0)

    def test_static_waiting_handler(self):
        configfile = self.setup_config('static-2-nodes-multilabel.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label')
        self.zk.storeNodeRequest(req)
        req = self.waitForNodeRequest(req, zk.FULFILLED)
        node = self.zk.getNode(req.nodes[0])
        self.zk.lockNode(node)
        node.state = zk.USED
        self.zk.storeNode(node)

        req_waiting = zk.NodeRequest()
        req_waiting.state = zk.REQUESTED
        req_waiting.node_types.append('fake-label')
        self.zk.storeNodeRequest(req_waiting)

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label2')
        self.zk.storeNodeRequest(req)
        req = self.waitForNodeRequest(req, zk.FULFILLED)

        req_waiting = self.zk.getNodeRequest(req_waiting.id)
        self.assertEqual(req_waiting.state, zk.REQUESTED)
        self.assertEqual(req_waiting.declined_by, [])

        self.zk.unlockNode(node)
        self.waitForNodeDeletion(node)
        self.waitForNodeRequest(req_waiting, zk.FULFILLED)

    def test_label_quota(self):
        configfile = self.setup_config('static-2-nodes-multilabel.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        req1 = zk.NodeRequest()
        req1.state = zk.REQUESTED
        req1.node_types.append('label-host-1')

        req2 = zk.NodeRequest()
        req2.state = zk.REQUESTED
        req2.node_types.append('label-host-2')

        # Request a label that is no longer available, but wasn't requested
        # by any of the previous requests.
        req_waiting = zk.NodeRequest()
        req_waiting.state = zk.REQUESTED
        req_waiting.node_types.append('fake-label2')

        self.zk.storeNodeRequest(req1)
        self.zk.storeNodeRequest(req2)
        self.zk.storeNodeRequest(req_waiting)

        req1 = self.waitForNodeRequest(req1, zk.FULFILLED)
        node = self.zk.getNode(req1.nodes[0])
        self.zk.lockNode(node)
        node.state = zk.USED
        self.zk.storeNode(node)

        req2 = self.waitForNodeRequest(req2, zk.FULFILLED)

        # Assert that the request was not accepted, which means that
        # the label quota was correctly adjusted.
        req_waiting = self.zk.getNodeRequest(req_waiting.id)
        self.assertEqual(req_waiting.state, zk.REQUESTED)
        self.assertEqual(req_waiting.declined_by, [])

        self.zk.unlockNode(node)
        self.waitForNodeDeletion(node)
        self.waitForNodeRequest(req_waiting, zk.FULFILLED)

    def test_static_ignore_assigned_ready_nodes(self):
        """Regression test to not touch assigned READY nodes"""
        configfile = self.setup_config('static-basic.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        # Make sure the cleanup worker is called that reallocated the node
        pool.cleanup_interval = .1
        self.startPool(pool)

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label')
        self.zk.storeNodeRequest(req)
        req = self.waitForNodeRequest(req, zk.FULFILLED)

        req_waiting = zk.NodeRequest()
        req_waiting.state = zk.REQUESTED
        req_waiting.node_types.append('fake-label')
        self.zk.storeNodeRequest(req_waiting)
        req_waiting = self.waitForNodeRequest(req_waiting, zk.REQUESTED)

        # Make sure the node is not reallocated
        node = self.zk.getNode(req.nodes[0])
        self.assertIsNotNone(node)
        self.assertEqual(node.slot, 0)

    def test_static_waiting_handler_order(self):
        configfile = self.setup_config('static-basic.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label')
        self.zk.storeNodeRequest(req)
        req = self.waitForNodeRequest(req, zk.FULFILLED)
        node = self.zk.getNode(req.nodes[0])
        self.assertEqual(node.slot, 0)
        self.zk.lockNode(node)
        node.state = zk.USED
        self.zk.storeNode(node)

        req_waiting1 = zk.NodeRequest()
        req_waiting1.state = zk.REQUESTED
        req_waiting1.node_types.append('fake-label')
        self.zk.storeNodeRequest(req_waiting1, priority="300")

        req_waiting2 = zk.NodeRequest()
        req_waiting2.state = zk.REQUESTED
        req_waiting2.node_types.append('fake-label')
        self.zk.storeNodeRequest(req_waiting2, priority="200")

        req_waiting3 = zk.NodeRequest()
        req_waiting3.state = zk.REQUESTED
        req_waiting3.node_types.append('fake-label')
        self.zk.storeNodeRequest(req_waiting3, priority="200")

        self.zk.unlockNode(node)
        self.waitForNodeDeletion(node)

        req_waiting2 = self.waitForNodeRequest(req_waiting2, zk.FULFILLED)
        req_waiting1 = self.zk.getNodeRequest(req_waiting1.id)
        self.assertEqual(req_waiting1.state, zk.REQUESTED)
        req_waiting3 = self.zk.getNodeRequest(req_waiting3.id)
        self.assertEqual(req_waiting3.state, zk.REQUESTED)

        node_waiting2 = self.zk.getNode(req_waiting2.nodes[0])
        self.assertEqual(node_waiting2.slot, 0)
        self.zk.lockNode(node_waiting2)
        node_waiting2.state = zk.USED
        self.zk.storeNode(node_waiting2)
        self.zk.unlockNode(node_waiting2)

        req_waiting3 = self.waitForNodeRequest(req_waiting3, zk.FULFILLED)
        req_waiting1 = self.zk.getNodeRequest(req_waiting1.id)
        self.assertEqual(req_waiting1.state, zk.REQUESTED)

        node_waiting3 = self.zk.getNode(req_waiting3.nodes[0])
        self.assertEqual(node_waiting3.slot, 0)
        self.zk.lockNode(node_waiting3)
        node_waiting3.state = zk.USED
        self.zk.storeNode(node_waiting3)
        self.zk.unlockNode(node_waiting3)

        self.waitForNodeRequest(req_waiting1, zk.FULFILLED)

    def test_static_multinode_handler(self):
        configfile = self.setup_config('static.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label')
        req.node_types.append('fake-concurrent-label')
        self.zk.storeNodeRequest(req)

        self.log.debug("Waiting for request %s", req.id)
        req = self.waitForNodeRequest(req)
        self.assertEqual(req.state, zk.FULFILLED)
        self.assertEqual(len(req.nodes), 2)

    def test_static_multiprovider_handler(self):
        configfile = self.setup_config('multiproviders.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        manager = pool.getProviderManager('openstack-provider')
        manager.adapter._client.create_image(name="fake-image")
        manager.adapter.IMAGE_CHECK_TIMEOUT = 0

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-static-label')
        self.zk.storeNodeRequest(req)

        self.log.debug("Waiting for request %s", req.id)
        req = self.waitForNodeRequest(req)
        self.assertEqual(req.state, zk.FULFILLED)
        self.assertEqual(len(req.nodes), 1)

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-openstack-label')
        self.zk.storeNodeRequest(req)

        self.log.debug("Waiting for request %s", req.id)
        req = self.waitForNodeRequest(req)
        self.assertEqual(req.state, zk.FULFILLED)
        self.assertEqual(len(req.nodes), 1)

    def test_static_request_handled(self):
        '''
        Test that a node is reregistered after handling a request.
        '''
        configfile = self.setup_config('static-basic.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)
        self.assertEqual(nodes[0].slot, 0)

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label')
        self.zk.storeNodeRequest(req)

        self.log.debug("Waiting for request %s", req.id)
        req = self.waitForNodeRequest(req)
        self.assertEqual(req.state, zk.FULFILLED)
        self.assertEqual(len(req.nodes), 1)
        self.assertEqual(req.nodes[0], nodes[0].id)

        # Mark node as used
        nodes[0].state = zk.USED
        self.zk.storeNode(nodes[0])

        # Our single node should have been used, deleted, then reregistered
        new_nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(nodes[0].hostname, new_nodes[0].hostname)
        self.assertEqual(nodes[0].slot, 0)

    def test_liveness_check(self):
        '''
        Test liveness check during request handling.
        '''
        configfile = self.setup_config('static-basic.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)

        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('fake-label')

        with mock.patch("nodepool.nodeutils.nodescan") as nodescan_mock:
            nodescan_mock.side_effect = OSError
            self.zk.storeNodeRequest(req)
            self.waitForNodeDeletion(nodes[0])

        self.log.debug("Waiting for request %s", req.id)
        req = self.waitForNodeRequest(req)

        self.assertEqual(req.state, zk.FULFILLED)
        self.assertEqual(len(req.nodes), 1)
        self.assertNotEqual(req.nodes[0], nodes[0].id)

    def test_liveness_two_node(self):
        '''
        Test that a node going offline doesn't block a static provider
        '''
        configfile = self.setup_config('static-two-node.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        nodes1 = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes1), 1)
        nodes2 = self.waitForNodes('fake-label2')
        self.assertEqual(len(nodes2), 1)

        # We will take this node offline later
        req1 = zk.NodeRequest()
        req1.state = zk.REQUESTED
        req1.node_types.append('fake-label')

        # This nod does not perform host checks so never goes offline
        req2 = zk.NodeRequest()
        req2.state = zk.REQUESTED
        req2.node_types.append('fake-label2')

        # Take the first node offline then submit a node request for
        # it (which should be accepted but then released once the
        # driver fails the liveness check).
        with mock.patch("nodepool.nodeutils.nodescan") as nodescan_mock:
            nodescan_mock.side_effect = OSError
            self.zk.storeNodeRequest(req1)
            self.waitForNodeDeletion(nodes1[0])

            # We know the first request has been accepted and
            # processed since the node was deleted.  At this point,
            # submit the second request.
            self.zk.storeNodeRequest(req2)

            self.log.debug("Waiting for request %s", req2.id)
            req2 = self.waitForNodeRequest(req2)
            # The second request is fulfilled; get the status of the
            # first request at the same time.
            req1 = self.zk.getNodeRequest(req1.id)

        # Verify that the first request was not fulfilled at the time
        # that the second was.
        self.assertEqual(req1.state, zk.REQUESTED)
        self.assertEqual(req2.state, zk.FULFILLED)
        self.assertEqual(len(req2.nodes), 1)
        self.assertNotEqual(req2.nodes[0], nodes2[0].id)

        # Now let req1 complete with the node online.
        self.log.debug("Waiting for request %s", req1.id)
        req1 = self.waitForNodeRequest(req1)
        self.assertEqual(req1.state, zk.FULFILLED)
        self.assertEqual(len(req1.nodes), 1)
        self.assertNotEqual(req1.nodes[0], nodes1[0].id)

    def test_host_key_checking_toggle(self):
        """Test that host key checking can be disabled"""
        configfile = self.setup_config('static-no-check.yaml')
        with mock.patch("nodepool.nodeutils.nodescan") as nodescan_mock:
            pool = self.useNodepool(configfile, watermark_sleep=1)
            self.startPool(pool)
            nodes = self.waitForNodes('fake-label')
            self.assertEqual(len(nodes), 1)
            nodescan_mock.assert_not_called()

    def test_static_shell_type(self):
        '''
        Test that static python-path works.
        '''
        configfile = self.setup_config('static-shell-type.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        self.log.debug("Waiting for node pre-registration")
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(nodes[0].shell_type, "cmd")

        nodes[0].state = zk.USED
        self.zk.storeNode(nodes[0])

        self.log.debug("Waiting for node to be re-available")
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(nodes[0].shell_type, "cmd")

    def test_missing_static_node(self):
        """Test that a missing static node is added"""
        configfile = self.setup_config('static-2-nodes.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)

        self.log.debug("Waiting for initial nodes")
        nodes = self.waitForNodes('fake-label', 2)
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].slot, 0)
        self.assertEqual(nodes[1].slot, 0)

        self.zk.deleteNode(nodes[0])

        self.log.debug("Waiting for node to transition to ready again")
        nodes = self.waitForNodes('fake-label', 2)
        self.assertEqual(len(nodes), 2)
        self.assertEqual(nodes[0].slot, 0)
        self.assertEqual(nodes[1].slot, 0)
