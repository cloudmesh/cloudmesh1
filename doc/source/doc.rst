

I started a framework for sphinx docs at

http://futuregrid.github.com/flask_cm/

how to contribute, go to the doc/source add stuff::

   cd doc
   make html
   open a browser on build/html/index.html

if this works 

go to flask_cm

::

    fab clean
    git status

see which files you changed

add them explicitly with git add <dir/filename>

do git status just to be sure::

   git commit -a

if nothing wrong::

   git push 
