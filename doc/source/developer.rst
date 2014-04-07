.. sidebar:: Page Contents

   .. contents::
      :local:


.. sectnum::
   :start: 7

**********************************************************************
Usage Quickstart 
**********************************************************************

The following are the current steps to bring all services for
cloudmesh up and running. After you have Installed the software (see
). Naturally we could have included them in the Section `ref:s-instalation`
one script, which we will do at a later time. For now we want o keep
the services separate to simplify development and debugging of various
parts. Naturally, if you can just pick the commands that you really
need and do not have to execute all of them. Over time you will notice
which commands are needed by you. An overview of available commands
can be found with::

   $ fab -l


With access to LDAP 
===============
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
===============

::

    fab build.install
    fab mongo.start
    fab mongo.simple
    fab user.mongo
    # fab mq.start
    # fab queue.start:1
    fab hpc.touch
    fab server.start

.. _s-instalation:

**********************************************************************
Installation
**********************************************************************

In this Section, we describe how to  deploy cloudmesh for
**developers**. It is much the same as for those that want to deploy
it. 

Pip
====

We typically do not use easy_install, but use pip instead. Please make
sure that you install pip. THis can be done with::

    $ sudo easy_install pip 

Once installed we will typically not use easy_install any more. If you do not have easy_install setup previously you might have to set it up. It can be done as follows::

    $ sudo apt-get install python-setuptools

Virtualenv
================

As we like to have an isolated development environment we require that
you use virtualenv. For simplicity our virtual env will be placed in
the home directory under ~/ENV. If you already have such a directory
for other projects, we suggest that you find a new name for the
virtualenv. However, for the rest of the manual we assume it is "ENV"

Install virtualenv
------------------------

This step is only needed if virtualenv is not installed. To
test this say::

    $ which virtualenv

In case virtualenv is not installed, you can install it via pip::


    $ sudo pip install virtualenv

Once that is accomplished you can create a virtual env as follows in
the directory ENV::
         
    $ virtualenv  --no-site-packages ~/ENV

If you do not have root access you can install it from source as
documented at 

* http://www.virtualenv.org/en/latest/
          
Activate virtualenv
------------------------

After installation of virtualenv, you can activate virtualenv by
following command::

    $ source ~/ENV/bin/activate

Please note that you have to do this every time you open a terminal or login on the computer you work. Often you may forget it, so we recommend that you put it in your .bash_profile or .bashrc page at the end. 
    
Modify your rc file (optional):
------------------------

Go to your home directory, log in and change your .bash_profile, 
.bashrc, or .bash_login file (e.g. whatever works best for you). ON my computer I added it to the .bash_profile which is a MAC OSX machine::

    $ echo "source ~/ENV/bin/activate" >> .bash_profile

On ubuntu, you can add it to::

  $ echo "source ~/ENV/bin/activate" >> .bashrc

If in doubt add it to both. It will be up to you to decide if you like
to go into virtual env at login time. If you do it this way you do not
forget. You can also add a ``cd`` command so that you go into the
working directory immediately after you login. For example when you
check out cloudmesh to ~/github/cloudmesh you can add::

   cd ~/github/cloudmesh

SO you jump into your working directory after you start a new
terminal, which is quite handy. Alternatively, you may want to set an
alias such as::

   alias dev="cd ~/github/cloudmesh"

This way if you type dev you cd into the development directory


Install fabric
===========================================================

Much of our setup scripts are using fabric which is a nice management tool and is for our purpose a fancy makefile like tool (with many additional feature). This tool(and several other packages) use the python-dev package. If you do not have it installed already you can get by doing the following::

    $ sudo apt-get install python-dev

Fabric can now be installed as follows::

    $ pip install fabric

Github
=======

Next we need to make sure github is properly usable for you. First you need to get an account on github and make sure you have a gravatar. Without this you can not become a developer. Than please contact Gregor von Laszewski (laszewski@gmail.com) so you can be added to the github dev list.

In order for you to participate in code development you also need to do the following steps on **ANY** machine from which you like toc check code back into github. If you do not have git on your machine you can get by::

    $ sudo apt-get install git

Github ssh keys
------------------

