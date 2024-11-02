.. _kubernetes-driver:

.. default-domain:: zuul

Kubernetes Driver
-----------------

Selecting the kubernetes driver adds the following options to the
:attr:`providers` section of the configuration.

.. attr-overview::
   :prefix: providers.[kubernetes]
   :maxdepth: 3

.. attr:: providers.[kubernetes]
   :type: list

   A Kubernetes provider's resources are partitioned into groups
   called `pools` (see :attr:`providers.[kubernetes].pools` for
   details), and within a pool, the node types which are to be made
   available are listed (see :attr:`providers.[kubernetes].pools.labels` for
   details).

   .. note:: For documentation purposes the option names are prefixed
             ``providers.[kubernetes]`` to disambiguate from other
             drivers, but ``[kubernetes]`` is not required in the
             configuration (e.g. below
             ``providers.[kubernetes].pools`` refers to the ``pools``
             key in the ``providers`` section when the ``kubernetes``
             driver is selected).

   Example:

   .. code-block:: yaml

     providers:
       - name: kubespray
         driver: kubernetes
         context: admin-cluster.local
         pools:
           - name: main
             labels:
               - name: kubernetes-namespace
                 type: namespace
               - name: pod-fedora
                 type: pod
                 image: docker.io/fedora:28


   .. attr:: context

      Name of the context configured in ``kube/config``.

      Before using the driver, Nodepool either needs a ``kube/config``
      file installed with a cluster admin context, in which case this
      setting is required, or if Nodepool is running inside
      Kubernetes, this setting and the ``kube/config`` file may be
      omitted and Nodepool will use a service account loaded from the
      in-cluster configuration path.

   .. attr:: launch-retries
      :default: 3

      The number of times to retry launching a node before considering
      the job failed.

   .. attr:: max-cores
      :type: int
      :default: unlimited

      Maximum number of cores usable from this provider's pools by
      default. This can be used to limit usage of the kubernetes
      backend. If not defined nodepool can use all cores up to the
      limit of the backend.

   .. attr:: max-servers
      :type: int
      :default: unlimited

      Maximum number of pods spawnable from this provider's pools by
      default. This can be used to limit the number of pods. If not
      defined nodepool can create as many servers the kubernetes
      backend allows.

   .. attr:: max-ram
      :type: int
      :default: unlimited

      Maximum ram usable from this provider's pools by default. This
      can be used to limit the amount of ram allocated by nodepool. If
      not defined nodepool can use as much ram as the kubernetes
      backend allows.

   .. attr:: max-resources
      :type: dict
      :default: unlimited

      A dictionary of other quota resource limits applicable to this
      provider's pools by default.  Arbitrary limits may be supplied
      with the
      :attr:`providers.[kubernetes].pools.labels.extra-resources`
      attribute.

   .. attr:: pools
      :type: list

      A pool defines a group of resources from a Kubernetes
      provider.

      .. attr:: name
         :required:

         Namespaces are prefixed with the pool's name.

      .. attr:: priority
         :type: int
         :default: 100

         The priority of this provider pool (a lesser number is a higher
         priority).  Nodepool launchers will yield requests to other
         provider pools with a higher priority as long as they are not
         paused.  This means that in general, higher priority pools will
         reach quota first before lower priority pools begin to be used.

         This setting may be specified at the provider level in order
         to apply to all pools within that provider, or it can be
         overridden here for a specific pool.

      .. attr:: node-attributes
         :type: dict

         A dictionary of key-value pairs that will be stored with the node data
         in ZooKeeper. The keys and values can be any arbitrary string.

      .. attr:: max-cores
         :type: int

         Maximum number of cores usable from this pool. This can be used
         to limit usage of the kubernetes backend. If not defined nodepool can
         use all cores up to the limit of the backend.

      .. attr:: max-servers
         :type: int

         Maximum number of pods spawnable from this pool. This can
         be used to limit the number of pods. If not defined
         nodepool can create as many servers the kubernetes backend allows.

      .. attr:: max-ram
         :type: int

         Maximum ram usable from this pool. This can be used to limit
         the amount of ram allocated by nodepool. If not defined
         nodepool can use as much ram as the kubernetes backend allows.

      .. attr:: max-resources
         :type: dict
         :default: unlimited

         A dictionary of other quota resource limits applicable to
         this pool.  Arbitrary limits may be supplied with the
         :attr:`providers.[kubernetes].pools.labels.extra-resources` attribute.

      .. attr:: default-label-cpu
         :type: int

         Only used by the
         :value:`providers.[kubernetes].pools.labels.type.pod` label type;
         specifies specifies a default value for
         :attr:`providers.[kubernetes].pools.labels.cpu` for all labels of
         this pool that do not set their own value.

      .. attr:: default-label-memory
         :type: int

         Only used by the
         :value:`providers.[kubernetes].pools.labels.type.pod` label type;
         specifies a default value in MiB for
         :attr:`providers.[kubernetes].pools.labels.memory` for all labels of
         this pool that do not set their own value.

      .. attr:: default-label-storage
         :type: int

         Only used by the
         :value:`providers.[kubernetes].pools.labels.type.pod` label type;
         specifies a default value in MB for
         :attr:`providers.[kubernetes].pools.labels.storage` for all labels of
         this pool that do not set their own value.

      .. attr:: default-label-extra-resources
         :type: dict

         Only used by the
         :value:`providers.[kubernetes].pools.labels.type.pod` label type;
         specifies default values for
         :attr:`providers.[kubernetes].pools.labels.extra-resources` for all labels of
         this pool that do not set their own value.

      .. attr:: default-label-cpu-limit
         :type: int

         Only used by the
         :value:`providers.[kubernetes].pools.labels.type.pod` label type;
         specifies specifies a default value for
         :attr:`providers.[kubernetes].pools.labels.cpu-limit` for all labels of
         this pool that do not set their own value.

      .. attr:: default-label-memory-limit
         :type: int

         Only used by the
         :value:`providers.[kubernetes].pools.labels.type.pod` label type;
         specifies a default value in MiB for
         :attr:`providers.[kubernetes].pools.labels.memory-limit` for all labels of
         this pool that do not set their own value.

      .. attr:: default-label-storage-limit
         :type: int

         Only used by the
         :value:`providers.[kubernetes].pools.labels.type.pod` label type;
         specifies a default value in MB for
         :attr:`providers.[kubernetes].pools.labels.storage-limit` for all labels of
         this pool that do not set their own value.

      .. attr:: labels
         :type: list

         Each entry in a pool`s `labels` section indicates that the
         corresponding label is available for use in this pool.

         Each entry is a dictionary with the following keys

         .. attr:: name
            :required:

            Identifier for this label; references an entry in the
            :attr:`labels` section.

         .. attr:: type

            The Kubernetes provider supports two types of labels:

            .. value:: namespace

               Namespace labels provide an empty namespace configured
               with a service account that can create pods, services,
               configmaps, etc.

            .. value:: pod

               Pod labels provide a dedicated namespace with a single pod
               created using the
               :attr:`providers.[kubernetes].pools.labels.image` parameter and it
               is configured with a service account that can exec and get
               the logs of the pod.

         .. attr:: image

            Only used by the
            :value:`providers.[kubernetes].pools.labels.type.pod` label type;
            specifies the image name used by the pod.

         .. attr:: image-pull
            :default: IfNotPresent
            :type: str

            The ImagePullPolicy, can be IfNotPresent, Always or Never.

         .. attr:: labels
            :type: dict

            A dictionary of additional values to be added to the
            namespace or pod metadata.  The value of this field is
            added to the `metadata.labels` field in Kubernetes.  Note
            that this field contains arbitrary key/value pairs and is
            unrelated to the concept of labels in Nodepool.

         .. attr:: dynamic-labels
            :type: dict
            :default: None

            Similar to
            :attr:`providers.[kubernetes].pools.labels.labels`,
            but is interpreted as a format string with the following
            values available:

            * request: Information about the request which prompted the
              creation of this node (note that the node may ultimately
              be used for a different request and in that case this
              information will not be updated).

              * id: The request ID.

              * labels: The list of labels in the request.

              * requestor: The name of the requestor.

              * requestor_data: Key/value information from the requestor.

              * relative_priority: The relative priority of the request.

              * event_id: The external event ID of the request.

              * created_time: The creation time of the request.

              * tenant_name: The name of the tenant associated with the
                request.

            For example:

            .. code-block:: yaml

               labels:
                 - name: pod-fedora
                   dynamic-labels:
                     request_info: "{request.id}"

         .. attr:: annotations
            :type: dict

            A dictionary of additional values to be added to the
            pod metadata.  The value of this field is
            added to the `metadata.annotations` field in Kubernetes.
            This field contains arbitrary key/value pairs that can be accessed
            by tools and libraries. E.g custom schedulers can make use of this
            metadata.

         .. attr:: python-path
            :type: str
            :default: auto

            The path of the default python interpreter.  Used by Zuul to set
            ``ansible_python_interpreter``.  The special value ``auto`` will
            direct Zuul to use inbuilt Ansible logic to select the
            interpreter on Ansible >=2.8, and default to
            ``/usr/bin/python2`` for earlier versions.

         .. attr:: shell-type
            :type: str
            :default: sh

            The shell type of the node's default shell executable. Used by Zuul
            to set ``ansible_shell_type``. This setting should only be used

            - For a windows pod with the experimental `connection-type`
              ``ssh``, in which case ``cmd`` or ``powershell`` should be set
              and reflect the node's ``DefaultShell`` configuration.
            - If the default shell is not Bourne compatible (sh), but instead
              e.g. ``csh`` or ``fish``, and the user is aware that there is a
              long-standing issue with ``ansible_shell_type`` in combination
              with ``become``

         .. attr:: cpu
            :type: int

            Only used by the
            :value:`providers.[kubernetes].pools.labels.type.pod`
            label type; specifies the number of cpu to request for the
            pod.  If no limit is specified, this will also be used as
            the limit.

         .. attr:: memory
            :type: int

            Only used by the
            :value:`providers.[kubernetes].pools.labels.type.pod`
            label type; specifies the amount of memory in MiB to
            request for the pod.  If no limit is specified, this will
            also be used as the limit.

         .. attr:: storage
            :type: int

            Only used by the
            :value:`providers.[kubernetes].pools.labels.type.pod`
            label type; specifies the amount of ephemeral-storage in
            MB to request for the pod.  If no limit is specified, this
            will also be used as the limit.

         .. attr:: extra-resources
            :type: dict

            Only used by the
            :value:`providers.[kubernetes].pools.labels.type.pod`
            label type; specifies any extra resources that Nodepool
            should consider in its quota calculation other than the
            resources described above (cpu, memory, storage).

         .. attr:: cpu-limit
            :type: int

            Only used by the
            :value:`providers.[kubernetes].pools.labels.type.pod`
            label type; specifies the cpu limit for the pod.

         .. attr:: memory-limit
            :type: int

            Only used by the
            :value:`providers.[kubernetes].pools.labels.type.pod`
            label type; specifies the memory limit in MiB for the pod.

         .. attr:: storage-limit
            :type: int

            Only used by the
            :value:`providers.[kubernetes].pools.labels.type.pod`
            label type; specifies the ephemeral-storage limit in
            MB for the pod.

         .. attr:: gpu
            :type: float

            Only used by the
            :value:`providers.[kubernetes].pools.labels.type.pod`
            label type; specifies the amount of gpu allocated to the pod.
            This will be used to set both requests and limits to the same
            value, based on how kubernetes assigns gpu resources:
            https://kubernetes.io/docs/tasks/manage-gpus/scheduling-gpus/.

         .. attr:: gpu-resource
            :type: str

            Only used by the
            :value:`providers.[kubernetes].pools.labels.type.pod`
            label type; specifies the custom schedulable resource
            associated with the installed gpu that is available
            in the cluster.

         .. attr:: env
            :type: list
            :default: []

            Only used by the
            :value:`providers.[kubernetes].pools.labels.type.pod` label type;
            A list of environment variables to pass to the Pod.

            .. attr:: name
               :type: str
               :required:

               The name of the environment variable passed to the Pod.

            .. attr:: value
               :type: str
               :required:

               The value of the environment variable passed to the Pod.

         .. attr:: node-selector
            :type: dict

            Only used by the
            :value:`providers.[kubernetes].pools.labels.type.pod` label type;
            A map of key-value pairs to ensure the Kubernetes scheduler
            places the Pod on a node with specific node labels.

         .. attr:: scheduler-name
            :type: str

            Only used by the
            :value:`providers.[kubernetes].pools.labels.type.pod`
            label type.  Sets the `schedulerName` field on the
            container.  Normally left unset for the Kubernetes
            default.

         .. attr:: privileged
            :type: bool

            Only used by the
            :value:`providers.[kubernetes].pools.labels.type.pod`
            label type.  Sets the `securityContext.privileged` flag on
            the container.  Normally left unset for the Kubernetes default.

         .. attr:: volumes
            :type: list

            Only used by the
            :value:`providers.[kubernetes].pools.labels.type.pod`
            label type.  Sets the `volumes` field on the pod.  If
            supplied, this should be a list of Kubernetes Pod Volume
            definitions.

         .. attr:: volume-mounts
            :type: list

            Only used by the
            :value:`providers.[kubernetes].pools.labels.type.pod`
            label type.  Sets the `volumeMounts` flag on the
            container.  If supplied, this should be a list of
            Kubernetes Container VolumeMount definitions.

         .. attr:: spec
            :type: dict

            This attribute is exclusive with all other label
            attributes except
            :attr:`providers.[kubernetes].pools.labels.name`,
            :attr:`providers.[kubernetes].pools.labels.type`,
            :attr:`providers.[kubernetes].pools.labels.annotations`,
            :attr:`providers.[kubernetes].pools.labels.labels` and
            :attr:`providers.[kubernetes].pools.labels.dynamic-labels`.
            If a `spec` is provided, then Nodepool will supply the
            contents of this value verbatim to Kubernetes as the
            ``spec`` attribute of the Kubernetes ``Pod`` definition.
            No other Nodepool attributes are used, including any
            default values set at the provider level (such as
            `default-label-cpu` and similar).

            This attribute allows for the creation of arbitrary
            complex pod definitions but the user is responsible for
            ensuring that they are suitable.  The first container in
            the pod is expected to be a long-running container that
            hosts a shell environment for running commands.  The
            following minimal definition matches what Nodepool itself
            normally creates and is recommended as a starting point:

            .. code-block:: yaml

               labels:
                 - name: custom-pod
                   type: pod
                   spec:
                     containers:
                       - name: custom-pod
                         image: ubuntu:jammy
                         imagePullPolicy: IfNotPresent
                         command: ["/bin/sh", "-c"]
                         args: ["while true; do sleep 30; done;"]
