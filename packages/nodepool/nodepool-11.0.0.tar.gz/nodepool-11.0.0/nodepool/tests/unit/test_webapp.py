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

import json
import logging
import yaml
from urllib import request
from urllib.error import HTTPError

from nodepool import tests
from nodepool.zk import zookeeper as zk
from nodepool.nodeutils import iterate_timeout


class TestWebApp(tests.DBTestCase):
    log = logging.getLogger("nodepool.TestWebApp")

    # A standard browser accept header
    browser_accept = (
        'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')

    def test_image_list(self):
        configfile = self.setup_config('node.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        webapp = self.useWebApp(pool, port=0)
        webapp.start()
        port = webapp.server.socket.getsockname()[1]

        # Start the builder after the pool + webapp so they see the
        # cache update
        self.useBuilder(configfile)

        self.waitForImage('fake-provider', 'fake-image')
        self.waitForNodes('fake-label')

        req = request.Request(
            "http://localhost:%s/image-list" % port)
        # NOTE(ianw): we want pretty printed text/plain back, but
        # simulating a normal web-browser request.
        req.add_header('Accept', self.browser_accept)
        f = request.urlopen(req)
        self.assertEqual(f.info().get('Content-Type'),
                         'text/plain; charset=UTF-8')
        data = f.read()
        self.assertTrue('fake-image' in data.decode('utf8'))

        # also ensure that text/plain works (might be hand-set by a
        # command-line curl script, etc)
        req = request.Request(
            "http://localhost:%s/image-list" % port)
        req.add_header('Accept', 'text/plain')
        f = request.urlopen(req)
        self.assertEqual(f.info().get('Content-Type'),
                         'text/plain; charset=UTF-8')
        data = f.read()
        self.assertTrue('fake-image' in data.decode('utf8'))

    def test_image_list_filtered(self):
        configfile = self.setup_config('node.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        webapp = self.useWebApp(pool, port=0)
        webapp.start()
        port = webapp.server.socket.getsockname()[1]

        # Start the builder after the pool + webapp so they see the
        # cache update
        self.useBuilder(configfile)

        image = self.waitForImage('fake-provider', 'fake-image')
        self.waitForNodes('fake-label')

        req = request.Request(
            "http://localhost:%s/image-list?fields=id,image,state" % port)
        req.add_header('Accept', self.browser_accept)
        f = request.urlopen(req)
        self.assertEqual(f.info().get('Content-Type'),
                         'text/plain; charset=UTF-8')
        data = f.read()
        self.assertIn(f"| {image.build_id} | fake-image | ready |",
                      data.decode('utf8'))

    def test_image_list_json(self):
        configfile = self.setup_config('node.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        webapp = self.useWebApp(pool, port=0)
        webapp.start()
        port = webapp.server.socket.getsockname()[1]

        # Start the builder after the pool + webapp so they see the
        # cache update
        self.useBuilder(configfile)

        image = self.waitForImage('fake-provider', 'fake-image')
        self.waitForNodes('fake-label')

        req = request.Request(
            "http://localhost:%s/image-list" % port)
        req.add_header('Accept', 'application/json')
        f = request.urlopen(req)
        self.assertEqual(f.info().get('Content-Type'),
                         'application/json')
        data = f.read()
        objs = json.loads(data.decode('utf8'))
        self.assertDictContainsSubset({'id': image.build_id,
                                       'image': 'fake-image',
                                       'provider': 'fake-provider',
                                       'state': 'ready'}, objs[0])

    def test_dib_image_list_json(self):
        configfile = self.setup_config('node.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        webapp = self.useWebApp(pool, port=0)
        webapp.start()
        port = webapp.server.socket.getsockname()[1]

        # Start the builder after the pool + webapp so they see the
        # cache update
        self.useBuilder(configfile)

        image = self.waitForImage('fake-provider', 'fake-image')
        self.waitForNodes('fake-label')

        req = request.Request(
            "http://localhost:%s/dib-image-list" % port)
        req.add_header('Accept', 'application/json')
        f = request.urlopen(req)
        self.assertEqual(f.info().get('Content-Type'),
                         'application/json')
        data = f.read()
        objs = json.loads(data.decode('utf8'))
        # make sure this is valid json and has some of the
        # non-changing keys
        self.assertDictContainsSubset({'id': f'fake-image-{image.build_id}',
                                       'formats': ['qcow2'],
                                       'state': 'ready'}, objs[0])

    def test_image_status_json(self):
        configfile = self.setup_config("node.yaml")
        pool = self.useNodepool(configfile, watermark_sleep=1)

        self.startPool(pool)
        webapp = self.useWebApp(pool, port=0)
        webapp.start()
        port = webapp.server.socket.getsockname()[1]

        builder = self.useBuilder(configfile)
        # Make sure we have enough time to test for the build request
        # before it's processed by the build worker.
        for worker in builder._build_workers:
            worker._interval = 60

        self.waitForImage("fake-provider", "fake-image")
        self.waitForNodes('fake-label')

        req = request.Request(
            "http://localhost:{}/image-status".format(port))
        req.add_header("Accept", "application/json")

        f = request.urlopen(req)
        self.assertEqual(f.info().get("Content-Type"),
                         "application/json")

        data = f.read()
        objs = json.loads(data.decode("utf8"))
        self.assertDictContainsSubset({"image": "fake-image",
                                       "paused": False,
                                       "build_request": None}, objs[0])

        self.zk.submitBuildRequest("fake-image")

        webapp.cache.cache.clear()
        f = request.urlopen(req)
        data = f.read()
        objs = json.loads(data.decode("utf8"))
        self.assertDictContainsSubset({"image": "fake-image",
                                       "paused": False,
                                       "build_request": "pending"}, objs[0])

        builder._janitor._emitBuildRequestStats()
        self.assertReportedStat('nodepool.image_build_requests', '1', 'g')

        webapp.cache.cache.clear()
        with self.zk.imageBuildLock('fake-image', blocking=True, timeout=1):
            f = request.urlopen(req)
            data = f.read()

        objs = json.loads(data.decode("utf8"))
        self.assertDictContainsSubset({"image": "fake-image",
                                       "paused": False,
                                       "build_request": "building"}, objs[0])

    def test_node_list_json(self):
        configfile = self.setup_config('node.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.useBuilder(configfile)
        self.startPool(pool)
        webapp = self.useWebApp(pool, port=0)
        webapp.start()
        port = webapp.server.socket.getsockname()[1]

        self.waitForImage('fake-provider', 'fake-image')
        self.waitForNodes('fake-label')

        req = request.Request(
            "http://localhost:%s/node-list" % port)
        req.add_header('Accept', 'application/json')
        f = request.urlopen(req)
        self.assertEqual(f.info().get('Content-Type'),
                         'application/json')
        data = f.read()
        objs = json.loads(data.decode('utf8'))
        # We don't check the value of 'locked' because we may get a
        # cached value returned.
        self.assertDictContainsSubset({'id': '0000000000',
                                       'ipv6': '',
                                       'label': ['fake-label'],
                                       'provider': 'fake-provider',
                                       'public_ipv4': 'fake',
                                       'connection_port': 22,
                                       'state': 'ready'}, objs[0])
        self.assertTrue('locked' in objs[0])
        # specify valid node_id
        req = request.Request(
            "http://localhost:%s/node-list?node_id=%s" % (port,
                                                          '0000000000'))
        req.add_header('Accept', 'application/json')
        f = request.urlopen(req)
        self.assertEqual(f.info().get('Content-Type'),
                         'application/json')
        data = f.read()
        objs = json.loads(data.decode('utf8'))
        # We don't check the value of 'locked' because we may get a
        # cached value returned.
        self.assertDictContainsSubset({'id': '0000000000',
                                       'ipv6': '',
                                       'label': ['fake-label'],
                                       'provider': 'fake-provider',
                                       'public_ipv4': 'fake',
                                       'connection_port': 22,
                                       'state': 'ready'}, objs[0])
        self.assertTrue('locked' in objs[0])
        # node_id not found
        req = request.Request(
            "http://localhost:%s/node-list?node_id=%s" % (port,
                                                          '999999'))
        req.add_header('Accept', 'application/json')
        f = request.urlopen(req)
        self.assertEqual(f.info().get('Content-Type'),
                         'application/json')
        data = f.read()
        objs = json.loads(data.decode('utf8'))
        self.assertEqual(0, len(objs), objs)

    def test_request_list_json(self):
        configfile = self.setup_config('node.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.useBuilder(configfile)
        self.startPool(pool)
        webapp = self.useWebApp(pool, port=0)
        webapp.start()
        port = webapp.server.socket.getsockname()[1]

        self.waitForImage('fake-provider', 'fake-image')
        self.waitForNodes('fake-label')
        req = zk.NodeRequest()
        req.state = zk.PENDING   # so it will be ignored
        req.node_types = ['fake-label']
        req.requestor = 'test_request_list'
        self.zk.storeNodeRequest(req)

        webzk = webapp.nodepool.getZK()
        for _ in iterate_timeout(30, Exception, 'cache update'):
            reqs = webzk._request_cache.getNodeRequestIds()
            if req.id in reqs:
                break

        http_req = request.Request(
            "http://localhost:%s/request-list" % port)
        http_req.add_header('Accept', 'application/json')
        f = request.urlopen(http_req)
        self.assertEqual(f.info().get('Content-Type'),
                         'application/json')
        data = f.read()
        objs = json.loads(data.decode('utf8'))
        objs = [o for o in objs if 'min-ready' not in o['requestor']]
        self.assertDictContainsSubset({'node_types': ['fake-label'],
                                       'requestor': 'test_request_list',
                                       'event_id': req.event_id, },
                                      objs[0])

    def test_label_list_json(self):
        configfile = self.setup_config('node.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.useBuilder(configfile)
        self.startPool(pool)
        webapp = self.useWebApp(pool, port=0)
        webapp.start()
        port = webapp.server.socket.getsockname()[1]

        self.waitForImage('fake-provider', 'fake-image')
        self.waitForNodes('fake-label')

        req = request.Request(
            "http://localhost:%s/label-list" % port)
        req.add_header('Accept', 'application/json')
        f = request.urlopen(req)
        self.assertEqual(f.info().get('Content-Type'),
                         'application/json')
        data = f.read()
        objs = json.loads(data.decode('utf8'))
        self.assertEqual([{'label': 'fake-label'}], objs)

    def test_webapp_config(self):
        configfile = self.setup_config('webapp.yaml')
        config = yaml.safe_load(open(configfile))
        self.assertEqual(config['webapp']['port'], 8080)
        self.assertEqual(config['webapp']['listen_address'], '127.0.0.1')

    def test_webapp_ready(self):
        configfile = self.setup_config('node.yaml')
        pool = self.useNodepool(configfile, watermark_sleep=1)

        webapp = self.useWebApp(pool, port=0)
        webapp.start()
        port = webapp.server.socket.getsockname()[1]

        # Query ready endpoint before the pool has been started. We expect
        # an error in this case.
        req = request.Request("http://localhost:%s/ready" % port)
        with self.assertRaises(HTTPError, request.urlopen, req):
            pass

        self.startPool(pool)

        # Now wait until we get a valid response.
        for _ in iterate_timeout(30, Exception, 'ready succeeds'):
            try:
                f = request.urlopen(req)
                break
            except HTTPError:
                pass

        data = f.read()
        self.assertEqual(data, b"OK")
