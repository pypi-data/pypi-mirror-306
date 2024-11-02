# Copyright (C) 2018 Red Hat
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

import abc
import concurrent.futures
import copy
import logging
import math
import os
import threading
import time
from collections import defaultdict

from kazoo import exceptions as kze

from nodepool import exceptions
from nodepool import stats
from nodepool.zk import zookeeper as zk
from nodepool.logconfig import get_annotated_logger


MAX_QUOTA_AGE = 5 * 60  # How long to keep the quota information cached


class NodeLauncher(threading.Thread,
                   stats.StatsReporter,
                   metaclass=abc.ABCMeta):
    '''
    Class to launch a single node within a thread and record stats.

    At this time, the implementing class must manage this thread.
    '''

    def __init__(self, handler, node, provider_config):
        '''
        :param NodeRequestHandler handler: The handler object.
        :param Node node: A Node object describing the node to launch.
        :param ProviderConfig provider_config: A ProviderConfig object
            describing the provider launching this node.
        '''
        threading.Thread.__init__(self, name="NodeLauncher-%s" % node.id)
        launcher = handler.pw.nodepool
        stats.StatsReporter.__init__(self, launcher.statsd)
        logger = logging.getLogger("nodepool.NodeLauncher")
        request = handler.request
        self.log = get_annotated_logger(logger,
                                        event_id=request.event_id,
                                        node_request_id=request.id,
                                        node_id=node.id)
        self.handler = handler
        self.zk = handler.zk
        self.node = node
        self.provider_config = provider_config

    @abc.abstractmethod
    def launch(self):
        pass

    def run(self):
        start_time = time.monotonic()
        statsd_key = 'ready'

        try:
            self.launch()
        except kze.SessionExpiredError:
            # Our node lock is gone, leaving the node state as BUILDING.
            # This will get cleaned up in ZooKeeper automatically, but we
            # must still set our cached node state to FAILED for the
            # NodeLaunchManager's poll() method.
            self.log.error(
                "Lost ZooKeeper session trying to launch for node %s",
                self.node.id)
            self.node.state = zk.FAILED
            statsd_key = 'error.zksession'
        except exceptions.QuotaException:
            # We encountered a quota error when trying to launch a
            # node. In this case we need to abort the launch. The upper
            # layers will take care of this and reschedule a new node once
            # the quota is ok again.
            self.log.info("Aborting node %s due to quota failure" %
                          self.node.id)
            self.node.state = zk.ABORTED
            self.zk.storeNode(self.node)
            statsd_key = 'error.quota'
        except Exception as e:
            self.log.exception(
                "Launch failed for node %s: tenant=%s label=%s hostname=%s",
                self.node.id,
                self.node.tenant_name,
                self.node.type,
                self.node.hostname)
            self.node.state = zk.FAILED
            self.zk.storeNode(self.node)

            if hasattr(e, 'statsd_key'):
                statsd_key = e.statsd_key
            else:
                statsd_key = 'error.unknown'

        try:
            dt = int((time.monotonic() - start_time) * 1000)
            self.recordLaunchStats(statsd_key, dt)
        except Exception:
            self.log.exception("Exception while reporting stats:")


class NodeDeleter(threading.Thread):
    log = logging.getLogger("nodepool.NodeDeleter")

    def __init__(self, zk, provider_manager, node):
        threading.Thread.__init__(self, name='NodeDeleter for %s %s' %
                                  (node.provider, node.external_id))
        self._zk = zk
        self._provider_manager = provider_manager
        self._node = node

    @staticmethod
    def delete(zk_conn, manager, node, node_exists=True):
        '''
        Delete a server instance and ZooKeeper node.

        This is a class method so we can support instantaneous deletes.

        :param ZooKeeper zk_conn: A ZooKeeper object to use.
        :param ProviderManager provider_manager: ProviderManager object to
            use fo deleting the server.
        :param Node node: A locked Node object that describes the server to
            delete.
        :param bool node_exists: True if the node actually exists in ZooKeeper.
            An artifical Node object can be passed that can be used to delete
            a leaked instance.
        '''
        try:
            node.state = zk.DELETING
            zk_conn.storeNode(node)
            if node.external_id:
                manager.cleanupNode(node.external_id)
                manager.waitForNodeCleanup(node.external_id)
        except exceptions.NotFound:
            NodeDeleter.log.info("Instance %s not found in provider %s",
                                 node.external_id, node.provider)
        except Exception:
            NodeDeleter.log.exception(
                "Exception deleting instance %s from %s:",
                node.external_id, node.provider)
            # Don't delete the ZK node in this case, but do unlock it
            if node_exists:
                zk_conn.unlockNode(node)
            return

        if node_exists:
            NodeDeleter.log.info(
                "Deleting ZK node id=%s, state=%s, external_id=%s",
                node.id, node.state, node.external_id)
            # This also effectively releases the lock
            zk_conn.deleteNode(node)
            manager.nodeDeletedNotification(node)

    def run(self):
        # Since leaked instances won't have an actual node in ZooKeeper,
        # we need to check 'id' to see if this is an artificial Node.
        if self._node.id is None:
            node_exists = False
        else:
            node_exists = True

        try:
            self.delete(self._zk, self._provider_manager,
                        self._node, node_exists)
        except Exception:
            self.log.exception("Error deleting node %s:", self._node)


