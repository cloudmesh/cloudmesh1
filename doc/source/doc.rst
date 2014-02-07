Documentation Management
======================================================================

Before doing anything please set up and use virtualenv and pip. (see
develoeprs Documentation). Make sure to activate your virtualenv.

This document is maintained via sphinx and uploaded regularly to github

* https://cloudmes.github.com/cloudmesh/

You can check it out the code and the documentation with::

  git clone git@github.com:cloudmesh/cloudmesh.git

A number of packages need to be installed on your machine. YOu can do
this with 

    $ cd cloudmesh
    $ fab -f install/fabfile.py deploy
    $ fab build.install

Installation Requirements for the Documentation Generation
---------------------------

We assume you have autodoc installed for sphinx (see previously) it is
not in the requirements file, as I could not find it in pypi. Hence we
install it before hand::

    mkdir /tmp/install-cloudmesh
    hg clone http://bitbucket.org/birkenfeld/sphinx-contrib/
    cd sphinx-contrib/autorun
    python setup.py install

    cd /tmp/install-cloudmesh

    git@github.com:cloudmesh/cloudmesh.git
    cd cloudmesh
    pip install -r requirements.txt

If anything is missing, please let us know so we can update this documentation.

Creating the Documentation
----------------------------------------------------------------------

Once you make changes to the documentation you can say::

   fab doc.html

The pages will be locally available to you under::

  doc/build/html/index.html 

The pages will be regularly uploaded to github by Gregor von Laszewski. Make sure that the documentation do not contain any compile errors. Once that is done the pages can be uploaded.   
with the command::   

   fab doc.gh

Please note that the fab doc.gh should only be executed by
Gregor von Laszewski (laszewski@gmail.com). Please notify him when you think that your documentation
contribution justifies an update.



Document Generation
--------------------

This will publish the documentation locally::

    fab doc.html

Publishing the Documentation
--------------------------

If you do (which you should not, only Gregor should do this)::

    fab doc.gh

it will publish the page to gh-pages at

* http://cloudmesh.github.io/cloudmesh/



Adding to the Documentation
------------------------

Creating the documentation locally
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The documentation to this project is kept in doc/sources. You will
find there a number of rst files. You can add new files, but must make
sure that they are listed in the index.rst page. To create the
documentation in your local directory you can do this from the main
cloudmesh directory with::

   fab doc.html

Than open a browser on the file build/html/index.html. In OSX this can be done with::
  
    open doc/build/html/index.html
    
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

    fab doc.gh

..


This will go into the barnch gh-pages, checkout the content under /tmp
and recreate the documentation. Than it will check it back into the
branch and do a git push. If everything is normal (no errors occur)
you wil see the new documentation. 

Published Documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The final documentation will be located at

* http://cloudmesh.github.com/cloudmesh

If you find something missing communicate with Gregor von Laszewski (laszewski@gmail.com) so
he updates the gh-pages.
