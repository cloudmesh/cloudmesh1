Quick deployment
================

::
    git clone git@github.com:cloudmesh/cloudmesh.git
    cd cloudmesh
	fab install.deploy()

YAML files
===========

You will need three yaml files. Samples can be found in the etc source directory. 
More elaborate examples can be obtained from Gregor for the personel that work 
directly with him on FutureGrid.

Configure the yaml files if changes need to be done.

Mongo
=======

::
	mongod
   

Quick Configuration
====================

::
	fab mongo.cloud
	
Now you have data in the mongo db and you can use and test it

Quick Test
==========

Inventory::

    fab test.start:ninventory,host
    
What is if this does not work?
==============================

Please get help from Allan. He is responsible for getting this deployment script properly done.