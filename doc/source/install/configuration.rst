.. sectnum::
   :start: 8
   
Basic Configuration
--------------------

open a new terminal and type in::

   mongod
   
Now you can either generate a simple cloud without user or a cloud with user information. What you chose depends on what you need to develop and have access to.


To generating a simple cloud do::

   fab mongo.simple
   

This will print something like (if everything is ok)::

        clusters: 5 -> bravo, delta, gamma, india, sierra
        services: 0
        servers: 304
        images: 2 -> centos6, ubuntu
   
To generate a complete cloud including users (requires access to LDAP):

    fab mongo.cloud

Next you can start the Webui with::

	fab server.start    
	
	
If you like to start with a particular route, you can pass it as parameter.

    fab server.start:inventory
    
opens the page 

    http://localhost:5000/inventory in your browser


You can repeatedly issue that command and it will shut down the server. If you want to do thia by hand you can do this with::

    $ fab server.stop


    
	