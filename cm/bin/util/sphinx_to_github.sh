#! /bin/sh

# assume the following directory structure where contents of doc/ 
# and source/ are already checked into repo., with the exception 
# of the _build directory (i,e. you can check in _themes or _sources 
# or whatever else).
#
# proj/
#    source/
#    doc/
 
# remove doc/_build/html if present
cd doc && rm -rf doc/_build/html
 
# edit .gitignore to ignore _build
echo "_build" >> .gitignore
git add .gitignore
git commit -m 'ignoring _build'
 
#create a new directory (in doc/)
mkdir -p _build/html
 
# clone the entire repo into this directory (yes, this duplicates it)
git clone git@github.com:username/project.git _build/html
 
# set this directory to track gh-pages
git symbolic-ref HEAD refs/heads/gh-pages
rm .git/index
git clean -fdx
 
# in docs/, run `make html` to generate our doc, which will fill 
# _build/html, but not overwrite the .git directory
make html
 
# now, add these bad-boys to the gh-pages repo, along with .nojekyll:
cd _build/html
touch .nojekyll
git add .
git commit -m 'first docs to gh-pages'
git push origin gh-pages
 
# [optional] cleanup stuff in duplicate master (in docs/_build/html)
git co master
rm .git/index
git clean -fdx
 
# now, when you run `make html` and need to update your documentation, 
# you can do it "normally" without worrying about the many vagaries of 
# submodule syncing (I can never get the order correct).  just make 
# changes, then:
make html
cd _build/html
git commit -a -m 'made some changes, yo'
git push origin gh-pages