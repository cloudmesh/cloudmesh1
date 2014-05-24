.. sidebar:: Page Contents

   .. contents::
      :local:


.. _s-instalation:

**********************************************************************
Tips for Editing
**********************************************************************

Aptana Studio - Develpment Environment(optional)
======================================================================

A good IDE for python development for Python is `Aptana Studio 
<http://www.aptana.com/>`_, which is based
on eclipse . It contains the ability to directly import packages from
github by filling out a simple form. So instead of using the
command line github tool you can use the Aptana Studio version. It
also contains a very nice way of managing your commits while allowing
you to select via a GUI the files you have changed and commit them
with a nice commit message. Pull and Push functions are also
available. Having said that there is some advantage of using the
Aptana GUI tools for git as it makes it easier. Aptana Studio has also the
ability to use emacs key mappings, which is a real nice
feature. Naturally not all of emacs is supported.

For those new to python an the project we recommend you use it for
development.


Emacs as editor
======================================================================

Emacs is a real good editor for development and has a very good
interactive macro definition tool that you can use to create
sophisticated searches and query replacements. This can safe a lot of
time. 

Query replace all ocurences::

  ESC % <old text> RET <new text> RET !

Instead of ! you can use RET followed by y/n question to selectively
replace.

To create a macro that you can reexecute which may include tabs,
cursor movements or other fancy tricks you can do::

   CTRL-x (  <do edit what yo need> CTRL x-)
  
A good recource for emacs is the `Emacs Reference Card
<http://www.gnu.org/software/emacs/refcards/pdf/refcard.pdf>`_

This is realy all you need for emacs to make it a useful editor for
you. xemacs, aquaemacs, carbonemacs are GUI enhanced versions of
emacs.

Often you may want to use a nice underline in an rst document with 70 characters in width. This is easy in emacs. You simply go to the beginning of the line and say::

  ESC x 70 =

IN cae you like another character simply replace the = with the character.
 

Replace Text in many files from the commandline
======================================================================

Assume you have changed the location of an import eg yo like to change
`import a.b.c` to `import a_b.c`. Editing the files with an editor an
fisiting every file is too time consuming. instead you could use a
perl one liner such as::

  perl -pi -e 's/import a.b.c/import a_b.c/g' *.py
  perl -pi -e 's/import a.b.c/import a_b.c/g' */*.py
  perl -pi -e 's/import a.b.c/import a_b.c/g' */*/*.py

to replace the statement in the given subdirs or a shorter form::

  perl -pi -e 's/import a.b.c/import a_b.c/g' `find ./ -name *.py`

MongoDB Tools
======================================================================

Robomongo
----------------------------------------------------------------------

A nice tool to visualize and browse contents in mongodb is `Robomongo
<http://robomongo.org>`_. It is available for OSX, Windows, and Linux.
Wne using it, you will need to use the admin user and password that is
defined in the cloudmesh_server.yaml file.
