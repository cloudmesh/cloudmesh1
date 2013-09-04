.. raw:: html

 <a href="https://github.com/cloudmesh/cloudmesh"
     class="visible-desktop"><img
    style="position: absolute; top: 40px; right: 0; border: 0;"
    src="https://s3.amazonaws.com/github/ribbons/forkme_right_gray_6d6d6d.png"
    alt="Fork me on GitHub"></a>

.. sectnum::
   :start: 4
   
Nosetests
==========================================

Install
-------

Due to a bug in nose-json plugin, we install it via::

    $ fab nose.json

Run
-----

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
