assign 
------

- assigns a default parameter 

Usage
"""""""""
::

	assign type:name
	assign server:servername
	assign service:servicename
	assign prefix: prefixname
Description
"""""""""""

The assign command defines a default parameter for parameters defined by other commands. Presently we are suporting the assignment of default parameters for servers,services and prefix.

List of Parameters
""""""""""""""""""

type
     the type of the parameter to be stored as a default in case no command line parameter is specified.

name
     the value for the type field.


Example
"""""""

The following example adds a server into the inventory with range from 1-3 and prefix as specified using the assigned value for the field server ::

  fg-inventory> 
  > assign server:myserver
  > add server -r 1-3 -p i#.iu.edu
