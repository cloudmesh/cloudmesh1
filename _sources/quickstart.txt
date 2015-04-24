Quick Start on your desktop
============================

- CloudMesh requires Python 2.7 or higher.
- Ubuntu 14.04 and OSX tested.

If you have git, the easy way to download CloudMesh is::
   
  git clone https://github.com/cloudmesh/cloudmesh.git

Using virtualenv, you have isolated spaces for python packages.
It is recommended in the CloudMesh installation::

  virtualenv ~/ENV
  $ source ~/ENV/bin/activate

The following commands install required packages of CloudMesh::

  cd cloudmesh
  ./install system
  ./install requirements
  ./install new

To get access to IaaS cloud platforms, you need to apply your credentials to
cloudmesh by the following step::

  ./install rc fetch
  ./install rc fill

In the FutureGrid resources, you need SSH access to india.futuregrid.org,
sierra.futuregrid.org with your private key. you can test ssh login like this::

  ssh [username]@india.futuregrid.org
  ssh [username]@sierra.futuregrid.org


You install cloudmesh and mongodb database::

  ./install cloudmesh
  fab mongo.start
  fab mongo.boot
  fab user.mongo
  fab mongo.simple

Web interface can be started at http://127.0.0.1:5000 by::

  fab server.start

Command line tool can be tested by::

  cm
  
  ======================================================
  / ___| | ___  _   _  __| |_ __ ___   ___  ___| |__
  | |   | |/ _ \| | | |/ _` | '_ ` _ \ / _ \/ __| '_ \
  | |___| | (_) | |_| | (_| | | | | | |  __/\__ \ | | |
  \____|_|\___/ \__,_|\__,_|_| |_| |_|\___||___/_| |_|
  ======================================================
  Cloudmesh Shell
  
  cm> cloud
  +--------------------------+----------+
  | cloud                    | active   |
  +==========================+==========+
  | alamo                    |          |
  +--------------------------+----------+
  | aws                      |          |
  +--------------------------+----------+
  | azure                    |          |
  +--------------------------+----------+
  | dreamhost                |          |
  +--------------------------+----------+
  | hp                       |          |
  +--------------------------+----------+
  | hp_east                  |          |
  +--------------------------+----------+
  | india_eucalyptus         |          |
  +--------------------------+----------+
  | india_openstack_havana   |          |
  +--------------------------+----------+
  | sierra_eucalyptus        |          |
  +--------------------------+----------+
  | sierra                   |          |
  +--------------------------+----------+

  cm> cloud on sierra
  activate cloud 'sierra'? (y/N) ('q' to discard) <- type Y

  ...

  ... cloud 'sierra' activated.

  cm> flavor sierra --refresh
  ...
  Refresh time: 0.190665006638
  Store time: 0.0578060150146
  +--------+------+--------------+---------+-------+--------+----------------------+
  | CLOUD  |   id | name         |   vcpus |   ram |   disk | cm_refresh           |
  |--------+------+--------------+---------+-------+--------+----------------------|
  | sierra |    1 | m1.tiny      |       1 |   512 |      0 | 2014-08-26T01-15-20Z |
  | sierra |    3 | m1.medium    |       2 |  4096 |     40 | 2014-08-26T01-15-20Z |
  | sierra |    2 | m1.small     |       1 |  2048 |     20 | 2014-08-26T01-15-20Z |
  | sierra |    4 | m1.large     |       4 |  8192 |     40 | 2014-08-26T01-15-20Z |
  | sierra |    7 | m1.memmedium |       1 |  4096 |     20 | 2014-08-26T01-15-20Z |
  | sierra |    6 | m1.memlarge  |       1 |  8192 |     20 | 2014-08-26T01-15-20Z |
  +--------+------+--------------+---------+-------+--------+----------------------+


Commands only without description
---------------------------------

::

  git clone https://github.com/cloudmesh/cloudmesh.git
  virtualenv ~/ENV
  source ~/ENV/bin/activate
  cd cloudmesh
  ./install system
  ./install requirements
  ./install new
  ./install rc fetch
  ./install rc fill
  ./install cloudmesh
  fab mongo.start
  fab mongo.boot
  fab user.mongo
  fab mongo.simple
  fab server.start
  cm cloud list
  echo "y" | cm cloud on sierra
  cm flavor sierra --refresh

