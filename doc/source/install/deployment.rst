Quick deployment on ubuntu
===========================

This quick deployment is targeted for ubuntu. It can be achieved in several easy steps.
First, obtain a avanilla ubuntu system. Make sure that git is installed, which is standard by now.
Next execute the following commands ::

    $ git clone git@github.com:cloudmesh/cloudmesh.git
    $ cd cloudmesh
    $ cd install
    $ fab deploy


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

To stop mongod   

	fab mongod.stop
	
To clean the entire data base (not just the data for cloudmesh, so be careful) say::

	fab mongo.clean
	
To create a simple cluster without usernames, say::

	fab mongo.simple
	
To create a cluster with user data base say::

	fab mongo.cloud
	
Now you have data in the mongo db and you can use and test it

Quick Test
------------


Inventory::

    fab test.start:ninventory,host
    
What is if this does not work?
----------------------------------

Please get help from Allan. He is responsible for getting this deployment script properly done.