If you are on a new machine you must create a new github ssh key for
it. This is nicely described at

* https://help.github.com/articles/generating-ssh-keys

You must upload the key to github, either via a command, or simply via
the github gui. Simply go to your setting and find the ssh key menu
entry. Click on it and upload your new key by pasting and copying the
public key. Make sure you do not copy the privat key. 


Git username and e-mail
------------------------------

It is very important to set the git username and e-mail. This can be
done with the following commands. You must use your full name and your
e-mail that you use with github as part of your registered
account. Otherwise our commits will not properly work::

    git config --global user.name "Gregor von Laszewski"
    git config --global user.email "laszewski@gmail.com"

Please replace name and e-mail with the once you used in Github. Please make sure your name is spelled out properly. We do not accept pseudonyms. If you do not agree to this, you can not participate in the code development.


Quick deployment 
===========================

This quick deployment is targeted for ubuntu. It can be achieved in several easy steps.
First, obtain a vanilla ubuntu system. Make sure that git is installed, which is standard by now.

Note: that on osx we have to set the ldflags to get to the ttfonts


OSX

::

  xcode-select --install

  ??? does not work

::

  LDFLAGS="-L/usr/local/opt/freetype/lib -L/usr/local/opt/libpng/lib" CPPFLAGS="-I/usr/local/opt/freetype/include -I/usr/local/opt/libpng/include -I/usr/local/opt/freetype/include/freetype2" pip install matplotlib 

Next execute the following commands ::

    $ git clone git@github.com:cloudmesh/cloudmesh.git
    $ cd cloudmesh
    $ fab -f install/fabfile.py deploy
    $ fab build.install

Some developers may prefer using https for accessing git::

    $ git clone https://github.com/cloudmesh/cloudmesh.git

We recommend that you use the non https version if you are part of the
development team as it is much faster.

Aptana Studio
--------------------------------------------------

A good IDE for python development for Python is Aptana Studio (based
on eclypse). It contains the ability to directly import packages from
github by filling out a simple form. So instead of using the
command line github tool you can use the Aptana Studio version. It
also contains a very nice way of managing your commits while allowing
you to select via a GUI the files you have changed and commit them
with a nice commit message. Pull and Push functions are also
available. HAving said that there is some advantage of using the
Aptana GUI tools for git as it makes it easier. Aptana Studio has also the
ability to use emacs key mappings, which is a real nice
feature. Naturally not all of emacs is supported.

For those new to python an the project we recommend you use it for development.


Requirements
------------

Although the install contains the automatic installation of
requirements, we like to point out that changes in the requirements.txt
file that you may do does require an installation with::

    pip install -r requirements.txt

If you do not change the requirements file, this step will be
automatically executed as part of the installation.

YAML files
---------------

You will need a number of  yaml files. Samples can be found in the etc source directory. 
More elaborate examples can be obtained from Gregor for the personel that work 
directly with him on FutureGrid.

Configure the yaml files if changes need to be done.

We to copy and modify the files in the .futuregrid directory. THis has
to be done only once, but you maust make sure you keep the yaml files
up to date in case we change them, typically we send an e-mail to all
develpers when a change occured so you can update yours:

* `cloudmesh.yaml <https://github.com/cloudmesh/cloudmesh/blob/master/etc/cloudmesh.yaml>`_
* `cloudmesh_server.yaml <https://github.com/cloudmesh/cloudmesh/blob/master/etc/cloudmesh_server.yaml>`_
* `cloumesh_cluster.yaml (ask Gregor)
* `cloumesh_launcher.yaml <https://github.com/cloudmesh/cloudmesh/blob/master/etc/cloudmesh_launcher.yaml>`_
* `cloumesh_bootspec.yaml <https://github.com/cloudmesh/cloudmesh/blob/master/etc/cloudmesh_bootspec.yaml>`_

