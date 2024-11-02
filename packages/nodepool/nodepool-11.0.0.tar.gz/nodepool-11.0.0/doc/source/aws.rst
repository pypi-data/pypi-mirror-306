.. _aws-driver:

.. default-domain:: zuul

AWS Driver
----------

If using the AWS driver to upload diskimages, see `VM Import/Export
service role`_ for information on configuring the required permissions
in AWS.  You must also create an S3 Bucket for use by Nodepool if
uploading images (except when using the ebs-direct upload method).

Selecting the ``aws`` driver adds the following options to the
:attr:`providers` section of the configuration.

.. attr-overview::
   :prefix: providers.[aws]
   :maxdepth: 3

.. attr:: providers.[aws]
   :type: list

   An AWS provider's resources are partitioned into groups called `pool`
   (see :attr:`providers.[aws].pools` for details), and within a pool,
   the node types which are to be made available are listed
   (see :attr:`providers.[aws].pools.labels` for details).

   See `Boto Configuration`_ for information on how to configure credentials
   and other settings for AWS access in Nodepool's runtime environment.

   .. note:: For documentation purposes the option names are prefixed
             ``providers.[aws]`` to disambiguate from other
             drivers, but ``[aws]`` is not required in the
             configuration (e.g. below
             ``providers.[aws].pools`` refers to the ``pools``
             key in the ``providers`` section when the ``aws``
             driver is selected).

   Example:

   .. code-block:: yaml

     providers:
       - name: ec2-us-west-2
         driver: aws
         region-name: us-west-2
         cloud-images:
           - name: debian9
             image-id: ami-09c308526d9534717
             username: admin
         pools:
           - name: main
             max-servers: 5
             subnet-id: subnet-0123456789abcdef0
             security-group-id: sg-01234567890abcdef
             labels:
               - name: debian9
                 cloud-image: debian9
                 instance-type: t3.medium
                 iam-instance-profile:
                   arn: arn:aws:iam::123456789012:instance-profile/s3-read-only
                 key-name: zuul
                 tags:
                   key1: value1
               - name: debian9-large
                 cloud-image: debian9
                 instance-type: t3.large
                 key-name: zuul
                 use-spot: True
                 tags:
                   key1: value1
                   key2: value2

   .. attr:: name
      :required:

      A unique name for this provider configuration.

   .. attr:: region-name
      :required:

      Name of the `AWS region`_ to interact with.

   .. attr:: profile-name

      The AWS credentials profile to load for this provider. If unspecified the
      `boto3` library will select a profile.

      See `Boto Configuration`_ for more information.

   .. attr:: rate
      :type: float
      :default: 2.0

      The number of operations per second to perform against the provider.

   .. attr:: boot-timeout
      :type: int seconds
      :default: 180

      Once an instance is active, how long to try connecting to the
      image via SSH.  If the timeout is exceeded, the node launch is
      aborted and the instance deleted.

   .. attr:: launch-timeout
      :type: int seconds
      :default: 3600

      The time to wait from issuing the command to create a new instance
      until that instance is reported as "active".  If the timeout is
      exceeded, the node launch is aborted and the instance deleted.

   .. attr:: max-cores
      :type: int
      :default: unlimited

      Maximum number of cores usable from this provider's pools by default.

   .. attr:: max-servers
      :type: int
      :default: unlimited

      Maximum number of servers spawnable from this provider's pools by default.

   .. attr:: max-ram
      :type: int
      :default: unlimited

      Maximum RAM usable from this provider's pools by default.

   .. attr:: max-resources
      :type: dict
      :default: unlimited

      A dictionary of other quota resource limits.  AWS has quotas
      for certain instance types.  These may be specified here to
      limit Nodepool's usage.

      The following example limits the number of high-memory
      instance cores:

      .. code-block:: yaml

         max-resources:
           'L-43DA4232': 448

      See `instance quotas`_ for more information.

   .. attr:: launch-retries
      :default: 3

      The number of times to retry launching a node before considering
      the request failed.

   .. attr:: post-upload-hook
      :type: string
      :default: None

      Filename of an optional script that can be called after an image has
      been uploaded to a provider but before it is taken into use. This is
      useful to perform last minute validation tests before an image is
      really used for build nodes. The script will be called as follows:

      ``<SCRIPT> <PROVIDER> <EXTERNAL_IMAGE_ID> <LOCAL_IMAGE_FILENAME>``

      If the script returns with result code 0 it is treated as successful
      otherwise it is treated as failed and the image gets deleted.

   .. attr:: object-storage

      This section is only required when using Nodepool to upload
      diskimages.

      .. attr:: bucket-name

         The name of a bucket to use for temporary storage of
         diskimages while creating snapshots.  The bucket must already
         exist.

   .. attr:: image-format
      :type: str
      :default: raw

      The image format that should be requested from diskimage-builder
      and also specified to AWS when importing images.  One of:
      ``ova``, ``vhd``, ``vhdx``, ``vmdk``, ``raw`` (not all of which
      are supported by diskimage-builder).

   .. attr:: image-import-timeout
      :type: int

      Generally there is no limit on the amount of time a successful
      image import can take.  However, some import tasks may encounter
      temporary resource limitations from AWS.  In these cases, if
      this value is set, Nodepool will retry the import tasks until
      the timeout is reached.  If this is unset (the default), then
      the first resource limitation detected will result in an error.
      The value is in seconds.

   .. attr:: cloud-images
      :type: list

      Each entry in this section must refer to an entry in the
      :attr:`labels` section.

      .. code-block:: yaml

         cloud-images:
           - name: ubuntu1804
             image-id: ami-082fd9a18128c9e8c
             username: ubuntu
           - name: ubuntu1804-by-filters
             image-filters:
               - name: name
                 values:
                  - named-ami
             username: ubuntu
           - name: my-custom-win2k3
             connection-type: winrm
             username: admin

      Each entry is a dictionary with the following keys

      .. attr:: name
         :type: string
         :required:

         Identifier to refer this cloud-image from :attr:`providers.[aws].pools.labels` section.
         Since this name appears elsewhere in the nodepool configuration file,
         you may want to use your own descriptive name here and use
         ``image-id`` to specify the cloud image so that if
         the image id changes on the cloud, the impact to your Nodepool
         configuration will be minimal. However, if ``image-id`` is not
         provided, this is assumed to be the image id in the cloud.

      .. attr:: image-id
         :type: str

         If this is provided, it is used to select the image from the
         cloud provider by ID.  Either this field or
         :attr:`providers.[aws].cloud-images.image-filters` must be
         provided.

      .. attr:: image-filters
         :type: list

         If provided, this is used to select an AMI by filters.  If
         the filters provided match more than one image, the most
         recent will be returned.  Either this field or
         :attr:`providers.[aws].cloud-images.image-id` must be
         provided.

         Each entry is a dictionary with the following keys

         .. attr:: name
            :type: str
            :required:

            The filter name. See `Boto describe images`_ for a list of valid filters.

         .. attr:: values
            :type: list
            :required:

            A list of string values on which to filter.

      .. attr:: username
         :type: str

         The username that a consumer should use when connecting to the node.

      .. attr:: python-path
         :type: str
         :default: auto

         The path of the default python interpreter.  Used by Zuul to set
         ``ansible_python_interpreter``.  The special value ``auto`` will
         direct Zuul to use inbuilt Ansible logic to select the
         interpreter on Ansible >=2.8, and default to
         ``/usr/bin/python2`` for earlier versions.

      .. attr:: connection-type
         :type: str

         The connection type that a consumer should use when connecting to the
         node. For most images this is not necessary. However when creating
         Windows images this could be 'winrm' to enable access via ansible.

      .. attr:: connection-port
         :type: int
         :default: 22/ 5986

         The port that a consumer should use when connecting to the node. For
         most diskimages this is not necessary. This defaults to 22 for ssh and
         5986 for winrm.

      .. attr:: shell-type
         :type: str
         :default: sh

         The shell type of the node's default shell executable. Used by Zuul
         to set ``ansible_shell_type``. This setting should only be used

         - For a windows image with the experimental `connection-type` ``ssh``
           in which case ``cmd`` or ``powershell`` should be set
           and reflect the node's ``DefaultShell`` configuration.
         - If the default shell is not Bourne compatible (sh), but instead
           e.g. ``csh`` or ``fish``, and the user is aware that there is a
           long-standing issue with ``ansible_shell_type`` in combination
           with ``become``.

   .. attr:: diskimages
      :type: list

      Each entry in a provider's `diskimages` section must correspond
      to an entry in :attr:`diskimages`.  Such an entry indicates that
      the corresponding diskimage should be uploaded for use in this
      provider.  Additionally, any nodes that are created using the
      uploaded image will have the associated attributes (such as
      flavor or metadata).

      If an image is removed from this section, any previously uploaded
      images will be deleted from the provider.

      .. code-block:: yaml

         diskimages:
           - name: bionic
             pause: False
           - name: windows
             connection-type: winrm
             connection-port: 5986


      Each entry is a dictionary with the following keys

      .. attr:: name
         :type: string
         :required:

         Identifier to refer this image from
         :attr:`providers.[aws].pools.labels` and
         :attr:`diskimages` sections.

      .. attr:: pause
         :type: bool
         :default: False

         When set to True, nodepool-builder will not upload the image
         to the provider.

      .. attr:: username
         :type: str

         The username that should be used when connecting to the node.

         .. warning:: This option is deprecated.  Specify the username
                      on the diskimage definition itself instead.

      .. attr:: connection-type
         :type: string

         The connection type that a consumer should use when connecting
         to the node. For most diskimages this is not
         necessary. However when creating Windows images this could be
         ``winrm`` to enable access via ansible.

      .. attr:: connection-port
         :type: int
         :default: 22 / 5986

         The port that a consumer should use when connecting to the
         node. For most diskimages this is not necessary. This defaults
         to 22 for ssh and 5986 for winrm.

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

         - For a windows image with the experimental `connection-type` ``ssh``
           in which case ``cmd`` or ``powershell`` should be set
           and reflect the node's ``DefaultShell`` configuration.
         - If the default shell is not Bourne compatible (sh), but instead
           e.g. ``csh`` or ``fish``, and the user is aware that there is a
           long-standing issue with ``ansible_shell_type`` in combination
           with ``become``.

      .. attr:: architecture
         :type: str
         :default: x86_64

         The architecture of the image.  See the `AWS RegisterImage API
         documentation`_ for valid values.

      .. attr:: ena-support
         :type: bool
         :default: True

         Whether the image has support for the AWS Enhanced Networking
         Adapter (ENA).  Many newer operating systems include driver
         support as standard and some AWS instance types require it.

      .. attr:: volume-type
         :type: str
         :default: gp3

         The root `EBS volume type`_ for the image.
         Only used with the
         :value:`providers.[aws].diskimages.import-method.snapshot` or
         :value:`providers.[aws].diskimages.import-method.ebs-direct`
         import methods.

      .. attr:: volume-size
         :type: int

         The size of the root EBS volume, in GiB, for the image.  If
         omitted, the volume size reported for the imported snapshot
         will be used.  Only used with the
         :value:`providers.[aws].diskimages.import-method.snapshot` or
         :value:`providers.[aws].diskimages.import-method.ebs-direct`
         import methods.

      .. attr:: imds-support
         :type: str

         To enforce usage of IMDSv2 by default on instances created
         from the image, set this value to `v2.0`.  If omitted, IMDSv2
         is optional by default.  This is only supported using the
         :value:`providers.[aws].diskimages.import-method.snapshot` or
         :value:`providers.[aws].diskimages.import-method.ebs-direct`
         import methods.

      .. attr:: import-method
         :default: snapshot

         The method to use when importing the image.

         .. value:: snapshot

            This method uploads the image file to AWS as a snapshot
            and then registers an AMI directly from the snapshot.
            This is faster compared to the `image` method and may be
            used with operating systems and versions that AWS does not
            otherwise support.  However, it is incompatible with some
            operating systems which require special licensing or other
            metadata in AWS.

         .. value:: ebs-direct

            This is similar to the `snapshot` method, but uses the
            `EBS direct API`_ instead of S3.  This may be faster and
            more efficient, but it may incur additional costs.

         .. value:: image

            This method uploads the image file to AWS and performs an
            "image import" on the file.  This causes AWS to boot the
            image in a temporary VM and then take a snapshot of that
            VM which is then used as the basis of the AMI.  This is
            slower compared to the `snapshot` method and may only be
            used with operating systems and versions which AWS already
            supports.  This may be necessary in order to use Windows
            images.

      .. attr:: iops
         :type: int

         The number of I/O operations per second to be provisioned for
         the volume.  The default varies based on the volume type; see
         the documentation under `EBS volume type`_ for the specific
         volume type for details.

      .. attr:: throughput
         :type: int

         The throughput of the volume in MiB/s.  This is only valid for
         ``gp3`` volumes.

      .. attr:: tags
         :type: dict
         :default: None

         A dictionary of tags to add to uploaded images.  This will be
         merged with any existing metadata from the global `diskimage`
         configuration for this image.  Avoid the use of `nodepool_`
         as a key prefix since Nodepool uses this for internal values.

   .. attr:: pools
      :type: list

      A pool defines a group of resources from an AWS provider. Each pool has a
      maximum number of nodes which can be launched from it, along with a number
      of cloud-related attributes used when launching nodes.

      .. attr:: name
         :required:

         A unique name within the provider for this pool of resources.

      .. attr:: availability-zone
         :type: str

         If provided, instances launched from this pool will be
         assigned to the specified availibility zone.  If omitted, AWS
         will select from the available zones.

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

         Maximum number of cores usable from this pool.  Defaults to
         :attr:`providers.[aws].max-cores`.

      .. attr:: max-servers
         :type: int

         Maximum number of servers spawnable from this pool.  Defaults to
         :attr:`providers.[aws].max-servers`.

      .. attr:: max-ram
         :type: int

         Maximum RAM usable from this pool.  Defaults to
         :attr:`providers.[aws].max-ram`.

      .. attr:: max-resources
         :type: dict

         A dictionary of other quota resource limits.  AWS has quotas
         for certain instance types.  These may be specified here to
         limit Nodepool's usage.  Defaults to
         :attr:`providers.[aws].max-resources`.

         The following example limits the number of high-memory
         instance cores:

         .. code-block:: yaml

            max-resources:
              'L-43DA4232': 448

         See `instance quotas`_ for more information.

      .. attr:: subnet-id

         If provided, specifies the subnet to assign to the primary network
         interface of nodes.

      .. attr:: security-group-id

         If provided, specifies the security group ID to assign to the primary
         network interface of nodes.

      .. attr:: public-ip-address
         :type: bool
         :default: True

         Deprecated alias for :attr:`providers.[aws].pools.public-ipv4`.

      .. attr:: public-ipv4
         :type: bool
         :default: True

         Specify if a public IPv4 address shall be attached to nodes.

      .. attr:: public-ipv6
         :type: bool
         :default: True

         Specify if a public IPv6 address shall be attached to nodes.

      .. attr:: use-internal-ip
         :type: bool
         :default: false

         If a public IP is attached but Nodepool should prefer the
         private IP, set this to true.

      .. attr:: host-key-checking
         :type: bool
         :default: True

         Whether to validate SSH host keys.  When true, this helps ensure
         that nodes are ready to receive SSH connections before they are
         supplied to the requestor.  When set to false, nodepool-launcher
         will not attempt to ssh-keyscan nodes after they are booted.
         Disable this if nodepool-launcher and the nodes it launches are
         on different networks, where the launcher is unable to reach the
         nodes directly, or when using Nodepool with non-SSH node
         platforms.  The default value is true.

      .. attr:: labels
         :type: list

         Each entry in a pool's `labels` section indicates that the
         corresponding label is available for use in this pool.  When creating
         nodes for a label, the flavor-related attributes in that label's
         section will be used.

         .. code-block:: yaml

            labels:
              - name: bionic
                instance-type: m5a.large

         Each entry is a dictionary with the following keys

           .. attr:: name
              :type: str
              :required:

              Identifier to refer to this label.

           .. attr:: cloud-image
              :type: str
              :required:

              Refers to the name of an externally managed image in the
              cloud that already exists on the provider. The value of
              ``cloud-image`` should match the ``name`` of a
              previously configured entry from the ``cloud-images``
              section of the provider. See
              :attr:`providers.[aws].cloud-images`.  Mutually
              exclusive with
              :attr:`providers.[aws].pools.labels.diskimage`

           .. attr:: diskimage
              :type: str
              :required:

              Refers to provider's diskimages, see
              :attr:`providers.[aws].diskimages`.  Mutually exclusive
              with :attr:`providers.[aws].pools.labels.cloud-image`

           .. attr:: dedicated-host
              :type: bool

              If set to ``true``, an AWS dedicated host will be
              allocated for the instance.  Nodepool only supports
              running a single instance on dedicated hosts, so it will
              treat the host and the instance launched on it as a
              matched pair.  The host will not be used for any other
              instances, and will be released when the associated
              Nodepool node is deleted.

              If this option is set, the
              :attr:`providers.[aws].pools.labels.use-spot` option is
              not available, and
              :attr:`providers.[aws].pools.availability-zone`
              option is required.

           .. attr:: ebs-optimized
              :type: bool
              :default: False

              Indicates whether EBS optimization
              (additional, dedicated throughput between Amazon EC2 and Amazon EBS,)
              has been enabled for the instance.

           .. attr:: instance-type
              :type: str

              Name of the flavor to use.
              Mutually exclusive with :attr:`providers.[aws].pools.labels.fleet`

           .. attr:: fleet
              :type: dict

              If specified, EC2 fleet API would be used for launching
              the instance.  In this case, quota is not checked before
              launching the instance, but is taken into account after
              the instance is launched.  Mutually exclusive with
              :attr:`providers.[aws].pools.labels.instance-type`

              .. attr:: instance-types
                 :type: list

                 Names of the flavors of the instance that to be launched.

              .. attr:: allocation-strategy
                 :type: str
                 :required:

                 Allowed values for on On-Demand: ``lowest-price`` or ``prioritized``.
                 Allowed values for Spot: ``price-capacity-optimized``, ``capacity-optimized``,
                 ``diversified`` or ``lowest-price``

           .. attr:: iam-instance-profile
              :type: dict

              Used to attach an iam instance profile.
              Useful for giving access to services without needing any secrets.

              .. attr:: name

                 Name of the instance profile.
                 Mutually exclusive with :attr:`providers.[aws].pools.labels.iam-instance-profile.arn`

              .. attr:: arn

                 ARN identifier of the profile.
                 Mutually exclusive with :attr:`providers.[aws].pools.labels.iam-instance-profile.name`

           .. attr:: imdsv2
              :type: str

              Specify whether IMDSv2 is required.  If this is omitted,
              then AWS defaults are used (usually equivalent to
              `optional` but may be influenced by the image used).

              .. value:: optional

                 Allows usage of IMDSv2 but do not require it.  This
                 sets the following metadata options:

                 * `HttpTokens` is `optional`
                 * `HttpEndpoint` is `enabled`

              .. value:: required

                 Require IMDSv2.  This sets the following metadata
                 options:

                 * `HttpTokens` is `required`
                 * `HttpEndpoint` is `enabled`

           .. attr:: key-name
              :type: string
              :required:

              The name of a keypair that will be used when
              booting each server.

           .. attr:: volume-type
              :type: string

              If given, the root `EBS volume type`_

           .. attr:: volume-size
              :type: int

              If given, the size of the root EBS volume, in GiB.

           .. attr:: iops
              :type: int

              The number of I/O operations per second to be
              provisioned for the volume.  The default varies based on
              the volume type; see the documentation under `EBS volume
              type`_ for the specific volume type for details.

           .. attr:: throughput
              :type: int

              The throughput of the volume in MiB/s.  This is only
              valid for ``gp3`` volumes.

           .. attr:: userdata
              :type: str
              :default: None

              A string of userdata for a node. Example usage is to install
              cloud-init package on image which will apply the userdata.
              Additional info about options in cloud-config:
              https://cloudinit.readthedocs.io/en/latest/topics/examples.html

           .. attr:: tags
              :type: dict
              :default: None

              A dictionary of tags to add to the EC2 instances.
              Values must be supplied as strings.

           .. attr:: dynamic-tags
              :type: dict
              :default: None

              Similar to
              :attr:`providers.[aws].pools.labels.tags`,
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
                   - name: precise
                     dynamic-tags:
                       request_info: "Created for request {request.id}"

           .. attr:: use-spot
              :type: bool
              :default: False

              When set to True, Nodepool will try to launch an Amazon EC2 Spot
              instance, instead of an On-Demand instance. Spot instances let
              you take advantage of unused EC2 capacity at a discount.

              For example:

              .. code-block:: yaml

                 labels:
                   - name: frugal
                     use-spot: True

              .. note:: As Amazon EC2 Spot instances take advantage of unused
                        EC2 capacity, you may not get an instance, if demand
                        is high. In addition, Amazon EC2 may interrupt your
                        Spot instance and reclaim it with a two minutes warning
                        upfront. Therefore, you might want to setup alternative
                        nodesets as fallback.


.. _`EBS volume type`: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EBSVolumeTypes.html
.. _`AWS region`: https://docs.aws.amazon.com/general/latest/gr/rande.html
.. _`Boto configuration`: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html
.. _`Boto describe images`: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_images
.. _`VM Import/Export service role`: https://docs.aws.amazon.com/vm-import/latest/userguide/vmie_prereqs.html#vmimport-role
.. _`instance quotas`: https://us-west-1.console.aws.amazon.com/servicequotas/home/services/ec2/quotas
.. _`AWS RegisterImage API documentation`: https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_RegisterImage.html
.. _`EBS direct API`: https://docs.aws.amazon.com/ebs/latest/userguide/ebs-accessing-snapshot.html
