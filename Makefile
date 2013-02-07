PATHNAME=$(shell pwd)
BASENAME=$(shell basename $(PATHNAME))

all:
	make -f Makefile force

######################################################################
# NOVA CLIENT
######################################################################
nova:
	#pip install --upgrade -e git+https://github.com/openstack/python-novaclient.git#egg=python-novaclient
	pip install --upgrade -e git://github.com/openstack/python-novaclient.git#egg=python-novaclient

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
	git remote set-url origin git@github.com:futuregrid/$(BASENAME).git


######################################################################
# INSTALLATION
######################################################################
dist:
	make -f Makefile pip

pip:
	make -f Makefile clean
	python setup.py sdist


force:
	make -f Makefile nova
	make -f Makefile pip
	pip install -U dist/*.tar.gz
	cp bin/cm $(VIRTUAL_ENV)/bin/cm
	chmod a+x $(VIRTUAL_ENV)/bin/cm


install:
	pip install dist/*.tar.gz

test:
	make -f Makefile clean	
	make -f Makefile distall
	pip install --upgrade dist/*.tar.gz
	fg-cluster
	fg-local

######################################################################
# PYPI
######################################################################

upload:
	make -f Makefile pip
#	python setup.py register
	python setup.py sdist upload

######################################################################
# QC
######################################################################

qc-install:
	pip install pep8
	pip install pylint
	pip install pyflakes

qc:
	pep8 ./futuregrid/virtual/cluster/
	pylint ./futuregrid/virtual/cluster/ | less
	pyflakes ./futuregrid/virtual/cluster/

# #####################################################################
# CLEAN
# #####################################################################


clean:
	find . -name "*~" -exec rm {} \;  
	find . -name "*.pyc" -exec rm {} \;  
	rm -rf build dist *.egg-info *~ #*
#	cd doc; make clean

######################################################################
# pypi
######################################################################

pip-register:
	python setup.py register

upload:
	make -f Makefile pip
	python setup.py sdist upload

#############################################################################
# SPHINX DOC
###############################################################################

sphinx:
	cd doc; make html

#############################################################################
# PUBLISH GIT HUB PAGES
###############################################################################

gh-pages:
	git checkout gh-pages
	make
