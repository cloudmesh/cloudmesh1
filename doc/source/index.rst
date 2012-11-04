Welcome to FutureGrid Cloud Inventory
=====================================

This project is intended to provide information about a simple database to manage inventory in support of cloud seeding and cloud shifting.

Cloud Inventory
"""""""""""""""
  * A project to do bare metal and VM based dynamic provisioning
  * Documentation: http://futuregrid.github.com/inventory
  * Source: https://github.com/futuregrid/inventory


Quickstart Example
""""""""""""""""""

- **Note** : These commands work only in the context of fg-inventory shell. They wont work on normal shell.

::

	fg-inventory> assign server:india
	> add server -r 1-5 -p i%.iu.edu
	> assign service:euca
	> add service -r 1-5
	> list server
	> unassign service
	> add server
	> list server

List of Commands	
""""""""""""""""
.. toctree::
	:maxdepth: 1
	
	assign
	add
	unassign
	list
	support

.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`


