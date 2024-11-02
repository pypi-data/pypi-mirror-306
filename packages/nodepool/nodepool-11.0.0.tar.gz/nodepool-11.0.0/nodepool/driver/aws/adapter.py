# Copyright 2018 Red Hat
# Copyright 2022-2023 Acme Gating, LLC
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
import cachetools.func
from concurrent.futures import ThreadPoolExecutor
import copy
import functools
import hashlib
import json
import logging
import math
import queue
import re
import threading
import time
import urllib.parse
from uuid import uuid4

from nodepool.driver.utils import (
    QuotaInformation,
    LazyExecutorTTLCache,
    RateLimiter,
    ImageUploader,
)
from nodepool.driver import statemachine
from nodepool import exceptions

import boto3
import botocore.exceptions


def tag_dict_to_list(tagdict):
    # TODO: validate tag values are strings in config and deprecate
    # non-string values.
    return [{"Key": k, "Value": str(v)} for k, v in tagdict.items()]


def tag_list_to_dict(taglist):
    if taglist is None:
        return {}
    return {t["Key"]: t["Value"] for t in taglist}


# This is a map of instance types to quota codes.  There does not
# appear to be an automated way to determine what quota code to use
# for an instance type, therefore this list was manually created by
# visiting
# https://us-west-1.console.aws.amazon.com/servicequotas/home/services/ec2/quotas
# and filtering by "Instances".  An example description is "Running
# On-Demand P instances" which we can infer means we should use that
# quota code for instance types starting with the letter "p".  All
# instance type names follow the format "([a-z\-]+)\d", so we can
# match the first letters (up to the first number) of the instance
# type name with the letters in the quota name.  The prefix "u-" for
# "Running On-Demand High Memory instances" was determined from
# https://aws.amazon.com/ec2/instance-types/high-memory/

INSTANCE_QUOTA_CODES = {
    # INSTANCE FAMILY: [ON-DEMAND, SPOT]
    'a': ['L-1216C47A', 'L-34B43A08'],
    'c': ['L-1216C47A', 'L-34B43A08'],
    'd': ['L-1216C47A', 'L-34B43A08'],
    'h': ['L-1216C47A', 'L-34B43A08'],
    'i': ['L-1216C47A', 'L-34B43A08'],
    'm': ['L-1216C47A', 'L-34B43A08'],
    'r': ['L-1216C47A', 'L-34B43A08'],
    't': ['L-1216C47A', 'L-34B43A08'],
    'z': ['L-1216C47A', 'L-34B43A08'],
    'dl': ['L-6E869C2A', 'L-85EED4F7'],
    'f': ['L-74FC7D96', 'L-88CF9481'],
    'g': ['L-DB2E81BA', 'L-3819A6DF'],
    'vt': ['L-DB2E81BA', 'L-3819A6DF'],
    'u-': ['L-43DA4232', ''],          # 'high memory'
    'inf': ['L-1945791B', 'L-B5D1601B'],
    'p': ['L-417A185B', 'L-7212CCBC'],
    'x': ['L-7295265B', 'L-E3A00192'],
    'trn': ['L-2C3B7624', 'L-6B0D517C'],
    'hpc': ['L-F7808C92', '']
}

HOST_QUOTA_CODES = {
    'a1': 'L-949445B0',
    'c3': 'L-8D142A2E',
    'c4': 'L-E4BF28E0',
    'c5': 'L-81657574',
    'c5a': 'L-03F01FD8',
    'c5d': 'L-C93F66A2',
    'c5n': 'L-20F13EBD',
    'c6a': 'L-D75D2E84',
    'c6g': 'L-A749B537',
    'c6gd': 'L-545AED39',
    'c6gn': 'L-5E3A299D',
    'c6i': 'L-5FA3355A',
    'c6id': 'L-1BBC5241',
    'c6in': 'L-6C2C40CC',
    'c7a': 'L-698B67E5',
    'c7g': 'L-13B8FCE8',
    'c7gd': 'L-EF58B059',
    'c7gn': 'L-97677CE3',
    'c7i': 'L-587AA6E3',
    'd2': 'L-8B27377A',
    'dl1': 'L-AD667A3D',
    'f1': 'L-5C4CD236',
    'g3': 'L-DE82EABA',
    'g3s': 'L-9675FDCD',
    'g4ad': 'L-FD8E9B9A',
    'g4dn': 'L-CAE24619',
    'g5': 'L-A6E7FE5E',
    'g5g': 'L-4714FFEA',
    'g6': 'L-B88B9D6B',
    'gr6': 'L-E68C3AFF',
    'h1': 'L-84391ECC',
    'i2': 'L-6222C1B6',
    'i3': 'L-8E60B0B1',
    'i3en': 'L-77EE2B11',
    'i4g': 'L-F62CBADB',
    'i4i': 'L-0300530D',
    'im4gn': 'L-93155D6F',
    'inf': 'L-5480EFD2',
    'inf2': 'L-E5BCF7B5',
    'is4gen': 'L-CB4F5825',
    'm3': 'L-3C82F907',
    'm4': 'L-EF30B25E',
    'm5': 'L-8B7BF662',
    'm5a': 'L-B10F70D6',
    'm5ad': 'L-74F41837',
    'm5d': 'L-8CCBD91B',
    'm5dn': 'L-DA07429F',
    'm5n': 'L-24D7D4AD',
    'm5zn': 'L-BD9BD803',
    'm6a': 'L-80F2B67F',
    'm6g': 'L-D50A37FA',
    'm6gd': 'L-84FB37AA',
    'm6i': 'L-D269BEFD',
    'm6id': 'L-FDB0A352',
    'm6idn': 'L-9721EDD9',
    'm6in': 'L-D037CF10',
    'm7a': 'L-4740F819',
    'm7g': 'L-9126620E',
    'm7gd': 'L-F8516154',
    'm7i': 'L-30E31217',
    'mac1': 'L-A8448DC5',
    'mac2': 'L-5D8DADF5',
    'mac2-m2': 'L-B90B5B66',
    'mac2-m2pro': 'L-14F120D1',
    'p2': 'L-2753CF59',
    'p3': 'L-A0A19F79',
    'p3dn': 'L-B601B3B6',
    'p4d': 'L-86A789C3',
    'p5': 'L-5136197D',
    'r3': 'L-B7208018',
    'r4': 'L-313524BA',
    'r5': 'L-EA4FD6CF',
    'r5a': 'L-8FE30D52',
    'r5ad': 'L-EC7178B6',
    'r5b': 'L-A2D59C67',
    'r5d': 'L-8814B54F',
    'r5dn': 'L-4AB14223',
    'r5n': 'L-52EF324A',
    'r6a': 'L-BC1589C5',
    'r6g': 'L-B6D6065D',
    'r6gd': 'L-EF284EFB',
    'r6i': 'L-F13A970A',
    'r6id': 'L-B89271A9',
    'r6idn': 'L-C4EABC2C',
    'r6in': 'L-EA99608B',
    'r7a': 'L-4D15192B',
    'r7g': 'L-67B8B4C7',
    'r7gd': 'L-01137DCE',
    'r7i': 'L-55E05032',
    'r7iz': 'L-BC9FCC71',
    't3': 'L-1586174D',
    'trn1': 'L-5E4FB836',
    'trn1n': 'L-39926A58',
    'u-12tb1': 'L-D6994875',
    'u-18tb1': 'L-5F7FD336',
    'u-24tb1': 'L-FACBE655',
    'u-3tb1': 'L-7F5506AB',
    'u-6tb1': 'L-89870E8E',
    'u-9tb1': 'L-98E1FFAC',
    'u7in-16tb': 'L-75B9BECB',
    'u7in-24tb': 'L-CA51381E',
    'u7in-32tb': 'L-9D28191F',
    'vt1': 'L-A68CFBF7',
    'x1': 'L-DE3D9563',
    'x1e': 'L-DEF8E115',
    'x2gd': 'L-5CC9EA82',
    'x2idn': 'L-A84ABF80',
    'x2iedn': 'L-D0AA08B1',
    'x2iezn': 'L-888B4496',
    'z1d': 'L-F035E935',
}

VOLUME_QUOTA_CODES = {
    'io1': dict(iops='L-B3A130E6', storage='L-FD252861'),
    'io2': dict(iops='L-8D977E7E', storage='L-09BD8365'),
    'sc1': dict(storage='L-17AF77E8'),
    'gp2': dict(storage='L-D18FCD1D'),
    'gp3': dict(storage='L-7A658B76'),
    'standard': dict(storage='L-9CF3C2EB'),
    'st1': dict(storage='L-82ACEF56'),
}

CACHE_TTL = 10
SERVICE_QUOTA_CACHE_TTL = 300
ON_DEMAND = 0
SPOT = 1
KIB = 1024
GIB = 1024 ** 3


