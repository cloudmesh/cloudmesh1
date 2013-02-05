Documentation will be at 

http://futuregrid.github.com/cm

A video about its use can be found at 

* http://www.youtube.com/watch?v=CAaFvT76dMk

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
