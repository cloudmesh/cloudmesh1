CM
======================================================================

Setting-up the COmmandline version of Cloud Mesh

Run make::

    make

Set the key for Open Stack (You could get this key from your futuregrid account.)::

    scp gregor@india.futuregrid.org:.cloudmesh/openstack/novarc .  
    cat novarc  
    mkdir -p ~/.cloudmesh/openstack/  
    cp novarc ~/.cloudmesh/openstack/  
    source ~/.cloudmesh/openstack/novarc 

Type in a nova command to check whether the key was set properly::

    $ nova list

You will see::

    +--------------------------------------+--------------+--------+------------------------------------+
    | ID                                   | Name         | Status | Networks                           |
    +--------------------------------------+--------------+--------+------------------------------------+
    | 26a41ff1-72bc-4185-a212-9d6ceXXXXXXX | Server 47XX  | ACTIVE | vlanXXX=1X.X.2.3, XXX.XXX.XXX.8    |
    +--------------------------------------+--------------+--------+------------------------------------+


If you are getting some table like above then you are good.

Install euca2ools (if you have not already done so.) ::

    $ sudo apt-get install euca2ools

Generate euca key pair (this is done wrong we want nova's commands to do that)::

    $ euca-import-keypair -f ~/.ssh/id_dsa.pub gregor

List the generated key pair::

    $ nova keypair-list

You will see::

    +--------+-------------------------------------------------+
    | Name   | Fingerprint                                     |
    +--------+-------------------------------------------------+
    | gregor | shfjpaiuFEHFHEBXPNWUIXEFYBEFYPARUFIYPNERUYFPUEF |
    +--------+-------------------------------------------------+


If you are getting something like above, then you are good (I have replaced my fingerprint with 'X's)


Using Cloud Mesh
======================================================================

You can use following commands to play around with Cloud Mesh.

Refresh::

   $ cm r

You will see::

    Processing |................................| 10/10
    Done.

Start VM::

    $ cm start:1

You will see::

    Launching VM gregor-001

    +------------------------+-------------------------+
    | **Property**           | **Value**               |
    +------------------------+-------------------------+
    | status                 | BUILD                   |
    +------------------------+-------------------------+
    | updated                | 2013-03-01T10:17:23Z    |
    +------------------------+-------------------------+
    | metadata               | {}                      |
    +------------------------+-------------------------+

    Processing |................................| 10/10
    Done.

Start 5 VMs in parallel::

    $ cm par:5

You will see::

    Launching VM gregor-000
    Launching VM gregor-001
    Launching VM gregor-003
    Launching VM gregor-004
    Launching VM gregor-002
    Done.

Reindex the already started VMs::

    $ cm reindex

You will see::

    Skipping gregor-000
    Skipping gregor-001
    Renameing gregor-001 -> gregor-002
    Renameing gregor-002 -> gregor-003
    Renameing gregor-003 -> gregor-004
    Renameing gregor-004 -> gregor-005
    Processing |................................| 10/10 
    Done.


