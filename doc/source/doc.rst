.. sectnum::
   :start: 6


.. sidebar:: 
   . 

  .. contents:: Table of Contents
     :depth: 5

..

Documentation Management
======================================================================

Before doing anything please set up and use virtualenv and pip. (see
developers documentation). Make sure to activate your virtualenv.

This document is maintained via sphinx and uploaded regularly to github

* https://cloudmesh.github.com/cloudmesh/

You can check it out the code and the documentation with::

  git clone git@github.com:cloudmesh/cloudmesh.git

A number of packages need to be installed on your machine. You can do
this with:: 

    $ cd cloudmesh
    $ fab -f install/fabfile.py deploy
    $ fab build.install


Creating the Documentation
----------------------------------------------------------------------

The documentation to this project is kept in doc/sources in RST
format. Information about rst and sphinx can be found at 

* http://sphinx-doc.org/rest.html
* http://sphinx-doc.org/markup/index.html#sphinxmarkup

You will find there a number of rst files. You can add new files, but
must make sure that they are listed in the index.rst page. To create
the documentation in your local directory you can do this from the
main cloudmesh directory with::

   fab doc.html

The pages will be locally available to you under::

  doc/build/html/index.html 

To view the documentation you can also say::

  fab doc.view

The pages will be regularly uploaded to github by Gregor von Laszewski. Make sure that the documentation do not contain any compile errors. Once that is done the pages can be uploaded.   
with the command::   

   fab doc.gh

.. warning:: Please note that the fab doc.gh should only be executed by
Gregor von Laszewski (laszewski@gmail.com). Please notify him when you
think that your documentation contribution justifies an update. This
step will publish the page to gh-pages at

* http://cloudmesh.github.io/cloudmesh/

Sometimes it is necessary to clean the documentation and code before you build
it. This is achieved with:: 

    fab clean


Creating the documentation in a single page
----------------------------------------------------------------------

To create a single html page you can say ::

   cd doc
   make singlehtml
   open build/singlehtml/index.html


Documenting the code
----------------------------------------------------------------------

A sample code documentation is given bellow

::

    def my_method(attribute, value[, limit=None])
       """
       Format the exception with a traceback.

       :param attribute: the name of the attribute
       :param value: the value for the attribute
       :param limit: maximum number of stack frames to show
       :type limit: integer or None
       :rtype: list of strings
       """
       ...	   
       return ['a','b']

(Deprecated) Old Requirements for the Documentation
----------------------------------------------------------------------

.. warning:: This stap has been deprecated and is part of the previous
   setup step.

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

