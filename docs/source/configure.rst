Configuration
======================================================================

cloudmesh comes with a set of convenient configuration files in the
yaml format. Important is that you make sure that prior to saving the
file, that the indentation is correct and that all tabs are replaced
with spaces.  Cloudmesh comes with two configuration files. One
dedicated to interact as regular user. The other one allows you to
interact with the backend system. In general it is sufficient to have
just a cloudmesh.yaml file so you run cloudmesh in user mode.


cloudmesh.yaml
----------------------------------------------------------------------

Next we will present the outline of the::

   cloudmesh.yaml 

file which looks like::

  cloudmesh:
    active: 
    - sierra_openstack_grizzly
    clouds:
      sierra_openstack_grizzly:
        cm_heading: Sierra OpenStack, Grizzly
        cm_host: sierra.futuregrid.org
        cm_label: sos
        cm_type: openstack
        cm_type_version: grizzly
        credentials:
          OS_AUTH_URL: https://s77r.idp.sdsc.futuregrid.org:5000/v2.0
          OS_CACERT: $HOME/.cloudmesh/sierra-cacert.pem
          OS_PASSWORD: jhdjaTYWUIYBY
          OS_TENANT_NAME: fg1000
          OS_USERNAME: albert
          OS_VERSION: grizzly
        default:
          flavor: m1.tiny
          image: 4199d988-0833-4497-a473-96fc456fac2f

The file begins with the keyword cloudmesh and has all further
information indented under it. An active: attribute allows you to
specify clouds that you would like to use. This enables you to select
from a large list of predefined clouds that may be given to you as
template in a cloudmesh.yaml file those clouds you like to actually
use. In our initial example we provide you with just one active cloud
called. Hence you see under active: ::

  active:
  - sierra_openstack_grizzly

If there are more than one cloud you would simply add the label of
that cloud to the lit of active clouds such as ::

  active:
  - sierra_openstack_grizzly
  - india_openstack_havana

Next, we need to define several attributes for the active clouds. This
must be done carefully and you need to possibly check with your
cloudprovider for the information that is filled in as part of a
credential section. As we need to identify a cloud we use the same
identifier that we used in the active cloud. This identifier is rather
arbitrary, but from experience we use on FutureGrid the nameing scheme
machinename_cloudtype_cloudversion. But one can naturally chose any
name that follows the yaml conventions. Pleas eonly use characters in
[A-Za-z0-9_]. Do not us a minus sign but use an underscor instead in
any attribute name to avoid issues.

Cloudmesh uses a number of convenient attributes that are starting
with "cm_". These include

:cm_heading:
  Specifies a heading for the cloud that is used in several user
  interfaces when refering to this cloud
  
  Example: Sierra OpenStack, Grizzly

:cm_host:
  Specifies the hostname of the cloud that is used in some cases to
  connect to it.  In many cases this value is not needed.
  
  Example: sierra.futuregrid.org

:cm_label:
  Specifies a simple very short abbreviation of the cloud that can be
  used with the commandline tools. Often it is inconvenient so specify
  for example sierra_openstack_grizzly. instead a user can specify an
  arbitrary label for that cloud such as sierra, or in our case we
  used sos.
  
  Example: sos

:cm_type:
  The type of a cloud is very important as it will deterimine how we
  interact with it

  Example: openstack

:cm_type_version:
  Besides the type we can have also a number of versions that
  specifies how we interact with the cloud.

  Example: havana

Configuration file (rc file)
----------------------------------------------------------------------


