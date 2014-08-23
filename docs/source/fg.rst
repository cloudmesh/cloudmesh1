FutureGrid Specific tips
======================================================================

If you are a FutureGrid users, you may have several .cloudmesh directories on 
several machines. To consolodate them you can do the following::


    PORTALNAME=<putyour portalname here>

    mkdir ~/.futuregird
    cd ~/.cloudmesh

    scp -r $PORTALNAME@india.futuregrid.org:.futuregrid india
    scp -r $PORTALNAME@sierra.futuregrid.org:.futuregrid sierra
    #scp -r $PORTALNAME@hotel.futuregrid.org:.futuregrid hotel

Also you may need to add some machines into your authorized keys file. 
A simple way to do this is to just to log in once by executing a simple 
command::

    ssh $PORTALNAME@india.futuregrid.org uname 
    ssh $PORTALNAME@sierra.futuregrid.org uname 
    ssh $PORTALNAME@alamo.futuregrid.org uname 
    ssh $PORTALNAME@hotel.futuregrid.org uname

