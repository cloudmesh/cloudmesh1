Instalation
===========

Virtualenv
----------

* **Step 1: Download virtualenv**
	
	Since you do not have super user priviledges, you need virtualenv in
	order to finish the installtion. You may download virtualenv.py by
	following command::

	    $ wget https://raw.github.com/pypa/virtualenv/master/virtualenv.py
 
* **Step 2: Install virtualenv**
	
	After you downloaded virtualenv, you can install it by following
	command::

	    $ python virtualenv.py --system-site-packages ENV
	  
* **Step 3: Activate virtualenv**

	After installation of virtualenv, you can activate virtualenv by
	following command::

	    $ source ENV/bin/activate
    
* **Step 4 (optional): modify your rc file**

  	 Go to your home directory, log in your .bashrc,
  	 .bash_profile, or .bash_login file and add::

	     echo "source ENV/bin/activate" >> .bash_profile

	 .This way you do not forget to type it in next time you
	 login. Only do this if you are familar with .bash_profile.
