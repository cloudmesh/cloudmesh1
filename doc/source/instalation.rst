Instalation
===========

Virtualenv
----------

Download virtualenv
^^^^^^^^^^^^^^^^

This step is only needed if virtualenv is not installed. To
test this say::

    $ which virtualenv

..

If the result does not provide the path followed by
virtualenv, it is installed, you can do::
         
    $virtualenv ENV

..

and skip step 2.
        
Since you do not have super user priviledges, you need virtualenv in
order to finish the installtion. You may download virtualenv.py by
following command::

    $ wget https://raw.github.com/pypa/virtualenv/master/virtualenv.py
 
Install virtualenv
^^^^^^^^^^^^^^^^
        
After you downloaded virtualenv, you can install it by following
command::

    $ python virtualenv.py --system-site-packages ENV
          
Activate virtualenv
^^^^^^^^^^^^^^^^

After installation of virtualenv, you can activate virtualenv by
following command::

    $ source ENV/bin/activate
    
Modify your rc file (optional):
^^^^^^^^^^^^^^^^

Go to your home directory, log in your .bashrc,
.bash_profile, or .bash_login file and add::

    $ echo "source ENV/bin/activate" >> .bash_profile

..


This way you do not forget to type it in next time you 
login. Only do this if you are familar with .bash_profile.