class QuotaInformation:

    def __init__(self, cores=None, instances=None, ram=None, default=0, **kw):
        '''
        Initializes the quota information with some values. None values will
        be initialized with default which will be typically 0 or math.inf
        indicating an infinite limit.

        :param cores: An integer number of (v)CPU cores.
        :param instances: An integer number of instances.
        :param ram: An integer amount of RAM in Mebibytes.
        :param default: The default value to use for any attribute not supplied
                        (usually 0 or math.inf).
        '''
        # Note that the self.quota['compute'] map is inserted into ZK as
        # a node property (via get_resources) and is consumed by Zuul to
        # calculate resource usage.  Thus care should be taken if
        # modifying fields below.
        self.quota = {
            'compute': {
                'cores': self._get_default(cores, default),
                'instances': self._get_default(instances, default),
                'ram': self._get_default(ram, default),
            }
        }
        for k, v in kw.items():
            self.quota['compute'][k] = v
        self.default = default

    def _get_default(self, value, default):
        return value if value is not None else default

    def _add_subtract(self, other, add=True):
        for category in other.quota.keys():
            self.quota.setdefault(category, {})
            for resource in other.quota[category].keys():
                self.quota[category].setdefault(resource, self.default)
        for category in self.quota.keys():
            for resource in self.quota[category].keys():
                second_value = other.quota.get(category, {}).get(
                    resource, other.default)
                if add:
                    self.quota[category][resource] += second_value
                else:
                    self.quota[category][resource] -= second_value

    def subtract(self, other):
        self._add_subtract(other, add=False)

    def add(self, other):
        self._add_subtract(other, True)

    def non_negative(self):
        for key_i, category in self.quota.items():
            for resource, value in category.items():
                if value < 0:
                    return False
        return True

    def get_resources(self):
        '''Return resources value to register in ZK node'''
        return self.quota['compute']

    @staticmethod
    def from_resources(resources):
        qi = QuotaInformation()
        qi.quota['compute'] = resources
        return qi

    def __str__(self):
        return str(self.quota)


