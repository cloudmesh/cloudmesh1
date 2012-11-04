add
---
- adds an entity into the inventory

Usage
+++++
To add an object to the inventory::

	add object-type <parameters>
To add a server to the inventory::

	add server <parameters>
To add a service to the inventory::

	add service <parameters>

Description
++++++++++

The assign command defines a defualt parameter for parameters defined by other commands. Presently we are suporting the assignment of default parameters for servers and serivices. First we have to specify the type whic in our case is either service or server. Than we specify the name that is used whenever we would normally define a parameter defining a server or service


The add command defines a way to add entities into the inventory, an entity can either be a server or a service according to the requirements and can be invoked as shown in the usage. The add command is followed by the entity name to be added along with the list of parameters specified below.

List of Parameters
++++++++++
::

	server
used to add a server entity to the inventory
::
	
	service
used to add the service entity to the inventory
::

	--name/-n
used to specify the name of the server or the service.
::

	--range/-r
used to specify the range over which to use the command
::

	--prefix/-p
used to specify the url prefix to be used for the entities to be added 
::

	--servicename/-s
used only with adding a service entity to specify the name of the service to be added

Example
++++++++++

The following example adds a server into the inventory with range from 1-3 and prefix as specified using the name as india ::

  fg-inventory> 
  > add server -r 1-3 -p i%.iu.edu -n india
  > add service -r 1-3 -p i%.iu.edu -n india -s eucalyptus
  
