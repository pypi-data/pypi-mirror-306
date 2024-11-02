# Copyright 2018 Red Hat
# Copyright 2022 Acme Gating, LLC
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

from collections import defaultdict
import math

import voluptuous as v

from nodepool.driver import ConfigPool
from nodepool.driver import ConfigValue
from nodepool.driver import ProviderConfig


class AwsProviderCloudImage(ConfigValue):
    def __init__(self, image):
        default_port_mapping = {
            'ssh': 22,
            'winrm': 5986,
        }
        self.name = image['name']
        self.username = image['username']
        self.image_id = image.get('image-id')
        self.python_path = image.get('python-path', 'auto')
        self.shell_type = image.get('shell-type')
        self.connection_type = image.get('connection-type', 'ssh')
        self.connection_port = image.get(
            'connection-port',
            default_port_mapping.get(self.connection_type, 22))

        image_filters = image.get("image-filters", None)
        if image_filters is not None:
            # ensure 'name' and 'values' keys are capitalized for boto
            def capitalize_keys(image_filter):
                return {
                    k.capitalize(): v for (k, v) in image_filter.items()
                }

            image_filters = [capitalize_keys(f) for f in image_filters]
        self.image_filters = image_filters

    @property
    def external_name(self):
        '''Human readable version of external.'''
        return (self.image_id or self.name)

    @staticmethod
    def getSchema():
        image_filters = {
            v.Any('Name', 'name'): str,
            v.Any('Values', 'values'): [str]
        }

        return v.All({
            v.Required('name'): str,
            v.Required('username'): str,
            v.Exclusive('image-id', 'spec'): str,
            v.Exclusive('image-filters', 'spec'): [image_filters],
            'connection-type': str,
            'connection-port': int,
            'python-path': str,
            'shell-type': str,
        }, {
            v.Required(
                v.Any('image-id', 'image-filters'),
                msg=('Provide either '
                     '"image-filters", or "image-id" keys')
            ): object,
            object: object,
        })


class AwsProviderDiskImage(ConfigValue):
    def __init__(self, image_type, image, diskimage):
        default_port_mapping = {
            'ssh': 22,
            'winrm': 5986,
        }
        self.name = image['name']
        diskimage.image_types.add(image_type)
        self.pause = bool(image.get('pause', False))
        self.python_path = image.get('python-path', 'auto')
        self.shell_type = image.get('shell-type')
        self.username = image.get('username', diskimage.username)
        self.connection_type = image.get('connection-type', 'ssh')
        self.connection_port = image.get(
            'connection-port',
            default_port_mapping.get(self.connection_type, 22))
        self.meta = image.get('tags', {})
        self.architecture = image.get('architecture', 'x86_64')
        self.ena_support = image.get('ena-support', True)
        self.volume_size = image.get('volume-size', None)
        self.volume_type = image.get('volume-type', 'gp3')
        self.import_method = image.get('import-method', 'snapshot')
        self.imds_support = image.get('imds-support', None)
        if (self.imds_support == 'v2.0' and
            self.import_method == 'image'):
            raise Exception("IMDSv2 requires 'snapshot' or 'ebs-direct' "
                            "import method")
        self.iops = image.get('iops', None)
        self.throughput = image.get('throughput', None)

    @property
    def external_name(self):
        '''Human readable version of external.'''
        return self.name

    @staticmethod
    def getSchema():
        return {
            v.Required('name'): str,
            'username': str,
            'pause': bool,
            'connection-type': str,
            'connection-port': int,
            'python-path': str,
            'shell-type': str,
            'architecture': str,
            'ena-support': bool,
            'volume-size': int,
            'volume-type': str,
            'import-method': v.Any('snapshot', 'ebs-direct', 'image'),
            'imds-support': v.Any('v2.0', None),
            'iops': int,
            'throughput': int,
            'tags': dict,
        }


