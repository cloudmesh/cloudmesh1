

Generating the documentation
======================================================================

This document is maintained via sphinx and uploaded regularly to github

* https://cloudmes.github.com/cloudmesh/

You can check it out the code and the documentation with::

  git clone git@github.com:cloudmesh/cloudmesh.git

Once you make changes to the documentation you can say::

   make sphinx

The pages will be locally available to you under::

   src/build/html/index.html

The pages will be regularly uploaded to github by Gregor von Laszewski. Make sure that the documentation do not contain any compile errors. Once that is done the pages can be uploaded.   
with the command::   

  make gh-pages

Please note that the make gh-pages should only be executed by
Gregor von Laszewski (laszewski@gmail.com). Please notify him when you think that your documentation
contribution justifies an update.


Installation requirements for the Documentation Generation
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

Document creation
----------------

This will publish the documentation locally::

    fab doc.html

If you do::

    fab doc.gh

it will publish the page to gh-pages
