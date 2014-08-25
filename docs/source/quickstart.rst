Quick Start on your desktop
============================

- CloudMesh requires Python 2.7 or higher.
- Ubuntu 14.04 and OSX tested.

If you have git, the easy way to download CloudMesh is::
   
  $ git clone https://github.com/cloudmesh/cloudmesh.git

Using virtualenv, you have isolated spaces for python packages.
It is recommended in the CloudMesh installation::

  $ virtualenv ~/ENV
  $ source ~/ENV/bin/activate

The following commands install required packages of CloudMesh::

  $ cd cloudmesh
  $ ./install system
  $ ./install requirements
  $ ./install new

To get access to IaaS cloud platforms, you need to apply your credentials to
cloudmesh by the following step::
  $ ./install rc fetch
  $ ./install rc fill

In the FutureGrid resources, you need SSH access to india.futuregrid.org,
sierra.futuregrid.org with your private key. you can test ssh login like this::

  $ ssh [username]@india.futuregrid.org
  $ ssh [username]@sierra.futuregrid.org


You install cloudmesh and mongodb database::

  $ ./install cloudmesh
  $ fab mongo.start
  $ fab mongo.boot
  $ fab user.mongo
  $ fab mongo.simple

Web interface can be started at http://127.0.0.1:5000 by::

  $ fab server.start

Commands only without description
---------------------------------

::

  $ git clone https://github.com/cloudmesh/cloudmesh.git
  $ virtualenv ~/ENV
  $ source ~/ENV/bin/activate
  $ cd cloudmesh
  $ ./install system
  $ ./install requirements
  $ ./install new
  $ ./install rc fetch
  $ ./install rc fill
  $ ssh [username]@india.futuregrid.org
  $ ssh [username]@sierra.futuregrid.org
  $ ./install cloudmesh
  $ fab mongo.start
  $ fab mongo.boot
  $ fab user.mongo
  $ fab mongo.simple
  $ fab server.start

