
Cloud Mesh
==========

A project to interface easily with multiple clouds from the
commandline and a command shell.


Commands
--------

cm manage initialize --user<name> --password <password>

* connects to FG and retrieves important information for you to use
* uses an ssh connection to connect to a FG service to retrieve the
  information
* if the connection is refused n=5 times within the hour the
* account is disabled
* if the command is called more than 10 times a day the account is disabled

cm project list

* lists the projects a user is in

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

* see fg-inventory

cm resource register

* see fg-inventory

cm image --list

* list the images

cm id --list

* list all ids and their types

cm label --id <id>

* associates a human readable lable with an id

cm create <label>

cm destroy <label>

cm terminate <label>

