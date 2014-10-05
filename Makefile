gh-ATHNAME=$(shell pwd)
BASENAME=$(shell basename $(PATHNAME))

TAG=`echo "print __version__" > v.py;  cat cloudmesh/__init__.py v.py > /tmp/v1.py; python /tmp/v1.py; rm /tmp/v1.py v.py`

all:
	make -f Makefile force


stats:
	pep8 --statistics --filename *.py */*.py */*/*.py */*/*/*.py */*/*/*/*.py */*/*/*/*/*.py

autopep8:
	autopep8 -i */*.py
	autopep8 -i */*/*.py
	autopep8 -i */*/*/*.py
	autopep8 -i */*/*/*/*.py
	autopep8 -i */*/*/*/*/*.py
	autopep8 -i */*/*/*/*/*/*.py

######################################################################
# GIT INTERFACES
######################################################################
push:
	make -f Makefile clean
	git commit -a 
	git push

pull:
	git pull 

gregor:
	git config --global user.name "Gregor von Laszewski"
	git config --global user.email laszewski@gmail.com

git-ssh:
	git remote set-url origin git@github.com:cloudmesh/$(BASENAME).git


######################################################################
# INSTALLATION
######################################################################
req:
	pip install -r requirements.txt

dist:
	make -f Makefile pip

sdist: clean
	#make -f Makefile clean
	python setup.py sdist --format=bztar,zip


force:
	make -f Makefile nova
	make -f Makefile pip
	pip install -U dist/*.tar.gz

install:
	pip install dist/*.tar.gz

######################################################################
# PYPI
######################################################################

upload: sdist
#	python setup.py register
	python setup.py sdist upload

pip-register:
	python setup.py register

######################################################################
# QC
######################################################################

qc-install:
	pip install pep8
	pip install pylint
	pip install pyflakes

qc:
	pep8 ./cloudmesh/virtual/cluster/
	pylint ./cloudmesh/virtual/cluster/ | less
	pyflakes ./cloudmesh/virtual/cluster/

# #####################################################################
# CLEAN
# #####################################################################


clean:
	fab clean.all

uninstall:
	yes | pip uninstall cloudmesh

#############################################################################
# SPHINX DOC
###############################################################################

sphinx:
	@echo "please use fab doc.html and fab doc.view instead"

#	cd doc; make html
#ifeq ("$(shell uname)","Darwin")
#	open doc/build/html/index.html
#endif

#############################################################################
# PUBLISH GIT HUB PAGES
###############################################################################

gh-pages:
	git checkout gh-pages
	make pages

######################################################################
# TAGGING
######################################################################

print_tag:
	@echo "VERSION: $(TAG)"

tag:
	@echo "VERSION: $(TAG)"
	make clean
	python bin/util/next_tag.py
	git tag $(TAG)
	echo $(TAG) > VERSION.txt
	git add .
	git commit -m "adding version $(TAG)"
	git push


