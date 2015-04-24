Deprecated packages, developments
=================================

In Cloudmesh, if some functions, modules or classes are no longer needed, we
move them into the deprecated place with a new replacement.  This document
describes the rule as how to deal with deprecated packages and development.

Deprecated directory 
--------------------

In each (sub)module, you have `deprecated` directory to contain outdated files.

Python Files 
------------

File name should be changed with the suffix `-old`. For example, `abc.py` will
be changed to `abc.py-old` so that `pylint` program can ignore such a file
while it's processing.

Python Functions 
------------------

Triple quoted strings (Multi-line comments) are recommended to change functions
to a string.

Replacement 
-----------

To provide better performance and easier development, the source code need to
be improved. Functions, modules, or classes can be updated with a general
protocol to be used in many places in an easy way. This requires sometimes a
new function name, a new module or a new class.

Gradual Change 
--------------

We keep the deprecated development for a certain amount of time until they
permanently removed from the Git repository. [x] months later, we delete
`*-old` files. [x] months lter, we remove commented functions. The history of
Git keeps all development so we don't loose any changes from the beginning.