Generating a cloudmesh.yaml file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To generate a simple cloudmesh.yaml file, you may want to use place
the following contents (with modifications applying to you), in a file
called ~/.futuregrid/me.yaml. In that file, please replace the
appropriate values with your cloud information. If you do not knwo the
values you can just fill in a placeholder, such as None. With active
we specify the clouds that we like to activate. Clouds not listed in
activate will be ignored::

    meta:
      kind: me
      yaml_version: 1.2

    portalname: gvonlasz

    profile:
	firstname: Gregor
	lastname: von Laszewski
	e-mail: gvonlasz@gmail.com  

    active:
    - sierra_openstack_grizzly

    password:
      sierra_openstack_grizzly: mypassword

    azure:
      subscriptionid: None

    aws: 
      access_key_id: None
      secret_access_key: None
      userid: None

    projects:
      default: fg82
      active:
      - fg82
      - fg101
      completed:
      - fg130
    keys:
      fg_0: ssh-rsa ABCD .... fg-0
      fg_1: ssh-rsa VWXY .... fg-1

Than you can print the contents of the yaml file that this input
generets to the stdout with::

    fab user.yaml

ERROR: not that this prints a Done. msg at the end so if you redirect
it to ~/.futuregrid/cloudmesh.yaml you need to correct this.

WARNING: If you have a working yaml file, than I suggest you copy this
first into a backup before overwriting somthing that worked befor ;-)

In future we will have::

   fab user.yaml,safe

which safes this into ~/.futuregrid/cloudmesh.yaml and

   fab user.verify

which will verify if you can log into the clouds with your credentials

WARNING: fab user.verify, and    fab user.yaml,safe are not yet implemented

Mongo - Commands Overview
--------------------------

Cloudmesh uses mongo for serving information to the different
services.  To managing mongo db it is important that you use our
special fabric commands in order to make sure that the database is
properly initialized and managed. We make this real simple:

To start mongod do::

	fab mongo.start

To stop mongod::

	fab mongo.stop
	
To clean the entire data base (not just the data for cloudmesh, so be careful) say::

	fab mongo.clean
	
To create a simple cluster without usernames, say::

	fab mongo.simple
	
To create a cluster with user data base say (requires access to LDAP)::

	fab mongo.cloud
	
Now you have data in the mongo db and you can use and test it.

Mongo commands that need to be issued
---------------------------------------

In order for the everything to work right, please do the following mongo steps.::

    fab mongo.start
    fab mongo.boot
    fab mongo.simple
    fab user.mongo

Starting the Web Service
----------------------

To start a service you can use::

   fab server.start:/provision/summary/

Which starts the server and goes to the provision summary page. If you
just use::

   fab server.start

It will be just starting at the home page.


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
------------------------------

blockdiag uses TrueType Font to render text. blockdiag try to detect installed fonts but if nothing detected, You can specify fonts with -f (–font) option::

    $ blockdiag -f /usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif.ttf simple.diag

If you always use same font, write $HOME/.blockdiagrc::

    $ cat $HOME/.blockdiagrc
    [blockdiag]
    fontpath = /usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif.ttf

TODO: distribute a standard ttf font and use sh so that the -f font is included from the deployed package

The t.py program
---------------

(May not work)

There is also a program called t.py in the base dir, so if you say::

    python t.py
   
and refresh quickly the /provision/summary page you will see some
commands queued up. The commands have random state updates and are very
short as to allow for a quick debugging simulation. One could add the
refresh of the web page automatically to other test programs.

Developer Tests
-----------------

Python has a very good unit test framework called nosetests. As we have many different tests it is sometimes useful not to run all of them but to run a selected test. Running all of the tests would take simply to long during debugging. We are providing an easy to use test fabric command that can be used as follows. Assume that in your directory tests are located a number of tests. They can be listed with::

    $ fab test.info 

This will list the available test files/groups by name (the test_ prefix is omitted). To list the individual tests in a file/grou, you can use it as a parameter to info. Thus::

   fab test.info:compute 

will list the tests in the file test_compute.py. To call an individual test, you can use the name of the file and a unique prefix of the test you like to call via test.start. Thus::


     fab test.start:compute,label

will execute the test which has label in its method name first


Cleaning
=========

sometimes it is important to clean things and start new. This can be done by ::

    fab clean.all

After that you naturally need to do a new install. 
``fab server.start`` automatically does such an install for you.



Convenient command shortcuts
=================================

