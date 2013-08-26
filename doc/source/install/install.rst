.. sectnum::
   :start: 2

Operating System Preparation
================================

In this Section we summarize some important packages that need to be installed in order to run cloudmesh.


OSX
----------

TODO: lots of missing 

Install Mongo
^^^^^^^^^^^^^^^



Install RabbitMQ
^^^^^^^^^^^^^^^^

TBD

Sphinx autorun
^^^^^^^^^^^^^^^

This package is only needed if you like to generate the documentation. Most developers will want to install it::

    $ hg clone http://bitbucket.org/birkenfeld/sphinx-contrib/
    $ cd sphinx-contrib/autorun
    $ python setup.py install

Blockdiag family
^^^^^^^^^^^^^^^^^

TODO: this expalanation is incomplete

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

Assuming a basic Ubuntu Desktop 13.04, install prerequsites::

   $ sudo apt-get install \
      git \
      curl \
      python-virtualenv \
      python-dev \
      libldap2-dev \
      libsasl2-dev

TODO: do we also have to do::

   (Allan did not need to do this, already in requirements.txt)
   $ pip install python-ldap

TODO: do we have to install ldap-user

   sudo apt-get install ldap-user


TODO: What is different for Ubuntu 12.04 ?
 
TODO: Do we need to test Ubuntu 10.04 ?


Install Mongo
^^^^^^^^^^^^^^^

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

Assuming a basic CentOS 6.4 Server, install prerequsites::

    $ sudo yum install git openldap-devel bzip2-devel


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

    $ curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-1.10.1.tar.gz
    $ tar xfz virtualenv-1.10.1.tar.gz
    $ cd virtualenv-1.10.1.tar.gz
    $ sudo python setup.py install


Install Mongo
^^^^^^^^^^^^^^^
Create /etc/yum.repos.d/10gen containing::

    [10gen]
    name=10gen Repository
    baseurl=http://downloads-distro.mongodb.org/repo/redhat/os/x86_64
    gpgcheck=0
    enabled=1

Then::

    $ sudo yum install mongo-10gen mongo-10gen-server


Install RabbitMQ
^^^^^^^^^^^^^^^^

Intstall from standard packages::

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

Activate the vitrualenv::

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

We are providing a number of useful command that will make your development efforts easier.  These commands are build with fablies in the fabfile directory. in the cloudmesh directory, you will find a diretcory called fabfile that includes the agglomerated helper files. To access them you can use the name of the file, followed by a task that is defined within the file. Next we list the available commands:

.. runblock:: console

   $ fab -l 

Creating the Documentation:
---------------------------

We assume you have autodoc installed for sphinx (see previously) it is
not in the requirements file, As I could not finss it in pypi

    mkdir /tmp/install-cloudmesh
    hg clone http://bitbucket.org/birkenfeld/sphinx-contrib/
    cd sphinx-contrib/autorun
    python setup.py install

    cd /tmp/install-cloudmesh

    git@github.com:cloudmesh/cloudmesh.git
    cd cloudmesh
    pip install -r requirements.txt

This will publish the documentation locally::

    fab doc.html

If you do::

    fab doc.gh

it will publish the page to gh-pages


Starting and testing the Queue Service
----------------------------------------------------------------------

To start the queue service please use the command::

    fab queue.start:True

This will start the necessary background services, but also will shut
down existing services. Essentially it will start a clean development
environment. To start a service you can use::

   fab server.start:/provision/summary/

Which starts the server oand gos to the provision summay page

There is also a program called t.py in the base dir, so if you say::

    python t.py
   
and refresh quickly the /provision/summary page you will see some
commands queed up. The commands hafe random state updates and aer very
short as to allow for a quick debuging simulation. One could add the
refresh of the web page automatically to other test programs.


In virtualenv we did:

pip install -r requirements.txt
pip install python-novaclient




sudo aptitude install libldap2-dev
sudo aptitude install libsasl2-dev
sudo aptitude install mongodb

lsb_release -a
No LSB modules are available.
Distributor ID:    Ubuntu
Description:    Ubuntu 12.10
Release:    12.10
Codename:    quantal


