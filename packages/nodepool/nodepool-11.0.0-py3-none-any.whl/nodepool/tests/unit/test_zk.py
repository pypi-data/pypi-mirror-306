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

import testtools
import time
import uuid
import socket

from kazoo.protocol.states import KazooState

from nodepool import exceptions as npe
from nodepool import tests
from nodepool.zk import zookeeper as zk
from nodepool.zk.components import PoolComponent
from nodepool.config import ZooKeeperConnectionConfig, buildZooKeeperHosts
from nodepool.nodeutils import iterate_timeout
from nodepool.version import get_version_string


class TestComponentRegistry(tests.DBTestCase):

    def test_pool_component(self):
        hostname = socket.gethostname()
        launcher = PoolComponent(
            self.zk.client, hostname,
            version=get_version_string())
        launcher.content.update({
            'id': "launcher-Poolworker.provider-main-" + uuid.uuid4().hex,
            'name': 'main',
            'provider_name': 'provider',
            'supported_labels': [],
            'state': launcher.RUNNING,
        })
        launcher.register()

        for _ in iterate_timeout(10, Exception,
                                 "node in registry"):
            launcher_pools = self.zk.getRegisteredPools()
            if (len(launcher_pools) == 1 and
                launcher.id == list(launcher_pools)[0].id):
                break

        launcher.unregister()
        for _ in iterate_timeout(10, Exception,
                                 "node not in registry"):
            launcher_pools = self.zk.getRegisteredPools()
            if len(launcher_pools) == 0:
                break


