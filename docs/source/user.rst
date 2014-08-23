**********************************************************************
Cloudmesh Shell
**********************************************************************

User Commands
======================================================================

cloudmesh shell contains a number of user commands. with `init` a user can create their own configuration file sin yaml format. Please see the developers manaul for mor information.

The command `user` allows to find out current information for a particular user. However, this command works only if you are able to authenticate against the system.

Thus the command::

  cm> user info

prints the information about yourself. If you specify a username, you will see some information about this user with the username albert::

  cm> user info albert

To see a list of all user data you can say:: 

  cm> user list