class QuotaSupport:
    """A mix-in class for providers to supply quota support methods"""

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self._current_nodepool_quota_timestamp = 0
        self._current_nodepool_quota = {}

    @abc.abstractmethod
    def quotaNeededByLabel(self, label, pool):
        """Return quota information about a label

        :param str label: The label name
        :param ProviderPool pool: A ProviderPool config object with the label

        :return: QuotaInformation about the label
        """
        pass

    @abc.abstractmethod
    def unmanagedQuotaUsed(self):
        '''
        Sums up the quota used by servers unmanaged by nodepool.

        :return: Calculated quota in use by unmanaged servers
        '''
        pass

    @abc.abstractmethod
    def getProviderLimits(self):
        '''
        Get the resource limits from the provider.

        :return: QuotaInformation about the label
        '''
        pass

    def invalidateQuotaCache(self):
        self._current_nodepool_quota_timestamp = 0

    def estimatedNodepoolQuota(self):
        '''
        Determine how much quota is available for nodepool managed
        resources.  This needs to take into account the quota of the
        tenant, resources used outside of nodepool, and the max
        settings in nodepool config. This is cached for MAX_QUOTA_AGE
        seconds.

        :return: Total amount of resources available which is currently
                 available to nodepool including currently existing nodes.

        '''

        if self._current_nodepool_quota:
            now = time.time()
            if now < self._current_nodepool_quota_timestamp + MAX_QUOTA_AGE:
                return copy.deepcopy(self._current_nodepool_quota)

        # This is initialized with the full tenant quota and later becomes
        # the quota available for nodepool.
        try:
            nodepool_quota = self.getProviderLimits()
        except Exception:
            if self._current_nodepool_quota:
                self.log.exception("Unable to get provider quota, "
                                   "using cached value")
                return copy.deepcopy(self._current_nodepool_quota)
            raise

        self.log.debug("Provider quota for %s: %s",
                       self.provider.name, nodepool_quota)

        # Subtract the unmanaged quota usage from nodepool_max
        # to get the quota available for us.
        nodepool_quota.subtract(self.unmanagedQuotaUsed())

        self._current_nodepool_quota = nodepool_quota
        self._current_nodepool_quota_timestamp = time.time()

        self.log.debug("Available quota for %s: %s",
                       self.provider.name, nodepool_quota)

        return copy.deepcopy(nodepool_quota)

    def estimatedNodepoolQuotaUsed(self, pool=None):
        '''
        Sums up the quota used (or planned) currently by nodepool. If pool is
        given it is filtered by the pool.

        :param pool: If given, filtered by the pool.
        :return: Calculated quota in use by nodepool
        '''
        used_quota = QuotaInformation()

        for node in self._zk.nodeIterator(cached_ids=True):
            if node.provider == self.provider.name:
                try:
                    if pool and not node.pool == pool.name:
                        continue
                    provider_pool = self.provider.pools.get(node.pool)
                    if not provider_pool:
                        self.log.warning(
                            "Cannot find provider pool for node %s" % node)
                        # This node is in a funny state we log it for debugging
                        # but move on and don't account it as we can't properly
                        # calculate its cost without pool info.
                        continue
                    if node.type[0] not in provider_pool.labels:
                        self.log.warning("Node type is not in provider pool "
                                         "for node %s" % node)
                        # This node is also in a funny state; the config
                        # may have changed under it.  It should settle out
                        # eventually when it's deleted.
                        continue
                    # If the node resources is not None, we can use that to
                    # construct the qi object for the node.
                    if node.resources:
                        node_resources = QuotaInformation.from_resources(
                            node.resources)
                    else:
                        node_resources = self.quotaNeededByLabel(
                            node.type[0], provider_pool)
                    used_quota.add(node_resources)
                except Exception:
                    self.log.exception("Couldn't consider invalid node %s "
                                       "for quota:" % node)
        return used_quota

    def getLabelQuota(self):
        """Return available quota per label.

        :returns: Mapping of labels to available quota
        """
        return defaultdict(lambda: math.inf)


class RateLimitInstance:
    def __init__(self, limiter, logger, msg):
        self.limiter = limiter
        self.logger = logger
        self.msg = msg

    def __enter__(self):
        self.delay = self.limiter._enter()
        self.start_time = time.monotonic()

    def __exit__(self, etype, value, tb):
        end_time = time.monotonic()
        self.limiter._exit(etype, value, tb)
        self.logger("%s in %ss after %ss delay",
                    self.msg,
                    end_time - self.start_time,
                    self.delay)


class RateLimiter:
    """A Rate limiter

    :param str name: The provider name; used in logging.
    :param float rate_limit: The rate limit expressed in
        requests per second.

    Example:
    .. code:: python

        rate_limiter = RateLimiter('provider', 1.0)
        with rate_limiter:
            api_call()

    You can optionally use the limiter as a callable in which case it
    will log a supplied message with timing information.

    .. code:: python

        rate_limiter = RateLimiter('provider', 1.0)
        with rate_limiter(log.debug, "an API call"):
            api_call()

    """

    def __init__(self, name, rate_limit):
        self._running = True
        self.name = name
        if not rate_limit:
            self.delta = 0.0
        else:
            self.delta = 1.0 / rate_limit
        self.last_ts = None
        self.lock = threading.Lock()

    def __call__(self, logmethod, msg):
        return RateLimitInstance(self, logmethod, msg)

    def __enter__(self):
        self._enter()

    def _enter(self):
        with self.lock:
            total_delay = 0.0
            if self.last_ts is None:
                self.last_ts = time.monotonic()
                return total_delay
            while True:
                now = time.monotonic()
                delta = now - self.last_ts
                if delta >= self.delta:
                    break
                delay = self.delta - delta
                time.sleep(delay)
                total_delay += delay
            self.last_ts = time.monotonic()
            return total_delay

    def __exit__(self, etype, value, tb):
        self._exit(etype, value, tb)

    def _exit(self, etype, value, tb):
        pass


