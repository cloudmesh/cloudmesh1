
.. _s-instalation:
**********************************************************************
Prepare the Environment 
**********************************************************************

In this Section, we describe how to  deploy cloudmesh for
**developers**. It is much the same as for those that want to deploy
it as users, however we provide additional information and set up
additional tools to make contributions easier. 

.. warning::

   Please read the entire manual before executing any of the commands
   listed below. Only if you understand the workflow and have become
   familiar with this manual you can follow the steps. If any step
   needs correction or better explanation, please get in contact with
   us with your improvement suggestions.

You will need to use **github** and **virtualenv**. We do **NOT**
support any use of cloudmesh without `virtualenv`.

Furthermore, we assume that you use **ubuntu 14.04** as your
development environment. Although we started including information for
other OS, we have not verified if they work.


Github
----------------------------------------------------------------------

This use of github assumes you are a development team member and have
direct access to the github repository. To become a member please
contact  Gregor von Laszewski at laszewski@gmail.com to discuss how
you can contribute to cloudmesh and if a membership is appropriate.

.. note::

   If you are not a member you still can check out the code from
   github and further develop it and communicate the changes to
   us. Please contact Gregor von Laszewski at laszewski@gmail.com.


First we need to make sure github is properly usable for you. First
you need to get an account on github and make sure you have a
gravatar. Without this you can not become a developer. Than please
contact Gregor von Laszewski (laszewski@gmail.com) so you can be added
to the github dev list.

In order for you to participate in code development you also need to
do the following steps on **ANY** machine from which you will
check code back into github. 

If you do not have git on your machine
you can get it as follows.

**Ubuntu**::

      $ sudo apt-get install git


**Centos/RHEL**::

       $ sudo yum install git


**OSX**:

Please obtain and install xcode as documented in 

1. https://developer.apple.com/xcode/downloads/

In a terminal window execute::
    
   $ xcode-select --install

This will opens a user interface dialog to request automatic
installation of the command line developer tools which you will need
if you like to conduct development on OSX. 


**Others**:

If you use a different operating system, please consult how to install
it there.


Github ssh keys
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you are on a new machine you must create a new github ssh key for
it. This is nicely described at

2. https://help.github.com/articles/generating-ssh-keys

You must upload the key to github, either via a command, or via
the github gui. Simply go to your setting and find the ssh key menu
entry. Click on it and upload your new key by copying and pasting the
public key. Make sure you do not copy the private key. 


Git username and e-mail
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is very important to set the git username and e-mail. This can be
done with the following commands. You must use your full name and your
e-mail that you use with github as part of your registered
account. Otherwise our commits will not properly work::

    $ git config --global user.name "Gregor von Laszewski"
    $ git config --global user.email "laszewski@gmail.com"

Please replace name and e-mail with the once you used in
Github. Please make sure your name is spelled out properly. We do not
accept pseudonyms. If you do not agree to this, you can not
participate in the code development.

Getting the Cloudmesh Source Code
----------------------------------------------------------------------

The code in github contains some convenient install scripts to prepare
your environment including the setup of the virtualenv. To have a
uniform environment among all developers we prefer if you clone the
cloudmesh code into `~/github`. Hence please do::

   $ mkdir ~/github
   $ cd ~/github

If this directory exists already, make an assessment if you can reuse it
for development.  Next the git repository needs to be cloned. It can
be done using::

    $ git clone git@github.com:cloudmesh/cloudmesh.git

Some developers may prefer using https for accessing git. If you are
not added in github with your github username to the project you will
see the following error::

  fatal: Could not read from remote repository.

  Please make sure you have the correct access rights
  and the repository exists.

In this case you should clarify with Gregor if you are added to the
github directory, or if you should checkout the code with the https
method::

    $ git clone https://github.com/cloudmesh/cloudmesh.git

For the rest of the section we will assume that you are working in the
cloudmesh directory. You can get there after cloning by ::
    
    $ cd cloudmesh

In some programs we need the location of the cloudmesh source for
development. Hence it is important to add the environment variable
`CLOUDMESH` to your shell. In bash you can do this with (assuming you
are in the cloudmesh directory)::

  $ export CLOUDMESH=`pwd`

Naturally, you can also add the location into your bashrc file so you
do not have to add it everytime to your shell.

