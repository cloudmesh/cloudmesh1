Cloud
======================================================================

Cloudmesh provides a convenient set of interfaces to various clouds. 
Currently we focus on virtual machine management, but a future version
will include other services. 

Interfaces
---------------------------

The Cloudmesh interfaces include 

:API: A python API that simplifies access to clouds while being able o use the native 
      cloud protocols and not just an EC2 compatibility mode as is provided by libcloud or boto.
      However, we are also providing an EC2 interface based on libcloud, making it possible to 
      integrate easily the many clouds supported by it.

:Shell: A command shell allows the easy interaction with various clouds while using simple
        commands. As the commands can be included in scripts, it can 
        also help to formulate simple experiment templates.

:Commands: The shell commands can also be used on the Unix command line.
           Making it possible to integrate cloudmesh features into the
           unix ecosystem
           
:Web UI: We are providing on FutureGrid an example for  a hosted mode of cloudmesh.
       
:Console UI: It is possible to host cloudmesh on your own computer. This may be desirable, if
       	you like to customize the interfaces. We like to hear back from you if you use it
       	in this fashion. We like to also integrate your new components and 
       	features into cloudmesh. If you like to become a developer, please 
       	contact laszewski@gmail.com     
      
:iPython: We are currently developing a set of simple examples to let users know how easy it is to use the API.

Integration of External Clouds
---------------------------------

Currently we support the native OpenStack and the EC2 protocol. This allows you to integrate a large number 
of clouds. Hence it is possible to not only integrate FutureGrid Cloud resources.
However, some clouds require you to use a certificate. In this case you can
talk to us. 

We have demonstrated successfully the integration with

* OpenStack Grizzly clouds, an example is sierra.futuregrid.org 
* EC2 OpenStack cloud, an example is alamo.futuregrid.org
* HP Cloud East
* HP Cloud West
* Karlsruhe Institute of Technology
* Azure (standalone mode)
* AWS (standalone mode)

Although we have demonstrated that it is possible to integrate with cloudmesh we have not yet exposed this feature by default to the users. Users are welcome to try it.

Open Source     
-----------------------      

:Apache: Cloudmesh is distributed with the Apache 2.0 license

:Github: Cloudmesh is hosted on github.gom. More information is provided at 
         `our github page </git>`_. 

:Issues: We are collecting issues on github and provide a convenient
         `table view </bugs>`_.
         
:Bugs:   You can submit bugs through the FutureGrid help page at
         `https://portal.futuregrid.org/help <https://portal.futuregrid.org/help>`_.  
