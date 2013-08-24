Adding to the Documentation
------------------------

Creating the documentation locally
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The documentation to this project is kept in doc/sources. You will
find there a number of rst files. You can add new files, but must make
sure that they are listed in the index.rst page. To create the
documentation in your local directory, do::

   cd doc
   make html

Than open a browser on the file build/html/index.html. In OSX this can be done with::
  
    open build/html/index.html
    
On a Linux machien you may want to substitute the open call with firefox or another browser. 
To create a single html page you can say ::

   cd doc
   make singlehtml
   open build/singlehtml/index.html

..

RST Documentation
^^^^^^^^^^^^^^^^^^^^^

Information about rst and sphinx can be found at 

* http://sphinx-doc.org/rest.html
* http://sphinx-doc.org/markup/index.html#sphinxmarkup

gh-pages
^^^^^^^^

.. warning:: This step is only to be executed by Gregor von Laszewski

The document can be published into gh-pages as follows. Firts make
sure you have everything committed. Second, go into
the root directory of the project and say::

    fab clean

..


This will create a clean dir. Third, execute the command::

    make gh-pages

..


This will go into the barnch gh-pages, checkout the content under /tmp
and recreate the documentation. Than it will check it back into the
branch and do a git push. If everything is normal (no errors occur)
you wil see the new documentation. 

Published Documentation
^^^^^^^^^^^^^^^^^^^^

The final documentation will be located at

* http://cloudmesh.github.com/cloudmesh

If you find something missing communicate with Gregor von Laszewski (laszewski@gmail.com) so
he updates the gh-pages.
