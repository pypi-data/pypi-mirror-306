# Copyright (C) 2011-2013 OpenStack Foundation
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
#
# See the License for the specific language governing permissions and
# limitations under the License.

import math
import voluptuous as v

from nodepool.driver import ProviderConfig
from nodepool.driver import ConfigValue
from nodepool.driver import ConfigPool


class ProviderDiskImage(ConfigValue):
    def __init__(self):
        self.name = None
        self.pause = False
        self.config_drive = None
        self.connection_type = None
        self.connection_port = None
        self.username = None
        self.python_path = None
        self.shell_type = None
        self.meta = None


class ProviderCloudImage(ConfigValue):
    def __init__(self):
        self.name = None
        self.config_drive = None
        self.image_id = None
        self.image_name = None
        self.username = None
        self.python_path = None
        self.shell_type = None
        self.connection_type = None
        self.connection_port = None

    @property
    def external_name(self):
        '''Human readable version of external.'''
        return self.image_id or self.image_name or self.name


class ProviderLabel(ConfigValue):
    ignore_equality = ['pool']

    def __init__(self):
        self.name = None
        self.diskimage = None
        self.cloud_image = None
        self.min_ram = None
        self.flavor_name = None
        self.key_name = None
        self.console_log = False
        self.boot_from_volume = False
        self.volume_size = None
        self.instance_properties = None
        self.userdata = None
        self.networks = []
        self.host_key_checking = True
        # The ProviderPool object that owns this label.
        self.pool = None


class ProviderPool(ConfigPool):
    ignore_equality = ['provider']

    def __init__(self):
        self.name = None
        self.max_cores = None
        self.max_ram = None
        self.ignore_provider_quota = False
        self.azs = None
        self.networks = None
        self.security_groups = None
        self.auto_floating_ip = True
        self.host_key_checking = True
        self.use_internal_ip = False
        self.labels = None
        # The OpenStackProviderConfig object that owns this pool.
        self.provider = None

        # Initialize base class attributes
        super().__init__()

    def load(self, pool_config, full_config, provider):
        '''
        Load pool configuration options.

        :param dict pool_config: A single pool config section from which we
            will load the values.
        :param dict full_config: The full nodepool config.
        :param OpenStackProviderConfig: The calling provider object.
        '''
        super().load(pool_config)

        self.provider = provider
        self.name = pool_config['name']
        self.max_cores = pool_config.get('max-cores', math.inf)
        self.max_ram = pool_config.get('max-ram', math.inf)
        self.max_volumes = pool_config.get('max-volumes', math.inf)
        self.max_volume_gb = pool_config.get('max-volume-gb', math.inf)
        self.ignore_provider_quota = pool_config.get('ignore-provider-quota',
                                                     False)
        self.azs = pool_config.get('availability-zones')
        self.networks = pool_config.get('networks', [])
        self.security_groups = pool_config.get('security-groups', [])
        self.auto_floating_ip = bool(pool_config.get('auto-floating-ip', True))
        self.host_key_checking = bool(pool_config.get('host-key-checking',
                                                      True))

        for label in pool_config.get('labels', []):
            pl = ProviderLabel()
            pl.name = label['name']
            pl.pool = self
            self.labels[pl.name] = pl
            diskimage = label.get('diskimage', None)
            if diskimage:
                pl.diskimage = full_config.diskimages[diskimage]
            else:
                pl.diskimage = None
            cloud_image_name = label.get('cloud-image', None)
            if cloud_image_name:
                cloud_image = provider.cloud_images.get(cloud_image_name, None)
                if not cloud_image:
                    raise ValueError(
                        "cloud-image %s does not exist in provider %s"
                        " but is referenced in label %s" %
                        (cloud_image_name, self.name, pl.name))
            else:
                cloud_image = None
            pl.cloud_image = cloud_image
            pl.min_ram = label.get('min-ram', 0)
            pl.flavor_name = label.get('flavor-name', None)
            pl.key_name = label.get('key-name')
            pl.console_log = label.get('console-log', False)
            pl.boot_from_volume = bool(label.get('boot-from-volume',
                                                 False))
            pl.volume_size = label.get('volume-size', 50)
            pl.instance_properties = label.get('instance-properties',
                                               {})
            pl.dynamic_instance_properties = label.get(
                'dynamic-instance-properties', {})
            pl.userdata = label.get('userdata', None)
            pl.networks = label.get('networks', self.networks)
            pl.host_key_checking = label.get(
                'host-key-checking', self.host_key_checking)

            top_label = full_config.labels[pl.name]
            top_label.pools.append(self)


