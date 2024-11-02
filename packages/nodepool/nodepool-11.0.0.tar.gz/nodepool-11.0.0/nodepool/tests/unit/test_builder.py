# Copyright (C) 2015 Hewlett-Packard Development Company, L.P.
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

import os
import uuid
import fixtures
import mock
import socket
import time

from nodepool import builder, tests
from nodepool.driver.fake import adapter as fakeadapter
from nodepool.zk import zookeeper as zk
from nodepool.config import Config
from nodepool.nodeutils import iterate_timeout


class TestNodepoolBuilderDibImage(tests.BaseTestCase):
    def test_from_image_id(self):
        tempdir = fixtures.TempDir()
        self.useFixture(tempdir)
        image_path = os.path.join(tempdir.path, 'myid1234.qcow2')
        open(image_path, 'w')

        images = builder.DibImageFile.from_image_id(tempdir.path, 'myid1234')
        self.assertEqual(len(images), 1)

        image = images[0]
        self.assertEqual(image.image_id, 'myid1234')
        self.assertEqual(image.extension, 'qcow2')

    def test_from_id_multiple(self):
        tempdir = fixtures.TempDir()
        self.useFixture(tempdir)
        image_path_1 = os.path.join(tempdir.path, 'myid1234.qcow2')
        image_path_2 = os.path.join(tempdir.path, 'myid1234.raw')
        open(image_path_1, 'w')
        open(image_path_2, 'w')

        images = builder.DibImageFile.from_image_id(tempdir.path, 'myid1234')
        images = sorted(images, key=lambda x: x.extension)
        self.assertEqual(len(images), 2)

        self.assertEqual(images[0].extension, 'qcow2')
        self.assertEqual(images[1].extension, 'raw')

    def test_to_path(self):
        image = builder.DibImageFile('myid1234', 'qcow2')
        self.assertEqual(image.to_path('/imagedir'),
                         '/imagedir/myid1234.qcow2')
        self.assertEqual(image.to_path('/imagedir/'),
                         '/imagedir/myid1234.qcow2')


class TestNodepoolBuilderImageInheritance(tests.BaseTestCase):
    def test_parent_job(self):
        config = Config()
        diskimages = [
            {
                'name': 'parent',
                'dib-cmd': 'parent-dib-cmd',
                'elements': ['a', 'b'],
                'env-vars': {
                    'A': 'foo',
                    'B': 'bar',
                },
                'release': 21,
            },
            {
                'name': 'child',
                'parent': 'parent',
                'dib-cmd': 'override-dib-cmd',
                'elements': ['c'],
                'env-vars': {
                    'A': 'override_foo',
                    'C': 'moo'
                },
            },

        ]
        config.setDiskImages(diskimages)
        parsed = config.diskimages['child']
        self.assertEqual(parsed.dib_cmd, 'override-dib-cmd')
        self.assertEqual(parsed.release, '21')
        self.assertEqual(parsed.elements, 'a b c')
        self.assertDictEqual({
            'A': 'override_foo',
            'B': 'bar',
            'C': 'moo',
        }, parsed.env_vars)

    def test_abstract_jobs(self):
        config = Config()
        diskimages = [
            {
                'name': 'abstract',
                'abstract': True,
                'elements': ['a', 'b'],
                'env-vars': {
                    'A': 'foo',
                    'B': 'bar',
                },
            },
            {
                'name': 'another-abstract',
                'abstract': True,
                'parent': 'abstract',
                'elements': ['c'],
                'env-vars': {
                    'A': 'override_abstract',
                    'C': 'moo'
                },
            },
            {
                'name': 'job',
                'parent': 'another-abstract',
                'elements': ['d'],
                'dib-cmd': 'override-dib-cmd',
                'env-vars': {
                    'A': 'override_foo_again',
                    'D': 'zoo'
                },
            },

        ]
        config.setDiskImages(diskimages)
        parsed = config.diskimages['job']
        self.assertEqual(parsed.dib_cmd, 'override-dib-cmd')
        self.assertEqual(parsed.elements, 'a b c d')
        self.assertDictEqual({
            'A': 'override_foo_again',
            'B': 'bar',
            'C': 'moo',
            'D': 'zoo',
        }, parsed.env_vars)