To see if the `CLOUDMESH` variable has the correct value, you can
simply say::

  echo $CLOUDMESH

Preparing the system
----------------------------------------------------------------------

On a vanilla operating system a couple of packages and tools need to
be installed. For ubuntu and other OSes we have provided a simple
script that prepares the system.


For ubuntu systems there is a ready-made script to get all the 
pre-requisites install. To run this script do ::

    $ ./install system

    Note. 
    This command must be run as root or with superuser privileges. 

This will make sure all requirements are fulfilled and the cloudmesh
programs are installed in your environment.

After this you have to create and activate a virtual env.  As we like
to have an isolated development environment we require that you use
virtualenv. For simplicity our virtual env will be placed in the home
directory under `~/ENV`. If you already have such a directory for
other projects, you can use another name. However, for the rest of the
manual we assume it is "ENV"

To create the virtual env in `~/ENV`, run the following command ::

  $ virtualenv  --no-site-packages ~/ENV

After installation of virtualenv, you can activate the virtual env
with the following command::

    $ source ~/ENV/bin/activate

Please note that you have to do this every time you open a terminal or
login. Since it is easy to forget to do it, we recommend that you activate 
the virtualenv in your .bash_profile.

If you ever need to deactivate the virtual env, you can run::

    $ deactivate

from within the active virtualenv shell.

    
Modify your rc file:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::

   Changing your rc files is optional, but may be useful if you do a
   lot of development and you for example tend to forget to activate
   the virtualenv.

Go to your home directory, log in and change your .bash_profile,
.bashrc, or .bash_login file (e.g. whatever works best for you). ON my
computer I added it to the .bash_profile which is a MAC OSX machine::

    $ echo "source ~/ENV/bin/activate" >> .bash_profile

On ubuntu, you can add it to::

  $ echo "source ~/ENV/bin/activate" >> .bashrc

If in doubt add it to both. It will be up to you to decide if you like
to go into virtual env at login time. If you do it this way you do not
forget. You can also add a ``cd`` command so that you go into the
working directory immediately after you login. For example when you
check out cloudmesh to ~/github/cloudmesh you can add::

   cd ~/github/cloudmesh

So you jump into your working directory after you start a new
terminal, which is quite handy. Alternatively, you may want to set an
alias such as::

   alias dev="cd ~/github/cloudmesh"

This way if you type dev you cd into the development directory

Install the Requirements
----------------------------------------------------------------------

.. warning::

  Please remember to activate your virtualenv. Out of caution do not
  proceed or execute this command in your system environment.

In addition to the system packages we will now install into the
virtual env a number of python packages.
It is important to note that the requirements in requirements.txt must
be installed in a particular order. As pip does not support this
properly, we use the following command instead of simply calling `pip
install -r requirements.txt`::

  ./install requirements

Creating an initial user
----------------------------------------------------------------------

To create the initial user and cloudmesh yaml files you can use the
command::

  ./install new

From this point on you should be able to create the user manual
locally. IF this does not work you may have some error on your system
and you may carefully revisit the above instruction and locate the
error.



Initial Documentation
----------------------------------------------------------------------

An initial set of documentation can now be created with the command::

  fab doc.html


.. note::

   If this does not yet work you can do ::

      make sphinx

The documentation is located in::

  doc/build/html/index.html

please use your browser to open it. If you just run on ubuntu server,
you also need to install the ubuntu-desktop::

   sudo apt-get install ubuntu-desktop


Quickinstall the Environment
----------------------------------------------------------------------

We do not recommend that you conduct this quickinstall, but it may
provide you with a rough overview of the previous steps::

  git config --global user.name "yourname"
  git config --global user.email "youremail@example.com"

  git clone git@github.com:cloudmesh/cloudmesh.git
  cd cloudmesh
  ./install system
  virtualenv ~/ENV
  . ~/ENV/bin/activate
  ./install requirements
  ./install new
  fab doc.html

Please remember to use the ./ infront of the install as there could be
other install commands in your $PATH.

Configuration Details
======================================================================

Initial YAML files
----------------------------------------------------------------------

You will need a number of yaml files. Samples can be found in the etc/
source directory.  More elaborate examples can be obtained from Gregor
for the personnel that work directly with him on FutureGrid.

As we asume you have initially no yaml files, you can create a default
set with the command::

  ./install new