In most IaaS platforms, configuration files (in the form of an "rc
file") are provided as credentials. These credentials should be
imported in cloudmesh.yaml.


Retrieval of rc file by command
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

   ./install gatherrc

This will create for you in your $HOME/.cloudmesh directory a tree of the
following format::
   
   .cloudmesh/clouds
        india_openstack_havana
	sierra_openstack_grizzly

In future we will also have the following directories::

        hotel_openstack_ ...
	alamo_openstack_ ...

At this time the credentials from hotel and alamo are not
automatically retrieved, you need to get them in the following way and
fill them into the cloudmesh.yaml file:

* TBD

Retrieval of rc files by Hand
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ 

Location of rc files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

========= ================================== ====================================================
Host      OpenStack (novarc)                 Eucalyptus (eucarc)
--------- ---------------------------------- ----------------------------------------------------
india     $HOME/.cloudmesh/openstack/novarc $HOME/.cloudmesh/eucalyptus/$fgprojectnumber/eucarc*
sierra    $HOME/.cloudmesh/novarc           $HOME/.cloudmesh/eucalyptus/$fgprojectnumber/eucarc*
hotel     Download EC2 Credentials**         n/a
alamo     Download EC2 Credentials**         n/a
foxtrot   n/a                                n/a
========= ================================== ====================================================

:\*\*: 
   For Eucalyptus, compressed file is provided in the directory. Unzip
   it and load credentials are required like as follows::

         unzip ineuca3-{username}-{cluster}-fgprojectnumber.zip
         source eucarc

:\*:
   With OpenStack Horizon, EC2 credentials can be downloaded.

   - login `OpenStack Havana on Hotel
     <https://openstack.uc.futuregrid.org/dashboard/>`_ or `OpenStack
     Folsom on Alamo
     <https://openstack.futuregrid.tacc.utexas.edu/horizon>`_

   - Click 'Access & Security'

   - Select 'API Access' tab
   
   - Click 'Download EC2 Credentials' (which is a direct link here for
     `Hotel
     <http://openstack.uc.futuregrid.org/horizon/project/access_and_security/api_access/ec2/>`_
     or `Alamo
     <http://openstack.futuregrid.tacc.utexas.edu/horizon/project/access_and_security/api_access/ec2/>`_)

Next we specify the credentials of the cloud. We can obtain them
typically from the cloud provider. The mechnism to obtain them may
vary and you will need to look it up. Often you will have an rc file
or a GUI that allows you to export the needed information. We have
strived to keep the same attributes that are provided by the supported
cloud providors. Hence typically no change is needed and you can just
paste and copy the values. However, if your cloud needs certificates,
they may have to be specially dealt with and placed in special
directories. For cloudmesn we provide them as part of the install and
ainclude them in the::

  $HOME/.cloudmesh/ 

directory. Naturally the attributes in credentials depend on the cloud
type and are different between the different clouds. In our case we
define the cloud on sierra which has the following credentials::

        credentials:
          OS_AUTH_URL: https://s77r.idp.sdsc.futuregrid.org:5000/v2.0
          OS_CACERT: $HOME/.cloudmesh/sierra-cacert.pem
          OS_PASSWORD: jhdjaTYWUIYBY
          OS_TENANT_NAME: fg1000
          OS_USERNAME: albert
          OS_VERSION: grizzly

Only the last field OS_VERSION is not provided by the openstack rc
file. We simply specify the version and must make sure it is the same
as provided in cm_type_version. In future versions of cloudmesh we may
remove this attribute and only work with cm_type_version, but it is
very convenient to have the value also in credentials, so we left it
there for now also. The rest of the attributes are regular attributes
you find in the rc file. For Futuregrid Openstack clouds they will
have the following meaning:

:OS_AUTH_URL:
  The endpount that is used to manage virtual machines   

  Example: https://s77r.idp.sdsc.futuregrid.org:5000/v2.0

:OS_CACERT:
  The location in which the certificate for the cloud is placed to
  interact with https in case your cloud is properly protected. In
  case it does not use https please inform yourself about the security
  consequences.

  Example: $HOME/.cloudmesh/sierra-cacert.pem

:OS_PASSWORD:
  The password you use for this cloud

  Example: jhdjaTYWUIYBY

:OS_TENANT_NAME:
  The fg project number. In case you have multiple projects, you need to define multiple clouds 
  with multiple credentials that are distinguished by different tennant names.

  Example: fg1000

:OS_USERNAME:
  Your futuregrid portal name.

  Example: albert

:OS_VERSION:
  The version of openstack you use as described also by cm_type_version

  Example: grizzly

As it is often the case that users have a default image or flavor and
try to avoid remembering the values for them, such values can also be
specified in the cloudmesh.yaml file. This comes especially handy in
case of classes in which a teacher may provide the class with a custom
image and give students hints for which flavor to use. Also users that
deal with the instantiation of many VMs clearly benefit from this
feature::

  default:
    flavor: m1.tiny
    image: 4199d988-0833-4497-a473-96fc456fac2f

In our example above we have set the default to m1.tine for the falvor
and one of our default images available on the cloud.

The next sections show examples for several clouds with ficticious
account information. Please replace it with your own.

HP Cloud
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

HP provides multiple regions and they can be easily configured in
cloudmesh. We provide examples for two regions::

    hp:
      cm_heading: HP Openstack
      cm_label: hpos
      cm_type: openstack
      cm_type_version: grizzly
      credentials:
        OS_AUTH_URL: https://region-a.geo-1.identity.hpcloudsvc.com:35357/v2.0/
        OS_CACERT: None
        OS_PASSWORD: mypassword
        OS_TENANT_NAME: mytenantname
        OS_USERNAME: myusername
        OS_REGION: az-1.region-a.geo-1
      default:
        flavor: standard.small
        image: 142792
    hp_east:
      cm_heading: HP Openstack
      cm_label: hpeos
      cm_type: openstack
      cm_type_version: grizzly
      credentials:
        OS_AUTH_URL: https://region-b.geo-1.identity.hpcloudsvc.com:35357/v2.0/
        OS_CACERT: None
        OS_PASSWORD: mypassword
        OS_TENANT_NAME: mytenantname
        OS_USERNAME: myusername
        OS_REGION: region-b.geo-1
      default:
        flavor: standard.small
        image: 142792


Azure
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    azure:
      cm_host: windowsazure.com
      cm_label: waz
      cm_type: azure
      cm_type_version: null
      credentials:
        managementcertfile: $HOME/.cloudmesh/azure_managementCertificate.pem
        servicecertfile: $HOME/.cloudmesh/azure_serviceCertificate.pfx
        subscriptionid: 367367382-7687-6767-6767-6876dsa87ds
        thumbprint: $HOME/.cloudmesh/azure_thumbprint
      default:
        flavor: ExtraSmall
        image: b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu_DAILY_BUILD-saucy-13_10-amd64-server-20130930-en-us-30GB
        location: East US


Amazon Web Services
----------------------

::

    aws:
      cm_host: aws.amazon.com
      cm_label: aws
      cm_type: aws
      cm_type_version: null
      credentials:
        access_key_id: ABCDHJLKHLDKJHLDKJH
        keyname: cloudmesh
        privatekeyfile: $HOME/.cloudmesh/aws_pk.pem
        secret_access_key: abcgfiuegfiuesgfudsgfgdskjgfkdjsg
        userid: albert
      default:
        flavor: m1.small
        image: ami-fbb2fc92
        location: us-east-1


India
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Note the endpoint is wrong.

::

    india_openstack_havana:
      cm_heading: Sierra OpenStack, Grizzly
      cm_host: india.futuregrid.org
      cm_label: iosh
      cm_type: openstack
      cm_type_version: havana
      credentials:
        OS_AUTH_URL: https://i57r.idp.iu.futuregrid.org:5000/v2.0
        OS_CACERT: $HOME/.cloudmesh/india_cacert.pem
        OS_PASSWORD: uetruieiuf
        OS_TENANT_NAME: fg1000
        OS_USERNAME: albert
        OS_VERSION: havana
      default:
        flavor: m1.tiny
        image: 4199d988-0833-4497-a473-96fc456fac2f




Sierra
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    sierra_openstack_grizzly:
      cm_heading: Sierra OpenStack, Grizzly
      cm_host: sierra.futuregrid.org
      cm_label: sos
      cm_type: openstack
      cm_type_version: grizzly
      credentials:
        OS_AUTH_URL: https://s77r.idp.sdsc.futuregrid.org:5000/v2.0
        OS_CACERT: $HOME/.cloudmesh/sierra-cacert.pem
        OS_PASSWORD: 63763876827
        OS_TENANT_NAME: fg1000
        OS_USERNAME: albert
        OS_VERSION: grizzly
      default:
        flavor: m1.tiny
        image: 4199d988-0833-4497-a473-96fc456fac2f


Alamo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Although Alamo on FG is an openstack grizzly cloud, it is not as
sophisticated configured as the clouds on india and sierra. Instead is
uses for horizon the username and password from the openstack portal,
but does not expose its native cloud interfaces through the https
protocol. Instead it only offers access with the limited EC2 cloud
interfaces that are inferior in capabilities to the openstack
interfaces. Here is an example::


    alamo:
      cm_host: alamo.futuregrid.org
      cm_label: alamo
      cm_type: ec2
      cm_type_version: null
      credentials:
        EC2_PRIVATE_KEY: $HOME/.cloudmesh/alamo/pk.pem
        EC2_CERT: $HOME/.cloudmesh/alamo/cert.pem
        NOVA_CERT: $HOME/.cloudmesh/alamo/cacert.pem
        EUCALYPTUS_CERT: $HOME/.cloudmesh/alamo/cacert.pem
        EC2_URL: https://openstack.futuregrid.tacc.utexas.edu:8773/services/Cloud
        EC2_ACCESS_KEY: hfghfgejfhfdgjdhgjdhdgfjdhfgjhdg
        EC2_SECRET_KEY: utiutiueteyuieywiuywiuweyriuweyu
        keyname: cloudmesh
        userid: albert
      default:
        flavor: m1.small
        image: ami-fbb2fc92
        location: us-east-1


A complete example
~~~~~~~~~~~~~~~~~~~~~~

A more complete example of a cloudmesh.yaml file is available at 

 * https://github.com/cloudmesh/cloudmesh/blob/master/etc/cloudmesh.yaml

Here you need to replace all varibles in brackets. However there is a
more convenient way to do this with an additional yaml file that is
called me.yaml



cloudmesh-server.yaml
----------------------------------------------------------------------

Cloudmesh contains also a configuration file which i used to interface
with some server functionality. THis is only needed for some advanced
concepts such as power and temperature management as wel as bare metal
provisioning. As we at times modify the server yaml file and add new
features we have added a meta attribute to the file to document the
version and the type::

  meta:
    yaml_version: 2.0
    kind: server
  cloudmesh:
    server:
      ... all other text gis here ...

In addition a file starts with the attributes cloudmesh and
server. All other contents is indented under server.

Debugging
~~~~~~~~~~~~~

cloudmesh allows to set the debug level conveniently via the loglevel
attribute. Furthermore, one can disable the use of the production
environment (which disables the use of LDAP) while setting the
production attribute to False::

  server:
    loglevel: DEBUG
    production: False


Web UI
~~~~~~~~~~~~

Cloudmesh contains an optional Web UI interface that can be used to
interface with various clouds similar to horizon. However in contrast
to Horizopn it is not limited to OpenStack. It also provides access to
temperature data and user interfaces to bare metal provisioning. These
may be role based and not every user may be allowed to access
them. Thus they may not see links in the user interface for them. Only
priveleged users will.

The userinterface can be configured as follows::

    webui:
        host: 127.0.0.1
        port: 5555
        secret: development key
        browser: True
        page: ""

The host on which the server is placeed is either specified by ip or
hostname. A port on which the ui is started needs to be specified. In
addition a secret key has to be specified to enable some security
settings. It is best to use a key that is very difficult to crack.

If you set the browser variable to true, cloudmesh will automatically
upon restart open a web page. The web page can be specified via the
page attribute. If you specify "" it will go to the home page. This is
useful if you like to develop cloudmesh and like to repeatedly open a
particular page you work on.

LDAP Integration
~~~~~~~~~~~~~~~~~

Cloudmesh can be configured to read usernames from an LDAP server. On
FutureGrid we use the server configured for our FG users. However you
can certainly manage your own LDAP server. The configuration is done
via a proxy server that allows you to execute ldap commands. This
allows you to connect to the proxy server as other servers may not
allow to access the LDAP server as it is behind a firewall. The dn
location of the people and groups are also specifiable::

    ldap:
        with_ldap: False
        hostname: localhost
        cert: $HOME/.cloudmesh/FGLdapCacert.pem
        proxyhost: <ip>
        proxyuser: <username>
        proxyldap: proxy.<yourdomain.org>
        personbase: "ou=People,dc=futuregrid,dc=org"
        projectbase: "ou=Groups,dc=futuregrid,dc=org"

Clusters
~~~~~~~~~~~~

To access the control network of the clusters you can specify a
username and password for each cluster. This is done via the following
configuration::


    clusters:
        india:
            bmc:
                user: <username>
                password: <password>
                proxy: 
                   ip: <proxyip>
                   user: <proxyusername>
        echo:
                user: <username>
                password: <password>
                proxy: 
                   ip: <proxyip>
                   user: <proxyusername>
        bravo:
            pxe:
                proxy: 
                   ip: <ip>
                   user: <username>
            bmc:
                user: <username>
                password: <password>
                proxy: 
                   ip: <proxyip>
                   user: <proxyusername>

Note that you have te ability to specify a proxy machine in case the
access to the control network is behind a firewall. Also it is
possible to specify different usernames for access to pxe and bmc.

Roles
~~~~~~~

The portal framework can specify explicitly different roles and users
and projects to restrict access to specific web pages. Some of the
information such as active users and projects are fetsched frm the
LDAP server for the role "user".

However, two specific roles can be explicitly set, such as the admin
and rain roles. Here it is possible to add usernames or project
numbers and the specified user in the projects or the explicitly
specified users will have the given role. This allows a fine grained
control of users and roles. Additional roles could be added and become
useful for customized plugins to cloudmesh to expose features
seclectively.

todo::

    roles:
        user:
           users: 
           - active
           projects:
           - active
        admin:
           users:
           - albert
           projects:
           - fg1000
           - fg1001
        rain:
            users:
            - albert
            projects:
            - fg1000

Keystone server
~~~~~~~~~~~~~~~~~~

certain actions of a keystone server may not be executed by a regular
user. in his case the server yaml file allows you to use an
administrative account that can be configured under the keystone
attribute::

    keystone:
        sierra_openstack_grizzly:    
            OS_AUTH_URL : https://<ipsdsc>:35357/v2.0
            OS_CACERT : $HOME/.cloudmesh/sierra-cacert.pem
            OS_PASSWORD : <password>
            OS_TENANT_NAME : <tenant>
            OS_USERNAME : <username>
        india_openstack_essex:
            OS_AUTH_URL : http://<ipindia>:5000/v2.0
            OS_PASSWORD : <password>
            OS_TENANT_NAME : <tenant>
            OS_USERNAME : <username>
            OS_CACERT : None

please note that the names of the clouds need to be the exact names
used as in cloudmesh.yaml. The username and password can be obtained
from the cloud administrator if allowed.

Mongo
~~~~~~

currently we use mongo to save the state of cloudmesh. We have created
an easy schem to separate information and we simply recommend to reuse
the mongo section from the server yaml example file. Simply change the
valeus for username, password, and key to values you like if you set
it up on your local machine::

    mongo:
        db: cloudmesh
        host: localhost
        port: 27017
        path: $HOME/.cloudmesh/mongodb
        username: <username>
        password: <password>
        collections:
            inventory:
                db: inventory
            cloudmesh:
                db: cloudmesh
            profile:
                db: cloudmesh
            user:
                db: user
            metric:
                db: metric
            clouds:
                db: clouds
            pbs:
                db: hpc
            qstat:
                db: hpc
            qinfo:
                db: hpc
            pbsnodes:
                db: hpc
            launcher:
                db: launcher
            pagestatus:
                db: defaults
            password:
                key: <key>
                db: hallo
            defaults:
                db: defaults
            experiment:
                db: experiment
            store:
                db: store

Complete Example
~~~~~~~~~~~~~~~~~~

An example cloudmesh_server.yaml file is located at

* https://github.com/cloudmesh/cloudmesh/blob/master/etc/cloudmesh_server.yaml


cloudmesh_cluster.yaml
----------------------------------------------------------------------

Cloudmesh has the ability to create automatically an inventory of
large clusters based on some statically defined information. Because
the cluster may be in offline mode this static definition is useful in
order to also identif resources that may be offline or not reachable.

The definition will be used to create for each resource a number of
objects that can be used to easier access the resource or be used for
starting services on the resource.

We have created a simple program that creates a single yaml file for a
resource form this information. However we also have a json
representation that can be used in order not to depend on the file
system and interface directly with the database. This is of advantage
in a multi tenanted multi hosted environments in which provisioning of
resources is executed by multiple users. It also allows more easily
the dynamic management of resources that can be swapped in and out of
the inventory. 

A typical cloudmesh_cluster.yaml file looks as follows::

  meta:
    yaml_version: 1.2
    kind: clusters
  cloudmesh:
      inventory:
	  mycluster:
	      id: c[001-016]
	      nameserver: 123.123.1.1
	      publickeys:
	      - name: management
		path: $HOME/.cloudmesh/id_rsa_management.pub
	      - name: storage
		path: $HOME/.cloudmesh/id_rsa_storage.pub
	      network:
	      - name: eth0
		type: internal
		id: c[001-016]
		label: c-internal[001-016]
		range: 172.100.100.[11-26]
		broadcast: 172.100.101.255
		netmask: 255.255.252.0
		bootproto: dhcp
		onboot: yes
	      - name: eth1
		type: public
		id: c[001-016]
		label: c-compuet[001-016]
		range: 149.103.104.[11-26]
		broadcast: 149.103.104.255
		netmask: 255.255.255.0
		gateway: 149.103.104.254
		bootproto: static
		onboot: yes
	      - name: ib0
		type: infiniband
		id: c[001-016]
		label: c-ib[001-016]
		range: 192.168.0.[11-26]
		broadcast: 192.168.0.255
		netmask: 255.255.255.0
		bootproto: static
		onboot: yes
	      - name: bmc
		type: bmc
		id: c[001-016]
		label: bmc-c[001-016]
		range: 192.168.105.[11-26]
	      - name: pxe
		id: c[001-016]
		label: c-pxe[001-016]
		range: na[001-016]
		type: pxe
		pxe_prefix: /tftpboot/pxelinux.cfg

Metadata
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  meta:
    yaml_version: 1.2
    kind: clusters

Clusters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  cloudmesh:
      inventory:
	  mycluster1:
               ...
	  mycluster2:
               ...

A Cluster
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	  mycluster:
	      id: c[001-016]
	      nameserver: 123.123.1.1
	      publickeys:
	      - name: management
		path: $HOME/.cloudmesh/id_rsa_management.pub
	      - name: storage
		path: $HOME/.cloudmesh/id_rsa_storage.pub
	      network:
              - name: eth0
                 ...                
              - name: ib0
                 ...                
             - name: bmc
                 ...                
  
Network:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

	      network:
	      - name: eth0
		type: internal
		id: c[001-016]
		label: c-internal[001-016]
		range: 172.100.100.[11-26]
		broadcast: 172.100.101.255
		netmask: 255.255.252.0
		bootproto: [dhcp, static]
		onboot: yes

type:
   internal, public, pxe, bmc

id:
   TBD

label:
    TBD

range:
    TBD

broadcast:
     TBD

Bootprooto:
   TBD

onboot:
   TBD




Special resources bmc and pxe

bmc::

	      - name: bmc
		type: bmc
		id: c[001-016]
		label: bmc-c[001-016]
		range: 192.168.105.[11-26]

pxe::
	      - name: pxe
		id: c[001-016]
		label: c-pxe[001-016]
		range: na[001-016]
		type: pxe
		pxe_prefix: /tftpboot/pxelinux.cfg




Other Yaml files
-----------------

* https://github.com/cloudmesh/cloudmesh/blob/master/etc/cloudmesh_celery.yaml

Note the the ip addresses in this file are ficticious
* https://github.com/cloudmesh/cloudmesh/blob/master/etc/cloudmesh_cluster.yaml

* https://github.com/cloudmesh/cloudmesh/blob/master/etc/cloudmesh_launcher.yaml


Me Sample
------------

* https://github.com/cloudmesh/cloudmesh/blob/master/etc/me-sample.yaml
* https://github.com/cloudmesh/cloudmesh/blob/master/etc/me.yaml
