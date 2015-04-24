**********************************************************************
Cloudmesh Vagrant Developers Environment
**********************************************************************

This section is for experts that like to deploy cloudmesh in a vagrant
ubuntu 14.04 image under virtual box. We further assume you have
checked out cloudmesh from github and are standing in the github
directory::

    $ git clone git@github.com:cloudmesh/cloudmesh.git
    $ cd cloudmesh

We assume you have uploaded a box to vagarnt with the name:: 

   ubuntu-14.04-server-amd64

If you do not have such an image you can create it by::

   $ bin/install-veewee.sh
   $ bin/install-ubuntu64.sh

You can verify the list of boxes with::

   $ vagrant box list

To create a vagrant image you simply can say::
  
   deploy vagrant

This will start a vagrant vm. In the vm say::

   sudo apt-get install python-dev
   sudo apt-get install python-virtualenv
   virtualenv ~/ENV
   . ~/ENV/bin/activate
   pip install fabric


Than say::

  cd /vagrant/cloudmesh
  deploy cloudmesh

Please note that the changes in the cloudmesh directory are synced
with the directory::

  /tmp/vagrant/cloudmesh




Vagrant
======================================================================

Issues with vagrant

* default passwords
* insecure keys

Do not put your vagrant vm publicly on the net.

Veewee
======================================================================

Creating a base box for ubuntu 14.04::

  mkdir github
  cd github
  git clone git@github.com:jedi4ever/veewee.git
  cd veewee
  bundle install
  bundle exec veewee vbox define 'ubuntu-14.04-server-amd64' 'ubuntu-14.04-server-amd64'
  bundle exec veewee vbox build 'ubuntu-14.04-server-amd64'
  
Now you could logging into the image::

  ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -p 7222 -l vagrant 127.0.0.1

Exporting::

   bundle exec veewee vbox export 'ubuntu-14.04-server-amd64'


Adding::

  vagrant box add ubuntu-14.04-server-amd64 ubuntu-14.04-server-amd64.box

To see if the box is in vagrant you can say::

  vagrant box list

To create a new virtual macchine for ubuntu you should first create a new directory for your image. Let us call it `mytest`. You need to cd into the dirctory and than create a vagrantfile::

   mkdir my_test
   cd my_test
   vagrant init 'ubuntu-14.04-server-amd64'
   vagrant up
   vagrant ssh

If you like to find other boxes you can find some with the command::

  bundle exec veewee vbox templates | grep -i ubuntu

Creating a cloudmesh test
======================================================================

TBD

::

   mkdir test_cloudmesh
   cd my_test

   checkout the cloudmesh from git
   checkout a vagrantinit file from git
   
   the vagrant init file contains the cloudmesh as a shared folder

   vargant up
   vagrant ssh

   vagrant> cd cloudmesh
   vagrant> python install.py

install.py includes

   deployment of::
     pip
     virtualenv

   than we start the virtualenv
   than we install fabric

   than we do::

     fab -f install/fabric.py deploy

   the fab is actually part of the install.py script

Goal is that install.py is all we need to get cloudmesh installed on ubuntu
         
   
