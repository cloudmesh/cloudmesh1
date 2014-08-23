Cloudmesh Shell
=================

.. sidebar:: 
   . 

  .. contents:: Table of Contents
     :local:

..


The cloudmesh shell allows to interact with multiple clouds either
through the commandline or through a command shell.

Commandline
--------------

To start a command line simply type the command cm followed by the
actual cloudmesh command. For example to invoke the `help` command
type in::

  $ cm help

Note that $ indicates your command shell prompt.

Shell Usage
------------

In many cases you like to invoke multiple commands and preserve some
local state. This can easily be done while starting cloudmesh as a
shell via the `cm` command. Simply type in you command shell::

  $ cm

You will see next a prompt such as::

  cm> 

In which you can type in multiple cloudmesh commands. Please not that
each of the commands can be executed directly from the shell by
preceding the `cm` command.

The command shell is based on cmd3 which is in more detail documented
at:

* http://cloudmesh.github.com/cmd3/

  
After you start up the shell, you will be presented with a login
message such as seen next::

                FutureGrid - Cloud Mesh Shell
  ------------------------------------------------------
     ____ _                 _   __  __           _
    / ___| | ___  _   _  __| | |  \/  | ___  ___| |__
   | |   | |/ _ \| | | |/ _` | | |\/| |/ _ \/ __| '_ \ 
   | |___| | (_) | |_| | (_| | | |  | |  __/\__ \ | | |
    \____|_|\___/ \__,_|\__,_| |_|  |_|\___||___/_| |_|
  ======================================================

Additional debaug and logging information may be displayed.

You can cahnge the verbosity of the logging while changing in the::

  ~/.cloudmesh/cloudmesh_server.yaml 

file the loglevel variable. In that file you find::

  meta:
    yaml_version: 2.0
    kind: server
  cloudmesh:
    server:
      loglevel: DEBUG
      production: False
  ...

You can set the loglevel for example to `DEBUG`, `INFO`, or `NONE`.


Command Overview
=================


Help
----------------------------------------------------------------------

The help command is a standard command that is defined in cmd3 and
displays some internal information related to the command shell. It
lists the cmd3 dict, as well as information about versions and
scope-less commands. Commands with scopes can be activated with the use
command. For more information see::

  cm> help use

Info
----------------------------------------------------------------------

The `info` command provides the ability to print out a short
information regarding a command specified via a plugin. This command
will only work if an info is actually defined for that command.
To optain the info for all commands specify::

  cm> info

To specify the info for a specific command please use the info command
followded by the name of the command::

  cm> info list

.. note::

   The info command has not been implemented for the shell yet. 

Variables
----------------------------------------------------------------------

The shell allows you to set variables so it is easy for you to reuse
them at a later time two standard variables are defined as $date and
$time which will provide you with the current date and time. You can
list the variables with the command in the shell with::

  cm> var

The following options are available::

  Usage:
    var list
    var delete NAME
    var NAME=VALUE

See also: :doc:`/man/man.html#var`

Defaults
----------------------------------------------------------------------

This manages the defaults associated with the user. You can load, list and clean defaults associated with a user and a cloud. The default parameters include index, prefix, flavor and image.

::

  cm> defaults

The following options are available:

::

  Usage:
   defaults clean
   defaults load [CLOUD]
   defaults list [--json] [CLOUD]

Examples::

  defaults load
  defaults clean alamo
  defaults list --json alamo


Managing Users
----------------------------------------------------------------------

Administrative command to list information about the user, create configuration files and list the config details.

::

   cm> user

The following options are available:

::

   Usage:
     user list
     user ID
     user ID me
     user ID yaml
     user ID ldap
     user ID new FORMAT [dict|yaml]

Examples::

  cm> user list

::

  cm> user abcd

::

  cm> user abcd new dict


Managing Clouds
----------------------------------------------------------------------

Before you can use a cloud you need to register it. Registration will
allow you to log into the cloud and use its resources.

Register a cloud
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

  cm> reg <CloudName>

You can set the same cloud to active (activate a cloud) by using the switch '--activate'/'-a'
Also, a cloud can be removed from active list by using the switch '--deact'/'-d'::

  cm> reg --act <CloudName>
  cm> reg --deact <CloudName>


Examples::

  cm> reg sierra_openstack_grizzly

::

  cm> reg -a alamo

::
  cm> reg --deact india_openstack_essex

Activate cloud
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Clouds can be activated with the following commands::

   cm> cloud --on <CloudName>