class TestZooKeeper(tests.DBTestCase):

    def setUp(self):
        super(TestZooKeeper, self).setUp()

    def test_buildZooKeeperHosts_single(self):
        hosts = [
            ZooKeeperConnectionConfig('127.0.0.1', port=2181,
                                      chroot='/test1')
        ]
        self.assertEqual('127.0.0.1:2181/test1',
                         buildZooKeeperHosts(hosts))

    def test_buildZooKeeperHosts_multiple(self):
        hosts = [
            ZooKeeperConnectionConfig('127.0.0.1', port=2181,
                                      chroot='/test1'),
            ZooKeeperConnectionConfig('127.0.0.2', port=2182,
                                      chroot='/test2')
        ]
        self.assertEqual('127.0.0.1:2181/test1,127.0.0.2:2182/test2',
                         buildZooKeeperHosts(hosts))

    def test_buildZooKeeperHosts_ipv6(self):
        hosts = [
            ZooKeeperConnectionConfig(
                '2001:4800:7817:103:be76:4eff:fe04:e359', port=2181,
                chroot='/test1'),
            ZooKeeperConnectionConfig(
                '[2002:4800:7817:103:be76:4eff:fe04:e359]', port=2181,
                chroot='/test2'),
            ZooKeeperConnectionConfig('127.0.0.2', port=2182,
                                      chroot='/test3')
        ]
        self.assertEqual((
            '[2001:4800:7817:103:be76:4eff:fe04:e359]:2181/test1,'
            '[2002:4800:7817:103:be76:4eff:fe04:e359]:2181/test2,'
            '127.0.0.2:2182/test3'
        ), buildZooKeeperHosts(hosts))

    def test_imageBuildLock(self):
        path = self.zk._imageBuildLockPath("ubuntu-trusty")
        with self.zk.imageBuildLock("ubuntu-trusty", blocking=False):
            self.assertIsNotNone(self.zk.kazoo_client.exists(path))

    def test_imageBuildLock_exception_nonblocking(self):
        image = "ubuntu-trusty"
        with self.zk.imageBuildLock(image, blocking=False):
            with testtools.ExpectedException(
                npe.ZKLockException, "Did not get lock on .*"
            ):
                with self.zk.imageBuildLock(image, blocking=False):
                    pass

    def test_imageBuildLock_exception_blocking(self):
        image = "ubuntu-trusty"
        with self.zk.imageBuildLock(image, blocking=False):
            with testtools.ExpectedException(npe.TimeoutException):
                with self.zk.imageBuildLock(image, blocking=True, timeout=1):
                    pass

    def test_imageBuildIdLock(self):
        path = self.zk._imageBuildIdLockPath("ubuntu-trusty", "0000")
        with self.zk.imageBuildIdLock(
            "ubuntu-trusty", "0000", blocking=False
        ):
            self.assertIsNotNone(self.zk.kazoo_client.exists(path))

    def test_imageBuildIdLock_exception_nonblocking(self):
        image = "ubuntu-trusty"
        bnum = "0000000000"
        with self.zk.imageBuildIdLock(image, bnum, blocking=False):
            with testtools.ExpectedException(
                npe.ZKLockException, "Did not get lock on .*"
            ):
                with self.zk.imageBuildIdLock(image, bnum, blocking=False):
                    pass

    def test_imageBuildIdLock_exception_blocking(self):
        image = "ubuntu-trusty"
        bnum = "0000000000"
        with self.zk.imageBuildIdLock(image, bnum, blocking=False):
            with testtools.ExpectedException(npe.TimeoutException):
                with self.zk.imageBuildIdLock(
                    image, bnum, blocking=True, timeout=1
                ):
                    pass

    def test_imageUploadNumberLock_delete(self):
        '''
        Test that deleting an image upload number while we hold the lock
        on it works properly.
        '''
        upload = zk.ImageUpload()
        upload.image_name = "ubuntu-trusty"
        upload.build_id = "0000000003"
        upload.provider_name = "providerA"
        upload.id = "0000000001"
        path = self.zk._imageUploadNumberLockPath(upload.image_name,
                                                  upload.build_id,
                                                  upload.provider_name,
                                                  upload.id)
        with self.zk.imageUploadNumberLock(upload, blocking=False):
            self.assertIsNotNone(self.zk.kazoo_client.exists(path))
            self.zk.deleteUpload(upload.image_name,
                                 upload.build_id,
                                 upload.provider_name,
                                 upload.id)
        self.assertIsNone(self.zk.kazoo_client.exists(path))

    def test_imageUploadNumberLock_orphan(self):
        upload = zk.ImageUpload()
        upload.image_name = "ubuntu-trusty"
        upload.build_id = "0000000003"
        upload.provider_name = "providerA"

        path = self.zk._imageUploadNumberLockPath(upload.image_name,
                                                  upload.build_id,
                                                  upload.provider_name,
                                                  upload.id)

        with self.zk.imageUploadNumberLock(upload, blocking=False):
            self.assertIsNotNone(self.zk.kazoo_client.exists(path))
            self.zk.deleteUpload(upload.image_name,
                                 upload.build_id,
                                 upload.provider_name,
                                 upload.id)

        # Pretend we still think the image upload exists
        # (e.g. multiple cleanup workers itertating over uploads)
        with self.zk.imageUploadNumberLock(upload, blocking=False):
            # We now recreated an empty image upload number node
            pass

        self.assertIsNotNone(self.zk.kazoo_client.exists(path))

        # Should not throw an exception because of the empty upload
        self.zk.getImageUpload(upload.image_name, upload.build_id,
                               upload.provider_name, upload.id)

    def test_imageUploadNumberLock(self):
        upload = zk.ImageUpload()
        upload.image_name = "ubuntu-trusty"
        upload.build_id = "0000000003"
        upload.provider_name = "providerA"
        upload.id = "0000000001"
        path = self.zk._imageUploadNumberLockPath(upload.image_name,
                                                  upload.build_id,
                                                  upload.provider_name,
                                                  upload.id)
        with self.zk.imageUploadNumberLock(upload, blocking=False):
            self.assertIsNotNone(self.zk.kazoo_client.exists(path))

    def test_imageUploadNumberLock_exception_nonblocking(self):
        upload = zk.ImageUpload()
        upload.image_name = "ubuntu-trusty"
        upload.build_id = "0000000003"
        upload.provider_name = "providerA"
        upload.id = "0000000001"
        with self.zk.imageUploadNumberLock(upload, blocking=False):
            with testtools.ExpectedException(
                npe.ZKLockException, "Did not get lock on .*"
            ):
                with self.zk.imageUploadNumberLock(upload, blocking=False):
                    pass

    def test_imageUploadNumberLock_exception_blocking(self):
        upload = zk.ImageUpload()
        upload.image_name = "ubuntu-trusty"
        upload.build_id = "0000000003"
        upload.provider_name = "providerA"
        upload.id = "0000000001"
        with self.zk.imageUploadNumberLock(upload, blocking=False):
            with testtools.ExpectedException(npe.TimeoutException):
                with self.zk.imageUploadNumberLock(
                    upload, blocking=True, timeout=1
                ):
                    pass

    def test_imageUploadLock(self):
        path = self.zk._imageUploadLockPath("ubuntu-trusty", "0000", "prov1")
        with self.zk.imageUploadLock("ubuntu-trusty", "0000", "prov1",
                                     blocking=False):
            self.assertIsNotNone(self.zk.kazoo_client.exists(path))

    def test_imageUploadLock_exception_nonblocking(self):
        image = "ubuntu-trusty"
        bnum = "0000000000"
        prov = "rax"
        with self.zk.imageUploadLock(image, bnum, prov, blocking=False):
            with testtools.ExpectedException(
                npe.ZKLockException, "Did not get lock on .*"
            ):
                with self.zk.imageUploadLock(image, bnum, prov,
                                             blocking=False):
                    pass

    def test_imageUploadLock_exception_blocking(self):
        image = "ubuntu-trusty"
        bnum = "0000000000"
        prov = "rax"
        with self.zk.imageUploadLock(image, bnum, prov, blocking=False):
            with testtools.ExpectedException(npe.TimeoutException):
                with self.zk.imageUploadLock(image, bnum, prov,
                                             blocking=True, timeout=1):
                    pass

    def test_storeBuild(self):
        image = "ubuntu-trusty"
        b1 = self.zk.storeBuild(image, zk.ImageBuild())
        b2 = self.zk.storeBuild(image, zk.ImageBuild())
        self.assertNotEqual(b1, b2)

    def test_store_and_get_build(self):
        image = "ubuntu-trusty"
        orig_data = zk.ImageBuild()
        orig_data.builder = 'host.domain.com'
        orig_data.builder_id = 'ABC-123'
        orig_data.state = zk.READY
        with self.zk.imageBuildLock(image, blocking=True, timeout=1):
            build_id = self.zk.storeBuild(image, orig_data)

        data = self.zk.getBuild(image, build_id)
        self.assertEqual(orig_data.builder, data.builder)
        self.assertEqual(orig_data.builder_id, data.builder_id)
        self.assertEqual(orig_data.state, data.state)
        self.assertEqual(orig_data.state_time, data.state_time)
        self.assertEqual(build_id, data.id)
        self.assertEqual(self.zk.getImageNames(), ["ubuntu-trusty"])
        self.assertEqual(self.zk.getBuildIds("ubuntu-trusty"), [build_id])

    def test_getImageNames_not_found(self):
        self.assertEqual(self.zk.getImageNames(), [])

    def test_getBuildIds_not_found(self):
        self.assertEqual(self.zk.getBuildIds("ubuntu-trusty"), [])

    def test_getBuildProviders_not_found(self):
        self.assertEqual(self.zk.getBuildProviders(
            "ubuntu-trusty", "0000000000"), [])

    def test_getImageUploadNumbers_not_found(self):
        self.assertEqual(self.zk.getImageUploadNumbers(
            "ubuntu-trusty", "0000000000", "rax"), [])

    def test_getBuild_not_found(self):
        self.assertIsNone(self.zk.getBuild("ubuntu-trusty", "0000000000"))

    def test_getImageUpload_not_found(self):
        self.assertIsNone(
            self.zk.getImageUpload("trusty", "0001", "rax", "0000000001")
        )

    def test_storeImageUpload(self):
        image = "ubuntu-trusty"
        provider = "rax"
        bnum = self.zk.storeBuild(image, zk.ImageBuild())
        up1 = self.zk.storeImageUpload(image, bnum, provider, zk.ImageUpload())
        up2 = self.zk.storeImageUpload(image, bnum, provider, zk.ImageUpload())
        self.assertLess(int(up1), int(up2))

    def test_storeImageUpload_invalid_build(self):
        image = "ubuntu-trusty"
        build_id = uuid.uuid4().hex
        provider = "rax"
        orig_data = zk.ImageUpload()

        with testtools.ExpectedException(
            npe.ZKException, "Cannot find build .*"
        ):
            self.zk.storeImageUpload(image, build_id, provider, orig_data)

    def test_store_and_get_image_upload(self):
        image = "ubuntu-trusty"
        provider = "rax"
        orig_data = zk.ImageUpload()
        orig_data.external_id = "deadbeef"
        orig_data.state = zk.READY
        orig_data.format = "qcow2"

        build_id = self.zk.storeBuild(image, zk.ImageBuild())
        upload_id = self.zk.storeImageUpload(image, build_id, provider,
                                             orig_data)
        data = self.zk.getImageUpload(image, build_id, provider, upload_id)

        self.assertEqual(upload_id, data.id)
        self.assertEqual(orig_data.external_id, data.external_id)
        self.assertEqual(orig_data.state, data.state)
        self.assertEqual(orig_data.state_time, data.state_time)
        self.assertEqual(orig_data.format, data.format)
        self.assertEqual(self.zk.getBuildProviders("ubuntu-trusty",
                                                   build_id),
                         [provider])
        self.assertEqual(self.zk.getImageUploadNumbers("ubuntu-trusty",
                                                       build_id,
                                                       provider),
                         [upload_id])

    def test_build_request(self):
        '''Test the build request API methods (has/get/submit/remove)'''
        image = "ubuntu-trusty"
        self.zk.submitBuildRequest(image)
        self.assertTrue(self.zk.hasBuildRequest(image))
        build_request = self.zk.getBuildRequest(image)
        self.assertEqual(build_request.image_name, image)
        self.assertTrue(build_request.pending)
        self.zk.removeBuildRequest(image)
        self.assertFalse(self.zk.hasBuildRequest(image))
        build_request = self.zk.getBuildRequest(image)
        self.assertIsNone(build_request)

    def test_buildLock_orphan(self):
        image = "ubuntu-trusty"
        build_id = uuid.uuid4().hex

        path = self.zk._imageBuildIdLockPath(image, build_id)

        # Pretend we still think the image build exists
        # (e.g. multiple cleanup workers itertating over builds)
        with self.zk.imageBuildIdLock(image, build_id, blocking=False):
            # We now created an empty build id node
            pass

        self.assertIsNotNone(self.zk.kazoo_client.exists(path))

        # Should not throw an exception because of the empty upload
        self.assertIsNone(self.zk.getBuild(image, build_id))

    def test_getMostRecentBuilds(self):
        image = "ubuntu-trusty"
        v1 = {'state': zk.READY, 'state_time': int(time.time())}
        v2 = {'state': zk.READY, 'state_time': v1['state_time'] + 10}
        v3 = {'state': zk.READY, 'state_time': v1['state_time'] + 20}
        v4 = {'state': zk.DELETING, 'state_time': v2['state_time'] + 10}
        self.zk.storeBuild(image, zk.ImageBuild.fromDict(v1))
        v2_id = self.zk.storeBuild(image, zk.ImageBuild.fromDict(v2))
        v3_id = self.zk.storeBuild(image, zk.ImageBuild.fromDict(v3))
        self.zk.storeBuild(image, zk.ImageBuild.fromDict(v4))

        # v2 and v3 should be the 2 most recent 'ready' builds
        matches = self.zk.getMostRecentBuilds(2, image, zk.READY)
        self.assertEqual(2, len(matches))

        # Should be in descending order, according to state_time
        self.assertEqual(matches[0].id, v3_id)
        self.assertEqual(matches[1].id, v2_id)

    def test_getMostRecentBuildImageUploads_with_state(self):
        image = "ubuntu-trusty"
        provider = "rax"
        build = {'state': zk.READY, 'state_time': int(time.time())}
        up1 = zk.ImageUpload()
        up1.state = zk.READY
        up2 = zk.ImageUpload()
        up2.state = zk.READY
        up2.state_time = up1.state_time + 10
        up3 = zk.ImageUpload()
        up3.state = zk.DELETING
        up3.state_time = up2.state_time + 10

        bnum = self.zk.storeBuild(image, zk.ImageBuild.fromDict(build))
        self.zk.storeImageUpload(image, bnum, provider, up1)
        up2_id = self.zk.storeImageUpload(image, bnum, provider, up2)
        self.zk.storeImageUpload(image, bnum, provider, up3)

        # up2 should be the most recent 'ready' upload
        data = self.zk.getMostRecentBuildImageUploads(
            1, image, bnum, provider, zk.READY)
        self.assertNotEqual([], data)
        self.assertEqual(1, len(data))
        self.assertEqual(data[0].id, up2_id)

    def test_getMostRecentBuildImageUploads_any_state(self):
        image = "ubuntu-trusty"
        provider = "rax"
        build = {'state': zk.READY, 'state_time': int(time.time())}
        up1 = zk.ImageUpload()
        up1.state = zk.READY
        up2 = zk.ImageUpload()
        up2.state = zk.READY
        up2.state_time = up1.state_time + 10
        up3 = zk.ImageUpload()
        up3.state = zk.UPLOADING
        up3.state_time = up2.state_time + 10

        bnum = self.zk.storeBuild(image, zk.ImageBuild.fromDict(build))
        self.zk.storeImageUpload(image, bnum, provider, up1)
        self.zk.storeImageUpload(image, bnum, provider, up2)
        up3_id = self.zk.storeImageUpload(image, bnum, provider, up3)

        # up3 should be the most recent upload, regardless of state
        data = self.zk.getMostRecentBuildImageUploads(
            1, image, bnum, provider, None)
        self.assertNotEqual([], data)
        self.assertEqual(1, len(data))
        self.assertEqual(data[0].id, up3_id)

    def test_getMostRecentImageUpload(self):
        image = "ubuntu-trusty"
        provider = "rax"

        build1 = zk.ImageBuild()
        build1.state = zk.READY
        build2 = zk.ImageBuild()
        build2.state = zk.READY
        build2.state_time = build1.state_time + 10

        bnum1 = self.zk.storeBuild(image, build1)
        bnum2 = self.zk.storeBuild(image, build2)

        upload1 = zk.ImageUpload()
        upload1.state = zk.READY
        upload2 = zk.ImageUpload()
        upload2.state = zk.READY
        upload2.state_time = upload1.state_time + 10

        self.zk.storeImageUpload(image, bnum1, provider, upload1)
        self.zk.storeImageUpload(image, bnum2, provider, upload2)

        d = self.zk.getMostRecentImageUpload(image, provider, zk.READY)
        self.assertEqual(upload2.state_time, d.state_time)

    def test_getProviderUploads(self):
        image = "ubuntu-trusty"
        provider = "rax"

        build = zk.ImageBuild()
        build.state = zk.READY
        bnum = self.zk.storeBuild(image, build)

        upload = zk.ImageUpload()
        upload.state = zk.READY
        upnum = self.zk.storeImageUpload(image, bnum, provider, upload)

        d = self.zk.getProviderUploads(provider)
        self.assertIn(image, d)
        self.assertIn(bnum, d[image])
        self.assertEqual(1, len(d[image][bnum]))
        self.assertIsInstance(d[image][bnum][0], zk.ImageUpload)
        self.assertEqual(upnum, d[image][bnum][0].id)

    def test_getBuilds_any(self):
        image = "ubuntu-trusty"
        path = self.zk._imageBuildsPath(image)
        v1 = zk.ImageBuild()
        v1.state = zk.READY
        v2 = zk.ImageBuild()
        v2.state = zk.BUILDING
        v3 = zk.ImageBuild()
        v3.state = zk.FAILED
        v4 = zk.ImageBuild()
        v4.state = zk.DELETING
        self.zk.kazoo_client.create(path + "/1", value=v1.serialize(),
                                    makepath=True)
        self.zk.kazoo_client.create(path + "/2", value=v2.serialize(),
                                    makepath=True)
        self.zk.kazoo_client.create(path + "/3", value=v3.serialize(),
                                    makepath=True)
        self.zk.kazoo_client.create(path + "/4", value=v4.serialize(),
                                    makepath=True)
        self.zk.kazoo_client.create(path + "/lock", makepath=True)

        matches = self.zk.getBuilds(image, None)
        self.assertEqual(4, len(matches))

    def test_getBuilds(self):
        image = "ubuntu-trusty"
        path = self.zk._imageBuildsPath(image)
        v1 = zk.ImageBuild()
        v1.state = zk.READY
        v2 = zk.ImageBuild()
        v2.state = zk.BUILDING
        v3 = zk.ImageBuild()
        v3.state = zk.FAILED
        v4 = zk.ImageBuild()
        v4.state = zk.DELETING
        self.zk.kazoo_client.create(path + "/1", value=v1.serialize(),
                                    makepath=True)
        self.zk.kazoo_client.create(path + "/2", value=v2.serialize(),
                                    makepath=True)
        self.zk.kazoo_client.create(path + "/3", value=v3.serialize(),
                                    makepath=True)
        self.zk.kazoo_client.create(path + "/4", value=v4.serialize(),
                                    makepath=True)
        self.zk.kazoo_client.create(path + "/lock", makepath=True)

        matches = self.zk.getBuilds(image, [zk.DELETING, zk.FAILED])
        self.assertEqual(2, len(matches))

    def test_getUploads(self):
        path = self.zk._imageUploadPath("trusty", "000", "rax")
        v1 = zk.ImageUpload()
        v1.state = zk.READY
        v2 = zk.ImageUpload()
        v2.state = zk.UPLOADING
        v3 = zk.ImageUpload()
        v3.state = zk.FAILED
        v4 = zk.ImageUpload()
        v4.state = zk.DELETING
        self.zk.kazoo_client.create(path + "/1", value=v1.serialize(),
                                    makepath=True)
        self.zk.kazoo_client.create(path + "/2", value=v2.serialize(),
                                    makepath=True)
        self.zk.kazoo_client.create(path + "/3", value=v3.serialize(),
                                    makepath=True)
        self.zk.kazoo_client.create(path + "/4", value=v4.serialize(),
                                    makepath=True)
        self.zk.kazoo_client.create(path + "/lock", makepath=True)

        matches = self.zk.getUploads("trusty", "000", "rax",
                                     [zk.DELETING, zk.FAILED])
        self.assertEqual(2, len(matches))

    def test_getUploads_any(self):
        path = self.zk._imageUploadPath("trusty", "000", "rax")
        v1 = zk.ImageUpload()
        v1.state = zk.READY
        v2 = zk.ImageUpload()
        v2.state = zk.UPLOADING
        v3 = zk.ImageUpload()
        v3.state = zk.FAILED
        v4 = zk.ImageUpload()
        v4.state = zk.DELETING
        self.zk.kazoo_client.create(path + "/1", value=v1.serialize(),
                                    makepath=True)
        self.zk.kazoo_client.create(path + "/2", value=v2.serialize(),
                                    makepath=True)
        self.zk.kazoo_client.create(path + "/3", value=v3.serialize(),
                                    makepath=True)
        self.zk.kazoo_client.create(path + "/4", value=v4.serialize(),
                                    makepath=True)
        self.zk.kazoo_client.create(path + "/lock", makepath=True)

        matches = self.zk.getUploads("trusty", "000", "rax", None)
        self.assertEqual(4, len(matches))

    def test_deleteBuild(self):
        image = 'trusty'
        build = zk.ImageBuild()
        build.state = zk.READY
        bnum = self.zk.storeBuild(image, build)
        self.assertTrue(self.zk.deleteBuild(image, bnum))

    def test_deleteBuild_with_uploads(self):
        image = 'trusty'
        provider = 'rax'

        build = zk.ImageBuild()
        build.state = zk.READY
        bnum = self.zk.storeBuild(image, build)

        upload = zk.ImageUpload()
        upload.state = zk.READY
        self.zk.storeImageUpload(image, bnum, provider, upload)

        self.assertFalse(self.zk.deleteBuild(image, bnum))

    def test_deleteUpload(self):
        path = self.zk._imageUploadPath("trusty", "000", "rax") + "/000001"
        self.zk.kazoo_client.create(path, makepath=True)
        self.zk.deleteUpload("trusty", "000", "rax", "000001")
        self.assertIsNone(self.zk.kazoo_client.exists(path))

    def test_getNodeRequests_empty(self):
        self.assertEqual([], self.zk.getNodeRequests())

    def test_getNodeRequests(self):
        r1 = self.zk._requestPath("500-123")
        r2 = self.zk._requestPath("100-456")
        r3 = self.zk._requestPath("100-123")
        r4 = self.zk._requestPath("400-123")
        self.zk.kazoo_client.create(r1, makepath=True, ephemeral=True)
        self.zk.kazoo_client.create(r2, makepath=True, ephemeral=True)
        self.zk.kazoo_client.create(r3, makepath=True, ephemeral=True)
        self.zk.kazoo_client.create(r4, makepath=True, ephemeral=True)

        self.assertEqual(
            ["100-123", "100-456", "400-123", "500-123"],
            self.zk.getNodeRequests()
        )

    def test_getNodeRequest(self):
        r = zk.NodeRequest("500-123")
        r.state = zk.REQUESTED
        path = self.zk._requestPath(r.id)
        self.zk.kazoo_client.create(path, value=r.serialize(),
                                    makepath=True, ephemeral=True)
        o = self.zk.getNodeRequest(r.id)
        self.assertIsInstance(o, zk.NodeRequest)
        self.assertEqual(r.id, o.id)

    def test_getNodeRequest_not_found(self):
        self.assertIsNone(self.zk.getNodeRequest("invalid"))

    def test_getNodes(self):
        self.zk.kazoo_client.create(self.zk._nodePath('100'), makepath=True)
        self.zk.kazoo_client.create(self.zk._nodePath('200'), makepath=True)
        nodes = self.zk.getNodes()
        self.assertIn('100', nodes)
        self.assertIn('200', nodes)

    def test_getNode(self):
        n = zk.Node('100')
        n.state = zk.BUILDING
        path = self.zk._nodePath(n.id)
        self.zk.kazoo_client.create(path, value=n.serialize(), makepath=True)
        o = self.zk.getNode(n.id)
        self.assertIsInstance(o, zk.Node)
        self.assertEqual(n.id, o.id)

    def test_getNode_not_found(self):
        self.assertIsNone(self.zk.getNode("invalid"))

    def test_lockNode_multi(self):
        node = zk.Node('100')
        self.zk.lockNode(node)
        with testtools.ExpectedException(
            npe.ZKLockException, "Did not get thread lock on .*"
        ):
            self.zk.lockNode(node, blocking=False)

        node2 = zk.Node('100')
        with testtools.ExpectedException(
            npe.ZKLockException, "Did not get lock on .*"
        ):
            self.zk.lockNode(node2, blocking=False)

    def test_lockNode_unlockNode(self):
        node = zk.Node('100')
        self.zk.lockNode(node)
        self.assertIsNotNone(node.lock)
        self.assertIsNotNone(
            self.zk.kazoo_client.exists(self.zk._nodeLockPath(node.id))
        )
        self.zk.unlockNode(node)
        self.assertIsNone(node.lock)

    def test_unlockNode_not_locked(self):
        node = zk.Node('100')
        with testtools.ExpectedException(npe.ZKLockException):
            self.zk.unlockNode(node)

    def test_forceUnlockNode(self):
        node = zk.Node('100')
        self.zk.lockNode(node, ephemeral=False)
        self.assertIsNotNone(
            self.zk.kazoo_client.exists(self.zk._nodeLockPath(node.id))
        )
        lock_path = self.zk._nodeLockPath(node.id)
        children = self.zk.kazoo_client.get_children(lock_path)
        self.assertEqual(1, len(children))

        # Create a node that alpha sorts before the real lock
        fake_path = f'{lock_path}/aaaa'
        self.zk.kazoo_client.create(fake_path, sequence=True)

        self.zk.forceUnlockNode(node)

        children = self.zk.kazoo_client.get_children(lock_path)
        self.assertEqual(['aaaa0000000001'], children)

    def _create_node(self):
        node = zk.Node()
        node.state = zk.BUILDING
        node.provider = 'rax'

        self.assertIsNone(node.id)
        self.zk.storeNode(node)
        self.assertIsNotNone(node.id)
        self.assertIsNotNone(
            self.zk.kazoo_client.exists(self.zk._nodePath(node.id))
        )
        return node

    def test_storeNode(self):
        node = self._create_node()
        node2 = self.zk.getNode(node.id)
        self.assertEqual(node, node2)

    def test_storeNode_update(self):
        node = self._create_node()
        node.state = zk.READY
        self.zk.storeNode(node)
        node2 = self.zk.getNode(node.id)
        self.assertEqual(node, node2)

    def _create_node_request(self):
        req = zk.NodeRequest()
        req.state = zk.REQUESTED
        req.node_types.append('label1')
        self.zk.storeNodeRequest(req)
        self.assertIsNotNone(
            self.zk.kazoo_client.exists(self.zk._requestPath(req.id))
        )
        return req

    def test_storeNodeRequest(self):
        req = self._create_node_request()
        self.assertNotEqual(req.event_id, None)
        req2 = self.zk.getNodeRequest(req.id)
        self.assertEqual(req, req2)

    def test_storeNodeRequest_update(self):
        req = self._create_node_request()
        req.state = zk.FULFILLED
        self.zk.storeNodeRequest(req)
        self.assertIsNotNone(req.id)
        req2 = self.zk.getNodeRequest(req.id)
        self.assertEqual(req, req2)

    def test_deleteNodeRequest(self):
        req = self._create_node_request()
        self.zk.deleteNodeRequest(req)
        self.assertIsNone(
            self.zk.kazoo_client.exists(self.zk._requestPath(req.id))
        )

    def test_deleteNode(self):
        n1 = self._create_node()
        self.zk.deleteNode(n1)
        self.assertIsNone(
            self.zk.kazoo_client.exists(self.zk._nodePath(n1.id))
        )

    def test_getReadyNodesOfTypes(self):
        n1 = self._create_node()
        n1.type = 'label1'
        n1.state = zk.READY
        self.zk.storeNode(n1)
        n2 = self._create_node()
        n2.state = zk.READY
        n2.type = 'label1'
        self.zk.storeNode(n2)
        n3 = self._create_node()
        n3.state = zk.READY
        n3.type = 'label2'
        self.zk.storeNode(n3)

        for _ in iterate_timeout(10, Exception, "wait for cache"):
            r = self.zk.getReadyNodesOfTypes(['label1'])
            if len(r.get('label1')) == 2:
                break

        self.assertIn('label1', r)
        self.assertEqual(2, len(r['label1']))
        self.assertIn(n1, r['label1'])
        self.assertIn(n2, r['label1'])

    def test_getReadyNodesOfTypes_multilabel(self):
        n1 = self._create_node()
        n1.type = 'label1'
        n1.state = zk.READY
        self.zk.storeNode(n1)
        n2 = self._create_node()
        n2.state = zk.READY
        n2.type = ['label1', 'label3']
        self.zk.storeNode(n2)
        n3 = self._create_node()
        n3.state = zk.READY
        n3.type = 'label2'
        self.zk.storeNode(n3)

        for _ in iterate_timeout(10, Exception, "wait for cache"):
            r = self.zk.getReadyNodesOfTypes(['label1', 'label3'])
            if (len(r.get('label1')) == 2 and
                len(r.get('label3')) == 1):
                break

        self.assertIn('label1', r)
        self.assertIn('label3', r)
        self.assertEqual(2, len(r['label1']))
        self.assertEqual(1, len(r['label3']))
        self.assertIn(n1, r['label1'])
        self.assertIn(n2, r['label1'])
        self.assertIn(n2, r['label3'])

    def test_nodeIterator(self):
        n1 = self._create_node()
        i = self.zk.nodeIterator(cached=False)
        self.assertEqual(n1, next(i))
        with testtools.ExpectedException(StopIteration):
            next(i)

    def test_getNodeRequestLockIDs(self):
        req = self._create_node_request()
        self.zk.lockNodeRequest(req, blocking=False)
        lock_ids = self.zk.getNodeRequestLockIDs()
        self.assertEqual(1, len(lock_ids))
        self.assertEqual(req.id, lock_ids[0])
        self.zk.unlockNodeRequest(req)
        self.zk.deleteNodeRequest(req)

    def test_getNodeRequestLockStats(self):
        req = self._create_node_request()
        self.zk.lockNodeRequest(req, blocking=False)
        lock_stats = self.zk.getNodeRequestLockStats(req.id)
        self.assertEqual(lock_stats.lock_id, req.id)
        self.assertIsNotNone(lock_stats.stat)
        self.zk.unlockNodeRequest(req)
        self.zk.deleteNodeRequest(req)

    def test_nodeRequestLockStatsIterator(self):
        req = self._create_node_request()
        self.zk.lockNodeRequest(req, blocking=False)
        i = self.zk.nodeRequestLockStatsIterator()
        self.assertEqual(zk.NodeRequestLockStats(req.id), next(i))
        with testtools.ExpectedException(StopIteration):
            next(i)
        self.zk.unlockNodeRequest(req)
        self.zk.deleteNodeRequest(req)

    def test_nodeRequestIterator(self):
        req = self._create_node_request()
        self.zk.lockNodeRequest(req, blocking=False)
        i = self.zk.nodeRequestIterator()
        self.assertEqual(req, next(i))
        with testtools.ExpectedException(StopIteration):
            next(i)
        self.zk.unlockNodeRequest(req)
        self.zk.deleteNodeRequest(req)

    def test_deleteNodeRequestLock(self):
        req = self._create_node_request()
        self.zk.lockNodeRequest(req, blocking=False)
        self.zk.unlockNodeRequest(req)
        self.zk.deleteNodeRequest(req)

        # We expect the lock to linger even after the request is deleted
        lock_ids = self.zk.getNodeRequestLockIDs()
        self.assertEqual(1, len(lock_ids))
        self.assertEqual(req.id, lock_ids[0])
        self.zk.deleteNodeRequestLock(lock_ids[0])
        self.assertEqual([], self.zk.getNodeRequestLockIDs())

    def test_node_caching(self):
        '''
        Test that node iteration using both cached and uncached calls
        produces identical results.
        '''
        # Test new node in node set
        n1 = self._create_node()

        # uncached
        a1 = self.zk.nodeIterator(cached=False)
        self.assertEqual(n1, next(a1))

        # cached
        a2 = self.zk.nodeIterator(cached=True)
        self.assertEqual(n1, next(a2))
        with testtools.ExpectedException(StopIteration):
            next(a2)

        # Test modification of existing node set
        n1.state = zk.HOLD
        n1.label = "oompaloompa"
        self.zk.storeNode(n1)

        # uncached
        b1 = self.zk.nodeIterator(cached=False)
        self.assertEqual(n1, next(b1))

        # cached
        for _ in iterate_timeout(10, Exception,
                                 "cached node equals original node"):
            b2 = self.zk.nodeIterator(cached=True)
            if n1 == next(b2):
                break