class OpenStackProviderConfig(ProviderConfig):
    def __init__(self, driver, provider):
        self.driver_object = driver
        self.__pools = {}
        self.cloud_config = None
        self.image_type = None
        self.rate = None
        self.boot_timeout = None
        self.launch_timeout = None
        self.image_upload_timeout = None
        self.clean_floating_ips = None
        self.port_cleanup_interval = None
        self.diskimages = {}
        self.cloud_images = {}
        self.image_name_format = None
        self.post_upload_hook = None
        super().__init__(provider)

    def _cloudKwargs(self):
        cloud_kwargs = {}
        for arg in ['region-name', 'cloud']:
            if arg in self.provider:
                cloud_kwargs[arg] = self.provider[arg]
        return cloud_kwargs

    @property
    def pools(self):
        return self.__pools

    @property
    def manage_images(self):
        return True

    def load(self, config):
        cloud_kwargs = self._cloudKwargs()
        openstack_config = self.driver_object.openstack_config
        self.cloud_config = openstack_config.get_one(**cloud_kwargs)

        self.image_type = self.cloud_config.config['image_format']
        self.region_name = self.provider.get('region-name')
        self.rate = float(self.provider.get('rate', 1.0))
        self.boot_timeout = self.provider.get('boot-timeout', 60)
        self.launch_timeout = self.provider.get('launch-timeout', 3600)
        self.launch_retries = self.provider.get('launch-retries', 3)
        self.image_upload_timeout = self.provider.get(
            'image-upload-timeout', 3600)
        self.clean_floating_ips = self.provider.get('clean-floating-ips')
        self.port_cleanup_interval = self.provider.get(
            'port-cleanup-interval',
            600
        )
        self.image_name_format = self.provider.get(
            'image-name-format',
            '{image_name}-{timestamp}'
        )
        self.post_upload_hook = self.provider.get('post-upload-hook')

        default_port_mapping = {
            'ssh': 22,
            'winrm': 5986,
        }

        for image in self.provider.get('diskimages', []):
            i = ProviderDiskImage()
            i.name = image['name']
            self.diskimages[i.name] = i
            diskimage = config.diskimages[i.name]
            diskimage.image_types.add(self.image_type)
            i.pause = bool(image.get('pause', False))
            i.config_drive = image.get('config-drive', None)
            i.username = diskimage.username
            i.python_path = diskimage.python_path
            i.shell_type = diskimage.shell_type
            i.connection_type = image.get('connection-type', 'ssh')
            i.connection_port = image.get(
                'connection-port',
                default_port_mapping.get(i.connection_type, 22))

            # This dict is expanded and used as custom properties when
            # the image is uploaded.
            i.meta = image.get('meta', {})

        for image in self.provider.get('cloud-images', []):
            i = ProviderCloudImage()
            i.name = image['name']
            i.config_drive = image.get('config-drive', None)
            i.image_id = image.get('image-id', None)
            i.image_name = image.get('image-name', None)
            i.username = image.get('username', None)
            i.python_path = image.get('python-path', 'auto')
            i.shell_type = image.get('shell-type', None)
            i.connection_type = image.get('connection-type', 'ssh')
            i.connection_port = image.get(
                'connection-port',
                default_port_mapping.get(i.connection_type, 22))
            self.cloud_images[i.name] = i

        for pool in self.provider.get('pools', []):
            pp = ProviderPool()
            pp.load(pool, config, self)
            self.pools[pp.name] = pp

    def getSchema(self):
        provider_diskimage = {
            'name': str,
            'pause': bool,
            'meta': dict,
            'config-drive': bool,
            'connection-type': str,
            'connection-port': int,
        }

        provider_cloud_images = {
            'name': str,
            'config-drive': bool,
            'connection-type': str,
            'connection-port': int,
            v.Exclusive('image-id', 'cloud-image-name-or-id'): str,
            v.Exclusive('image-name', 'cloud-image-name-or-id'): str,
            'username': str,
            'python-path': str,
            'shell-type': str,
        }

        pool_label_main = {
            v.Required('name'): str,
            v.Exclusive('diskimage', 'label-image'): str,
            v.Exclusive('cloud-image', 'label-image'): str,
            'min-ram': int,
            'flavor-name': str,
            'key-name': str,
            'console-log': bool,
            'boot-from-volume': bool,
            'volume-size': int,
            'instance-properties': dict,
            'dynamic-instance-properties': dict,
            'userdata': str,
            'networks': [str],
            'host-key-checking': bool,
        }

        label_min_ram = v.Schema({v.Required('min-ram'): int}, extra=True)

        label_flavor_name = v.Schema({v.Required('flavor-name'): str},
                                     extra=True)

        label_diskimage = v.Schema({v.Required('diskimage'): str}, extra=True)

        label_cloud_image = v.Schema({v.Required('cloud-image'): str},
                                     extra=True)

        pool_label = v.All(pool_label_main,
                           v.Any(label_min_ram, label_flavor_name),
                           v.Any(label_diskimage, label_cloud_image))

        pool = ConfigPool.getCommonSchemaDict()
        pool.update({
            'name': str,
            'networks': [str],
            'auto-floating-ip': bool,
            'host-key-checking': bool,
            'ignore-provider-quota': bool,
            'max-cores': int,
            'max-ram': int,
            'max-volumes': int,
            'max-volume-gb': int,
            'labels': [pool_label],
            'availability-zones': [str],
            'security-groups': [str]
        })

        schema = ProviderConfig.getCommonSchemaDict()
        schema.update({
            'region-name': str,
            v.Required('cloud'): str,
            'boot-timeout': int,
            'image-upload-timeout': int,
            'launch-timeout': int,
            'launch-retries': int,
            'nodepool-id': str,
            'rate': v.Coerce(float),
            'image-name-format': str,
            'clean-floating-ips': bool,
            'port-cleanup-interval': int,
            'pools': [pool],
            'diskimages': [provider_diskimage],
            'cloud-images': [provider_cloud_images],
            'post-upload-hook': str,
        })
        return v.Schema(schema)

    def getSupportedLabels(self, pool_name=None):
        labels = set()
        for pool in self.pools.values():
            if not pool_name or (pool.name == pool_name):
                labels.update(pool.labels.keys())
        return labels
