Setup Cloudmesh in an Vagrant VM for Testing
============================================

This tutorial provides as how to deploy Cloudmesh with Vagrant and VirtualBox. Official Ubuntu 14.04 Server LTS 64 bit and 32 bit are supported as base images of Vagrant.

Download cloudmesh
--------------------------

::

  git clone https://github.com/cloudmesh/cloudmesh.git
  cd cloudmesh

Install Vagrant and VirtualBox
--------------------------------

This instructions are tested on Ubuntu 14.04.

::

  sudo apt-get install vagrant
  sudo add-apt-repository multiverse 
  sudo apt-get update
  sudo apt-get install virtualbox

Install Veewee
--------------

There are `requirements <veewee-requirement.html>`_ prior installing Veewee.

::
  
   gem install veewee

* On OS X Mavericks::

   $ ARCHFLAGS=-Wno-error=unused-command-line-argument-hard-error-in-future gem install veewee


Vagrant up
----------

::

  cd ~/cloudmesh/vagrant/example1
  ./run.sh


FutureGrid Portal ID
^^^^^^^^^^^^^^^^^^^^^

Provide your portal ID::

  ==================================
  Futuregrid portal id? (def: )

  ==================================

Base Image
^^^^^^^^^^^

Select one of the base image::

  ==================================
  Select base image to launch
  ==================================
  1) Ubuntu Server 14.04 64bit
  2) Ubuntu Server 14.04 32bit
  Please choose an option: 
  
  Ubuntu Server 14.04 xxbit selected
  Bringing machine 'default' up with 'virtualbox' provider...
  ==> default: Checking if box 'ubuntu/trusty32' is up to date...

Vagrant will be loaded.
