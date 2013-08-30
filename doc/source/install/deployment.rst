**********************************************************************
Development Documentation
**********************************************************************

Pip
====

We do not use easy_install, but pip instead. 

please make sure that you install pip. In most cases this can be doen
with::

     easy_install pip 

Once installed we will typically not use easy_install.


Virtualenv
================

As we like to have an isolated development environment we require that
you use virtualenv. For simplicity our virtual env will be placed in
the home directory under ~/ENV. If you already have such a directory
for other projects, we suggest that you find a new name for the
virtualenv. However, for the rest of the manual we assum it is "ENV"

Download virtualenv
------------------------

This step is only needed if virtualenv is not installed. To
test this say::

    $ which virtualenv

In case virtualenv is not isntalled, you can download it for example
with 

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

..

and skip step 2.
        
          
Activate virtualenv
------------------------

After installation of virtualenv, you can activate virtualenv by
following command::

    $ source ENV/bin/activate
    
Modify your rc file (optional):
------------------------

Go to your home directory, log in your .bashrc,
.bash_profile, or .bash_login file and add::

    $ echo "source ENV/bin/activate" >> .bash_profile

..


This way you do not forget to type it in next time you 
login. Only do this if you are familar with .bash_profile.





Install fabric
======================================================================

::

    pip install fabric

GIthub ssh keys.
======================================================================

If you are on a new machine you must create a new github ssh key for
it. This is nicely described at

* https://help.github.com/articles/generating-ssh-keys

You must upload the key to github, either via a command, or simply via
the github gui. Simply go to your settinga nd find the ssh key menu
entry. Klick on it and upload your new key by pasting and copying the
public key. Make sure you do not copy the privat key. 


Git username and e-mail
======================================================================

It is very important to set the git username and e-mail. This can be
done with the following commands. you must use your full name and your
e-mail that ypou use with github as part of your registered
account. Otherwise our commits will not properly work.

::

    git config --global user.name "Gregor von Laszewski"
    git config --global user.email "laszewski@gmail.com"



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


working on cloudmesh
===============

portforwarding

ssh -L 80:localhost:5000 gvonlasz@cm 


http://localhost:5001

eval `ssh-agent -s`
Agent pid 14355

ssh-add 







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