We are providing a number of useful command that will make your development efforts easier.  These commands are build with fabfiles in the fabfile directory. in the cloudmesh directory, you will find a directory called fabfile that includes the agglomerated helper files. To access them you can use the name of the file, followed by a task that is defined within the file. Next we list the available commands:

.. runblock:: console

   $ fab -l 



Working with Cloudmesh on a remote server
==============================

Sometimes it is desirable to work on cloudmesh on a remote server and use your laptop to connect to that server. This can be done for example via port forwarding. Let us assume you are running a cloudmesh server on the machine my.org. Than you can establish a port forwarding from port 5000 to 5001 as follows, where 5001 is the locally used port::

     ssh -L 5001:localhost:5000 user@machine.edu

Once you have started cloudmesh, you will be able to see the page form that server in the browser at::

      http://localhost:5001

However, before you start the server with::

    python setup.py install; fab server.start

it is best if you do an ssh agent so you can access some more sophisticated services that require authentication. To do so you can type in the following lines on the terminal in which you will start the server::

   $  eval `ssh-agent -s`
   $ ssh-add 



Special notes for CentOS
============================================================

Minimal initial requirements, git, python2.7, and virtualenv
installed.  If you don't have python2.7, see the manual installation
steps below.  The system will also need to be configure to use the
EPEL repo (for mongodb and rabbitmq).


Install Python
------------------------------

Cloudmesh requires python 2.7, and CentOS comes with Python 2.6.
However we cannot replace the system python as yum and other tools
depend on it, so we will configure it to install in /opt/python::

    $ wget http://www.python.org/ftp/python/2.7.5/Python-2.7.5.tgz

Recommended: verify the md5 checksum, b4f01a1d0ba0b46b05c73b2ac909b1df for the above.::

    $ tar xzf Python-2.7.5.tgz
    $ cd Python-2.7.5
    $ configure --prefix=/opt/python && make
    $ sudo make install

Edit your ~/.bash_profile to add /opt/python/bin to the start of your
PATH, then log out and back in.


Starting the  RabbitMQ service
------------------------------

On centos rabbit mq can be started as a service with as follows::

    $ sudo service rabbitmq-server start

Note: I am not yet sure if this is needed for development, this is
probably good at deployment. I am not sure about default
values. 


Making the documentation
====================

A simple way to creat ethe documentation is with::

   fab doc.html


However, some extensions may require additional packages for sphinx.
These add ons are unfortunatly not included in the requirements.txt. 
However, they can be installed with (on OSX hg is a prerequisit)::

   $ fab build.sphinx

After that you can create the newest documentation with::

    $ fab doc.html

To view it just say::

    $ fab doc.view

To publish to github::

    $ fab doc.gh
   
Example: Start the GUI for development
--------------------

Open a new terminal and type in::

   fab mongo.start
   
Now you can either generate a simple cloud without user or a cloud with user information. 
To generating a simple cloud do without user information do::

   fab mongo.simple
   
This will print something like (if everything is ok) at the end::

        clusters: 5 -> bravo, delta, gamma, india, sierra
        services: 0
        servers: 304
        images: 2 -> centos6, ubuntu
   
To generate a complete cloud including users (requires access to LDAP) do::

    fab mongo.cloud

Next you can start the webui with::

	fab server.start    
	
	
If you like to start with a particular route, you can pass it as parameter::

    fab server.start:inventory
    
opens the page 

*    http://localhost:5000/inventory 

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
===================

In case you do not need to work with a cloud, you can also use our hpc
queue server. That inspects certain queues. This can be done by
specifing a specific server at startup called hpc::

    $ fab server.start:server=hpc


ENVIRONMENT
==========

::

    deactivate
    cd
    virtualenv --no-site-packages ENV

open a new terminal 

::

    $ pip install numpy matplotlib fabric
    $ git clone git@github.com:cloudmesh/cloudmesh.git
    $ cd cloudmesh
    $ fab -f install/fabfile.py deploy
    $ fab build.install

    
HPC services::

   fab hpc.touch

   logs into
   alamo
   india
   sierra
   foxtrot
   hotel

   is neede fo the hpc commands