class TestZKModel(tests.BaseTestCase):

    def setUp(self):
        super(TestZKModel, self).setUp()

    def test_BaseModel_bad_id(self):
        with testtools.ExpectedException(
            TypeError, "'id' attribute must be a string type"
        ):
            zk.BaseModel(123)

    def test_BaseModel_bad_state(self):
        with testtools.ExpectedException(
            TypeError, "'blah' is not a valid state"
        ):
            o = zk.BaseModel('0001')
            o.state = 'blah'

    def test_BaseModel_toDict(self):
        o = zk.BaseModel('0001')
        d = o.toDict()
        self.assertNotIn('id', d)

    def test_ImageBuild_toDict(self):
        o = zk.ImageBuild('0001')
        o.state = zk.BUILDING
        o.builder = 'localhost'
        o.builder_id = 'ABC-123'
        o.formats = ['qemu', 'raw']

        d = o.toDict()
        self.assertNotIn('id', d)
        self.assertEqual(o.state, d['state'])
        self.assertIsNotNone(d['state_time'])
        self.assertEqual(','.join(o.formats), d['formats'])
        self.assertEqual(o.builder, d['builder'])
        self.assertEqual(o.builder_id, d['builder_id'])

    def test_ImageBuild_fromDict(self):
        now = int(time.time())
        d_id = '0001'
        d = {
            'builder': 'localhost',
            'builder_id': 'ABC-123',
            'formats': 'qemu,raw',
            'state': zk.BUILDING,
            'state_time': now
        }

        o = zk.ImageBuild.fromDict(d, 'image_name', d_id)
        self.assertEqual(o.id, d_id)
        self.assertEqual(o.state, d['state'])
        self.assertEqual(o.state_time, d['state_time'])
        self.assertEqual(o.builder, d['builder'])
        self.assertEqual(o.builder_id, d['builder_id'])
        self.assertEqual(o.formats, d['formats'].split(','))

    def test_ImageUpload_toDict(self):
        o = zk.ImageUpload('0001', '0003')
        o.state = zk.UPLOADING
        o.external_id = 'DEADBEEF'
        o.external_name = 'trusty'
        o.format = 'qcow2'

        d = o.toDict()
        self.assertNotIn('id', d)
        self.assertNotIn('build_id', d)
        self.assertNotIn('provider_name', d)
        self.assertNotIn('image_name', d)
        self.assertEqual(o.state, d['state'])
        self.assertEqual(o.state_time, d['state_time'])
        self.assertEqual(o.external_id, d['external_id'])
        self.assertEqual(o.external_name, d['external_name'])
        self.assertEqual(o.format, d['format'])

    def test_ImageUpload_fromDict(self):
        now = int(time.time())
        upload_id = '0001'
        build_id = '0003'
        d = {
            'external_id': 'DEADBEEF',
            'external_name': 'trusty',
            'format': 'qcow2',
            'state': zk.READY,
            'state_time': now
        }

        o = zk.ImageUpload.fromDict(d, build_id, 'rax', 'trusty', upload_id)
        self.assertEqual(o.id, upload_id)
        self.assertEqual(o.build_id, build_id)
        self.assertEqual(o.provider_name, 'rax')
        self.assertEqual(o.image_name, 'trusty')
        self.assertEqual(o.state, d['state'])
        self.assertEqual(o.state_time, d['state_time'])
        self.assertEqual(o.external_id, d['external_id'])
        self.assertEqual(o.external_name, d['external_name'])
        self.assertEqual(o.format, d['format'])

    def test_NodeRequest_toDict(self):
        o = zk.NodeRequest("500-123")
        o.declined_by.append("abc")
        o.node_types.append('trusty')
        o.nodes.append('100')
        o.reuse = False
        o.requestor = 'zuul'
        o.provider = "test"
        o.relative_priority = 1
        o.event_id = "deadbeef"
        d = o.toDict()
        self.assertNotIn('id', d)
        self.assertIn('state', d)
        self.assertIn('state_time', d)
        self.assertEqual(d['declined_by'], o.declined_by)
        self.assertEqual(d['node_types'], o.node_types)
        self.assertEqual(d['nodes'], o.nodes)
        self.assertEqual(d['reuse'], o.reuse)
        self.assertEqual(d['requestor'], o.requestor)
        self.assertEqual(d['provider'], o.provider)
        self.assertEqual(d['relative_priority'], o.relative_priority)
        self.assertEqual(d['event_id'], o.event_id)

    def test_NodeRequest_fromDict(self):
        now = int(time.time())
        req_id = "500-123"
        d = {
            'state': zk.REQUESTED,
            'state_time': now,
            'declined_by': ['abc'],
            'node_types': ['trusty'],
            'nodes': ['100'],
            'reuse': False,
            'requestor': 'zuul',
            'provider': 'test',
            'relative_priority': 1,
            'event_id': 'deadbeef',
        }

        o = zk.NodeRequest.fromDict(d, req_id)
        self.assertEqual(o.id, req_id)
        self.assertEqual(o.state, d['state'])
        self.assertEqual(o.state_time, d['state_time'])
        self.assertEqual(o.declined_by, d['declined_by'])
        self.assertEqual(o.node_types, d['node_types'])
        self.assertEqual(o.nodes, d['nodes'])
        self.assertEqual(o.reuse, d['reuse'])
        self.assertEqual(o.requestor, d['requestor'])
        self.assertEqual(o.provider, d['provider'])
        self.assertEqual(o.relative_priority, d['relative_priority'])
        self.assertEqual(o.event_id, d['event_id'])

    def test_Node_toDict(self):
        o = zk.Node('123')
        o.state = zk.INIT
        o.provider = 'rax'
        o.type = 'trusty'
        o.allocated_to = '456-789'
        o.az = 'RegionOne'
        o.region = 'fake-region'
        o.public_ipv4 = '<ipv4>'
        o.private_ipv4 = '<pvt-ipv4>'
        o.public_ipv6 = '<ipv6>'
        o.host_id = 'fake-host-id'
        o.image_id = 'image-id'
        o.launcher = 'launcher-Poolworker.provider-main-' + uuid.uuid4().hex
        o.external_id = 'ABCD'
        o.hostname = 'xyz'
        o.comment = 'comment'
        o.hold_job = 'hold job'
        o.host_keys = ['key1', 'key2']
        o.attributes = {'executor-zone': 'vpn'}
        o.node_properties = {}

        d = o.toDict()
        self.assertNotIn('id', d)
        self.assertEqual(d['state'], o.state)
        self.assertIn('state_time', d)
        self.assertIn('created_time', d)
        self.assertEqual(d['provider'], o.provider)
        self.assertEqual(d['type'], o.type)
        self.assertEqual(d['allocated_to'], o.allocated_to)
        self.assertEqual(d['az'], o.az)
        self.assertEqual(d['region'], o.region)
        self.assertEqual(d['public_ipv4'], o.public_ipv4)
        self.assertEqual(d['private_ipv4'], o.private_ipv4)
        self.assertEqual(d['public_ipv6'], o.public_ipv6)
        self.assertEqual(d['host_id'], o.host_id)
        self.assertEqual(d['image_id'], o.image_id)
        self.assertEqual(d['launcher'], o.launcher)
        self.assertEqual(d['external_id'], o.external_id)
        self.assertEqual(d['hostname'], o.hostname)
        self.assertEqual(d['comment'], o.comment)
        self.assertEqual(d['hold_job'], o.hold_job)
        self.assertEqual(d['host_keys'], o.host_keys)
        self.assertEqual(d['attributes'], o.attributes)
        self.assertEqual(d['node_properties'], o.node_properties)

    def test_Node_fromDict(self):
        now = int(time.time())
        node_id = '123'
        launcher_id = 'launcher-Poolworker.provider-main-' + uuid.uuid4().hex
        d = {
            'state': zk.READY,
            'state_time': now,
            'created_time': now - 2,
            'provider': 'rax',
            'type': ['trusty'],
            'allocated_to': '456-789',
            'az': 'RegionOne',
            'region': 'fake-region',
            'public_ipv4': '<ipv4>',
            'private_ipv4': '<pvt-ipv4>',
            'public_ipv6': '<ipv6>',
            'host_id': 'fake-host-id',
            'image_id': 'image-id',
            'launcher': launcher_id,
            'external_id': 'ABCD',
            'hostname': 'xyz',
            'comment': 'comment',
            'hold_job': 'hold job',
            'host_keys': ['key1', 'key2'],
            'connection_port': 22022,
            'attributes': {'executor-zone': 'vpn'},
        }

        o = zk.Node.fromDict(d, node_id)
        self.assertEqual(o.id, node_id)
        self.assertEqual(o.state, d['state'])
        self.assertEqual(o.state_time, d['state_time'])
        self.assertEqual(o.created_time, d['created_time'])
        self.assertEqual(o.provider, d['provider'])
        self.assertEqual(o.type, d['type'])
        self.assertEqual(o.allocated_to, d['allocated_to'])
        self.assertEqual(o.az, d['az'])
        self.assertEqual(o.region, d['region'])
        self.assertEqual(o.public_ipv4, d['public_ipv4'])
        self.assertEqual(o.private_ipv4, d['private_ipv4'])
        self.assertEqual(o.public_ipv6, d['public_ipv6'])
        self.assertEqual(o.host_id, d['host_id'])
        self.assertEqual(o.image_id, d['image_id'])
        self.assertEqual(o.launcher, d['launcher'])
        self.assertEqual(o.external_id, d['external_id'])
        self.assertEqual(o.hostname, d['hostname'])
        self.assertEqual(o.comment, d['comment'])
        self.assertEqual(o.hold_job, d['hold_job'])
        self.assertEqual(o.host_keys, d['host_keys'])
        self.assertEqual(o.connection_port, d['connection_port'])
        self.assertEqual(o.attributes, d['attributes'])

    def test_custom_connection_port(self):
        n = zk.Node('0001')
        n.state = zk.BUILDING
        d = n.toDict()
        self.assertEqual(d["connection_port"], 22, "Default port not 22")
        n = zk.Node.fromDict(d, '0001')
        self.assertEqual(n.connection_port, 22, "Default port not 22")
        n.connection_port = 22022
        d = n.toDict()
        self.assertEqual(d["connection_port"], 22022,
                         "Custom ssh port not set")


