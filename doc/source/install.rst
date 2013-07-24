Documentation 
==============

    $ hg clone http://bitbucket.org/birkenfeld/sphinx-contrib/
    $ cd sphinx-contrib/autorun
    $ python setup.py install

Developmnet Version
===============

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
