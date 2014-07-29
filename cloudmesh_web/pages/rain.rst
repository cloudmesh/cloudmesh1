Rain
======================================================================

**THIS FEATURE OF CLOUDMESH IS NOT YET ENABLED FOR THIS RELEASE**

Cloudmesh provides a convenient interface to baremetal access of
resources and to provision services on these bare metal resources. We
term this concept **rain**.

Rain is integrated into the cloudmesh UI through a role based access
control mechanism allowing either specific users or specific projects
to gain access. Furthermore, users and projects can be restricted in
which resources the users have access to.  This is of special
importance to be able to conduct successive experiments on the exact
same resources.

Although we can enable a scheduler based interface to bare metal
provisioning, the our current rol based, resource reservation provides
the user with more access to specific experiment setups.

Some `screenshots </screenshots>`_ show details of the User interface

The following provisioning concepts are important and are included in
rain

:Baremetal: bare metal provisioning provides the ability to provision
            an OS directly on the server.

:Service: services can be dynamically provisioned either via bare
          metal or IaaS provisioning.
         
:Infrastructure: It will be possible to deploy IaaS frameworks with
		 the help of rain allowing users to stage their own
		 clouds with customizations that would otherwise not
		 be available to the users.
          
:Platform: A combination of bare metal, IaaS, and service provisioning
           may provide users with a platform. Instead of users needing
           to put together such a platform, they can benefit from
           previous instantiations and templates developed by others.
          
          
