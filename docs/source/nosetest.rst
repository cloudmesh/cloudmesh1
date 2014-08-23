Testing
======================================================================

.. sidebar:: 
   . 

  .. contents:: Table of Contents
     :local:

..

With Python nose testing tool, Cloudmesh performs tests easily to find problems and verify commands, functions and classes.
*tests* directory contains test cases to check and nose produces captured output messages from failing test cases to help debugging.

Install
-------

Due to a bug in nose-json plugin, we install it via::

  $ fab nose.json
  $ fab nose.install

Run
-----

::

        $ fab nose.run

If there is a file in tests/test_keys.py for example, you can call the test as

http://127.0.0.1:5000/nose/keys

and it gets executed. you must be in the cludmesh dir.

System
-------

In test_system.py we collect a number of system tests, such as if 
the machines are pingable, or LDAP works ... Enough to help debugging 
and seing if the nevironment works. Start it with ::


    http://127.0.0.1:5000/nose/system

in your browser
