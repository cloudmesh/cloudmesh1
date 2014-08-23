
.. sidebar:: 
   . 

  .. contents:: Table of Contents
     :depth: 5

..

Cloudmesh Style Guide
=======================

Acknowledgements for this instructions: These instructions are taken from 
https://raw.github.com/openstack/nova/master/HACKING.rst

Information
------------

Our codeing style uses as much as possiple the pep-0008 format as
documented in 

* http://www.python.org/dev/peps/pep-0008/

Please read that document carefully. Please also read the following sections


General
-------
- Put two newlines between top-level code (funcs, classes, etc)
- Use only UNIX style newlines ("\n"), not Windows style ("\r\n")
- Put one newline between methods in classes and anywhere else
- Long lines should be wrapped in parentheses
  in preference to using a backslash for line continuation.
- Do not write "except:", use "except Exception:" at the very least
- Include your name with TODOs as in "#TODO(termie)"
- Do not shadow a built-in or reserved word. Example::

    def list():
        return [1, 2, 3]

    mylist = list() # BAD, shadows `list` built-in

    class Foo(object):
        def list(self):
            return [1, 2, 3]

    mylist = Foo().list() # OKAY, does not shadow built-in

- Use the "is not" operator when testing for unequal identities. Example::

    if not X is Y:  # BAD, intended behavior is ambiguous
        pass

    if X is not Y:  # OKAY, intuitive
        pass

- Use the "not in" operator for evaluating membership in a collection. Example::

    if not X in Y:  # BAD, intended behavior is ambiguous
        pass

    if X not in Y:  # OKAY, intuitive
        pass

    if not (X in Y or X in Z):  # OKAY, still better than all those 'not's
        pass


Imports
-------
- Do not import objects, only modules (*)
- Do not import more than one module per line (*)
- Do not use wildcard ``*`` import (*)
- Do not make relative imports
- Do not make new nova.db imports in nova/virt/*
- Order your imports by the full module path
- Organize your imports according to the following template

Human Alphabetical Order Examples
---------------------------------
Example::

  import httplib
  import logging
  import random
  import StringIO
  import time
  import unittest

  import eventlet
  import webob.exc

  import nova.api.ec2
  from nova.api import openstack
  from nova.auth import users
  from nova.endpoint import cloud
  import nova.flags
  from nova import test


Docstrings
----------
Example::

  """A one line docstring looks like this and ends in a period."""


  """A multi line docstring has a one-line summary, less than 80 characters.

  Then a new paragraph after a newline that explains in more detail any
  general information about the function, class or method. Example usages
  are also great to have here if it is a complex class for function.

  When writing the docstring for a class, an extra line should be placed
  after the closing quotations. For more in-depth explanations for these
  decisions see http://www.python.org/dev/peps/pep-0257/

  If you are going to describe parameters and return values, use Sphinx, the
  appropriate syntax is as follows.

  :param foo: the foo parameter
  :param bar: the bar parameter
  :returns: return_type -- description of the return value
  :returns: description of the return value
  :raises: AttributeError, KeyError
  """


Dictionaries/Lists
------------------
If a dictionary (dict) or list object is longer than 80 characters, its items
should be split with newlines. Embedded iterables should have their items
indented. Additionally, the last item in the dictionary should have a trailing
comma. This increases readability and simplifies future diffs.

Example::

  my_dictionary = {
      "image": {
          "name": "Just a Snapshot",
          "size": 2749573,
          "properties": {
               "user_id": 12,
               "arch": "x86_64",
          },
          "things": [
              "thing_one",
              "thing_two",
          ],
          "status": "ACTIVE",
      },
  }


Calling Methods
---------------
Calls to methods 80 characters or longer should format each argument with
newlines. This is not a requirement, but a guideline::

    unnecessarily_long_function_name('string one',
                                     'string two',
                                     kwarg1=constants.ACTIVE,
                                     kwarg2=['a', 'b', 'c'])


Rather than constructing parameters inline, it is better to break things up::

    list_of_strings = [
        'what_a_long_string',
        'not as long',
    ]

    dict_of_numbers = {
        'one': 1,
        'two': 2,
        'twenty four': 24,
    }

    object_one.call_a_method('string three',
                             'string four',
                             kwarg1=list_of_strings,
                             kwarg2=dict_of_numbers)


Internationalization (i18n) Strings
-----------------------------------

At this time we have not worried much about internationalization.

Python 3.x compatibility
------------------------
Cloudmesh code should stay Python 3.x compatible. That means all Python 2.x-only
constructs should be avoided. An example is::

    except x,y:

Use::

    except x as y:

instead. Other Python 3.x compatility issues, like e.g. print operator
can be avoided in new code by using::

    from __future__ import print_function

at the top of your module.


Creating Unit Tests
-------------------

For every new feature, unit tests should be created that both test and
(implicitly) document the usage of said feature. If submitting a patch
for a bug that had no unit test, a new passing unit test should be
added. If a submitted bug fix does have a unit test, be sure to add a
new one that fails without the patch and passes with the patch.

We are using nosetest for our unit test environment.


Running Tests
-------------

We have build an easy to use test environment. To list the available
tests, please issue::

  fab test.info

it will list a number of available test classes. To further drill
down, please use one of the classes and issue the command (in our case
we use "keys")::

  fab test.info:keys

This will list you individual tests::

  test00_file
  test01_print
  test02_names
  test03_default
  test04_getvalue
  test05_set
  test06_get
  test07_get
  test08_set
  test09_type
  test10_fingerprint

You can execute them while specifying them to the start command by
giving a unique substring for that test. Thus::

  fab test.start:keys,file

or::

  fab test.start:keys,00

would both execute the test in keys with the name::

  test00_file 

Please not that not all tests are designed to pass as of yet. They are
also used for debugging the deployment environments.

 
   
Commit Messages
---------------

Using a common format for commit messages will help keep our git
history readable. Follow these guidelines:

* First, provide a brief summary of 50 characters or less.  Summaries
  of greater then 72 characters will be rejected by the gate.

* The first line of the commit message should provide an accurate
  description of the change, not just a reference to a bug or
  blueprint. It must be followed by a single blank line.

* If the change relates to a specific driver (libvirt, xenapi, qpid, etc...),
  begin the first line of the commit message with the driver name, lowercased,
  followed by a colon.

* Following your brief summary, provide a more detailed description of
  the patch, manually wrapping the text at 72 characters. This
  description should provide enough detail that one does not have to
  refer to external resources to determine its high-level functionality.

* Once you use 'git review', two lines will be appended to the commit
  message: a blank line followed by a 'Change-Id'. This is important
  to correlate this commit with a specific review in Gerrit, and it
  should not be modified.

For further information on constructing high quality commit messages,
and how to split up commits into a series of changes, consult the
project wiki form the OpenStack project:

*   http://wiki.openstack.org/GitCommitMessages