class AwsLabel(ConfigValue):
    ignore_equality = ['pool']

    def __init__(self, label, provider_config, provider_pool):
        self.name = label['name']
        self.pool = provider_pool

        cloud_image_name = label.get('cloud-image', None)
        if cloud_image_name:
            cloud_image = provider_config.cloud_images.get(
                cloud_image_name, None)
            if not cloud_image:
                raise ValueError(
                    "cloud-image %s does not exist in provider %s"
                    " but is referenced in label %s" %
                    (cloud_image_name, provider_config.name, self.name))
            self.cloud_image = cloud_image
        else:
            self.cloud_image = None

        diskimage_name = label.get('diskimage')
        if diskimage_name:
            diskimage = provider_config.diskimages.get(
                diskimage_name, None)
            if not diskimage:
                raise ValueError(
                    "diskimage %s does not exist in provider %s"
                    " but is referenced in label %s" %
                    (diskimage_name, provider_config.name, self.name))
            self.diskimage = diskimage
        else:
            self.diskimage = None

        self.ebs_optimized = bool(label.get('ebs-optimized', False))
        self.instance_type = label.get('instance-type', None)
        self.key_name = label.get('key-name')
        self.volume_type = label.get('volume-type')
        self.volume_size = label.get('volume-size')
        self.iops = label.get('iops', None)
        self.throughput = label.get('throughput', None)
        self.userdata = label.get('userdata', None)
        self.iam_instance_profile = label.get('iam-instance-profile', None)
        self.tags = label.get('tags', {})
        self.dynamic_tags = label.get('dynamic-tags', {})
        self.host_key_checking = self.pool.host_key_checking
        self.use_spot = bool(label.get('use-spot', False))
        self.imdsv2 = label.get('imdsv2', None)
        self.dedicated_host = bool(label.get('dedicated-host', False))
        if self.dedicated_host:
            if self.use_spot:
                raise Exception(
                    "Spot instances can not be used on dedicated hosts")
            if not self.pool.az:
                raise Exception(
                    "Availability-zone is required for dedicated hosts")
        self.fleet = label.get('fleet', None)

    @staticmethod
    def getSchema():
        return {
            v.Required('name'): str,
            v.Exclusive('cloud-image', 'image'): str,
            v.Exclusive('diskimage', 'image'): str,
            v.Exclusive('instance-type', 'instance'): str,
            v.Exclusive('fleet', 'instance'): {
                v.Required('instance-types'): list,
                v.Required('allocation-strategy'): v.Any(
                    'prioritized', 'price-capacity-optimized',
                    'capacity-optimized', 'diversified', 'lowest-price')
            },
            v.Required('key-name'): str,
            'ebs-optimized': bool,
            'volume-type': str,
            'volume-size': int,
            'iops': int,
            'throughput': int,
            'userdata': str,
            'iam-instance-profile': {
                v.Exclusive('name', 'iam_instance_profile_id'): str,
                v.Exclusive('arn', 'iam_instance_profile_id'): str
            },
            'tags': dict,
            'dynamic-tags': dict,
            'use-spot': bool,
            'imdsv2': v.Any(None, 'required', 'optional'),
            'dedicated-host': bool,
        }


class AwsPool(ConfigPool):
    ignore_equality = ['provider']

    def __init__(self, provider_config, pool_config):
        super().__init__()
        self.provider = provider_config
        self.load(pool_config)

    def load(self, pool_config):
        super().load(pool_config)
        self.name = pool_config['name']
        self.security_group_id = pool_config.get('security-group-id')
        self.subnet_id = pool_config.get('subnet-id')
        self.public_ipv4 = pool_config.get(
            'public-ipv4', self.provider.public_ipv4)
        self.public_ipv6 = pool_config.get(
            'public-ipv6', self.provider.public_ipv6)
        # TODO: Deprecate public-ip-address
        self.public_ipv4 = pool_config.get(
            'public-ip-address', self.public_ipv4)
        self.use_internal_ip = pool_config.get(
            'use-internal-ip', self.provider.use_internal_ip)
        self.host_key_checking = pool_config.get(
            'host-key-checking', self.provider.host_key_checking)
        self.max_servers = pool_config.get(
            'max-servers', self.provider.max_servers)
        self.max_cores = pool_config.get('max-cores', self.provider.max_cores)
        self.max_ram = pool_config.get('max-ram', self.provider.max_ram)
        self.max_resources = self.provider.max_resources.copy()
        for k, val in pool_config.get('max-resources', {}).items():
            self.max_resources[k] = val
        self.az = pool_config.get('availability-zone')

    @staticmethod
    def getSchema():
        aws_label = AwsLabel.getSchema()

        pool = ConfigPool.getCommonSchemaDict()
        pool.update({
            v.Required('name'): str,
            v.Required('labels'): [aws_label],
            'security-group-id': str,
            'subnet-id': str,
            'public-ip-address': bool,
            'public-ipv4': bool,
            'public-ipv6': bool,
            'host-key-checking': bool,
            'max-cores': int,
            'max-ram': int,
            'max-resources': {str: int},
            'availability-zone': str,
        })
        return pool