This will create a ~/.cloudmesh directory in which you can find and
modify the yaml files. Important is that you modify the file called
``me.yaml``

You find the values for the clouds from your cloud provider. Simply
add them and fill out your user information and you should be done.

.. note::

   When editing YAML files we strongly recommend that you use an
   editor with YAML support. YAML syntax is not complicated but is
   sensitive to proper indentation, and it is very helpful to have an
   editor that will assist with proper formatting.

This has to be done only once, but you must make sure you keep the
yaml files up to date. Typically we send an e-mail to all developers
when a change occurred so you can update yours:

#. `cloudmesh.yaml <https://github.com/cloudmesh/cloudmesh/blob/master/etc/cloudmesh.yaml>`_
#. `cloudmesh_server.yaml <https://github.com/cloudmesh/cloudmesh/blob/master/etc/cloudmesh_server.yaml>`_
#. `cloudmesh_cluster.yaml <https://github.com/cloudmesh/cloudmesh/blob/master/etc/cloudmesh_cluster.yaml>`_
   *For the one from FG please contact Gregor (only if you really need
   it. Normal users will not get this file).*
#. `cloumesh_launcher.yaml <https://github.com/cloudmesh/cloudmesh/blob/master/etc/cloudmesh_launcher.yaml>`_
#. `cloumesh_mac.yaml <https://github.com/cloudmesh/cloudmesh/blob/master/etc/cloudmesh_mac.yaml>`_


Install cloudmesh code
----------------------------------------------------------------------

Next you install the basic cloudmesh code which you can do with::

   $ ./install cloudmesh
..   $ fab build.install
..   "./install cloudmesh" -> deploy() -> ubuntu, centos, osx -> python install setup.py install
..   "fab build.install" -> ./install requirements -> python setup.py install

The cloudmesh.yaml file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

