Virtualenv
==========


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

  	 Go to your home directory, log in your .bashrc, .bash_profile, or .bash_login file and add:: 
	  
	    $ source ENV/bin/activate

	  This way you do not forget to type it in next time you login

Cloud Mesh
==========

A project to interface easily with multiple clouds from the
commandline and a command shell.


Commands
========

cm manage initialize --user<name> --password <password>

   * connects to FG and retrieves important information for you to use
   * uses an ssh connection to connect to a FG service to retrieve the
     information
   * if the connection is refused n=5 times within the hour the
   * account is disabled
   * if the command is called more than 10 times a day the account is disabled

cm project list

   lists the projects a user is in

cm project --info <number>

   * retrieves information about the project
   * if the user is the manager or lead it returns member information

cm project --activate <number>

   * activates charging for this project
   * subsequent calls are charged against this project

cm project --deactivate

   * deactivates any charge of a project

cm env

   * prints the environment and its variables currently associated
     with cm

cm resource --list

   * lists the resources available for the user
   
cm service --list
  
  * list the services in the cloud mesh

cm service register

   see fg-inventory

cm resource register

   see fg-inventory

cm image --list

   * list the images

cm id --list

  * list all ids and their types

cm label --id <id>

   * associates a human readable lable with an id

cm create <label>

cm destroy <label>

cm terminate <label>

