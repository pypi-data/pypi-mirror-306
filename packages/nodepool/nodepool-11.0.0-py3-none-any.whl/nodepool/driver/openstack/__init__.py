# Copyright 2022 Acme Gating, LLC
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

from openstack.config import loader

from nodepool.driver.statemachine import StateMachineDriver
from nodepool.driver.openstack.config import OpenStackProviderConfig
from nodepool.driver.openstack.adapter import OpenStackAdapter


class OpenStackDriver(StateMachineDriver):
    def reset(self):
        self.openstack_config = loader.OpenStackConfig()

    def __init__(self):
        self.reset()
        super().__init__()

    def getProviderConfig(self, provider):
        return OpenStackProviderConfig(self, provider)

    def getAdapter(self, provider_config):
        return OpenStackAdapter(provider_config)