class TestNodePoolBuilder(tests.DBTestCase):

    def test_start_stop(self):
        config = self.setup_config('node.yaml')
        nb = builder.NodePoolBuilder(config)
        nb.cleanup_interval = .5
        nb.build_interval = .1
        nb.upload_interval = .1
        nb.start()
        nb.stop()

    def test_builder_id_file(self):
        configfile = self.setup_config('node.yaml')
        self.useBuilder(configfile)
        path = os.path.join(self._config_images_dir.path, 'builder_id.txt')

        # Validate the unique ID file exists and contents are what we expect
        self.assertTrue(os.path.exists(path))
        with open(path, "r") as f:
            the_id = f.read()
            obj = uuid.UUID(the_id, version=4)
            self.assertEqual(the_id, str(obj))

    def test_image_upload_fail(self):
        """Test that image upload fails are handled properly."""

        # Now swap out the upload fake so that the next uploads fail
        fake_client = fakeadapter.FakeUploadFailCloud(times_to_fail=1)

        def get_fake_client(*args, **kwargs):
            return fake_client

        self.useFixture(fixtures.MockPatchObject(
            fakeadapter.FakeAdapter, '_getClient',
            get_fake_client))

        configfile = self.setup_config('node_two_provider.yaml')
        # NOTE(pabelanger): Disable CleanupWorker thread for nodepool-builder
        # as we currently race it to validate our failed uploads.
        self.useBuilder(configfile, cleanup_interval=0)
        self.waitForImage('fake-provider', 'fake-image')
        pool = self.useNodepool(configfile, watermark_sleep=1)
        self.startPool(pool)
        nodes = self.waitForNodes('fake-label')
        self.assertEqual(len(nodes), 1)

        newest_builds = self.zk.getMostRecentBuilds(1, 'fake-image',
                                                    state=zk.READY)
        self.assertEqual(1, len(newest_builds))

        # Assert that it failed once and succeeded once for fake-provider
        uploads1 = self.zk.getUploads('fake-image', newest_builds[0].id,
                                      'fake-provider', states=[zk.FAILED])
        self.assertEqual(1, len(uploads1))
        uploads2 = self.zk.getUploads('fake-image', newest_builds[0].id,
                                      'fake-provider', states=[zk.READY])
        self.assertEqual(1, len(uploads2))

        # Assert that it never failed and succeeded once for fake-provider2
        uploads3 = self.zk.getUploads('fake-image', newest_builds[0].id,
                                      'fake-provider2', states=[zk.FAILED])
        self.assertEqual(0, len(uploads3))
        uploads4 = self.zk.getUploads('fake-image', newest_builds[0].id,
                                      'fake-provider2', states=[zk.READY])
        self.assertEqual(1, len(uploads4))

        # Assert that we performed the upload to the second provider
        # before we retried the first one (this verifies that we
        # continue working with other providers after a failure).
        self.assertTrue(uploads4[0].state_time < uploads2[0].state_time)

    def test_provider_addition(self):
        configfile = self.setup_config('node.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        self.replace_config(configfile, 'node_two_provider.yaml')
        self.waitForImage('fake-provider2', 'fake-image')

    def test_provider_removal(self):
        configfile = self.setup_config('node_two_provider.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        self.waitForImage('fake-provider2', 'fake-image')
        image = self.zk.getMostRecentImageUpload('fake-provider', 'fake-image')
        self.replace_config(configfile, 'node_two_provider_remove.yaml')
        self.waitForImageDeletion('fake-provider2', 'fake-image')
        image2 = self.zk.getMostRecentImageUpload('fake-provider',
                                                  'fake-image')
        self.assertEqual(image, image2)

    def test_image_addition(self):
        configfile = self.setup_config('node.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        self.replace_config(configfile, 'node_two_image.yaml')
        self.waitForImage('fake-provider', 'fake-image2')

    def test_image_removal(self):
        configfile = self.setup_config('node_two_image.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        image2 = self.waitForImage('fake-provider', 'fake-image2')
        self.replace_config(configfile, 'node_two_image_remove.yaml')
        self.waitForImageDeletion('fake-provider', 'fake-image2')
        self.waitForBuildDeletion('fake-image2', image2.build_id)

    def test_image_removal_two_builders(self):
        # This tests the gap between building and uploading an image.
        # We build an image on one builder, then delete any uploads
        # (to simulate the time between when the builder completed a
        # build and started the first upload).  Then we start a second
        # builder which is not configured with the same provider as
        # the first builder and ensure that it doesn't delete the
        # ready-but-not-yet-uploaded build from the other builder.
        configfile1 = self.setup_config('builder_image1.yaml')
        builder1 = self.useBuilder(configfile1)
        self.waitForImage('fake-provider1', 'fake-image1')
        self.waitForBuild('fake-image1')
        for worker in builder1._upload_workers:
            worker.shutdown()
            worker.join()
        builder1.stop()

        self.zk.deleteUpload('fake-image1', '0000000001',
                             'fake-provider1', '0000000001')

        configfile2 = self.setup_config('builder_image2.yaml')
        self.useBuilder(configfile2)
        self.waitForImage('fake-provider2', 'fake-image2')
        # Don't check files because the image path switched to the
        # second builder; we're really only interested in ZK.
        self.waitForBuild('fake-image1', check_files=False)

    def test_image_removal_dib_deletes_first(self):
        # Break cloud image deleting
        fake_client = fakeadapter.FakeDeleteImageFailCloud()

        def get_fake_client(*args, **kwargs):
            return fake_client

        self.useFixture(fixtures.MockPatchObject(
            fakeadapter.FakeAdapter, '_getClient',
            get_fake_client))

        configfile = self.setup_config('node_two_image.yaml')
        self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image')
        img = self.waitForImage('fake-provider', 'fake-image2')

        # Ask nodepool to delete the image build and uploads
        self.replace_config(configfile, 'node_two_image_remove.yaml')
        # Wait for image files on disk to be deleted.
        for _ in iterate_timeout(10, Exception,
                                 'DIB disk files did not delete first'):
            self.wait_for_threads()
            files = builder.DibImageFile.from_image_id(
                self._config_images_dir.path, f'fake-image2-{img.build_id}')
            if not files:
                break
        # Check image is still in fake-provider cloud
        img.state = zk.DELETING
        self.assertEqual(
            self.zk.getImageUpload('fake-image2', img.build_id,
                                   'fake-provider', '0000000001'),
            img)

        # Release things by unbreaking image deleting. This allows cloud
        # and zk records to be removed.
        fake_client._fail = False
        # Check image is removed from cloud and zk
        self.waitForImageDeletion('fake-provider', 'fake-image2', match=img)
        # Check build is removed from zk
        self.waitForBuildDeletion('fake-image2', img.build_id)

    def test_image_rebuild_age(self):
        self._test_image_rebuild_age()

    def _test_image_rebuild_age(self, expire=86400):
        configfile = self.setup_config('node.yaml')
        self.useBuilder(configfile)
        build1 = self.waitForBuild('fake-image')
        log_path1 = os.path.join(self._config_build_log_dir.path,
                                 f'fake-image-{build1.id}.log')
        self.assertTrue(os.path.exists(log_path1))
        image = self.waitForImage('fake-provider', 'fake-image')
        # Expire rebuild-age (default: 1day) to force a new build.
        build1.state_time -= expire
        with self.zk.imageBuildLock('fake-image', blocking=True, timeout=1):
            self.zk.storeBuild('fake-image', build1, build1.id)
        build2 = self.waitForBuild('fake-image', ignore_list=[build1])
        log_path2 = os.path.join(self._config_build_log_dir.path,
                                 f'fake-image-{build2.id}.log')
        self.assertTrue(os.path.exists(log_path2))
        self.waitForImage('fake-provider', 'fake-image', [image])
        builds = self.zk.getBuilds('fake-image', zk.READY)
        self.assertEqual(len(builds), 2)
        return (build1, build2, image)

    def test_image_rotation(self):
        # Expire rebuild-age (2days), to avoid problems when expiring 2 images.
        build1, build2, image = self._test_image_rebuild_age(expire=172800)
        # Expire rebuild-age (default: 1day) to force a new build.
        build2.state_time -= 86400
        with self.zk.imageBuildLock('fake-image', blocking=True, timeout=1):
            self.zk.storeBuild('fake-image', build2, build2.id)
        self.waitForBuildDeletion('fake-image', build1.id)
        build3 = self.waitForBuild('fake-image',
                                   ignore_list=[build1, build2])
        log_path1 = os.path.join(self._config_build_log_dir.path,
                                 f'fake-image-{build1.id}.log')
        log_path2 = os.path.join(self._config_build_log_dir.path,
                                 f'fake-image-{build2.id}.log')
        log_path3 = os.path.join(self._config_build_log_dir.path,
                                 f'fake-image-{build3.id}.log')
        # Our log retention is set to 1, so the first log should be deleted.
        self.assertFalse(os.path.exists(log_path1))
        self.assertTrue(os.path.exists(log_path2))
        self.assertTrue(os.path.exists(log_path3))
        builds = self.zk.getBuilds('fake-image', zk.READY)
        self.assertEqual(len(builds), 2)

    def test_image_rotation_invalid_external_name(self):
        # NOTE(pabelanger): We are forcing fake-image to leak in fake-provider.
        # We do this to test our CleanupWorker will properly delete diskimage
        # builds from the HDD. For this test, we don't care about the leaked
        # image.
        #
        # Ensure we have a total of 3 diskimages on disk, so we can confirm
        # nodepool-builder will properly purge the 1 diskimage build leaving a
        # total of 2 diskimages on disk at all times.

        # Expire rebuild-age (2days), to avoid problems when expiring 2 images.
        build1, build2, image1 = self._test_image_rebuild_age(expire=172800)

        # Make sure 2rd diskimage build was uploaded.
        image2 = self.waitForImage('fake-provider', 'fake-image',
                                   ignore_list=[image1])

        # Delete external name / id so we can test exception handlers.
        upload = self.zk.getUploads(
            'fake-image', build1.id, 'fake-provider', zk.READY)[0]
        upload.external_name = None
        upload.external_id = None
        with self.zk.imageUploadLock(upload.image_name, upload.build_id,
                                     upload.provider_name, blocking=True,
                                     timeout=1):
            self.zk.storeImageUpload(upload.image_name, upload.build_id,
                                     upload.provider_name, upload, upload.id)

        # Expire rebuild-age (default: 1day) to force a new build.
        build2.state_time -= 86400
        with self.zk.imageBuildLock('fake-image', blocking=True, timeout=1):
            self.zk.storeBuild('fake-image', build2, build2.id)
        self.waitForBuildDeletion('fake-image', build1.id)

        # Make sure fake-image for fake-provider is removed from zookeeper.
        upload = self.zk.getUploads(
            'fake-image', build1.id, 'fake-provider')
        self.assertEqual(len(upload), 0)
        build3 = self.waitForBuild('fake-image',
                                   ignore_list=[build1, build2])

        # Ensure we only have 2 builds on disk.
        builds = self.zk.getBuilds('fake-image', zk.READY)
        self.assertEqual(len(builds), 2)

        # Make sure 3rd diskimage build was uploaded.
        image3 = self.waitForImage(
            'fake-provider', 'fake-image', ignore_list=[image1, image2])
        self.assertEqual(image3.build_id, build3.id)

    def test_cleanup_hard_upload_fails(self):
        configfile = self.setup_config('node.yaml')
        self.useBuilder(configfile)
        image = self.waitForImage('fake-provider', 'fake-image')

        upload = self.zk.getUploads('fake-image', image.build_id,
                                    'fake-provider', zk.READY)[0]

        # Store a new ZK node as UPLOADING to represent a hard fail
        upload.state = zk.UPLOADING

        with self.zk.imageUploadLock(upload.image_name, upload.build_id,
                                     upload.provider_name, blocking=True,
                                     timeout=1):
            upnum = self.zk.storeImageUpload(upload.image_name,
                                             upload.build_id,
                                             upload.provider_name,
                                             upload)

        # Now it should disappear from the current build set of uploads
        self.waitForUploadRecordDeletion(upload.provider_name,
                                         upload.image_name,
                                         upload.build_id,
                                         upnum)

    def test_cleanup_failed_image_build(self):
        configfile = self.setup_config('node_diskimage_fail.yaml')
        self.useBuilder(configfile)
        # Wait for the build to fail before we replace our config. Otherwise
        # we may replace the config before we build the image.
        found = False
        for _ in iterate_timeout(10, Exception, 'image builds to fail', 0.1):
            builds = self.zk.getBuilds('fake-image')
            if builds:
                found = builds[0].id
                break

        # Now replace the config with a valid config and check that the image
        # builds successfully. Finally check that the failed image is gone.
        self.replace_config(configfile, 'node.yaml')
        self.waitForImage('fake-provider', 'fake-image')
        # Make sure our cleanup worker properly removes the first build.
        self.waitForBuildDeletion('fake-image', found)
        self.assertReportedStat('nodepool.dib_image_build.'
                                'fake-image.status.rc',
                                '127', 'g')
        self.assertReportedStat('nodepool.dib_image_build.'
                                'fake-image.status.duration', None, 'ms')

    def test_diskimage_build_only(self):
        configfile = self.setup_config('node_diskimage_only.yaml')
        self.useBuilder(configfile)
        build_tar = self.waitForBuild('fake-image')

        self.assertEqual(build_tar._formats, ['tar'])
        self.assertReportedStat('nodepool.dib_image_build.'
                                'fake-image.status.rc',
                                '0', 'g')
        self.assertReportedStat('nodepool.dib_image_build.'
                                'fake-image.status.duration', None, 'ms')
        self.assertReportedStat('nodepool.dib_image_build.'
                                'fake-image.tar.size', '4096', 'g')
        self.assertReportedStat('nodepool.dib_image_build.'
                                'fake-image.status.last_build', None, 'g')

    def test_diskimage_build_formats(self):
        configfile = self.setup_config('node_diskimage_formats.yaml')
        self.useBuilder(configfile)
        build_default = self.waitForBuild('fake-image-default-format')
        build_vhd = self.waitForBuild('fake-image-vhd')

        self.assertEqual(build_default._formats, ['qcow2'])
        self.assertEqual(build_vhd._formats, ['vhd'])
        self.assertReportedStat('nodepool.dib_image_build.'
                                'fake-image-default-format.qcow2.size',
                                '4096', 'g')
        self.assertReportedStat('nodepool.dib_image_build.'
                                'fake-image-vhd.vhd.size', '4096', 'g')
        fqdn = socket.getfqdn()
        self.assertReportedStat(f'nodepool.builder.{fqdn}.'
                                'image.fake-image-default-format.'
                                'build.state', '0', 'g')
        self.assertReportedStat(f'nodepool.builder.{fqdn}.'
                                'image.fake-image-default-format.'
                                'provider.fake-provider-default-format.'
                                'upload.state', '0', 'g')

    def test_diskimage_build_parents(self):
        configfile = self.setup_config('node_diskimage_parents.yaml')
        self.useBuilder(configfile)
        self.waitForBuild('parent-image-1')
        self.waitForBuild('parent-image-2')

    @mock.patch('select.poll')
    def test_diskimage_build_timeout(self, mock_poll):
        configfile = self.setup_config('diskimage_build_timeout.yaml')
        builder.BUILD_PROCESS_POLL_TIMEOUT = 500
        self.useBuilder(configfile, cleanup_interval=0)
        self.waitForBuild('fake-image', states=(zk.FAILED,))

    def test_session_loss_during_build(self):
        configfile = self.setup_config('node.yaml')

        # We need to make the image build process pause so we can introduce
        # a simulated ZK session loss. The fake dib process will sleep while
        # the pause file is present in the images directory supplied to it.
        pause_file = os.path.join(self._config_images_dir.path,
                                  "fake-image-create.pause")
        open(pause_file, 'w')

        # Disable cleanup thread to verify builder cleans up after itself
        bldr = self.useBuilder(configfile, cleanup_interval=0)
        self.waitForBuild('fake-image', states=(zk.BUILDING,))

        # The build should now be paused just before writing out any DIB files.
        # Mock the next call to storeBuild() which is supposed to be the update
        # of the current build in ZooKeeper. This failure simulates losing the
        # ZK session and not being able to update the record.
        bldr.zk.storeBuild = mock.Mock(side_effect=Exception('oops'))

        # Allow the fake-image-create to continue by removing the pause file
        os.remove(pause_file)

        # The fake dib process writes out a .done file at the end. We need
        # this so we do not continue in this test until *after* all files are
        # written by that dib process.
        done_file = os.path.join(self._config_images_dir.path,
                                 "fake-image-create.done")
        while not os.path.exists(done_file):
            time.sleep(.1)

        # There shouldn't be any DIB files even though cleanup thread is
        # disabled because the builder should clean up after itself.
        images_dir = bldr._config.images_dir

        # Wait for builder to remove the leaked files
        image_files = builder.DibImageFile.from_image_id(
            images_dir, 'fake-image-0000000001')
        while image_files:
            time.sleep(.1)
            image_files = builder.DibImageFile.from_image_id(
                images_dir, 'fake-image-0000000001')

    def test_upload_removal_retries_until_success(self):
        '''
        If removing an image from a provider fails on the first attempt, make
        sure that we retry until successful.

        This test starts with two images uploaded to the provider. It then
        removes one of the images by setting the state to FAILED which should
        begin the process to delete the image from the provider.
        '''
        configfile = self.setup_config('builder_2_diskimages.yaml')
        bldr = self.useBuilder(configfile)
        self.waitForImage('fake-provider', 'fake-image1')
        image = self.waitForImage('fake-provider', 'fake-image2')

        # Introduce a failure in the upload deletion process by replacing
        # the cleanup thread's deleteImage() call with one that fails.
        cleanup_thd = bldr._janitor
        cleanup_mgr = cleanup_thd._config.provider_managers['fake-provider']
        saved_method = cleanup_mgr.deleteImage
        cleanup_mgr.deleteImage = mock.Mock(side_effect=Exception('Conflict'))

        # Manually cause the image to be deleted from the provider. Note that
        # we set it to FAILED instead of DELETING because that bypasses the
        # bit of code we want to test here in the CleanupWorker._deleteUpload()
        # method.
        image.state = zk.FAILED
        bldr.zk.storeImageUpload(image.image_name, image.build_id,
                                 image.provider_name, image, image.id)

        # Pick a call count > 1 to verify we make multiple attempts at
        # deleting the image in the provider.
        for _ in iterate_timeout(10, Exception, 'call count to increase'):
            if cleanup_mgr.deleteImage.call_count >= 5:
                break

        # Remove the failure to verify deletion.
        cleanup_mgr.deleteImage = saved_method
        self.waitForUploadRecordDeletion(image.provider_name, image.image_name,
                                         image.build_id, image.id)

    def test_post_upload_hook(self):
        configfile = self.setup_config('node_upload_hook.yaml')
        bldr = self.useBuilder(configfile)
        image = self.waitForImage('fake-provider', 'fake-image')

        images_dir = bldr._config.images_dir
        post_file = os.path.join(
            images_dir, f'fake-image-{image.build_id}.qcow2.post')
        self.assertTrue(os.path.exists(post_file), 'Post hook file exists')

    def test_cleanup_image_format(self):
        def fail_callback(args):
            return 'fail' in args['nodepool_provider_name']

        fake_client = fakeadapter.FakeUploadFailCloud(
            fail_callback=fail_callback)

        def get_fake_client(*args, **kwargs):
            return fake_client

        self.useFixture(fixtures.MockPatchObject(
            fakeadapter.FakeAdapter, '_getClient',
            get_fake_client))

        configfile = self.setup_config('node_diskimage_cleanup_formats.yaml')

        # We need to make the image build process pause so we can introduce
        # a simulated ZK session loss. The fake dib process will sleep while
        # the pause file is present in the images directory supplied to it.
        pause_file = os.path.join(self._config_images_dir.path,
                                  "fake-image-create.pause")
        open(pause_file, 'w')

        bldr = self.useBuilder(configfile)
        build = self.waitForBuild('fake-image', check_files=False,
                                  states=(zk.BUILDING,))
        self.assertEqual(set(build._formats), set(['qcow2', 'raw', 'vhd']))
        base = "-".join(['fake-image', build.id])

        # Create an in-progress image build file that we should ensure
        # is not deleted.
        intermediate_path = (
            os.path.join(self._config_images_dir.path, base) +
            '.vhd'
        )
        open(intermediate_path, 'w')

        # Force a cleanup cycle to make sure we don't delete our
        # intermediate image file
        bldr._janitor._cleanup()

        files = builder.DibImageFile.from_image_id(
            self._config_images_dir.path, base)
        self.assertEqual(1, len(files))
        self.assertEqual('vhd', files[0].extension)

        # Allow the fake-image-create to continue by removing the pause file
        os.remove(pause_file)
        self.waitForImage('fake-provider-qcow2', 'fake-image')
        self.waitForImage('fake-provider-raw', 'fake-image')
        files = builder.DibImageFile.from_image_id(
            self._config_images_dir.path, base)
        self.assertEqual(2, len(files))
        files.sort(key=lambda x: x.extension)
        self.assertEqual('qcow2', files[0].extension)
        self.assertEqual('vhd', files[1].extension)
