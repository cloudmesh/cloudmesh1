Rain
======================================================================

**THIS FEATURE OF CLOUDMESH IS NOT YET ENABLED FOR THIS RELEASE**

Cloudmesh provides a convenient interface to baremetal access of resources 
and to provision services on these bare metal resources. We term this concept 
**rain**.

Rain is integrated into the cloudmesh UI through a 
role based access control mechanism allowing either specific users or
specific projects to gain access. Furthermore, users and projects can 
be restricted in which reosurces the users have access to.
This is of special importance to be able to conduct successive experiments on 
the exact same resources.

Although we can enable a scheduler based interface to bare metal provisioning, the 
our current rol based, resource reserveration provides the user with more access 
to specific experiment setups.

Some `screenshots </screenshots>`_ show deatils of the User interface

The following provisioning conccepts are important and are included in rain 

:Baremetal: bare metal provisioning provides the ability to provisin an OS directly on the server.

:Service: services can be dynamically provisioned either via bare metal or IaaS provisioning.
         
:Infrastructure: 
          
:Platform: A combination of pare metal, IaaS, and service provisioning may provide users with a platform. Instead of users needing to put together such a platform, they can benefit from previous instantiations and templates developed by others.
          
          
