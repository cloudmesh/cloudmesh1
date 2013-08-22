Documentation 
==============

::

    $ hg clone http://bitbucket.org/birkenfeld/sphinx-contrib/
    $ cd sphinx-contrib/autorun
    $ python setup.py install

Developmnet Version
===============

New way

window 1::

	mongod

window 2::

	fab queue.start:1

window 3::

	fab server.start

Other way
===========

Checkout the code from the repository::

    git@github.com:cloudmesh/cloudmesh.git
    cd cloudmesh
    pip install -r requirements.txt

Start mongod::

    $ mongod

Create a test cluster::

    $ fab server.fg

This will print something like (if everything is ok)::

        clusters: 5 -> bravo, delta, gamma, india, sierra
        services: 0
        servers: 304
        images: 2 -> centos6, ubuntu

To start the service you can say::

    $ fab server.start

You can repeatedly issue that command and it will shut down the server. If you want to do thia by hand you can do this with::

    $ fab server.stop

Note that when you edit anything related to the Fabric datatypes, you will most likely hav to recreate the test cluster data. DO this agian with::

    $ fab server.fg

And than start the server as descripbed above.


Convenient command shortcuts
----------------------------------------------------------------------

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

Ubuntu
======


apt-get install \
 python-virtualenv \
 python-dev \
 libsasl2-dev \
 python-ldap \
 libldap2-dev \
 ldap-devel \
 ldap-client \
 mongodb

In virtualenv we did:

pip install -r requirements.txt
pip install python-novaclient