class LazyExecutorTTLCache:
    """This is a lazy executor TTL cache.

    It's lazy because if it has cached data, it will always return it
    instantly.

    It's executor based, which means that if a cache miss occurs, it
    will submit a task to an executor to fetch new data.

    Finally, it's a TTL cache, which means it automatically expires data.

    Since it is only expected to be used when caching provider
    resource listing methods, it assumes there will only be one entry
    and ignores arguments -- it will return the same cached data no
    matter what arguments are supplied; but it will pass on those
    arguments to the underlying method in a cache miss.

    :param numeric ttl: The cache timeout in seconds.
    :param concurrent.futures.Executor executor: An executor to use to
        update data asynchronously in case of a cache miss.
    """

    def __init__(self, ttl, executor):
        self.ttl = ttl
        self.executor = executor
        # If we have an outstanding update being run by the executor,
        # this is the future.
        self.future = None
        # The last time the underlying method completed.
        self.last_time = None
        # The last value from the underlying method.
        self.last_value = None
        # A lock to make all of this thread safe (especially to ensure
        # we don't fire off multiple updates).
        self.lock = threading.Lock()

    def __call__(self, func):
        def decorator(*args, **kw):
            with self.lock:
                now = time.monotonic()
                if self.future and self.future.done():
                    # If a previous call spawned an update, resolve
                    # that now so we can use the data.
                    try:
                        self.last_time, self.last_value = self.future.result()
                    finally:
                        # Clear the future regardless so we don't loop.
                        self.future = None
                if (self.last_time is not None and
                    now - self.last_time < self.ttl):
                    # A cache hit.
                    return self.last_value
                # The rest of the method is a cache miss.
                if self.last_time is not None:
                    if not self.future:
                        # Fire off an asynchronous update request.
                        # This second wrapper ensures that we record
                        # the time that the update is complete along
                        # with the value.
                        def func_with_time():
                            ret = func(*args, **kw)
                            now = time.monotonic()
                            return (now, ret)
                        self.future = self.executor.submit(func_with_time)
                else:
                    # This is the first time this method has been
                    # called; since we don't have any cached data, we
                    # will synchronously update the data.
                    self.last_value = func(*args, **kw)
                    self.last_time = time.monotonic()
                return self.last_value
        return decorator


class Segment:
    def __init__(self, index, offset, data):
        self.index = index
        self.offset = offset
        self.data = data


class ImageUploader:
    """
    A helper class for drivers that upload large images in chunks.
    """

    # These values probably don't need to be changed
    error_retries = 3
    concurrency = 10

    # Subclasses must implement these
    segment_size = None

    def __init__(self, adapter, log, path, image_name, metadata):
        if self.segment_size is None:
            raise Exception("Subclass must set block size")
        self.adapter = adapter
        self.log = log
        self.path = path
        self.size = os.path.getsize(path)
        self.image_name = image_name
        self.metadata = metadata
        self.timeout = None

    def shouldRetryException(self, exception):
        return True

    def uploadSegment(self, segment):
        pass

    def startUpload(self):
        pass

    def finishUpload(self):
        pass

    def abortUpload(self):
        pass

    # Main API
    def upload(self, timeout=None):
        if timeout:
            self.timeout = time.monotonic() + timeout
        self.startUpload()
        try:
            with concurrent.futures.ThreadPoolExecutor(
                    max_workers=self.concurrency) as executor:
                with open(self.path, 'rb') as image_file:
                    self._uploadInner(executor, image_file)
            return self.finishUpload()
        except Exception:
            self.log.exception("Error uploading image:")
            self.abortUpload()

    # Subclasses can use this helper method for wrapping retryable calls
    def retry(self, func, *args, **kw):
        for x in range(self.error_retries):
            try:
                return func(*args, **kw)
            except Exception as e:
                if not self.shouldRetryException(e):
                    raise
                if x + 1 >= self.error_retries:
                    raise
                time.sleep(2 * x)

    def getTimeout(self):
        if self.timeout is None:
            return None
        return self.timeout - time.monotonic()

    def checkTimeout(self):
        if self.timeout is None:
            return
        if self.getTimeout() < 0:
            raise Exception("Timed out uploading image")

    # Internal methods
    def _uploadInner(self, executor, image_file):
        futures = set()
        for index, offset in enumerate(range(0, self.size, self.segment_size)):
            segment = Segment(index, offset,
                              image_file.read(self.segment_size))
            future = executor.submit(self.uploadSegment, segment)
            futures.add(future)
            # Keep the pool of workers supplied with data but without
            # reading the entire file into memory.
            if len(futures) >= (self.concurrency * 2):
                (done, futures) = concurrent.futures.wait(
                    futures,
                    timeout=self.getTimeout(),
                    return_when=concurrent.futures.FIRST_COMPLETED)
                for future in done:
                    future.result()
                # Only check the timeout after waiting (not every pass
                # through the loop)
                self.checkTimeout()
        # We're done reading the file, wait for all uploads to finish
        (done, futures) = concurrent.futures.wait(
            futures,
            timeout=self.getTimeout())
        for future in done:
            future.result()
        self.checkTimeout()
