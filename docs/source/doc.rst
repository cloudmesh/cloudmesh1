Documentation
======================================================================

Creating the Documentation
----------------------------------------------------------------------

The documentation to this project is kept in docs/sources in RST
format. Information about rst and sphinx can be found at 

* http://sphinx-doc.org/rest.html
* http://sphinx-doc.org/markup/index.html#sphinxmarkup

You will find there a number of rst files. You can add new files, but
must make sure that they are listed in the index.rst page. To create
the documentation in your local directory you can do this from the
main cloudmesh directory with::

   fab doc.html

The pages will be locally available to you under::

  docs/build/html/index.html 

To view the documentation you can also say::

  fab doc.view

The pages will be regularly uploaded to github by Gregor von Laszewski. Make sure that the documentation do not contain any compile errors. Once that is done the pages can be uploaded.   
with the command::   

   fab doc.publish

This step will publish the page to gh-pages at

* http://cloudmesh.github.io/cloudmesh/

Sometimes it is necessary to clean the documentation and code before you build
it. This is achieved with:: 

    fab clean.all


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

