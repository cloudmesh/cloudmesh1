Python Package requirements
---------------------------
* fabric
* sh
* multiprocessing
* progress
* webbrowser
* docopt

Tools requirements
------------------
* python-novaclient
* euca2ools

Configuration requirements
--------------------------
* novarc
* nova keypair

Documentation will in future (but nt yet) be at 

* http://futuregrid.github.com/cm

Screenshots can be found here:

* http://cloudmesh.blogspot.com/2013/02/cm-has-now-html-table.html

A video about its use can be found at 

* http://www.youtube.com/watch?v=CAaFvT76dMk

A community blog about this project can be found at

* http://cloudmesh.blogspot.com

In case you like to execute this on india.futuregrid.org please, get
an account and motivate a very good project. Once you have access you
can do the following:

    module load git
    module load python
    
    mkdir dev
    cd dev
    virtualenv TEST
    source TEST/bin/activate
    git clone git@github.com:futuregrid/cm.git
    cd cm
    make
    source ~/.futuregrid/openstack/novarc 
    cd src
    cm r

FutureGrid
----------

This project is part of FutureGrid and can be used currently on the 
OpenStack cloud of FutureGrid. To apply for an account, please 
go to https://portal.futuregrid.org 

However you also need to apply for a project in case you like to use FG resources.
If you have your own OpenStack cloud you naturally do not need to apply for a FG account.

