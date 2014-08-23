Overview 
==========

More information can also be found at 

* http://cloudmesh.futuregrid.org

Cloudmesh is an important component to deliver a software-defined
system – encompassing virtualized and bare-metal infrastructure,
networks, application, systems and platform software – with a unifying
goal of providing Cloud Testbeds as a Service (CTaaS). Cloudmesh
federates a number of resources from academia and industry. This
includes existing FutureGrid infrastructure (4704 cores used by more
than 355 projects), Amazon Web Services, Azure, HP Cloud, Karlsruhe
using various technologies.

.. figure:: images/cloudmesh-arch-2013.png	
   :scale: 75 %
   :alt: cloudmesh architecture

   **Figure:** The cloudmesh architecture. Green = components
    available, under improvement. Yellow = components under
    development.

A goal of Cloudmesh is to aggregate resources not only from
FutureGrid, but also from OpenCirrus, Amazon, Microsoft Azure, and HP
Cloud and GENI resources to name only a few. Cloudmesh was originally
developed in order to simplify the execution of multiple concurrent
experiments on a federated cloud infrastructure. In addition to
virtual resources, FutureGrid exposes bare-metal provisioning to
users, but also a subset of HPC monitoring infrastructure
tools. Services will be available through command line, API, and Web
interfaces.

The three layers of the Cloudmesh architecture include a Cloudmesh
Management Framework for monitoring and operations, user and project
management, experiment planning and deployment of services needed by
an experiment, provisioning and execution environments to be deployed
on resources to (or interfaced with) enable experiment management, and
resources.

System Monitoring and Operations
----------------------------------------------------------------------

The management framework contains services to facilitate FutureGrid
day-to-day operation, including federated or selective monitoring of
the infrastructure. Cloudmesh leverages FutureGrid for the operational
services and allows administrators to view ongoing system status and
experiments, as well as interact with users through ticket systems and
messaging queues to inform subscribed users on the status of the
system.

The cloudmesh management framework offers services that simplify
integration of resources in the FutureGrid nucleus or through
federation. This includes, for user management, access to predefined
setup templates for services in enabling resource and service
provisioning as well as experiment execution. To integrate IaaS
frameworks cloudmesh offers two distinct services:

1. a federated IaaS frameworks hosted on FutureGrid,

2. the availability of a service that is hosted on FutureGrid allowing
   the “integration” of IaaS frameworks through user credentials
   either registered by the users or automatically obtained from our
   distributed user directory.

For (2) several toolkits exist to create user-based federations,
including our own abstraction level which supports interoperability
via libcloud, but more importantly it supports directly the native
OpenStack protocol and overcomes limitations of the EC2 protocol and
the libcloud compatibility layer. Plugins that we currently develop
will enable access to clouds via firewall penetration, abstraction
layers for clouds with few public IP addresses and integration with
new services such as OpenStack Heat. We successfully federated
resources from Azure, AWS, the HP cloud, Karlsruhe Institute of
Technology Cloud, and four FutureGrid clouds using various versions of
OpenStack and Eucalyptus. The same will be done for OpenCirrus
resources at GT and CMU through firewalls or proxy servers.

Additional management flexibility will be introduced through automatic
cloud-bursting and shifting services. While cloud bursting will locate
empty resources in other clouds, cloud shifting will identify unused
services and resources, shut them down and provision them with
services that are requested by the users. We have demonstrated this
concept in 2012, moving resources for ~100 users to services that were
needed based on class schedules. A reservation system will be used to
allow for reserved creation of such environments, along with
improvements of automation of cloud-shifting.

User and Project Services
----------------------------------------------------------------------

FutureGrid user and project services simplify the application
processes needed to obtain user accounts and projects. We have
demonstrated in FutureGrid the ability to create accounts in a very
short time, including vetting projects and users – allowing fast
turn-around times for the majority of FutureGrid projects with an
initial startup allocation. Cloudmesh re-uses this infrastructure and
also allows users to manage proxy accounts to federate to other IaaS
services to provide an easy interface to integrate them.

Accounting and App Store
----------------------------------------------------------------------

To lower the barrier of entry Cloudmesh will be providing a shopping
cart which will allow checking out of predefined repeatable experiment
templates. A cost is associated with an experiment making it possible
to engage in careful planning and to save time by reusing previous
experiments. Additionally, the Cloudmesh App Store may function as a
clearing-house of images, image templates, services offered and
provisioning templates. Users may package complex deployment
descriptions in an easy parameter/form-based interface and other users
may be able to replicate the specified setup with.

Due to our advanced Cloudmesh Metrics framework we are in the position
to further develop an integrated accounting framework allowing a usage
cost model for users and management to identify the real impact of an
experiment on resources. This will be useful to avoid overprovisioning
and inefficient resource usage. The cost model will be based not only
on number of core hours used, but also the capabilities of the
resource, the time, and special support it takes to set up the
experiment. We will expand upon the metrics framework of FutureGrid
that allows measuring of VM and HPC usage and associate this with cost
models. Benchmarks will be used to normalize the charge models.

Networking 
----------------------------------------------------------------------

We have a broad vision of resource integration in FutureGrid with
systems offering different levels of control from "bare metal" to use
of a portion of a resource. Likewise, we must utilize networks
offering various levels of control, from standard IP connectivity to
completely configurable SDNs as novel cloud architectures will almost
certainly leverage NaaS and SDN alongside system software and
middleware. FutureGrid resources will make use of SDN using OpenFlow
whenever possible and the same level of networking control will not be
available in every location.



