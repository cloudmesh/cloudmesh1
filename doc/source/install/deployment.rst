Quick deployment on ubuntu
===========================

This quick deployment is targeted for ubuntu. It can be achieved in several easy steps.
First, obtain a vanilla ubuntu system. Make sure that git is installed, which is standard by now.
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