::

   cm> cloud --off <CloudName>

Examples::

  cm> cloud --on sierra_openstack_grizzly

::

  cm> cloud --off alamo

Managing Projects
----------------------------------------------------------------------

Projects are equivalent to tenants in openstack


Project List
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lists the projects a user is in

::

   cm> project list


Project Information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* retrieves information about the project
* if the user is the manager or lead it returns member information

::

   cm> project info <name>

Examples::

  cm> project info fg82

Project Activation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* activates charging for this project
* subsequent calls are charged against this project

::

   cm> project activate <name>

Managing Keys
----------------------------------------------------------------------
Retrieve your key information, get key fingerprint and view the key.

::

  cm> keys

Following options are available

::

   Usage:
     keys info [NAME]
     keys default
     keys show [NAME]

Examples::

  cm> keys info default_key

::

  cm> keys show key1

Managing Images
----------------------------------------------------------------------

Manage virtual machine images for clouds

List images
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List all images for specified cloud. If cloud name is not specified,
images for default cloud are displayed.::

  cm> image list <name>

Image information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Get specific information about the image.::

  cm> image info <name>

Default image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Set an image as default image.::

   cm> image --default <cloud> <label>


Managing Flavors
----------------------------------------------------------------------

Manage flavors for clouds.

List Flavors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

List all images for specified cloud. If cloud name is not specified,
flavors for default cloud are displayed.::

  cm> flavor list <name>

Flavor information
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Get specific information about the flavor.::

  cm> flavor info <name>


Default Flavor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Set a flavor as a default flavor.::

   cm> flavor --default <cloud> <label>


Managing Virtual Machines
----------------------------------------------------------------------

Starting VMs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. note:: The label in the vm commands is optional, if not specified,
	  we will use the appropriate defaults from the last vm.

Creates a new instance/VM on default cloud::

   cm> vm create <label>


Deletes the specified or last default instance/VM on default cloud::

   cm> vm delete <label>


Suspends the specified or last default instance/VM on default cloud::

   cm> vm suspend <label>


Resumes the specified or last suspended instance/VM on default cloud::

   cm> vm resume <label>


Login into the specified or last default instance/VM::

   cm> vm login <label>



SSH into the specified or last default instance/VM::

   cm> ssh vm <label>




VM History
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To list the history of all previously started vms, please use the
``history`` command. It will tell you when the vm was started,
launcched, and terminated. If no label is provided this information
returns a list of vms started in order. In contrast to the normal list
command given by IaaS framework, this list command sorts the vms by
the timestamp it was started in the shell. The history is maintained
in ~/.cloudmesh/cloudmesh/history::

   cm> history [<label>]

The history can be cleared with::

   cm> history --clear

Each command in the history is preceded with an id. You can rerun the
command by executing the history command followed by the id::

   cm> history 101

You can also set a convenient variables so you do not have to remember
the number and can introduce labels for the history id that you can
easier remember::

   cm> var mylabel=101

If you now type::

   cm> history $mylabel

It will start the command associated with the 101 id in the


Managing Security Groups
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Managing Volumes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Managing heat's for OpenStack
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

(Jonathan)




Managing Security Groups
----------------------------------------------------------------------


::

   cm> security group add <label> <parameters>

::

   cm> security group delete

::

   cm> security group default add <label>

::

   cm> security group default delete <label>


Examples
----------------------------------------------------------------------

The goal of this example is to .....

multiple vms, multiple clouds
configuration

starting vms

listing status of all started vms across all clouds

ssh login -> can not be done with python sha but must be done with os.system




TODO (most likely in cloud command and register command)
----------------------------------------------------------------------

What does this do?::

   cm> manage initialize --user<name> --password <password>

* connects to FG and retrieves important information for you to use
* uses an ssh connection to connect to a FG service to retrieve the
  information
* if the connection is refused n=5 times within the hour the
* account is disabled
* if the command is called more than 10 times a day the account is disabled

Lists the resources available for the user::

   cm> resource --list

List the services in the cloud mesh::

   cm> service --list

See fg-inventory::

   cm> service register

See fg-inventory::

   cm> resource register


List all ids and their types::

   cm id --list

Associates a human readable lable with an id::

   cm label --id <id>


.. warning:: 

   The following commands are automatically created with `fab doc.man`
   If you like to update them, please do not do this in the man.rst
   file, but update the commands in the actual manual page in the code