class AwsProviderConfig(ProviderConfig):
    def __init__(self, driver, provider):
        super().__init__(provider)
        self._pools = {}
        self.rate = None
        self.launch_retries = None
        self.profile_name = None
        self.region_name = None
        self.boot_timeout = None
        self.launch_retries = None
        self.cloud_images = {}
        self.diskimages = {}

    @property
    def pools(self):
        return self._pools

    @property
    def manage_images(self):
        return True

    @staticmethod
    def reset():
        pass

    def load(self, config):
        self.profile_name = self.provider.get('profile-name')
        self.region_name = self.provider.get('region-name')

        self.rate = self.provider.get('rate', 2)
        self.launch_retries = self.provider.get('launch-retries', 3)
        self.launch_timeout = self.provider.get('launch-timeout', 3600)
        self.boot_timeout = self.provider.get('boot-timeout', 180)
        self.use_internal_ip = self.provider.get('use-internal-ip', False)
        self.host_key_checking = self.provider.get('host-key-checking', True)
        self.public_ipv4 = self.provider.get('public-ipv4', True)
        self.public_ipv6 = self.provider.get('public-ipv6', False)
        self.object_storage = self.provider.get('object-storage')
        self.image_type = self.provider.get('image-format', 'raw')
        self.image_name_format = '{image_name}-{timestamp}'
        self.image_import_timeout = self.provider.get(
            'image-import-timeout', None)
        self.post_upload_hook = self.provider.get('post-upload-hook')
        self.max_servers = self.provider.get('max-servers', math.inf)
        self.max_cores = self.provider.get('max-cores', math.inf)
        self.max_ram = self.provider.get('max-ram', math.inf)
        self.max_resources = defaultdict(lambda: math.inf)
        for k, val in self.provider.get('max-resources', {}).items():
            self.max_resources[k] = val

        self.cloud_images = {}
        for image in self.provider.get('cloud-images', []):
            i = AwsProviderCloudImage(image)
            self.cloud_images[i.name] = i

        self.diskimages = {}
        for image in self.provider.get('diskimages', []):
            diskimage = config.diskimages[image['name']]
            i = AwsProviderDiskImage(self.image_type, image, diskimage)
            self.diskimages[i.name] = i

        for pool in self.provider.get('pools', []):
            pp = AwsPool(self, pool)
            self._pools[pp.name] = pp

            for label in pool.get('labels', []):
                pl = AwsLabel(label, self, pp)
                pp.labels[pl.name] = pl
                config.labels[pl.name].pools.append(pp)

    def getSchema(self):
        pool = AwsPool.getSchema()
        provider_cloud_images = AwsProviderCloudImage.getSchema()
        provider_diskimages = AwsProviderDiskImage.getSchema()
        object_storage = {
            v.Required('bucket-name'): str,
        }

        provider = ProviderConfig.getCommonSchemaDict()
        provider.update({
            v.Required('pools'): [pool],
            v.Required('region-name'): str,
            'rate': v.Any(int, float),
            'profile-name': str,
            'cloud-images': [provider_cloud_images],
            'diskimages': [provider_diskimages],
            'boot-timeout': int,
            'launch-timeout': int,
            'launch-retries': int,
            'object-storage': object_storage,
            'image-format': v.Any('ova', 'vhd', 'vhdx', 'vmdk', 'raw'),
            'image-import-timeout': int,
            'max-servers': int,
            'max-cores': int,
            'max-ram': int,
            'max-resources': {str: int},
            'post-upload-hook': str,
        })
        return v.Schema(provider)

    def getSupportedLabels(self, pool_name=None):
        labels = set()
        for pool in self.pools.values():
            if not pool_name or (pool.name == pool_name):
                labels.update(pool.labels.keys())
        return labels
