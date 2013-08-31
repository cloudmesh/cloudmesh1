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

    $ python virtualenv.py --system-site-packages ENV


..

If the result does not provide the path followed by
virtualenv, it is installed, you can do::
         
    $ virtualenv ENV

          
Activate virtualenv
------------------------

After installation of virtualenv, you can activate virtualenv by
following command::

    $ source ENV/bin/activate

Please note that you have to do this every time you open a terminal or login on the computer you work. Often you may forget it, so we recommend that you put it in your .bash_profile page at the end. 
    
Modify your rc file (optional):
------------------------

Go to your home directory, log in and change your .bash_profile,
.bashrc, or .bash_login file (e.g. whatever works best for you). ON my computer I added it to the .bash_profile which is a MAC OSX machine::

    $ echo "source ENV/bin/activate" >> .bash_profile


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

    $ git clone git@github.com:cloudmesh/cloudmesh.git
    $ cd cloudmesh
    $ cd install
    $ fab deploy
    $ fab install
    $ cd ..

YAML files
---------------

You will need three yaml files. Samples can be found in the etc source directory. 
More elaborate examples can be obtained from Gregor for the personel that work 
directly with him on FutureGrid.

Configure the yaml files if changes need to be done.

Mongo
---------------

To managing mongo db it is important that you use our special fabric commands fro doing so
To start mongod do::

	fab mongod.start

To stop mongod::

	fab mongod.stop
	
To clean the entire data base (not just the data for cloudmesh, so be careful) say::

	fab mongo.clean
	
To create a simple cluster without usernames, say::

	fab mongo.simple
	
To create a cluster with user data base say::

	fab mongo.cloud
	
Now you have data in the mongo db and you can use and test it

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

     ssh -L 80:localhost:5000 gvonlasz@cm 

Once you have started cloudmesh, you will be able to see the page form that server in the browser at::

      http://localhost:5001

However, before you start the server with 

    python setup.py install; fab server.start

it is best if you do an ssh agent so you can access some more sophisticated services that require authentication. To do so you can type in the following lines on the terminal in which you will start the server::

   $  eval `ssh-agent -s`
   $ ssh-add 


Unordered notes
=============


Sphinx autorun
------------------------------


This package is only needed if you like to generate the documentation. Most developers will want to install it::

    $ hg clone http://bitbucket.org/birkenfeld/sphinx-contrib/
    $ cd sphinx-contrib/autorun
    $ python setup.py install

Blockdiag family
------------------------------


TODO: this explanation is incomplete

To install these packages you need to execute::

    pip install "blockdiag[PDF]"
	pip install "rackdiag[PDF]"
	pip install nwdiag[PDF]"
	
The documentation to this package is located at 

* http://blockdiag.com/en/blockdiag/introduction.html#setup

blockdiag uses TrueType Font to render text. blockdiag try to detect installed fonts but if nothing detected, You can specify fonts with -f (–font) option::

    $ blockdiag -f /usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif.ttf simple.diag

If you always use same font, write $HOME/.blockdiagrc::

    $ cat $HOME/.blockdiagrc
    [blockdiag]
    fontpath = /usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif.ttf

TODO: distribute a standard ttf font and use sh so that the -f font is included from the deployed package

Ubuntu
------------

Minimal initial requirements, git, gcc, python-dev and virtualenv installed.  If
these are not in your base system you can run::

   $ sudo apt-get update
   $ sudo apt-get install gcc git python-dev python-virtualenv

Create a virtualenv for cloudmesh, activate it, and run::

    $ pip install fabric

Then clone the cloudmesh repository::

    $ git clone https://github.com/cloudmesh/cloudmesh.git

Then run::

    $ cd cloudmesh && fab -f install.fabfile.py deploy

TODO: Explain how the user gets their cloudmesh.yaml file.

Assuming there are no errors, run::

    $ fab server.start


Manual installation
^^^^^^^^^^^^^^^^^^^

Assuming a basic Ubuntu Desktop 13.04, install prerequsites::

   $ sudo apt-get install \
      git \
      curl \
      python-virtualenv \
      python-dev \
      libldap2-dev \
      libsasl2-dev



Install Mongo
^^^^^^^^^^^^^^^
Install from standard packages::

    $ sudo apt-get install mongodb

Note: the mongod process will by default try to use /data/db for its
database files.  We recommend using the --dbpath option to specify a
directory in your own home.  See start() method in fabfiles/server.py.

The first startup of mongod will take some time as it creates files in
the dbpath.  Unless these are deleted, subsequent startup times should
be much faster.


Install RabbitMQ
^^^^^^^^^^^^^^^^

Install from standard packages::

    $ sudo apt-get install rabbitmq-server


Sphinx autorun
^^^^^^^^^^^^^^^

TBD

Blockdiag family
^^^^^^^^^^^^^^^^^

TBD

CentOS
--------------------

Minimal initial requirements, git, python2.7, and virtualenv
installed.  If you don't have python2.7, see the manual installation
steps below.  The system will also need to be configure to use the
EPEL repo (for mongodb and rabbitmq).

Otherwise, create a virtualenv for cloudmesh, activate it, and run::

    $ pip install fabric

Then clone the cloudmesh repository::

    $ git clone https://github.com/cloudmesh/cloudmesh.git

Then run::

    $ cd cloudmesh && fab -f install.fabfile.py deploy

TODO: Explain how the user gets their cloudmesh.yaml file.

Assuming there are no errors, run::

    $ fab server.start


Manual installation
^^^^^^^^^^^^^^^^^^^

Assuming a basic CentOS 6.4 Server, install prerequsites::

    $ sudo yum install -y \
        git \
        wget \
        gcc \
        make \
        readline-devel \
        zlib-devel \
        openssl-devel \
        openldap-devel \
        bzip2-devel


Install Python
^^^^^^^^^^^^^^^

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

Install Python Virtualenv
^^^^^^^^^^^^^^^^^^^^^^^^^

Verify that python2.7 is active::

    $ python --version
    Python 2.7.5

If you see Python 2.6.6, fix your PATH to include /opt/python/bin before /usr/bin.::

    $ curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.10.1.tar.gzcd
    $ tar xfz virtualenv-1.10.1.tar.gz
    $ cd virtualenv-1.10.1.tar.gz
    $ sudo python setup.py install


Install Mongo
^^^^^^^^^^^^^^^
Intstall from EPEL packages::

    $ sudo yum install mongodb mongodb-server


Install RabbitMQ
^^^^^^^^^^^^^^^^

Intstall from EPEL packages::

    $ sudo yum install rabbitmq-server
    $ sudo service rabbitmq-server start


Sphinx autorun
^^^^^^^^^^^^^^^

TBD

Blockdiag family
^^^^^^^^^^^^^^^^^

TBD


Installing the source code
=============================

Create a virtualenv::

    $ virtualenv --no-site-packages cloudmesh_v

Note: the name of the virtualenv is your choice, it does not need to be called "cloudmesh_v."

Activate the virtualenv::

    $ . cloudmesh_v/bin/activate


From the shell checkout the code from the repository::

    git@github.com:cloudmesh/cloudmesh.git
    cd cloudmesh

Be sure you have activated your virtualenv, then::

    pip install -r requirements.txt

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