class AwsInstance(statemachine.Instance):
    def __init__(self, provider, instance, host, quota, label):
        super().__init__()
        self.external_id = dict()
        if instance:
            self.external_id['instance'] = instance['InstanceId']
        if host:
            self.external_id['host'] = host['HostId']
        self.metadata = tag_list_to_dict(instance.get('Tags'))
        self.private_ipv4 = instance.get('PrivateIpAddress')
        self.private_ipv6 = None
        self.public_ipv4 = instance.get('PublicIpAddress')
        self.public_ipv6 = None
        self.cloud = 'AWS'
        self.region = provider.region_name
        self.az = None
        self.quota = quota

        self.az = instance.get('Placement', {}).get('AvailabilityZone')

        for iface in instance.get('NetworkInterfaces', [])[:1]:
            if iface.get('Ipv6Addresses'):
                v6addr = iface['Ipv6Addresses'][0]
                self.public_ipv6 = v6addr.get('Ipv6Address')
        self.interface_ip = (self.public_ipv4 or self.public_ipv6 or
                             self.private_ipv4 or self.private_ipv6)

        if label:
            # `fleet` contains the parameters used to call the fleet API, in
            # a dictionary form. The interesting point is if fleet API was
            # used or not, so bool-it
            self.node_properties['fleet'] = bool(label.fleet)
            # `use_spot` is already bool, can directly be used as a flag
            self.node_properties['spot'] = label.use_spot

    def getQuotaInformation(self):
        return self.quota


class AwsResource(statemachine.Resource):
    TYPE_HOST = 'host'
    TYPE_INSTANCE = 'instance'
    TYPE_AMI = 'ami'
    TYPE_SNAPSHOT = 'snapshot'
    TYPE_VOLUME = 'volume'
    TYPE_OBJECT = 'object'

    def __init__(self, metadata, type, id):
        super().__init__(metadata, type)
        self.id = id


class AwsDeleteStateMachine(statemachine.StateMachine):
    HOST_RELEASING_START = 'start releasing host'
    HOST_RELEASING = 'releasing host'
    INSTANCE_DELETING_START = 'start deleting instance'
    INSTANCE_DELETING = 'deleting instance'
    COMPLETE = 'complete'

    def __init__(self, adapter, external_id, log):
        self.log = log
        super().__init__()
        self.adapter = adapter
        # Backwards compatible for old nodes where external_id is a
        # str
        if type(external_id) is str:
            external_id = dict(instance=external_id)
        self.external_id = external_id

    def advance(self):
        if self.state == self.START:
            if 'instance' in self.external_id:
                self.state = self.INSTANCE_DELETING_START
            elif 'host' in self.external_id:
                self.state = self.HOST_RELEASING_START
            else:
                self.state = self.COMPLETE

        if self.state == self.INSTANCE_DELETING_START:
            self.instance = self.adapter._deleteInstance(
                self.external_id['instance'], self.log)
            self.state = self.INSTANCE_DELETING

        if self.state == self.INSTANCE_DELETING:
            self.instance = self.adapter._refreshDelete(self.instance)
            if self.instance is None:
                if 'host' in self.external_id:
                    self.state = self.HOST_RELEASING_START
                else:
                    self.state = self.COMPLETE

        if self.state == self.HOST_RELEASING_START:
            self.host = self.adapter._releaseHost(
                self.external_id['host'], self.log)
            self.state = self.HOST_RELEASING

        if self.state == self.HOST_RELEASING:
            self.host = self.adapter._refreshDelete(self.host)
            if self.host is None:
                self.state = self.COMPLETE

        if self.state == self.COMPLETE:
            self.complete = True


class AwsCreateStateMachine(statemachine.StateMachine):
    HOST_ALLOCATING_START = 'start allocating host'
    HOST_ALLOCATING_SUBMIT = 'submit allocating host'
    HOST_ALLOCATING = 'allocating host'
    INSTANCE_CREATING_START = 'start creating instance'
    INSTANCE_CREATING_SUBMIT = 'submit creating instance'
    INSTANCE_CREATING = 'creating instance'
    COMPLETE = 'complete'

    def __init__(self, adapter, hostname, label, image_external_id,
                 metadata, request, log):
        self.log = log
        super().__init__()
        self.adapter = adapter
        self.attempts = 0
        self.image_external_id = image_external_id
        self.metadata = metadata
        self.tags = label.tags.copy() or {}
        for k, v in label.dynamic_tags.items():
            try:
                self.tags[k] = v.format(request=request.getSafeAttributes())
            except Exception:
                self.log.exception("Error formatting tag %s", k)
        self.tags.update(metadata)
        self.tags['Name'] = hostname
        self.hostname = hostname
        self.label = label
        self.public_ipv4 = None
        self.public_ipv6 = None
        self.nic = None
        self.instance = None
        self.host = None
        self.external_id = dict()
        self.dedicated_host_id = None

    def advance(self):
        if self.state == self.START:
            if self.label.dedicated_host:
                self.state = self.HOST_ALLOCATING_START
            else:
                self.state = self.INSTANCE_CREATING_START

        if self.state == self.HOST_ALLOCATING_START:
            self.host_create_future = self.adapter._submitAllocateHost(
                self.label,
                self.tags, self.hostname, self.log)
            self.state = self.HOST_ALLOCATING_SUBMIT

        if self.state == self.HOST_ALLOCATING_SUBMIT:
            host = self.adapter._completeAllocateHost(self.host_create_future)
            if host is None:
                return
            self.host = host
            self.external_id['host'] = host['HostId']
            self.state = self.HOST_ALLOCATING

        if self.state == self.HOST_ALLOCATING:
            self.host = self.adapter._refresh(self.host)

            state = self.host['State'].lower()
            if state == 'available':
                self.dedicated_host_id = self.host['HostId']
                self.state = self.INSTANCE_CREATING_START
            elif state in [
                    'permanent-failure', 'released',
                    'released-permanent-failure']:
                raise exceptions.LaunchStatusException(
                    f"Host in {state} state")
            else:
                return

        if self.state == self.INSTANCE_CREATING_START:
            self.create_future = self.adapter._submitCreateInstance(
                self.label, self.image_external_id,
                self.tags, self.hostname, self.dedicated_host_id, self.log)
            self.state = self.INSTANCE_CREATING_SUBMIT

        if self.state == self.INSTANCE_CREATING_SUBMIT:
            instance = self.adapter._completeCreateInstance(self.create_future)
            if instance is None:
                return
            self.instance = instance
            self.external_id['instance'] = instance['InstanceId']
            self.quota = self.adapter._getQuotaForLabel(self.label)
            self.state = self.INSTANCE_CREATING

        if self.state == self.INSTANCE_CREATING:
            self.instance = self.adapter._refresh(self.instance)

            if self.instance['State']['Name'].lower() == "running":
                self.state = self.COMPLETE
            elif self.instance['State']['Name'].lower() == "terminated":
                raise exceptions.LaunchStatusException(
                    "Instance in terminated state")
            else:
                return

        if self.state == self.COMPLETE:
            self.complete = True
            self.quota = self.adapter._getQuotaForLabel(
                self.label, self.instance['InstanceType'])
            return AwsInstance(
                self.adapter.provider, self.instance, self.host, self.quota,
                self.label
            )


class EBSSnapshotUploader(ImageUploader):
    segment_size = 512 * KIB

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.segment_count = 0
        self.size_in_gib = math.ceil(self.size / GIB)

    def shouldRetryException(self, exception):
        # Strictly speaking, ValidationException is only retryable
        # if we get a particular message, but that's impractical
        # to reproduce for testing.
        # https://docs.aws.amazon.com/ebs/latest/userguide/error-retries.html
        ex = self.adapter.ebs_client.exceptions
        if isinstance(exception, (
                ex.RequestThrottledException,
                ex.InternalServerException,
                ex.ValidationException,
        )):
            return True
        return False

    def _rateLimited(self, func):
        def rateLimitedFunc(*args, **kw):
            with self.adapter.rate_limiter:
                return func(*args, **kw)
        return rateLimitedFunc

    def uploadSegment(self, segment):
        # There is a default limit of 1000 put requests/second.
        # Actual value is available as a service quota.  We don't
        # expect to hit this.  If we do, and we need to rate-limit, we
        # will need to coordinate with other builders.
        # https://docs.aws.amazon.com/ebs/latest/userguide/ebs-resource-quotas.html
        data = segment.data
        if len(data) < self.segment_size:
            # Add zeros if the last block is smaller since the
            # block size in AWS is constant.
            data = data.ljust(self.segment_size, b'\0')
        checksum = hashlib.sha256(data)
        checksum_base64 = base64.b64encode(checksum.digest()).decode('utf-8')

        response = self.retry(
            self.adapter.ebs_client.put_snapshot_block,
            SnapshotId=self.snapshot_id,
            BlockIndex=segment.index,
            BlockData=data,
            DataLength=len(data),
            Checksum=checksum_base64,
            ChecksumAlgorithm='SHA256',
        )
        if (response['Checksum'] != checksum_base64):
            raise Exception("Checksums do not match; received "
                            f"{response['Checksum']} expected {checksum}")
        self.segment_count += 1

    def startUpload(self):
        # This is used by AWS to ensure idempotency across retries
        token = uuid4().hex
        response = self.retry(
            self._rateLimited(self.adapter.ebs_client.start_snapshot),
            VolumeSize=self.size_in_gib,
            ClientToken=token,
            Tags=tag_dict_to_list(self.metadata),
        )
        self.snapshot_id = response['SnapshotId']

    def finishUpload(self):
        while True:
            response = self.retry(
                self._rateLimited(self.adapter.ebs_client.complete_snapshot),
                SnapshotId=self.snapshot_id,
                ChangedBlocksCount=self.segment_count,
            )
            if response['Status'] == 'error':
                raise Exception("Snapshot in error state")
            if response['Status'] == 'completed':
                break
            self.checkTimeout()
        return self.size_in_gib, self.snapshot_id

    def abortUpload(self):
        try:
            self.finishUpload()
        except Exception:
            pass
        with self.adapter.rate_limiter:
            snapshot_id = getattr(self, 'snapshot_id', None)
            if snapshot_id:
                self.adapter.ec2_client.delete_snapshot(
                    SnapshotId=self.snapshot_id)