Monitoring 
----------------------------------------------------------------------

To serve the purposes of CISE researchers, Cloudmesh must be able to
access empirical data about the properties and performance of the
underlying infrastructure beyond what is available from commercial
cloud environments. To accommodate this requirement we have developed
a uniform access interface to virtual machine monitoring information
available for OpenStack, Eucalyptus, and Nimbus. In the future, we will
be enhancing the access to historical user information. Right now they
are exposed through predefined reports that we create on a regular
basis. To achieve this we will also leverage the ongoing work while
using the AMPQ protocol. Furthermore, Cloudmesh will provide access to
common monitoring infrastructure as provided by Ganglia, Nagios, Inca,
perfSonar, PAPI and others.


Role and Use of Standards and Open Source Software
----------------------------------------------------------------------

Cloudmesh will use standards and open source software as part of its
design principles towards sustainability. We will leverage efforts
such as OCCI and CDMI and are already using community efforts on
interoperability APIs as provided by Apache libcloud. However, as
libcloud is feature limited Cloudmesh provides an additional
abstraction layer that exposes cloud interfaces on the native-protocol
level. Furthermore we interface to commercial Clouds such as Microsoft
Azure, Amazon WS, and HP Cloud to providing access to robust
commercial high availability services.



Features
----------------------------------------------------------------------

We are working towards providing the following features into
cloudmesh:

* easy management of multiple clouds in cloudmesh while supporting
  various native libraries. 
* portability library to access information in regards to images,
  flavors, and vms
* management of hundreds/thousands of virtual machines
* integration of non FutureGrid cLouds by users into cloudmesh so
  users can access them from cloudmesh
* a command line shell 
* a web interface
* possibility to download and deploy cloudmesh locally by a user (so
  he can manage his own clouds)
* others


Bugs
----------------------------------------------------------------------

* AWS, Azure, and EC2 images can not yet be handled well in the
  data tables if there are thousands of entries.
* Adding an arbitrary cloud has not yet been enabled, although it can
  be achieved via adding it from the command line
* The asynchronous refresh has not yet been enabled
* The look of the table in server does not yet look nice on the header
  level (alignment)
* keys for Azure and AWS vms are not yet managed via cloudmesh
* certificates from AWS, and Azure are not yet uploadable by the user
* AWS, and Azure return a large number of images. data tables may have
  to be switched all to server side data tables.

Project Contributors
----------------------------------------------------------------------

`Cloudmesh <https://github.com/cloudmesh/cloudmesh>`_ is a community
project and has received contributions from 12 developers. Their names
and contributions to the code are maintained in Github and you can
find out more information about each individual contributor from out
`Github Project Page </git>`_ .


History
----------------------------------------------------------------------

Cloudmesh 0.1
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Cloudmesh is part of the effort of FutureGrid to provide a simple
experiment management functionality. It has been used at IU for about
9 month.

Originally cloudmesh was just a `command line tool
<https://github.com/futuregrid/cm>`_ that was able to start hundreds
of VMs on various clouds in order to conduct stress testing of cloud
deployments. There was no comparable tool available. Our requirements
were simple, but none of the tools fulfilled the following
requirements:

* start hundreds of VMs from the command line with a simple command
* delete the VMs from a user through the command line
* provide native support of the cloud and not just using a wrapper
  library such as libcloud or a standard such as OCCI (we wanted to
  debug the cloud and not the wrapper libraries or standards)
* provide an elementary display on which VMs run where.
* users should be able to deploy a stand alone version of cloudmesh

Through this tool we were able to identify issues with our clouds and
improve the deployment. 

Other tools that we tried to use were hiding these issues as they for
example did not use the native API protocol, but instead used
alternative protocols such as EC2 in case of our OpenStack clouds. As
a user this may be ok, but as a resource provider such limitation is
naturally problematic.


Cloudmesh 0.2
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Next we replaced the curses based user interface with a web browser
based user interface. This made it possible to more easily develop
more sophisticated interfaces in General.

At the same time we reused our python command shell interpreter cmd3
so that it is more easily possible to develop command line tools
automatically from the commands we already developed as part of the
command shell anyways.

A command shell is obviously important as it allows us to describe
experiments as scripts.

Cloudmesh 0.3
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Base on the success from the earlier versions and the use of a web
browser as interface, it became clear that users could benefit from
our effort. Thus we started to generalize the framework a bit and work
towards distributing cloudmesh as a single user environment while
users can install a stand alone version of the software.

Based on this internal success of cloudmesh we started thinking it
would be good to expose the functionality also to users.

Cloudmesh 0.4
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In cloudmesh 0.4 we transformed the store of the VM, flavor, and
images into a database, we also moved the development of the code in a
new  `Github Cloudmesh <https://github.com/cloudmesh/cloudmesh>`_ 
repository.

Cloudmesh 0.5 - 0.7
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following important changes took place:

* introduction of a role based authentication theme
* adding FG authentication from the portal account
* ingesting users either from a yaml file or LDAP directory
* adding capabilities to list vms, flavors, and images from AWS
* adding capabilities to list vms, flavors, and images from Azure
* adding capabilities to list vms, flavors, and images from EC2 (via libcloud)

