.. sectnum::
   :start: 2

Development Installation 
================================

Preparing the system with basic software

Install Mongo
-------------

OSX: TBD 
^^^^^^^^^

TODO: lots of missing 

Install sphinx autorun::

    $ hg clone http://bitbucket.org/birkenfeld/sphinx-contrib/
    $ cd sphinx-contrib/autorun
    $ python setup.py install



Ubuntu: TBD (Allan)
^^^^^^^^^^^^^^^^^^^^

TODO:: lots missing

On ubuntu you need first tto install curl. This can be done with::

   $ sudo apt-get install curl


You also need to install ldap which you need to do with::

   $ sudo apt-get install python-dev libldap2-dev libsasl2-dev libssl-dev
   $ pip install python-ldap

CentOS: TBD (Allan)


Get/create the yaml files
--------------------------

TBD

Installing the source code
=============================

From the shell checkout the code from the repository::

    git@github.com:cloudmesh/cloudmesh.git
    cd cloudmesh
    pip install -r requirements.txt

from Aptana Studio:

	Aptana studio contains an import function which is convenient for importing it directly from github.

Cleaning
=========

sometimes it is important to clean things and start new. This can be done by ::

    fab clean.all






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




sudo aptitude install libldap2-dev
sudo aptitude install libsasl2-dev
sudo aptitude install mongodb

lsb_release -a
No LSB modules are available.
Distributor ID:    Ubuntu
Description:    Ubuntu 12.10
Release:    12.10
Codename:    quantal


Instalation
===========

Virtualenv
----------

Download virtualenv
^^^^^^^^^^^^^^^^^^^^^^

This step is only needed if virtualenv is not installed. To
test this say::

    $ which virtualenv

..

If the result does not provide the path followed by
virtualenv, it is installed, you can do::
         
    $virtualenv ENV

..

and skip step 2.
        
Since you do not have super user priviledges, you need virtualenv in
order to finish the installtion. You may download virtualenv.py by
following command::

    $ wget https://raw.github.com/pypa/virtualenv/master/virtualenv.py
 
Install virtualenv
^^^^^^^^^^^^^^^^^^^^^
        
After you downloaded virtualenv, you can install it by following
command::

    $ python virtualenv.py --system-site-packages ENV
          
Activate virtualenv
^^^^^^^^^^^^^^^^^^^^^^

After installation of virtualenv, you can activate virtualenv by
following command::

    $ source ENV/bin/activate
    
Modify your rc file (optional):
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Go to your home directory, log in your .bashrc,
.bash_profile, or .bash_login file and add::

    $ echo "source ENV/bin/activate" >> .bash_profile

..


This way you do not forget to type it in next time you 
login. Only do this if you are familar with .bash_profile.

