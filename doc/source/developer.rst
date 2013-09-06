.. sectnum::
   :start: 3

**********************************************************************
Quickstart for a deployed version of cloudmesh
**********************************************************************

The following are the current steps to bring all services fro
cloudmesh up and running. Naturallky we could have included them in
one script, which we will do at a later time. For now we want o keep
the services seperate to ease debugging of various parts. It is
assumed that the machine has access to LDAP.

::

    python setup.py install
    fab mongo.start
    fab mongo.cloud     # if thsi does not work use fab mongo.simple
    fab mq.start
    fab queue.start:True
    fab server.start
    

**********************************************************************
Installation
**********************************************************************



Next we describe the installation for developers. However it is much the same as for those that want to deploy it.

Pip
====

We do not use easy_install, but pip instead. Please make sure that you install pip. In most cases this can be done with::

     easy_install pip 

Once installed we will typically not use easy_install any more.


Virtualenv
================

As we like to have an isolated development environment we require that
you use virtualenv. For simplicity our virtual env will be placed in
the home directory under ~/ENV. If you already have such a directory
for other projects, we suggest that you find a new name for the
virtualenv. However, for the rest of the manual we assume it is "ENV"

Download virtualenv
------------------------

This step is only needed if virtualenv is not installed. To
test this say::

    $ which virtualenv

In case virtualenv is not installed, you can download it for example
with::

    $ wget https://raw.github.com/pypa/virtualenv/master/virtualenv.py
 
Install virtualenv
------------------------
        
After you downloaded virtualenv, you can install it by following
command::

    $ python virtualenv.py --system-site-packages ~/ENV


Once that is accomplished you can create a virtual env as follows in the
directory ENV:
         
    $ virtualenv ~/ENV

          
Activate virtualenv
------------------------

After installation of virtualenv, you can activate virtualenv by
following command::

    $ source ~/ENV/bin/activate

Please note that you have to do this every time you open a terminal or login on the computer you work. Often you may forget it, so we recommend that you put it in your .bash_profile page at the end. 
    
Modify your rc file (optional):
------------------------

Go to your home directory, log in and change your .bash_profile,
.bashrc, or .bash_login file (e.g. whatever works best for you). ON my computer I added it to the .bash_profile which is a MAC OSX machine::

    $ echo "source ~/ENV/bin/activate" >> .bash_profile


Install fabric
==================================================================

Much of our setup scripts are using fabric which is a nice management tool and is for our purpose a fancy makefile like tool (with many additional feature). To install it, please say::

    pip install fabric

Github
=======

Next we need to make sure github is properly usable for you. First you need to get an account on github and make sure you have a gravatar. Without this you can not become a developer. Than please contact Gregor von Laszewski (laszewski@gmail.com) so you can be added to the github dev list.

In order for you to participate in code development you also need to do the following steps on **ANY** machine from which you like toc check code back into github.


GIthub ssh keys
------------------

If you are on a new machine you must create a new github ssh key for
it. This is nicely described at

* https://help.github.com/articles/generating-ssh-keys

You must upload the key to github, either via a command, or simply via
the github gui. Simply go to your setting and find the ssh key menu
entry. Klick on it and upload your new key by pasting and copying the
public key. Make sure you do not copy the privat key. 


Git username and e-mail
------------------------------

It is very important to set the git username and e-mail. This can be
done with the following commands. you must use your full name and your
e-mail that you use with github as part of your registered
account. Otherwise our commits will not properly work::

    git config --global user.name "Gregor von Laszewski"
    git config --global user.email "laszewski@gmail.com"

Please replace name and e-mail with the once you used in Github. Please make sure your name is spelled out properly. We do not accept pseudonyms. If you do not agree to this, you can not participate in the code development.

Quick deployment on ubuntu
===========================

This quick deployment is targeted for ubuntu. It can be achieved in several easy steps.
First, obtain a vanilla ubuntu system. Make sure that git is installed, which is standard by now.
Next execute the following commands ::

    $ git clone https://github.com/cloudmesh/cloudmesh.git
    $ cd cloudmesh
    $ cd install
    $ fab deploy
    $ fab install
    $ cd ..

Note: ALternative may be better fab -f install/fabfile.py deploy

Requirements
------------

Although the install contains the automatic installation of
requirements, we like to point out that changes in the requirements.txt
file that you may do does require an installation with::

    pip install -r requirements.txt

