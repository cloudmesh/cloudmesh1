Starting an Openstack VM on India with Vagrant
======================================================================

Requirements
----------------------------------------------------------------------

* We assume you have a .cloudmesh/cloudmesh.yaml file and properly
  configured it

* We assume you have a valud account on FutureSystems Openstack Juno
  cloud

* We assume you have vagrant installed

Install requirements
----------------------------------------------------------------------

You need to say::

    $ vagrant plugin install vagrant-openstack-provider

This will add the vagrant openstack provider to vagrant


Start the VM
----------------------------------------------------------------------

::

    $ vagrant up --provider=openstack


Login
----------------------------------------------------------------------

::

    $ vagrant ssh


Destroy the VM
----------------------------------------------------------------------

::

    $ vagrant destroy
