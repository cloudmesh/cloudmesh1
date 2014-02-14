.. sectnum::
   :start: 5
   

Cloud Mesh
==========

A project to interface easily with multiple clouds from the
commandline and a command shell.

Info
----------------------------------------------------------------------

The info command is a standard command that is defined in cmd3 and
displays some internal information related to the commandshell. It
lists the cmd3 dict, as well as information about verions and
scopeless commands. Commands with scops can be activated with the use
command. For more information see::

  cm> help use

Variables
----------------------------------------------------------------------

The shell allows you to set variables so it is easy for you to resuse
them at a later time two standard variables are defined as $date and
$time which will provide you with the current date and time. You can
list the variables with the command in the shell with::

  cm> var

Defaults
----------------------------------------------------------------------

::
   
   defaults

::

   default ...

Managing Users
----------------------------------------------------------------------

Creating configuration files

::

   cm> generate me

   cm> generat yaml



::
   cm-manage



Managing Clouds
----------------------------------------------------------------------

Before you can use a cloud you need to register it. Registration will
allow you to log into the cloud and use its resources.

Register an AWS account
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  cm register aws ...

Example:

- Amazon AWS account

Register an azure account
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  cm register azure ...

Example:

- Microsoft azure Cloud

Register an Eucalyptus account
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  cm register eucalyptus ...

- FutureGrid india (Eucalyptus)

Register an OpenStack account
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  cm register openstack ...


Examples:

- FutureGrid sierra
- FutureGrid india (Openstack)
- HP Cloud


Register an EC2 account
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  cm register ec2 ...

Examples:

- FutureGrid alamo
- FutureGrid hotel

Activate Clouds
----------------------------------------------------------------------

Clouds can be activated with the following commands

::

   cm> cloud --on <label>

::

   cm> cloud --off <label>


To select a specific cloud from a simple ascii menu you can use the
command ::

    cm> activate <label> select


Managing Projects
----------------------------------------------------------------------

projects = tennnats in openstack



Project List
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   cm> project list


lists the projects a user is in


Project Information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

   cm> project --info <number>

* retrieves information about the project
* if the user is the manager or lead it returns member information


Project Activation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
::

   cm> project --activate <number>

* activates charging for this project
* subsequent calls are charged against this project


Project Deactivation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   cm> project --deactivate




Managaging Images
----------------------------------------------------------------------

List images
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To list all images you do ::

  cm> image --list

To list a specfic image you can do::

  the other

To select an image you do::

  cm> image --select <cloud> 

If the cloud parameter is missing than also the cloud will be asked::

  cm> image --select 


Activating Images
----------------------------------------------------------------------

::

   cm> image --default <cloud> <label>

Managing Flavors
----------------------------------------------------------------------

see images and than complete the documentation here

List Flavors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Activating Flavors
----------------------------------------------------------------------


Manageing Virtual Machines
----------------------------------------------------------------------

Starting VMs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note:: The label in the vm commands is optional, if not specified,
	  we will use the approriate defaults from the last vm.

::

   cm> vm create <label>

::

   cm> vm destroy <label>


::

   cm> vm terminate <label>


::

   cm> vm suspend <label>


::

   cm> vm resume <label>


::

   cm> vm login <label>

::

   cm> ssh vm <label>


VM History
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To list the history of all previously started vms, please use the
``history`` command. It will tell you whne the vm was started,
launcched, and terminated. If no label is provided this information
returns a list of vms started in order. In contrast to the normal list
command given by IaaS framework, this list command sorts the vms by
the timestamp it was started in the shell. The history is maintained
in ~/.futuregrid/cloudmesh/history::
 
   cm> history [<label>]

The history can be cleared with:: 

   cm> history --clear

Each command in the history is preceeded with an id. You can rerun the
command by execuring the history command followed by the id::

   cm> history 101

You can also set a convenient variables so you do not have to remember
the number and can introduce labels for the history id that you can
easier remember

   cm> var mylabel=101

If you now type::

   cm> history $mylabel

It will start the command associated with the 101 id in the 

   


Manageing Security Groups
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Managing Volumes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Managing heat's for OpenStack
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

(Jonathan)




Managing Security Groups
----------------------------------------------------------------------


::

   cm> seceurity group add <label> <parameters>

::

   cm> seceurity group delete

::

   cm> seceurity group default add <label> 

::

   cm> seceurity group default delete <label> 


Examples
----------------------------------------------------------------------

The goal of this example is to .....

multiple vms, multiple clouds
configuration

starting vms

listng status of all started vmsd across all clouds

ssh login -> can not be don with pytho sha but must be done with os.system




TODO (most likely in cloud command and register command)
----------------------------------------------------------------------

::

   cm> manage initialize --user<name> --password <password>

* connects to FG and retrieves important information for you to use
* uses an ssh connection to connect to a FG service to retrieve the
  information
* if the connection is refused n=5 times within the hour the
* account is disabled
* if the command is called more than 10 times a day the account is disabled

::

   cm> resource --list

* lists the resources available for the user

::   

   cm> service --list
 
* list the services in the cloud mesh

::

   cm> service register

see fg-inventory

::

   cm> resource register

see fg-inventory

::

   cm id --list


* list all ids and their types

::

   cm label --id <id>

* associates a human readable lable with an id


.. warning:: The following commands are automatically created with

	       fab doc.man

	     If you like to update them, please donot do this in the man.rst file,
	     but update the commands in the actual manual page in the code

.. include:: man/man.rst