After updating the me.yaml file, you can generate a new cloudmesh.yaml
file. For this purpose you will need to copy the templates from cloudmesh to the ~/.cloudmesh directory::
  $ cp etc/*.yaml ~/.cloudmesh/etc
 
The command::

  $ cm-init fill --file=~/.cloudmesh/etc/cloudmesh.yaml ~/.cloudmesh/me.yaml

will test if the me.yaml file can successfully create a cloudmesh.yaml
file by printing its output. If no error occurs it will most likely be
fine. Then you can use the command::

  $ cm-init generate yaml

to create the cloudmesh yaml file from `~/.futuregird/me.yaml` and
write it to `~/.futuregird/cloudmesh.yaml`. Out of precaution we have
included a couple of questions that could be surpressed with the
`--force` option.


Mongo-Db
----------------------------------------------------------------------


List of Commands(Optional)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Cloudmesh uses mongo for serving information to the different
services.  To managing mongo db it is important that you use our
special fabric commands in order to make sure that the database is
properly initialized and managed. We make this real simple:

To start mongod do::

	fab mongo.start

To stop mongod::

	fab mongo.stop
	
To clean the entire data base (not just the data for cloudmesh, so be
careful) say::

	fab mongo.clean
	
To create a simple cluster without usernames, say::

	fab mongo.simple
	
To create a cluster with user data base say (requires access to LDAP)::

	fab mongo.cloud
	
Now you have data in the mongo db and you can use and test it.

Mongo commands that need to be issued (Important)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order for the everything to work right, please do the following
mongo steps.::

    fab mongo.start
    fab mongo.boot
    fab user.mongo
    fab mongo.simple

For some reason "fab mongo.boot" has to be issued twice for everything
to work right.

Starting the Web Service
----------------------------------------------------------------------

To start a service you can use. It will be just starting at the home page. ::

   fab server.start


Starting and testing the Queue Service
----------------------------------------------------------------------

Our framework uses rabbitMQ and Celery for managing asynchronous
processes. They require that additional services are running. This is
only important if you conduct development for dynamic provisioning and
our launcher framework. All others, probably do not need these
services. To start them simply say::

   $ fab mq.start

It will ask you for the system password as rabbitMQ runs system
wide. Next start the queue service with::

   $ fab queue.start:1

Now you are all set. and can access even the asynchronous queue services.
This will start the necessary background services, but also will shut
down existing services. Essentially it will start a clean development
environment. 

Configure the HPC Environment 
======================================================================

To use the HPC environment, you need to make sure you can login from
your machine to the various HPC login nodes. We have created a
convenient script for you that you can call as follows::
HPC services::

   fab hpc.touch

This script will log you into

*   alamo
*   india
*   sierra
*   foxtrot
*   hotel


Additional Installation for Documentation Generation
======================================================================

To create the documentation locally, a couple of additional steps are
needed that have not yet been included into the install fab scripts.

The documentation depends on the autorun package. This package can be
downloaded and installed as follows::

    $ cd /tmp
    $ mkdir autorun
    $ cd autorun
    $ hg clone http://bitbucket.org/birkenfeld/sphinx-contrib/
    $ cd sphinx-contrib/autorun
    $ python setup.py install

Blockdiag family
----------------------------------------------------------------------

blockdiag uses TrueType Font to render text. blockdiag try to detect
installed fonts but if nothing detected, You can specify fonts with -f
(–font) option::

    $ blockdiag -f /usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif.ttf simple.diag

If you always use same font, write $HOME/.blockdiagrc::

    $ cat $HOME/.blockdiagrc
    [blockdiag]
    fontpath = /usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif.ttf

TODO: distribute a standard ttf font and use sh so that the -f font is
included from the deployed package


Developer Tests
----------------------------------------------------------------------

Python has a very good unit test framework called nosetests. As we
have many different tests it is sometimes useful not to run all of
them but to run a selected test. Running all of the tests would take
simply to long during debugging. We are providing an easy to use test
fabric command that can be used as follows. Assume that in your
directory tests are located a number of tests. They can be listed
with::

    $ fab test.info 

This will list the available test files/groups by name (the test_
prefix is omitted). To list the individual tests in a file/grou, you
can use it as a parameter to info. Thus::

   fab test.info:compute 

will list the tests in the file test_compute.py. To call an individual
test, you can use the name of the file and a unique prefix of the test
you like to call via test.start. Thus::


     fab test.start:compute,label

will execute the test which has label in its method name first


Cleaning
======================================================================

sometimes it is important to clean things and start new. This can be done by ::

    fab clean.all

After that you naturally need to do a new install. 
``fab server.start`` automatically does such an install for you.



Convenient command shortcuts
======================================================================

We are providing a number of useful command that will make your
development efforts easier.  These commands are build with fabfiles in
the fabfile directory. in the cloudmesh directory, you will find a
directory called fabfile that includes the agglomerated helper
files. To access them you can use the name of the file, followed by a
task that is defined within the file. Next we list the available
commands:

.. runblock:: console

   $ fab -l 



Working with Cloudmesh on a remote server
======================================================================

Sometimes it is desirable to work on cloudmesh on a remote server and
use your laptop to connect to that server. This can be done for
example via port forwarding. Let us assume you are running a cloudmesh
server on the machine my.org. Than you can establish a port forwarding
from port 5000 to 5001 as follows, where 5001 is the locally used
port::

     ssh -L 5001:localhost:5000 user@machine.edu

Once you have started cloudmesh, you will be able to see the page form
that server in the browser at::

      http://localhost:5001

However, before you start the server with::

    python setup.py install; fab server.start

it is best if you do an ssh agent so you can access some more
sophisticated services that require authentication. To do so you can
type in the following lines on the terminal in which you will start
the server::

   $  eval `ssh-agent -s`
   $ ssh-add 



Special notes for CentOS
======================================================================

Minimal initial requirements, git, python2.7, and virtualenv
installed.  If you don't have python2.7, see the manual installation
steps below.  The system will also need to be configure to use the
EPEL repo (for mongodb and rabbitmq).


Install Python
----------------------------------------------------------------------

Cloudmesh requires python 2.7, and CentOS comes with Python 2.6.
However we cannot replace the system python as yum and other tools
depend on it, so we will configure it to install in /opt/python::

    $ wget http://www.python.org/ftp/python/2.7.5/Python-2.7.5.tgz

Recommended: verify the md5 checksum, b4f01a1d0ba0b46b05c73b2ac909b1df
for the above.::

    $ tar xzf Python-2.7.5.tgz
    $ cd Python-2.7.5
    $ configure --prefix=/opt/python && make
    $ sudo make install

Edit your ~/.bash_profile to add /opt/python/bin to the start of your
PATH, then log out and back in.


Starting the  RabbitMQ service
----------------------------------------------------------------------

On centos rabbit mq can be started as a service with as follows::

    $ sudo service rabbitmq-server start

Note: I am not yet sure if this is needed for development, this is
probably good at deployment. I am not sure about default
values. 


Making the documentation
======================================================================

A simple way to create the documentation is with::

   fab doc.html


However, some extensions may require additional packages for sphinx.
These add ons are unfortunately not included in the requirements.txt. 
However, they can be installed with (on OSX hg is a prerequisite)::

   $ fab build.sphinx

After that you can create the newest documentation with::

    $ fab doc.html

To view it just say::

    $ fab doc.view

To publish to github::

    $ fab doc.gh
   
Example: Start the GUI for development
----------------------------------------------------------------------

Open a new terminal and type in::

   fab mongo.start
   
Now you can either generate a simple cloud without user or a cloud
with user information.  To generating a simple cloud do without user
information do::

   fab mongo.simple
   
This will print something like (if everything is ok) at the end::

        clusters: 5 -> bravo, delta, gamma, india, sierra
        services: 0
        servers: 304
        images: 2 -> centos6, ubuntu
   
To generate a complete cloud including users (requires access to LDAP) do::

    fab mongo.cloud

Next you can start the cloudmesh Web with::

	fab server.start    
	
	
If you like to start with a particular route, you can pass it as parameter::

    fab server.start:inventory
    
opens the page 

9.    http://localhost:5000/inventory 

in your browser


You can repeatedly issue that command and it will shut down the server. 
If you want to do thia by hand you can do this with::

    $ fab server.stop
    
Sometimes you may want to say::

    killall python 
    
before you start the server. On ubuntu we found:::

    killall python;  server.start

works well

Example: HPC queue server
======================================================================

In case you do not need to work with a cloud, you can also use our hpc
queue server. That inspects certain queues. This can be done by
specifying a specific server at startup called hpc::

    $ fab server.start:server=hpc




Usage Quickstart 
======================================================================

The following are the current steps to bring all services for
cloudmesh up and running. After you have Installed the software (see
). Naturally we could have included them in the Section `ref:s-instalation`
one script, which we will do at a later time. For now we want to keep
the services separate to simplify development and debugging of various
parts. Naturally, if you can just pick the commands that you really
need and do not have to execute all of them. Over time you will notice
which commands are needed by you. An overview of available commands
can be found with::

   $ fab -l


With access to LDAP 
----------------------------------------------------------------------
It is assumed that the machine has access to LDAP.

::

    fab build.install
    fab mongo.start
    fab mongo.cloud     
    # fab mq.start
    # fab queue.start:1
    fab hpc.touch
    fab server.start
    
Without access to LDAP
----------------------------------------------------------------------

::

    fab build.install
    fab mongo.start
    fab mongo.simple
    fab user.mongo
    # fab mq.start
    # fab queue.start:1
    fab hpc.touch
    fab server.start



Cloudmesh deployment 
----------------------------------------------------------------------

yaml file first, than mongo

:: 

   fab mongo.install


Imports in cloudmesh_common
----------------------------------------------------------------------


The cloudmesh code contains a directory `cloudmesh_common` in which we
collect useful common reusable code that must not depend on an import
from cloudmesh. Thus no file in cloudmesh_common must include::

   import cloudmesh. ...

OSX System preparation Tips
----------------------------------------------------------------------

On OSX we recommend that you check if you have the freetype
fonts installed and set the LDFLAG as follows (if you find the
freetypes there)::

  LDFLAGS="-L/usr/local/opt/freetype/lib -L/usr/local/opt/libpng/lib" CPPFLAGS="-I/usr/local/opt/freetype/include -I/usr/local/opt/libpng/include -I/usr/local/opt/freetype/include/freetype2" pip install matplotlib 

Furthermore, since version 5.1 of XCode you may see the following error when
installing pycrypto on OSX::

  clang: error: unknown argument: '-mno-fused-madd' [-Wunused-command-line-argument-hard-error-in-future]

  clang: note: this will be a hard error (cannot be downgraded to a warning) in the future

  error: command 'cc' failed with exit status 1

This error can be fixed by ignoring the option with the following
shell commands::

   export CFLAGS=-Qunused-arguments
   export CPPFLAGS=-Qunused-arguments
