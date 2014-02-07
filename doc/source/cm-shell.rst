.. sectnum::
   :start: 5
   

Cloud Mesh
==========

A project to interface easily with multiple clouds from the
commandline and a command shell.

Defaults
----------------------------------------------------------------------

::
   
   env

::

   default ...



Register Clouds
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

::

   cm activate <label>

::

   cm deactivate <label>


:: 
    cm activate <label> yes
    cm activate <label> no

::
    cm activate <label> select

Prints a little menu that allows you to select a number and activate
the cloud from the menu

Managing Projects
----------------------------------------------------------------------


Managing Users
----------------------------------------------------------------------

TBD

Manageing Virtual Machines
----------------------------------------------------------------------

List images
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Starting VMs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Manageing Security Groups
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Managing Volumes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Managing heat's for OpenStack
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

(Jonathan)



Commands
========

Creating configuration files

::

   cm generate me

   cm generat yaml

   they do exist ;-)

   cm-manage



Listing images
----------------------------------------------------------------------

To list all images you do ::

  cm image --list

To list a specfic image you can do::

  the other



cm manage initialize --user<name> --password <password>
----------------------------------------------------------------------

   * connects to FG and retrieves important information for you to use
   * uses an ssh connection to connect to a FG service to retrieve the
     information
   * if the connection is refused n=5 times within the hour the
   * account is disabled
   * if the command is called more than 10 times a day the account is disabled

cm project list
----------------------------------------------------------------------

   lists the projects a user is in

cm project --info <number>
----------------------------------------------------------------------

   * retrieves information about the project
   * if the user is the manager or lead it returns member information

cm project --activate <number>
----------------------------------------------------------------------

   * activates charging for this project
   * subsequent calls are charged against this project

cm project --deactivate
----------------------------------------------------------------------

   * deactivates any charge of a project

cm env
----------------------------------------------------------------------

   * prints the environment and its variables currently associated
     with cm

cm resource --list
----------------------------------------------------------------------

   * lists the resources available for the user
   
cm service --list
----------------------------------------------------------------------
  
  * list the services in the cloud mesh

cm service register
----------------------------------------------------------------------
   see fg-inventory

cm resource register
----------------------------------------------------------------------

   see fg-inventory

cm image --list
----------------------------------------------------------------------

   * list the images

cm id --list
----------------------------------------------------------------------

  * list all ids and their types

cm label --id <id>
----------------------------------------------------------------------

   * associates a human readable lable with an id

cm vm create <label>
----------------------------------------------------------------------

cm vm destroy <label>
----------------------------------------------------------------------

cm vm terminate <label>
----------------------------------------------------------------------

cm vm suspoend <label>
----------------------------------------------------------------------

cm vm resume <label>
----------------------------------------------------------------------

cm vm login
---------------------

= ssh label


cm seceurity group add <label> <parameters>
----------------------------------------------------------------------

cm seceurity group delete
----------------------------------------------------------------------

cm seceurity group default add <label> 
----------------------------------------------------------------------

cm seceurity group default delete <label> 
----------------------------------------------------------------------


Examples
----------------------------------------------------------------------

The goal of this example is to .....

multiple vms, multiple clouds
configuration

starting vms

listng status of all started vmsd across all clouds

ssh login -> can not be don with pytho sha but must be done with os.system