class SimpleTreeCacheObject:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.path = '/'.join(key)

    def updateFromDict(self, data):
        self.data = data


class SimpleTreeCache(zk.NodepoolTreeCache):
    def objectFromDict(self, d, key):
        return SimpleTreeCacheObject(key, d)

    def parsePath(self, path):
        return tuple(path.split('/'))


class TestTreeCache(tests.DBTestCase):
    # A very simple smoke test of the tree cache

    def waitForCache(self, cache, contents):
        paths = set(contents.keys())
        for _ in iterate_timeout(10, Exception, 'cache to sync', interval=0.1):
            cached_paths = cache._cached_paths.copy()
            cached_paths.discard(cache.root)
            object_paths = set(
                [x.path for x in cache._cached_objects.values()])
            if paths == cached_paths == object_paths:
                found = True
                for obj in cache._cached_objects.values():
                    if contents[obj.path] != obj.data:
                        found = False
                if found:
                    return

    def test_tree_cache(self):
        client = self.zk.kazoo_client
        data = b'{}'
        client.create('/test', data)
        client.create('/test/foo', data)
        cache = SimpleTreeCache(self.zk, "/test")
        self.waitForCache(cache, {
            '/test/foo': {},
        })
        client.create('/test/bar', data)
        self.waitForCache(cache, {
            '/test/foo': {},
            '/test/bar': {},
        })
        client.set('/test/bar', b'{"value":1}')
        self.waitForCache(cache, {
            '/test/foo': {},
            '/test/bar': {'value': 1},
        })
        client.delete('/test/bar')
        self.waitForCache(cache, {
            '/test/foo': {},
        })

        # Simulate a change happening while the state was lost
        cache._cached_paths.add('/test/bar')
        cache._sessionListener(KazooState.LOST)
        cache._sessionListener(KazooState.CONNECTED)
        self.waitForCache(cache, {
            '/test/foo': {},
        })

        # Simulate a change happening while the state was suspendede
        cache._cached_paths.add('/test/bar')
        cache._sessionListener(KazooState.SUSPENDED)
        cache._sessionListener(KazooState.CONNECTED)
        self.waitForCache(cache, {
            '/test/foo': {},
        })

    def test_tree_cache_root(self):
        client = self.zk.kazoo_client
        data = b'{}'
        client.create('/foo', data)
        cache = SimpleTreeCache(self.zk, "/")
        for _ in iterate_timeout(10, Exception, 'cache to sync', interval=0.1):
            cached_paths = cache._cached_paths.copy()
            cached_paths.discard(cache.root)
            object_paths = set(
                [x.path for x in cache._cached_objects.values()])
            if ('/foo' in cached_paths and
                '/foo' in object_paths):
                break

    def test_tree_cache_qsize_warning(self):
        with self.assertLogs('nodepool.zk.ZooKeeper', level='DEBUG') as logs:
            cache = SimpleTreeCache(self.zk, "/test")
            cache._last_event_warning = 0
            cache._last_playback_warning = 0
            cache.qsize_warning_threshold = -1

            data = b'{}'
            client = self.zk.kazoo_client
            client.create('/test', data)
            client.create('/test/foo', data)
            self.waitForCache(cache, {
                '/test/foo': {},
            })

            found_event_warning = False
            found_playback_warning = False
            for line in logs.output:
                self.log.debug("Received %s", str(line))
                if 'Event queue size for cache' in str(line):
                    found_event_warning = True
                if 'Playback queue size for cache' in str(line):
                    found_playback_warning = True
            self.assertTrue(found_event_warning)
            self.assertTrue(found_playback_warning)

    def test_tree_cache_parsing(self):
        my_zk = zk.ZooKeeper(self.zk.client, enable_cache=True)
        # Node paths
        self.assertEqual(my_zk._node_cache.parsePath(
            '/nodepool/nodes/0000000001'),
            ('0000000001',))
        self.assertIsNone(my_zk._node_cache.parsePath(
            '/nodepool/nodes/0000000001/lock'))
        self.assertIsNone(my_zk._node_cache.parsePath(
            '/nodepool/nodes/0000000001/lock/foo'))

        self.assertEqual(my_zk._parseNodePath(
            '/nodepool/nodes/0000000001'),
            ('0000000001',))
        self.assertIsNone(my_zk._parseNodePath(
            '/nodepool/nodes/0000000001/lock'))
        self.assertIsNone(my_zk._parseNodePath(
            '/nodepool/nodes/0000000001/lock/foo'))

        self.assertIsNone(my_zk._parseNodeLockPath(
            '/nodepool/nodes/0000000001'))
        self.assertIsNone(my_zk._parseNodeLockPath(
            '/nodepool/nodes/0000000001/lock'))
        self.assertEqual(my_zk._parseNodeLockPath(
            '/nodepool/nodes/0000000001/lock/foo'),
            ('0000000001', 'foo'))

        # Request paths
        self.assertEqual(my_zk._request_cache.parsePath(
            '/nodepool/requests/0000000001'),
            ('0000000001',))
        self.assertIsNone(my_zk._request_cache.parsePath(
            '/nodepool/requests/0000000001/lock'))
        self.assertIsNone(my_zk._request_cache.parsePath(
            '/nodepool/requests/0000000001/lock/foo'))

        self.assertEqual(my_zk._parseRequestPath(
            '/nodepool/requests/0000000001'),
            ('0000000001',))
        self.assertIsNone(my_zk._parseRequestPath(
            '/nodepool/requests/0000000001/lock'))
        self.assertIsNone(my_zk._parseRequestPath(
            '/nodepool/requests/0000000001/lock/foo'))

        # Request cache doesn't cache lock contenders, so no lock path
        # parsing test

        # Image paths

        test_paths = [
            dict(path='/nodepool/images/NAME/builds/0000000001'
                 '/providers/PROVIDER/images/0000000002',
                 result=('NAME', '0000000001', 'PROVIDER', '0000000002'),
                 kind='upload'),
            dict(path='/nodepool/images/NAME/builds/0000000001'
                 '/providers/PROVIDER/images/0000000002/lock',
                 result=None,
                 kind=None),
            dict(path='/nodepool/images/NAME/builds/0000000001'
                 '/providers/PROVIDER/images/0000000002/lock/foo',
                 result=None,
                 kind=None),
            dict(path='/nodepool/images/NAME/builds/0000000001'
                 '/providers/PROVIDER/images',
                 result=None,
                 kind=None),
            dict(path='/nodepool/images/NAME/builds/0000000001'
                 '/providers/PROVIDER',
                 result=None,
                 kind=None),
            dict(path='/nodepool/images/NAME/builds/0000000001'
                 '/providers',
                 result=None,
                 kind=None),
            dict(path='/nodepool/images/NAME/builds/0000000001',
                 result=('NAME', '0000000001'),
                 kind='build'),
            dict(path='/nodepool/images/NAME/builds/0000000001'
                 '/lock',
                 result=None,
                 kind=None),
            dict(path='/nodepool/images/NAME/builds/0000000001'
                 '/lock/foo',
                 result=None,
                 kind=None),
            dict(path='/nodepool/images/NAME/builds',
                 result=None,
                 kind=None),
            dict(path='/nodepool/images/NAME/pause',
                 result=('NAME',),
                 kind='image pause'),
            dict(path='/nodepool/images/NAME',
                 result=('NAME',),
                 kind='image'),
        ]

        for test in test_paths:
            res = my_zk._image_cache.parsePath(test['path'])
            if test['result'] and test['kind'] != 'image pause':
                self.assertEqual(test['result'], res)
            else:
                self.assertIsNone(res)

            checked = False
            res = my_zk._parseImageUploadPath(test['path'])
            if test['kind'] == 'upload':
                checked = True
                self.assertEqual(test['result'], res)
            else:
                self.assertIsNone(res)

            res = my_zk._parseImageBuildPath(test['path'])
            if test['kind'] == 'build':
                checked = True
                self.assertEqual(test['result'], res)
            else:
                self.assertIsNone(res)

            res = my_zk._parseImagePausePath(test['path'])
            if test['kind'] == 'image pause':
                checked = True
                self.assertEqual(test['result'], res)
            else:
                self.assertIsNone(res)

            res = my_zk._parseImagePath(test['path'])
            if test['kind'] == 'image':
                checked = True
                self.assertEqual(test['result'], res)
            else:
                self.assertIsNone(res)

            if not checked and test['kind']:
                raise Exception("Unhandled kind %s" % (test['kind']))

    def test_node_cache_lock_handling(self):
        my_zk = zk.ZooKeeper(self.zk.client, enable_cache=True)
        node = zk.Node()
        node.state = zk.BUILDING
        node.provider = 'rax'
        my_zk.storeNode(node)
        my_zk.lockNode(node)

        for _ in iterate_timeout(10, Exception, 'cache to sync', interval=0.1):
            cached_node = my_zk.getNode(node.id, cached=True, only_cached=True)
            if len(cached_node.lock_contenders):
                break
        self.assertEqual(len(cached_node.lock_contenders), 1)

        my_zk._node_cache._sessionListener(KazooState.LOST)
        my_zk._node_cache._sessionListener(KazooState.CONNECTED)
        my_zk._node_cache.ensureReady()
        my_zk._node_cache._event_queue.join()
        my_zk._node_cache._playback_queue.join()

        self.assertEqual(len(cached_node.lock_contenders), 1)
        my_zk.unlockNode(node)

        for _ in iterate_timeout(10, Exception, 'cache to sync', interval=0.1):
            if not len(cached_node.lock_contenders):
                break
        self.assertEqual(len(cached_node.lock_contenders), 0)
