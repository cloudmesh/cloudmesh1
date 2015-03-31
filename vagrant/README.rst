Install Virtualbox
===================

`VirtualBox`_ is a virtualization technology available on multiple platforms, such as Windows, Mac OS X, and Linux.

.. _VirtualBox: https://www.virtualbox.org/

Setup Vagrant on Ubuntu
==========================

`Vagrant`_ provides an means of reproducibly creating, provisioning,
and configuring virtual machines.

.. _Vagrant: https://www.vagrantup.com/


Setup
======================================================================

:: 
  
  $ git clone https://github.com/cloudmesh/cloudmesh.git
  $ cd cloudmesh/vagrant

Use
======================================================================

In order to correctly set up a virtual machine with cloudmesh, set the
PORTALNAME and PROJECTID variables. For example::

  $ export PORTALNAME=albert
  $ export PROJECTID=fg101

In order for the VM to authenticate and access ``india``, make sure
that ``ssh-agent`` is running and knows about the appropriate key::

  $ eval `ssh-agent`
  $ ssh-add ~/.ssh/id_rsa

You can now bring up the virtual machine::

   $ vagrant up --provider virtualbox

Now that the machine is up, you can log in::

   $ vagrant ssh

and use cloudmesh immediately::

  $ cm list flavor india


Further details
======================================================================

Please see the contents of ``Vagrantfile`` for details on how this
works.
