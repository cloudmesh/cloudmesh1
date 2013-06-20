Welcome to FutureGrid Cloud Inventory
=====================================

This project is intended to provide information about a simple database to manage inventory in support of cloud seeding and cloud shifting.

Cloud Inventory
-------------
  * A project to do bare metal and VM based dynamic provisioning
  * Documentation: http://futuregrid.github.com/inventory
  * Source: https://github.com/futuregrid/inventory

Introduction
----------

In a heterogeneous cloud and HPC environment it is important to know
which services are running on what servers. Typically such an
environment is made up out of several clusters. Each cluster has a
number of servers and on each server multiple services may run. 

To reassign servers to different clouds and to start up new services a
simple and convenient information service is needed to track the
current status. In addition we need a mechanism to track historical
configurations so that we can identify at any time what servers and
services participated in our configuration.

Status
-----

At this tiem we have not implemented a historical logging framework.

Data Model
---------

The current data model is simple and reflects two types

* a "server" type that represents a compute node in a cluster
* a "service" type that represents a major service run on the server.

A service type could for example represent a OpenStack compute
service, or a HPC managementnode, or any other type. 

As underlaying database we have chosen mongodb as it allows us to
easily and quickly add new entries, as well as allowing us to modify
the data types when needed. 

In case the data model is changed a new version for the general
datamodel is introduced, and the data model is documented in our
source code.

At this time we have defined the follwoing server data::

 server = {        
                'ip_address':'',
                'name':'',
                'type':'',
                'label':'',
                'keyword':'',
                'uid':'',
                'start_time':'',
                'stop_time':'',
                'services':[
                             {'name':'',
                              'type':'',
                              'version':'',
                              'keyword':'',
                              'start_time':'',
                              'stop_time':'',
                              'status':'',
                            }]
            }

Additional attributes will be added over time and as needed.

Quickstart Example
---------------

We have provided a simple command shell that allows us to use the
inventory conveniently either interactively, or in scripts. A simple
example is provided next. Here we define a server (should be renamed
to cluster) that contains a collection of servers (1-5) with the name
i1.iu.edi to i5.iu.edu. On each of the 5 services we are intending to
run eucalyptus as a service::

	fg-inventory> assign server:india
	> add server -r 1-5 -p i%.iu.edu
	> assign service:euca
	> add service -r 1-5

To show the current inventory we simply use the command:: 

	> list server

To unassign the service we can use the command::

	> unassign service

To add them to the inventory we can use the command::

	> add server

Now we can observe the current status
	> list server

In future, each command will produce a log entry that allows us to
replay the server configuration.


List of Commands	
----------------

A more detailed description of the various commands is available.

.. toctree::
	:maxdepth: 1
	
	assign
	add
	unassign
	list
	support

.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`