class AwsAdapter(statemachine.Adapter):
    IMAGE_UPLOAD_SLEEP = 30
    LAUNCH_TEMPLATE_PREFIX = 'nodepool-launch-template'

    def __init__(self, provider_config):
        # Wrap these instance methods with a per-instance LRU cache so
        # that we don't leak memory over time when the adapter is
        # occasionally replaced.
        self._getInstanceType = functools.lru_cache(maxsize=None)(
            self._getInstanceType)
        self._getImage = functools.lru_cache(maxsize=None)(
            self._getImage)

        self.log = logging.getLogger(
            f"nodepool.AwsAdapter.{provider_config.name}")
        self.provider = provider_config
        self._running = True

        # AWS has a default rate limit for creating instances that
        # works out to a sustained 2 instances/sec, but the actual
        # create instance API call takes 1 second or more.  If we want
        # to achieve faster than 1 instance/second throughput, we need
        # to parallelize create instance calls, so we set up a
        # threadworker to do that.

        # A little bit of a heuristic here to set the worker count.
        # It appears that AWS typically takes 1-1.5 seconds to execute
        # a create API call.  Figure out how many we have to do in
        # parallel in order to run at the rate limit, then quadruple
        # that for headroom.  Max out at 8 so we don't end up with too
        # many threads.  In practice, this will be 8 with the default
        # values, and only less if users slow down the rate.
        workers = max(min(int(self.provider.rate * 4), 8), 1)
        self.log.info("Create executor with max workers=%s", workers)
        self.create_executor = ThreadPoolExecutor(max_workers=workers)

        # We can batch delete instances using the AWS API, so to do
        # that, create a queue for deletes, and a thread to process
        # the queue.  It will be greedy and collect as many pending
        # instance deletes as possible to delete together.  Typically
        # under load, that will mean a single instance delete followed
        # by larger batches.  That strikes a balance between
        # responsiveness and efficiency.  Reducing the overall number
        # of requests leaves more time for create instance calls.
        self.delete_host_queue = queue.Queue()
        self.delete_instance_queue = queue.Queue()
        self.delete_thread = threading.Thread(target=self._deleteThread)
        self.delete_thread.daemon = True
        self.delete_thread.start()

        self.rate_limiter = RateLimiter(self.provider.name,
                                        self.provider.rate)
        # Non mutating requests can be made more often at 10x the rate
        # of mutating requests by default.
        self.non_mutating_rate_limiter = RateLimiter(self.provider.name,
                                                     self.provider.rate * 10.0)
        # Experimentally, this rate limit refreshes tokens at
        # something like 0.16/second, so if we operated at the rate
        # limit, it would take us almost a minute to determine the
        # quota.  Instead, we're going to just use the normal provider
        # rate and rely on caching to avoid going over the limit.  At
        # the of writing, we'll issue bursts of 5 requests every 5
        # minutes.
        self.quota_service_rate_limiter = RateLimiter(self.provider.name,
                                                      self.provider.rate)
        self.image_id_by_filter_cache = cachetools.TTLCache(
            maxsize=8192, ttl=(5 * 60))
        self.aws = boto3.Session(
            region_name=self.provider.region_name,
            profile_name=self.provider.profile_name)
        self.ec2_client = self.aws.client("ec2")
        self.s3 = self.aws.resource('s3')
        self.s3_client = self.aws.client('s3')
        self.aws_quotas = self.aws.client("service-quotas")
        self.ebs_client = self.aws.client('ebs')

        workers = 10
        self.log.info("Create executor with max workers=%s", workers)
        self.api_executor = ThreadPoolExecutor(
            thread_name_prefix=f'aws-api-{provider_config.name}',
            max_workers=workers)

        # Use a lazy TTL cache for these.  This uses the TPE to
        # asynchronously update the cached values, meanwhile returning
        # the previous cached data if available.  This means every
        # call after the first one is instantaneous.
        self._listHosts = LazyExecutorTTLCache(
            CACHE_TTL, self.api_executor)(
                self._listHosts)
        self._listInstances = LazyExecutorTTLCache(
            CACHE_TTL, self.api_executor)(
                self._listInstances)
        self._listVolumes = LazyExecutorTTLCache(
            CACHE_TTL, self.api_executor)(
                self._listVolumes)
        self._listAmis = LazyExecutorTTLCache(
            CACHE_TTL, self.api_executor)(
                self._listAmis)
        self._listSnapshots = LazyExecutorTTLCache(
            CACHE_TTL, self.api_executor)(
                self._listSnapshots)
        self._listObjects = LazyExecutorTTLCache(
            CACHE_TTL, self.api_executor)(
                self._listObjects)
        self._listEC2Quotas = LazyExecutorTTLCache(
            SERVICE_QUOTA_CACHE_TTL, self.api_executor)(
                self._listEC2Quotas)
        self._listEBSQuotas = LazyExecutorTTLCache(
            SERVICE_QUOTA_CACHE_TTL, self.api_executor)(
                self._listEBSQuotas)

        # In listResources, we reconcile AMIs which appear to be
        # imports but have no nodepool tags, however it's possible
        # that these aren't nodepool images.  If we determine that's
        # the case, we'll add their ids here so we don't waste our
        # time on that again.
        self.not_our_images = set()
        self.not_our_snapshots = set()
        self._createLaunchTemplates()

    def stop(self):
        self.create_executor.shutdown()
        self.api_executor.shutdown()
        self._running = False

    def getCreateStateMachine(self, hostname, label, image_external_id,
                              metadata, request, az, log):
        return AwsCreateStateMachine(self, hostname, label, image_external_id,
                                     metadata, request, log)

    def getDeleteStateMachine(self, external_id, log):
        return AwsDeleteStateMachine(self, external_id, log)

    def listResources(self):
        self._tagSnapshots()
        self._tagAmis()
        for host in self._listHosts():
            try:
                if host['State'].lower() in [
                        "released", "released-permanent-failure"]:
                    continue
            except botocore.exceptions.ClientError:
                continue
            yield AwsResource(tag_list_to_dict(host.get('Tags')),
                              AwsResource.TYPE_HOST,
                              host['HostId'])
        for instance in self._listInstances():
            try:
                if instance['State']['Name'].lower() == "terminated":
                    continue
            except botocore.exceptions.ClientError:
                continue
            yield AwsResource(tag_list_to_dict(instance.get('Tags')),
                              AwsResource.TYPE_INSTANCE,
                              instance['InstanceId'])
        for volume in self._listVolumes():
            try:
                if volume['State'].lower() == "deleted":
                    continue
            except botocore.exceptions.ClientError:
                continue
            yield AwsResource(tag_list_to_dict(volume.get('Tags')),
                              AwsResource.TYPE_VOLUME, volume['VolumeId'])
        for ami in self._listAmis():
            try:
                if ami['State'].lower() == "deleted":
                    continue
            except botocore.exceptions.ClientError:
                continue
            yield AwsResource(tag_list_to_dict(ami.get('Tags')),
                              AwsResource.TYPE_AMI, ami['ImageId'])
        for snap in self._listSnapshots():
            try:
                if snap['State'].lower() == "deleted":
                    continue
            except botocore.exceptions.ClientError:
                continue
            yield AwsResource(tag_list_to_dict(snap.get('Tags')),
                              AwsResource.TYPE_SNAPSHOT, snap['SnapshotId'])
        if self.provider.object_storage:
            for obj in self._listObjects():
                with self.non_mutating_rate_limiter:
                    try:
                        tags = self.s3_client.get_object_tagging(
                            Bucket=obj.bucket_name, Key=obj.key)
                    except botocore.exceptions.ClientError:
                        continue
                yield AwsResource(tag_list_to_dict(tags['TagSet']),
                                  AwsResource.TYPE_OBJECT, obj.key)

    def deleteResource(self, resource):
        self.log.info(f"Deleting leaked {resource.type}: {resource.id}")
        if resource.type == AwsResource.TYPE_HOST:
            self._releaseHost(resource.id, immediate=True)
        if resource.type == AwsResource.TYPE_INSTANCE:
            self._deleteInstance(resource.id, immediate=True)
        if resource.type == AwsResource.TYPE_VOLUME:
            self._deleteVolume(resource.id)
        if resource.type == AwsResource.TYPE_AMI:
            self._deleteAmi(resource.id)
        if resource.type == AwsResource.TYPE_SNAPSHOT:
            self._deleteSnapshot(resource.id)
        if resource.type == AwsResource.TYPE_OBJECT:
            self._deleteObject(resource.id)

    def listInstances(self):
        volumes = {}
        for volume in self._listVolumes():
            volumes[volume['VolumeId']] = volume
        for instance in self._listInstances():
            if instance['State']["Name"].lower() == "terminated":
                continue
            # For now, we are optimistically assuming that when an
            # instance is launched on a dedicated host, it is not
            # counted against instance quota.  That may be overly
            # optimistic.  If it is, then we will merge the two quotas
            # below rather than switch.
            # Additionally, we are using the instance as a proxy for
            # the host.  It would be more correct to also list hosts
            # here to include hosts with no instances.  But since our
            # support for dedicated hosts is currently 1:1 with
            # instances, this should be sufficient.
            if instance['Placement'].get('HostId'):
                # Dedicated host
                quota = self._getQuotaForHostType(
                    instance['InstanceType'])
            else:
                quota = self._getQuotaForInstanceType(
                    instance['InstanceType'],
                    SPOT if instance.get('InstanceLifecycle') == 'spot'
                    else ON_DEMAND)
            for attachment in instance['BlockDeviceMappings']:
                volume_id = attachment['Ebs']['VolumeId']
                volume = volumes.get(volume_id)
                if volume is None:
                    self.log.warning(
                        "Volume %s of instance %s could not be found",
                        volume_id, instance['InstanceId'])
                    continue
                quota.add(self._getQuotaForVolume(volume))

            yield AwsInstance(self.provider, instance, None, quota, None)

    def getQuotaLimits(self):
        # Get the instance and volume types that this provider handles
        instance_types = {}
        host_types = set()
        volume_types = set()
        ec2_quotas = self._listEC2Quotas()
        ebs_quotas = self._listEBSQuotas()
        for pool in self.provider.pools.values():
            for label in pool.labels.values():
                if label.dedicated_host:
                    host_types.add(label.instance_type)
                else:
                    label_instance_types = []
                    if label.instance_type:
                        label_instance_types.append(label.instance_type)
                    elif label.fleet and label.fleet.get('instance-types'):
                        # Include instance-types from fleet config if available
                        label_instance_types.extend(
                            label.fleet.get('instance-types'))
                    for label_instance_type in label_instance_types:
                        if label_instance_type not in instance_types:
                            instance_types[label_instance_type] = set()
                        instance_types[label_instance_type].add(
                            SPOT if label.use_spot else ON_DEMAND)
                if label.volume_type:
                    volume_types.add(label.volume_type)
        args = dict(default=math.inf)
        for instance_type in instance_types:
            for market_type_option in instance_types[instance_type]:
                code = self._getQuotaCodeForInstanceType(instance_type,
                                                         market_type_option)
                if code in args:
                    continue
                if not code:
                    continue
                if code not in ec2_quotas:
                    self.log.warning(
                        "AWS quota code %s for instance type: %s not known",
                        code, instance_type)
                    continue
                args[code] = ec2_quotas[code]
        for host_type in host_types:
            code = self._getQuotaCodeForHostType(host_type)
            if code in args:
                continue
            if not code:
                continue
            if code not in ec2_quotas:
                self.log.warning(
                    "AWS quota code %s for host type: %s not known",
                    code, host_type)
                continue
            args[code] = ec2_quotas[code]
        for volume_type in volume_types:
            vquota_codes = VOLUME_QUOTA_CODES.get(volume_type)
            if not vquota_codes:
                self.log.warning(
                    "Unknown quota code for volume type: %s",
                    volume_type)
                continue
            for resource, code in vquota_codes.items():
                if code in args:
                    continue
                if code not in ebs_quotas:
                    self.log.warning(
                        "AWS quota code %s for volume type: %s not known",
                        code, volume_type)
                    continue
                value = ebs_quotas[code]
                # Unit mismatch: storage limit is in TB, but usage
                # is in GB.  Translate the limit to GB.
                if resource == 'storage':
                    value *= 1000
                args[code] = value
        return QuotaInformation(**args)

    def getQuotaForLabel(self, label):
        return self._getQuotaForLabel(label)

    def _getQuotaForLabel(self, label, instance_type=None):
        # When using the Fleet API, we may need to fill in quota
        # information from the actual instance, so this internal
        # method operates on the label alone or label+instance.

        # For now, we are optimistically assuming that when an
        # instance is launched on a dedicated host, it is not counted
        # against instance quota.  That may be overly optimistic.  If
        # it is, then we will merge the two quotas below rather than
        # switch.
        if label.dedicated_host:
            quota = self._getQuotaForHostType(
                label.instance_type)
        elif label.fleet and instance_type is None:
            # For fleet API, do not check quota before launch the instance
            quota = QuotaInformation(instances=1)
        else:
            check_instance_type = label.instance_type or instance_type
            quota = self._getQuotaForInstanceType(
                check_instance_type,
                SPOT if label.use_spot else ON_DEMAND)
        if label.volume_type:
            quota.add(self._getQuotaForVolumeType(
                label.volume_type,
                storage=label.volume_size,
                iops=label.iops))
        return quota

    def uploadImage(self, provider_image, image_name, filename,
                    image_format, metadata, md5, sha256):
        self.log.debug(f"Uploading image {image_name}")

        # There is no IMDS support option for the import_image call
        if (provider_image.import_method == 'image' and
            provider_image.imds_support == 'v2.0'):
            raise Exception("IMDSv2 requires 'snapshot' import method")

        if provider_image.import_method != 'ebs-direct':
            # Upload image to S3
            bucket_name = self.provider.object_storage['bucket-name']
            bucket = self.s3.Bucket(bucket_name)
            object_filename = f'{image_name}.{image_format}'
            extra_args = {'Tagging': urllib.parse.urlencode(metadata)}

            with open(filename, "rb") as fobj:
                with self.rate_limiter:
                    bucket.upload_fileobj(fobj, object_filename,
                                          ExtraArgs=extra_args)

        if provider_image.import_method == 'image':
            image_id = self._uploadImageImage(
                provider_image, image_name, filename,
                image_format, metadata, md5, sha256,
                bucket_name, object_filename)
        elif provider_image.import_method == 'snapshot':
            image_id = self._uploadImageSnapshot(
                provider_image, image_name, filename,
                image_format, metadata, md5, sha256,
                bucket_name, object_filename)
        elif provider_image.import_method == 'ebs-direct':
            image_id = self._uploadImageSnapshotEBS(
                provider_image, image_name, filename,
                image_format, metadata)
        else:
            raise Exception("Unknown image import method")
        return image_id

    def _registerImage(self, provider_image, image_name, metadata,
                       volume_size, snapshot_id):
        # Register the snapshot as an AMI
        with self.rate_limiter:
            bdm = {
                'DeviceName': '/dev/sda1',
                'Ebs': {
                    'DeleteOnTermination': True,
                    'SnapshotId': snapshot_id,
                    'VolumeSize': volume_size,
                    'VolumeType': provider_image.volume_type,
                },
            }
            if provider_image.iops:
                bdm['Ebs']['Iops'] = provider_image.iops
            if provider_image.throughput:
                bdm['Ebs']['Throughput'] = provider_image.throughput

            args = dict(
                Architecture=provider_image.architecture,
                BlockDeviceMappings=[bdm],
                RootDeviceName='/dev/sda1',
                VirtualizationType='hvm',
                EnaSupport=provider_image.ena_support,
                Name=image_name,
                TagSpecifications=[
                    {
                        'ResourceType': 'image',
                        'Tags': tag_dict_to_list(metadata),
                    },
                ]
            )
            if provider_image.imds_support == 'v2.0':
                args['ImdsSupport'] = 'v2.0'
            return self.ec2_client.register_image(**args)

    def _uploadImageSnapshotEBS(self, provider_image, image_name, filename,
                                image_format, metadata):
        # Import snapshot
        uploader = EBSSnapshotUploader(self, self.log, filename, image_name,
                                       metadata)
        self.log.debug(f"Importing {image_name} as EBS snapshot")
        volume_size, snapshot_id = uploader.upload(
            self.provider.image_import_timeout)

        register_response = self._registerImage(
            provider_image, image_name, metadata, volume_size, snapshot_id,
        )

        self.log.debug(f"Upload of {image_name} complete as "
                       f"{register_response['ImageId']}")
        return register_response['ImageId']

    def _uploadImageSnapshot(self, provider_image, image_name, filename,
                             image_format, metadata, md5, sha256,
                             bucket_name, object_filename):
        # Import snapshot
        self.log.debug(f"Importing {image_name} as snapshot")
        timeout = time.time()
        if self.provider.image_import_timeout:
            timeout += self.provider.image_import_timeout
        while True:
            try:
                with self.rate_limiter:
                    import_snapshot_task = self.ec2_client.import_snapshot(
                        DiskContainer={
                            'Format': image_format,
                            'UserBucket': {
                                'S3Bucket': bucket_name,
                                'S3Key': object_filename,
                            },
                        },
                        TagSpecifications=[
                            {
                                'ResourceType': 'import-snapshot-task',
                                'Tags': tag_dict_to_list(metadata),
                            },
                        ]
                    )
                    break
            except botocore.exceptions.ClientError as error:
                if (error.response['Error']['Code'] ==
                    'ResourceCountLimitExceeded'):
                    if time.time() < timeout:
                        self.log.warning("AWS error: '%s' will retry",
                                         str(error))
                        time.sleep(self.IMAGE_UPLOAD_SLEEP)
                        continue
                raise
        task_id = import_snapshot_task['ImportTaskId']

        paginator = self.ec2_client.get_paginator(
            'describe_import_snapshot_tasks')
        done = False
        while not done:
            time.sleep(self.IMAGE_UPLOAD_SLEEP)
            with self.non_mutating_rate_limiter:
                for page in paginator.paginate(ImportTaskIds=[task_id]):
                    for task in page['ImportSnapshotTasks']:
                        if task['SnapshotTaskDetail']['Status'].lower() in (
                                'completed', 'deleted'):
                            done = True
                            break

        self.log.debug(f"Deleting {image_name} from S3")
        with self.rate_limiter:
            self.s3.Object(bucket_name, object_filename).delete()

        if task['SnapshotTaskDetail']['Status'].lower() != 'completed':
            raise Exception(f"Error uploading image: {task}")

        # Tag the snapshot
        try:
            with self.non_mutating_rate_limiter:
                resp = self.ec2_client.describe_snapshots(
                    SnapshotIds=[task['SnapshotTaskDetail']['SnapshotId']])
                snap = resp['Snapshots'][0]
            with self.rate_limiter:
                self.ec2_client.create_tags(
                    Resources=[task['SnapshotTaskDetail']['SnapshotId']],
                    Tags=task['Tags'])
        except Exception:
            self.log.exception("Error tagging snapshot:")

        volume_size = provider_image.volume_size or snap['VolumeSize']
        snapshot_id = task['SnapshotTaskDetail']['SnapshotId']
        register_response = self._registerImage(
            provider_image, image_name, metadata, volume_size, snapshot_id,
        )

        self.log.debug(f"Upload of {image_name} complete as "
                       f"{register_response['ImageId']}")
        return register_response['ImageId']

    def _uploadImageImage(self, provider_image, image_name, filename,
                          image_format, metadata, md5, sha256,
                          bucket_name, object_filename):
        # Import image as AMI
        self.log.debug(f"Importing {image_name} as AMI")
        timeout = time.time()
        if self.provider.image_import_timeout:
            timeout += self.provider.image_import_timeout
        while True:
            try:
                with self.rate_limiter:
                    import_image_task = self.ec2_client.import_image(
                        Architecture=provider_image.architecture,
                        DiskContainers=[{
                            'Format': image_format,
                            'UserBucket': {
                                'S3Bucket': bucket_name,
                                'S3Key': object_filename,
                            },
                        }],
                        TagSpecifications=[
                            {
                                'ResourceType': 'import-image-task',
                                'Tags': tag_dict_to_list(metadata),
                            },
                        ]
                    )
                    break
            except botocore.exceptions.ClientError as error:
                if (error.response['Error']['Code'] ==
                    'ResourceCountLimitExceeded'):
                    if time.time() < timeout:
                        self.log.warning("AWS error: '%s' will retry",
                                         str(error))
                        time.sleep(self.IMAGE_UPLOAD_SLEEP)
                        continue
                raise
        task_id = import_image_task['ImportTaskId']

        paginator = self.ec2_client.get_paginator(
            'describe_import_image_tasks')
        done = False
        while not done:
            time.sleep(self.IMAGE_UPLOAD_SLEEP)
            with self.non_mutating_rate_limiter:
                for page in paginator.paginate(ImportTaskIds=[task_id]):
                    for task in page['ImportImageTasks']:
                        if task['Status'].lower() in ('completed', 'deleted'):
                            done = True
                            break

        self.log.debug(f"Deleting {image_name} from S3")
        with self.rate_limiter:
            self.s3.Object(bucket_name, object_filename).delete()

        if task['Status'].lower() != 'completed':
            raise Exception(f"Error uploading image: {task}")

        # Tag the AMI
        try:
            with self.rate_limiter:
                self.ec2_client.create_tags(
                    Resources=[task['ImageId']],
                    Tags=task['Tags'])
        except Exception:
            self.log.exception("Error tagging AMI:")

        # Tag the snapshot
        try:
            with self.rate_limiter:
                self.ec2_client.create_tags(
                    Resources=[task['SnapshotDetails'][0]['SnapshotId']],
                    Tags=task['Tags'])
        except Exception:
            self.log.exception("Error tagging snapshot:")

        self.log.debug(f"Upload of {image_name} complete as {task['ImageId']}")
        # Last task returned from paginator above
        return task['ImageId']

    def deleteImage(self, external_id):
        snaps = set()
        self.log.debug(f"Deleting image {external_id}")
        for ami in self._listAmis():
            if ami['ImageId'] == external_id:
                for bdm in ami.get('BlockDeviceMappings', []):
                    snapid = bdm.get('Ebs', {}).get('SnapshotId')
                    if snapid:
                        snaps.add(snapid)
        self._deleteAmi(external_id)
        for snapshot_id in snaps:
            self._deleteSnapshot(snapshot_id)

    # Local implementation below

    def _tagAmis(self):
        # There is no way to tag imported AMIs, so this routine
        # "eventually" tags them.  We look for any AMIs without tags
        # and we copy the tags from the associated snapshot or image
        # import task.
        to_examine = []
        for ami in self._listAmis():
            if ami['ImageId'] in self.not_our_images:
                continue
            if ami.get('Tags'):
                continue

            # This has no tags, which means it's either not a nodepool
            # image, or it's a new one which doesn't have tags yet.
            if ami['Name'].startswith('import-ami-'):
                task = self._getImportImageTask(ami['Name'])
                if task:
                    # This was an import image (not snapshot) so let's
                    # try to find tags from the import task.
                    tags = tag_list_to_dict(task.get('Tags'))
                    if (tags.get('nodepool_provider_name') ==
                        self.provider.name):
                        # Copy over tags
                        self.log.debug(
                            "Copying tags from import task %s to AMI",
                            ami['Name'])
                        with self.rate_limiter:
                            self.ec2_client.create_tags(
                                Resources=[ami['ImageId']],
                                Tags=task['Tags'])
                        continue

            # This may have been a snapshot import; try to copy over
            # any tags from the snapshot import task, otherwise, mark
            # it as an image we can ignore in future runs.
            if len(ami.get('BlockDeviceMappings', [])) < 1:
                self.not_our_images.add(ami['ImageId'])
                continue
            bdm = ami['BlockDeviceMappings'][0]
            ebs = bdm.get('Ebs')
            if not ebs:
                self.not_our_images.add(ami['ImageId'])
                continue
            snapshot_id = ebs.get('SnapshotId')
            if not snapshot_id:
                self.not_our_images.add(ami['ImageId'])
                continue
            to_examine.append((ami, snapshot_id))
        if not to_examine:
            return

        # We have images to examine; get a list of import tasks so
        # we can copy the tags from the import task that resulted in
        # this image.
        task_map = {}
        for task in self._listImportSnapshotTasks():
            detail = task['SnapshotTaskDetail']
            task_snapshot_id = detail.get('SnapshotId')
            if not task_snapshot_id:
                continue
            task_map[task_snapshot_id] = task['Tags']

        for ami, snapshot_id in to_examine:
            tags = task_map.get(snapshot_id)
            if not tags:
                self.not_our_images.add(ami['ImageId'])
                continue
            metadata = tag_list_to_dict(tags)
            if (metadata.get('nodepool_provider_name') == self.provider.name):
                # Copy over tags
                self.log.debug(
                    "Copying tags from import task to image %s",
                    ami['ImageId'])
                with self.rate_limiter:
                    self.ec2_client.create_tags(
                        Resources=[ami['ImageId']],
                        Tags=task['Tags'])
            else:
                self.not_our_images.add(ami['ImageId'])

    def _tagSnapshots(self):
        # See comments for _tagAmis
        to_examine = []
        for snap in self._listSnapshots():
            if snap['SnapshotId'] in self.not_our_snapshots:
                continue
            try:
                if snap.get('Tags'):
                    continue
            except botocore.exceptions.ClientError:
                # We may have cached a snapshot that doesn't exist
                continue

            if 'import-ami' in snap.get('Description', ''):
                match = re.match(r'.*?(import-ami-\w*)',
                                 snap.get('Description', ''))
                task = None
                if match:
                    task_id = match.group(1)
                    task = self._getImportImageTask(task_id)
                if task:
                    # This was an import image (not snapshot) so let's
                    # try to find tags from the import task.
                    tags = tag_list_to_dict(task.get('Tags'))
                    if (tags.get('nodepool_provider_name') ==
                        self.provider.name):
                        # Copy over tags
                        self.log.debug(
                            f"Copying tags from import task {task_id}"
                            " to snapshot")
                        with self.rate_limiter:
                            self.ec2_client.create_tags(
                                Resources=[snap['SnapshotId']],
                                Tags=task['Tags'])
                        continue

            # This may have been a snapshot import; try to copy over
            # any tags from the snapshot import task.
            to_examine.append(snap)

        if not to_examine:
            return

        # We have snapshots to examine; get a list of import tasks so
        # we can copy the tags from the import task that resulted in
        # this snapshot.
        task_map = {}
        for task in self._listImportSnapshotTasks():
            detail = task['SnapshotTaskDetail']
            task_snapshot_id = detail.get('SnapshotId')
            if not task_snapshot_id:
                continue
            task_map[task_snapshot_id] = task['Tags']

        for snap in to_examine:
            tags = task_map.get(snap['SnapshotId'])
            if not tags:
                self.not_our_snapshots.add(snap['SnapshotId'])
                continue
            metadata = tag_list_to_dict(tags)
            if (metadata.get('nodepool_provider_name') == self.provider.name):
                # Copy over tags
                self.log.debug(
                    "Copying tags from import task to snapshot %s",
                    snap['SnapshotId'])
                with self.rate_limiter:
                    self.ec2_client.create_tags(
                        Resources=[snap['SnapshotId']],
                        Tags=tags)
            else:
                self.not_our_snapshots.add(snap['SnapshotId'])

    def _getImportImageTask(self, task_id):
        paginator = self.ec2_client.get_paginator(
            'describe_import_image_tasks')
        with self.non_mutating_rate_limiter:
            try:
                for page in paginator.paginate(ImportTaskIds=[task_id]):
                    for task in page['ImportImageTasks']:
                        # Return the first and only task
                        return task
            except botocore.exceptions.ClientError as error:
                if (error.response['Error']['Code'] ==
                    'InvalidConversionTaskId.Malformed'):
                    # In practice, this can mean that the task no
                    # longer exists
                    pass
                else:
                    raise
        return None

    def _listImportSnapshotTasks(self):
        paginator = self.ec2_client.get_paginator(
            'describe_import_snapshot_tasks')
        with self.non_mutating_rate_limiter:
            for page in paginator.paginate():
                for task in page['ImportSnapshotTasks']:
                    yield task

    instance_key_re = re.compile(r'([a-z\-]+)\d.*')

    def _getQuotaCodeForInstanceType(self, instance_type, market_type_option):
        m = self.instance_key_re.match(instance_type)
        if m:
            key = m.group(1)
            code = INSTANCE_QUOTA_CODES.get(key)
            if code:
                return code[market_type_option]
            self.log.warning(
                "Unknown quota code for instance type: %s",
                instance_type)
        return None

    def _getQuotaForInstanceType(self, instance_type, market_type_option):
        try:
            itype = self._getInstanceType(instance_type)
            cores = itype['InstanceTypes'][0]['VCpuInfo']['DefaultCores']
            vcpus = itype['InstanceTypes'][0]['VCpuInfo']['DefaultVCpus']
            ram = itype['InstanceTypes'][0]['MemoryInfo']['SizeInMiB']
            code = self._getQuotaCodeForInstanceType(instance_type,
                                                     market_type_option)
        except botocore.exceptions.ClientError as error:
            if error.response['Error']['Code'] == 'InvalidInstanceType':
                self.log.exception("Error querying instance type: %s",
                                   instance_type)
                # Re-raise as a configuration exception so that the
                # statemachine driver resets quota.
                raise exceptions.RuntimeConfigurationException(str(error))
            raise
        # We include cores to match the overall cores quota (which may
        # be set as a tenant resource limit), and include vCPUs for the
        # specific AWS quota code which in for a specific instance
        # type. With two threads per core, the vCPU number is
        # typically twice the number of cores. AWS service quotas are
        # implemented in terms of vCPUs.
        args = dict(cores=cores, ram=ram, instances=1)
        if code:
            args[code] = vcpus

        return QuotaInformation(**args)

    host_key_re = re.compile(r'([a-z\d\-]+)\..*')

    def _getQuotaCodeForHostType(self, host_type):
        m = self.host_key_re.match(host_type)
        if m:
            key = m.group(1)
            code = HOST_QUOTA_CODES.get(key)
            if code:
                return code
            self.log.warning(
                "Unknown quota code for host type: %s",
                host_type)
        return None

    def _getQuotaForHostType(self, host_type):
        code = self._getQuotaCodeForHostType(host_type)
        args = dict(instances=1)
        if code:
            args[code] = 1

        return QuotaInformation(**args)

    def _getQuotaForVolume(self, volume):
        volume_type = volume['VolumeType']
        vquota_codes = VOLUME_QUOTA_CODES.get(volume_type, {})
        args = {}
        if 'iops' in vquota_codes and volume.get('Iops'):
            args[vquota_codes['iops']] = volume['Iops']
        if 'storage' in vquota_codes and volume.get('Size'):
            args[vquota_codes['storage']] = volume['Size']
        return QuotaInformation(**args)

    def _getQuotaForVolumeType(self, volume_type, storage=None, iops=None):
        vquota_codes = VOLUME_QUOTA_CODES.get(volume_type, {})
        args = {}
        if 'iops' in vquota_codes and iops is not None:
            args[vquota_codes['iops']] = iops
        if 'storage' in vquota_codes and storage is not None:
            args[vquota_codes['storage']] = storage
        return QuotaInformation(**args)

    # This method is wrapped with an LRU cache in the constructor.
    def _getInstanceType(self, instance_type):
        with self.non_mutating_rate_limiter:
            self.log.debug(
                f"Getting information for instance type {instance_type}")
            return self.ec2_client.describe_instance_types(
                InstanceTypes=[instance_type])

    def _refresh(self, obj):
        if 'InstanceId' in obj:
            for instance in self._listInstances():
                if instance['InstanceId'] == obj['InstanceId']:
                    return instance
        elif 'HostId' in obj:
            for host in self._listHosts():
                if host['HostId'] == obj['HostId']:
                    return host
        return obj

    def _refreshDelete(self, obj):
        if obj is None:
            return obj

        if 'InstanceId' in obj:
            for instance in self._listInstances():
                if instance['InstanceId'] == obj['InstanceId']:
                    if instance['State']['Name'].lower() == "terminated":
                        return None
                    return instance
        elif 'HostId' in obj:
            for host in self._listHosts():
                if host['HostId'] == obj['HostId']:
                    if host['State'].lower() in [
                            'released', 'released-permanent-failure']:
                        return None
                    return host
        return None

    def _listServiceQuotas(self, service_code):
        with self.quota_service_rate_limiter(
                self.log.debug, f"Listed {service_code} quotas"):
            paginator = self.aws_quotas.get_paginator(
                'list_service_quotas')
            quotas = {}
            for page in paginator.paginate(ServiceCode=service_code):
                for quota in page['Quotas']:
                    quotas[quota['QuotaCode']] = quota['Value']
            return quotas

    def _listEC2Quotas(self):
        return self._listServiceQuotas('ec2')

    def _listEBSQuotas(self):
        return self._listServiceQuotas('ebs')

    def _listHosts(self):
        with self.non_mutating_rate_limiter(
                self.log.debug, "Listed hosts"):
            paginator = self.ec2_client.get_paginator('describe_hosts')
            hosts = []
            for page in paginator.paginate():
                hosts.extend(page['Hosts'])
            return hosts

    def _listInstances(self):
        with self.non_mutating_rate_limiter(
                self.log.debug, "Listed instances"):
            paginator = self.ec2_client.get_paginator('describe_instances')
            instances = []
            for page in paginator.paginate():
                for res in page['Reservations']:
                    instances.extend(res['Instances'])
            return instances

    def _listVolumes(self):
        with self.non_mutating_rate_limiter(
                self.log.debug, "Listed volumes"):
            paginator = self.ec2_client.get_paginator('describe_volumes')
            volumes = []
            for page in paginator.paginate():
                volumes.extend(page['Volumes'])
            return volumes

    def _listAmis(self):
        # Note: this is overridden in tests due to the filter
        with self.non_mutating_rate_limiter(
                self.log.debug, "Listed images"):
            paginator = self.ec2_client.get_paginator('describe_images')
            images = []
            for page in paginator.paginate(Owners=['self']):
                images.extend(page['Images'])
            return images

    def _listSnapshots(self):
        # Note: this is overridden in tests due to the filter
        with self.non_mutating_rate_limiter(
                self.log.debug, "Listed snapshots"):
            paginator = self.ec2_client.get_paginator('describe_snapshots')
            snapshots = []
            for page in paginator.paginate(OwnerIds=['self']):
                snapshots.extend(page['Snapshots'])
            return snapshots

    def _listObjects(self):
        bucket_name = self.provider.object_storage.get('bucket-name')
        if not bucket_name:
            return []

        bucket = self.s3.Bucket(bucket_name)
        with self.non_mutating_rate_limiter(
                self.log.debug, "Listed S3 objects"):
            return list(bucket.objects.all())

    def _getLatestImageIdByFilters(self, image_filters):
        # Normally we would decorate this method, but our cache key is
        # complex, so we serialize it to JSON and manage the cache
        # ourselves.
        cache_key = json.dumps(image_filters)
        val = self.image_id_by_filter_cache.get(cache_key)
        if val:
            return val

        with self.non_mutating_rate_limiter:
            res = list(self.ec2_client.describe_images(
                Filters=image_filters
            ).get("Images"))

        images = sorted(
            res,
            key=lambda k: k["CreationDate"],
            reverse=True
        )

        if not images:
            raise Exception(
                "No cloud-image (AMI) matches supplied image filters")
        else:
            val = images[0].get("ImageId")
            self.image_id_by_filter_cache[cache_key] = val
            return val

    def _getImageId(self, cloud_image):
        image_id = cloud_image.image_id
        image_filters = cloud_image.image_filters

        if image_filters is not None:
            return self._getLatestImageIdByFilters(image_filters)

        return image_id

    # This method is wrapped with an LRU cache in the constructor.
    def _getImage(self, image_id):
        with self.non_mutating_rate_limiter:
            resp = self.ec2_client.describe_images(ImageIds=[image_id])
            return resp['Images'][0]

    def _submitAllocateHost(self, label,
                            tags, hostname, log):
        return self.create_executor.submit(
            self._allocateHost,
            label,
            tags, hostname, log)

    def _completeAllocateHost(self, future):
        if not future.done():
            return None
        try:
            return future.result()
        except botocore.exceptions.ClientError as error:
            if error.response['Error']['Code'] == 'HostLimitExceeded':
                # Re-raise as a quota exception so that the
                # statemachine driver resets quota.
                raise exceptions.QuotaException(str(error))
            if (error.response['Error']['Code'] ==
                'InsufficientInstanceCapacity'):
                # Re-raise as CapacityException so it would have
                # "error.capacity" statsd_key, which can be handled
                # differently than "error.unknown"
                raise exceptions.CapacityException(str(error))
            raise

    def _allocateHost(self, label,
                      tags, hostname, log):
        args = dict(
            AutoPlacement='off',
            AvailabilityZone=label.pool.az,
            InstanceType=label.instance_type,
            Quantity=1,
            HostRecovery='off',
            HostMaintenance='off',
            TagSpecifications=[
                {
                    'ResourceType': 'dedicated-host',
                    'Tags': tag_dict_to_list(tags),
                },
            ]
        )

        with self.rate_limiter(log.debug, "Allocated host"):
            log.debug("Allocating host %s", hostname)
            resp = self.ec2_client.allocate_hosts(**args)
            host_ids = resp['HostIds']
            log.debug("Allocated host %s as host %s",
                      hostname, host_ids[0])
            return dict(HostId=host_ids[0],
                        State='pending')

    def _submitCreateInstance(self, label, image_external_id,
                              tags, hostname, dedicated_host_id, log):
        return self.create_executor.submit(
            self._createInstance,
            label, image_external_id,
            tags, hostname, dedicated_host_id, log)

    def _completeCreateInstance(self, future):
        if not future.done():
            return None
        try:
            return future.result()
        except botocore.exceptions.ClientError as error:
            if error.response['Error']['Code'] == 'VolumeLimitExceeded':
                # Re-raise as a quota exception so that the
                # statemachine driver resets quota.
                raise exceptions.QuotaException(str(error))
            if (error.response['Error']['Code'] ==
                'InsufficientInstanceCapacity'):
                # Re-raise as CapacityException so it would have
                # "error.capacity" statsd_key, which can be handled
                # differently than "error.unknown"
                raise exceptions.CapacityException(str(error))
            raise

    def _createInstance(self, label, image_external_id,
                        tags, hostname, dedicated_host_id, log):
        if image_external_id:
            image_id = image_external_id
        else:
            image_id = self._getImageId(label.cloud_image)

        if label.fleet:
            return self._createFleet(label, image_id, tags, hostname, log)
        else:
            return self._runInstance(label, image_id, tags,
                                     hostname, dedicated_host_id, log)

    def _createLaunchTemplates(self):
        fleet_labels = []
        for pool_name, pool in self.provider.pools.items():
            for label_name, label in pool.labels.items():
                # Create launch templates only for labels which usage fleet
                if not label.fleet:
                    continue
                fleet_labels.append(label)

        if not fleet_labels:
            return

        self.log.info("Creating launch templates")
        tags = {
            'nodepool_managed': True,
            'nodepool_provider_name': self.provider.name,
        }
        existing_templates = dict()  # for clean up and avoid creation attempt
        created_templates = set()  # for avoid creation attempt
        configured_templates = set()  # for clean up

        name_filter = {
            'Name': 'launch-template-name',
            'Values': [f'{self.LAUNCH_TEMPLATE_PREFIX}-*'],
        }
        paginator = self.ec2_client.get_paginator(
            'describe_launch_templates')
        with self.non_mutating_rate_limiter:
            for page in paginator.paginate(Filters=[name_filter]):
                for template in page['LaunchTemplates']:
                    existing_templates[
                        template['LaunchTemplateName']] = template

        for label in fleet_labels:
            ebs_settings = {
                'DeleteOnTermination': True,
            }
            if label.volume_size:
                ebs_settings['VolumeSize'] = label.volume_size
            if label.volume_type:
                ebs_settings['VolumeType'] = label.volume_type
            if label.iops:
                ebs_settings['Iops'] = label.iops
            if label.throughput:
                ebs_settings['Throughput'] = label.throughput
            template_data = {
                'KeyName': label.key_name,
                'SecurityGroupIds': [label.pool.security_group_id],
                'BlockDeviceMappings': [
                    {
                        'DeviceName': '/dev/sda1',
                        'Ebs': ebs_settings,
                    },
                ],
            }
            if label.imdsv2 == 'required':
                template_data['MetadataOptions'] = {
                    'HttpTokens': 'required',
                    'HttpEndpoint': 'enabled',
                }
            elif label.imdsv2 == 'optional':
                template_data['MetadataOptions'] = {
                    'HttpTokens': 'optional',
                    'HttpEndpoint': 'enabled',
                }

            if label.userdata:
                userdata_base64 = base64.b64encode(
                    label.userdata.encode('ascii')).decode('utf-8')
                template_data['UserData'] = userdata_base64

            template_args = dict(
                LaunchTemplateData=template_data,
                TagSpecifications=[
                    {
                        'ResourceType': 'launch-template',
                        'Tags': tag_dict_to_list(tags),
                    },
                ]
            )

            template_name = self._getLaunchTemplateName(template_args)
            configured_templates.add(template_name)

            label._launch_template_name = template_name
            if (template_name in existing_templates or
                template_name in created_templates):
                self.log.debug(
                    'Launch template %s already exists', template_name)
                continue

            template_args['LaunchTemplateName'] = template_name
            self.log.debug('Creating launch template %s', template_name)
            try:
                self.ec2_client.create_launch_template(**template_args)
                created_templates.add(template_name)
                self.log.debug('Launch template %s created', template_name)
            except botocore.exceptions.ClientError as e:
                if (e.response['Error']['Code'] ==
                    'InvalidLaunchTemplateName.AlreadyExistsException'):
                    self.log.debug(
                        'Launch template %s already created',
                        template_name)
                else:
                    raise e
            except Exception:
                self.log.exception(
                    'Could not create launch template %s', template_name)

        # remove unused templates
        for template_name, template in existing_templates.items():
            if template_name not in configured_templates:
                # check if the template was created by the current provider
                tags = template.get('Tags', [])
                for tag in tags:
                    if (tag['Key'] == 'nodepool_provider_name' and
                        tag['Value'] == self.provider.name):
                        self.ec2_client.delete_launch_template(
                            LaunchTemplateName=template_name)
                        self.log.debug("Deleted unused launch template: %s",
                                       template_name)

    def _getLaunchTemplateName(self, args):
        hasher = hashlib.sha256()
        hasher.update(json.dumps(args, sort_keys=True).encode('utf8'))
        sha = hasher.hexdigest()
        return (f'{self.LAUNCH_TEMPLATE_PREFIX}-{sha}')

    def _createFleet(self, label, image_id, tags, hostname, log):
        overrides = []

        instance_types = label.fleet.get('instance-types', [])
        for instance_type in instance_types:
            overrides.append({
                'ImageId': image_id,
                'InstanceType': instance_type,
                'SubnetId': label.pool.subnet_id,
            })

        if label.use_spot:
            capacity_type_option = {
                'SpotOptions': {
                    'AllocationStrategy': label.fleet['allocation-strategy'],
                },
                'TargetCapacitySpecification': {
                    'TotalTargetCapacity': 1,
                    'DefaultTargetCapacityType': 'spot',
                },
            }
        else:
            capacity_type_option = {
                'OnDemandOptions': {
                    'AllocationStrategy': label.fleet['allocation-strategy'],
                },
                'TargetCapacitySpecification': {
                    'TotalTargetCapacity': 1,
                    'DefaultTargetCapacityType': 'on-demand',
                },
            }

        template_name = label._launch_template_name

        args = {
            **capacity_type_option,
            'LaunchTemplateConfigs': [
                {
                    'LaunchTemplateSpecification': {
                        'LaunchTemplateName': template_name,
                        'Version': '$Latest',
                    },
                    'Overrides': overrides,
                },
            ],
            'Type': 'instant',
            'TagSpecifications': [
                {
                    'ResourceType': 'instance',
                    'Tags': tag_dict_to_list(tags),
                },
                {
                    'ResourceType': 'volume',
                    'Tags': tag_dict_to_list(tags),
                },
            ],
        }

        with self.rate_limiter(log.debug, "Created fleet"):
            resp = self.ec2_client.create_fleet(**args)

            if resp['Instances']:
                instance_id = resp['Instances'][0]['InstanceIds'][0]
            else:
                if resp['Errors']:
                    error = resp['Errors'][0]
                    raise Exception("Couldn't create fleet instance because "
                                    "of %s: %s", error["ErrorCode"],
                                    error["ErrorMessage"])
                raise Exception("Couldn't create fleet instance because "
                                "empty instance list was returned")

            log.debug("Created VM %s as instance %s using EC2 Fleet API",
                      hostname, instance_id)

            # Only return instance id in creating state, the state machine will
            # refresh until the instance object is returned otherwise it can
            # happen that the instance does not exist yet due to the AWS
            # eventual consistency
            return {'InstanceId': instance_id, 'State': {'Name': 'creating'}}

    def _runInstance(self, label, image_id, tags, hostname,
                     dedicated_host_id, log):
        args = dict(
            ImageId=image_id,
            MinCount=1,
            MaxCount=1,
            KeyName=label.key_name,
            EbsOptimized=label.ebs_optimized,
            InstanceType=label.instance_type,
            NetworkInterfaces=[{
                'AssociatePublicIpAddress': label.pool.public_ipv4,
                'DeviceIndex': 0}],
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': tag_dict_to_list(tags),
                },
                {
                    'ResourceType': 'volume',
                    'Tags': tag_dict_to_list(tags),
                },
            ]
        )

        if label.pool.security_group_id:
            args['NetworkInterfaces'][0]['Groups'] = [
                label.pool.security_group_id
            ]
        if label.pool.subnet_id:
            args['NetworkInterfaces'][0]['SubnetId'] = label.pool.subnet_id

        if label.pool.public_ipv6:
            args['NetworkInterfaces'][0]['Ipv6AddressCount'] = 1

        if label.userdata:
            args['UserData'] = label.userdata

        if label.iam_instance_profile:
            if 'name' in label.iam_instance_profile:
                args['IamInstanceProfile'] = {
                    'Name': label.iam_instance_profile['name']
                }
            elif 'arn' in label.iam_instance_profile:
                args['IamInstanceProfile'] = {
                    'Arn': label.iam_instance_profile['arn']
                }

        # Default block device mapping parameters are embedded in AMIs.
        # We might need to supply our own mapping before lauching the instance.
        # We basically want to make sure DeleteOnTermination is true and be
        # able to set the volume type and size.
        image = self._getImage(image_id)
        # TODO: Flavors can also influence whether or not the VM spawns with a
        # volume -- we basically need to ensure DeleteOnTermination is true.
        # However, leaked volume detection may mitigate this.
        if image.get('BlockDeviceMappings'):
            bdm = image['BlockDeviceMappings']
            mapping = copy.deepcopy(bdm[0])
            if 'Ebs' in mapping:
                mapping['Ebs']['DeleteOnTermination'] = True
                if label.volume_size:
                    mapping['Ebs']['VolumeSize'] = label.volume_size
                if label.volume_type:
                    mapping['Ebs']['VolumeType'] = label.volume_type
                if label.iops:
                    mapping['Ebs']['Iops'] = label.iops
                if label.throughput:
                    mapping['Ebs']['Throughput'] = label.throughput
                # If the AMI is a snapshot, we cannot supply an "encrypted"
                # parameter
                if 'Encrypted' in mapping['Ebs']:
                    del mapping['Ebs']['Encrypted']
                args['BlockDeviceMappings'] = [mapping]

        # enable EC2 Spot
        if label.use_spot:
            args['InstanceMarketOptions'] = {
                'MarketType': 'spot',
                'SpotOptions': {
                    'SpotInstanceType': 'one-time',
                    'InstanceInterruptionBehavior': 'terminate'
                }
            }

        if label.imdsv2 == 'required':
            args['MetadataOptions'] = {
                'HttpTokens': 'required',
                'HttpEndpoint': 'enabled',
            }
        elif label.imdsv2 == 'optional':
            args['MetadataOptions'] = {
                'HttpTokens': 'optional',
                'HttpEndpoint': 'enabled',
            }

        if dedicated_host_id:
            placement = args.setdefault('Placement', {})
            placement.update({
                'Tenancy': 'host',
                'HostId': dedicated_host_id,
                'Affinity': 'host',
            })

        if label.pool.az:
            placement = args.setdefault('Placement', {})
            placement['AvailabilityZone'] = label.pool.az

        with self.rate_limiter(log.debug, "Created instance"):
            log.debug("Creating VM %s", hostname)
            resp = self.ec2_client.run_instances(**args)
            instances = resp['Instances']
            if dedicated_host_id:
                log.debug("Created VM %s as instance %s on host %s",
                          hostname, instances[0]['InstanceId'],
                          dedicated_host_id)
            else:
                log.debug("Created VM %s as instance %s",
                          hostname, instances[0]['InstanceId'])
            return instances[0]

    def _deleteThread(self):
        while self._running:
            try:
                self._deleteThreadInner()
            except Exception:
                self.log.exception("Error in delete thread:")
                time.sleep(5)

    @staticmethod
    def _getBatch(the_queue):
        records = []
        try:
            records.append(the_queue.get(block=True, timeout=10))
        except queue.Empty:
            return []
        while True:
            try:
                records.append(the_queue.get(block=False))
            except queue.Empty:
                break
            # The terminate call has a limit of 1k, but AWS recommends
            # smaller batches.  We limit to 50 here.
            if len(records) >= 50:
                break
        return records

    def _deleteThreadInner(self):
        records = self._getBatch(self.delete_instance_queue)
        if records:
            ids = []
            for (del_id, log) in records:
                ids.append(del_id)
                log.debug(f"Deleting instance {del_id}")
            count = len(ids)
            with self.rate_limiter(log.debug, f"Deleted {count} instances"):
                self.ec2_client.terminate_instances(InstanceIds=ids)

        records = self._getBatch(self.delete_host_queue)
        if records:
            ids = []
            for (del_id, log) in records:
                ids.append(del_id)
                log.debug(f"Releasing host {del_id}")
            count = len(ids)
            with self.rate_limiter(log.debug, f"Released {count} hosts"):
                self.ec2_client.release_hosts(HostIds=ids)

    def _releaseHost(self, external_id, log=None, immediate=False):
        if log is None:
            log = self.log
        for host in self._listHosts():
            if host['HostId'] == external_id:
                break
        else:
            log.warning(f"Host not found when releasing {external_id}")
            return None
        if immediate:
            with self.rate_limiter(log.debug, "Released host"):
                log.debug(f"Deleting host {external_id}")
                self.ec2_client.release_hosts(
                    HostIds=[host['HostId']])
        else:
            self.delete_host_queue.put((external_id, log))
        return host

    def _deleteInstance(self, external_id, log=None, immediate=False):
        if log is None:
            log = self.log
        for instance in self._listInstances():
            if instance['InstanceId'] == external_id:
                break
        else:
            log.warning(f"Instance not found when deleting {external_id}")
            return None
        if immediate:
            with self.rate_limiter(log.debug, "Deleted instance"):
                log.debug(f"Deleting instance {external_id}")
                self.ec2_client.terminate_instances(
                    InstanceIds=[instance['InstanceId']])
        else:
            self.delete_instance_queue.put((external_id, log))
        return instance

    def _deleteVolume(self, external_id):
        for volume in self._listVolumes():
            if volume['VolumeId'] == external_id:
                break
        else:
            self.log.warning(f"Volume not found when deleting {external_id}")
            return None
        with self.rate_limiter(self.log.debug, "Deleted volume"):
            self.log.debug(f"Deleting volume {external_id}")
            self.ec2_client.delete_volume(VolumeId=volume['VolumeId'])
        return volume

    def _deleteAmi(self, external_id):
        for ami in self._listAmis():
            if ami['ImageId'] == external_id:
                break
        else:
            self.log.warning(f"AMI not found when deleting {external_id}")
            return None
        with self.rate_limiter:
            self.log.debug(f"Deleting AMI {external_id}")
            self.ec2_client.deregister_image(ImageId=ami['ImageId'])
        return ami

    def _deleteSnapshot(self, external_id):
        for snap in self._listSnapshots():
            if snap['SnapshotId'] == external_id:
                break
        else:
            self.log.warning(f"Snapshot not found when deleting {external_id}")
            return None
        with self.rate_limiter:
            self.log.debug(f"Deleting Snapshot {external_id}")
            self.ec2_client.delete_snapshot(SnapshotId=snap['SnapshotId'])
        return snap

    def _deleteObject(self, external_id):
        bucket_name = self.provider.object_storage.get('bucket-name')
        with self.rate_limiter:
            self.log.debug(f"Deleting object {external_id}")
            self.s3.Object(bucket_name, external_id).delete()
