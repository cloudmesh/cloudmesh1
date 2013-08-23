unassign
--------
- Remove the assignment of a default parameter 

Usage
"""""
::

	unassign type
	unassign server
	unassign service
	unassign prefix

Description
"""""""""""

The unassign command removes a set default parameter for parameters to be used by other commands. Presently we are suporting the unassignment of default parameters for server, service and prefix which are set by assign command. The usage is specifying the type to be unassigned.

List of Parameters
""""""""""""""""""
::

type
     the type of the parameter to be stored as a default in case no command line parameter is specified.


Example
"""""""
The example removes the default assignment as server name being myserver.
::

  fg-inventory> assign server:myserver
  > unassign server