If you do not change the requirements file, this step will be
automatically executed as part of the installation.

Additional Installation for Documentation Generation
======================================================================

To create the documentation locally, a couple of additional steps are
needed that have not yet been included into the install fab scripts.

The documentation depends on the autorun
package. This package can be downloaded and installed as follows::

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

YAML files
---------------

You will need four yaml files. Samples can be found in the etc source directory. 
More elaborate examples can be obtained from Gregor for the personel that work 
directly with him on FutureGrid.

Configure the yaml files if changes need to be done.

We need four files in the .futuregrid directory:

* cloudmesh.yaml
* cloudmesh_server.yaml
* cloudmesh_clutser.yaml
* cloudmesh_bootspec.yaml


Mongo
---------------

To managing mongo db it is important that you use our special fabric commands fro doing so
To start mongod do::

	fab mongo.start

To stop mongod::

	fab mongo.stop
	
To clean the entire data base (not just the data for cloudmesh, so be careful) say::

	fab mongo.clean
	
To create a simple cluster without usernames, say::

	fab mongo.simple
	
To create a cluster with user data base say::

	fab mongo.cloud
	
Now you have data in the mongo db and you can use and test it

RabbitMQ
---------






Developer Tests
-----------------

Python has a very good unit test framework called nosetests. As we have many different tests it is sometimes useful not to run all of them but to run a selected test. Running all of the tests would take simply to long during debugging. We are providing an easy to use test fabric command that can be used as follows. Assume that in your directory tests are located a number of tests. They can be listed with::

    $ fab test.info 

This will list the available test files/groups by name (the test_ prefix is omitted). To list the individual tests in a file/grou, you can use it as a parameter to info. Thus::

   fab test.info:compute 

will list the tests in the file test_compute.py. To call an individual test, you can use the name of the file and a unique prefix of the test you like to call via test.start. Thus::


     fab test.start:compute,label

will execute the test which has label in its method name first




Working with Cloudmesh on a remote server
==============================

Sometimes it is desirable to work on cloudmesh on a remote server and use your laptop to connect to that server. This can be done for example via port forwarding. Let us assume you are running a cloudmesh server on the machine my.org. Than you can establish a port forwarding from port 5000 to 5001 as follows, where 5001 is the locally used port::

     ssh -L 5001:localhost:5000 user@machine.edu

Once you have started cloudmesh, you will be able to see the page form that server in the browser at::

      http://localhost:5001

However, before you start the server with 

    python setup.py install; fab server.start

it is best if you do an ssh agent so you can access some more sophisticated services that require authentication. To do so you can type in the following lines on the terminal in which you will start the server::

   $  eval `ssh-agent -s`
   $ ssh-add 







CentOS
================================================================

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

::

    $ sudo service rabbitmq-server start


Aptana Studio
=============================

from Aptana Studio:

	Aptana studio contains an import function which is convenient for importing it directly from github.

Cleaning
=========

sometimes it is important to clean things and start new. This can be done by ::

    fab clean.all


Convenient command shortcuts
=================================

We are providing a number of useful command that will make your development efforts easier.  These commands are build with fabfiles in the fabfile directory. in the cloudmesh directory, you will find a directory called fabfile that includes the agglomerated helper files. To access them you can use the name of the file, followed by a task that is defined within the file. Next we list the available commands:

.. runblock:: console

   $ fab -l 



Starting and testing the Queue Service
----------------------------------------------------------------------

To start the queue service please use the command::

    fab queue.start:True

This will start the necessary background services, but also will shut
down existing services. Essentially it will start a clean development
environment. To start a service you can use::

   fab server.start:/provision/summary/

Which starts the server and goes to the provision summary page

There is also a program called t.py in the base dir, so if you say::

    python t.py
   
and refresh quickly the /provision/summary page you will see some
commands queued up. The commands have random state updates and are very
short as to allow for a quick debugging simulation. One could add the
refresh of the web page automatically to other test programs.


In virtualenv we did:

pip install -r requirements.txt
pip install python-novaclient

sudo aptitude install mongodb

lsb_release -a
No LSB modules are available.
Distributor ID:    Ubuntu
Description:    Ubuntu 12.10
Release:    12.10
Codename:    quantal


Making the documentation
====================

::

    fab doc.html
    fab doc.view


   
Basic Configuration
--------------------

open a new terminal and type in::

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
	
	
If you like to start with a particular route, you can pass it as parameter.

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



