Documentation will in future (but nt yet) be at 

* http://futuregrid.github.com/cm

A video about its use can be found at 

* http://www.youtube.com/watch?v=CAaFvT76dMk

A community blog about this project can be found at

* http://cloudmesh.blogspot.com

In case you like to execute this on india.futuregrid.org please, get
an account and motivate a very good project. Once you have access you
can do the following:

    module load git
    module load python
    virtualenv TEST
    source TEST/bin/activate
    mkdir test
    git clone git@github.com:futuregrid/cm.git
    cd cm
    make
    chmod a+x ~/TEST/bin/cm 
    cd src
    source ~/.futuregrid/openstack/novarc 
    cm r

FutureGrid

This project is part of FutureGrid and can be used currently on the 
OpenStack cloud of FutureGrid. To apply for an account, please 
go to https://portal.futuregrid.org 

However you laso need to apply for a project in case you like to use FG resources.
If you have your own OpenStack cloud you naturally do not need to pply for a FG account.

