
BASENAME=$(shell basename $(PATHNAME))
GITREPO=cloudmesh

TAG=`cat VERSION.txt`
MANUALDIR=`pwd`


FILE=index

all:
	fab doc.html

random:
	python cloudmesh_management/generate.py

mongo:
	mongod --noauth --dbpath . --port 27777

watchdog:
	watchmedo shell-command --patterns="*.rst" --recursive --command="make; open doc/build/html/$(FILE).html" . 

c:
	/usr/bin/google-chrome-stable doc/build/html/index.html

f: 
	firefox doc/build/html/index.html 

doc.html:
	fab doc.html

doc.view:
	fab doc.view

server:
	python setup.py install
	cd cloudmesh_django; make server 

view:
	cd cloudmesh_django; make view

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
	git remote set-url origin git@github.com:$(GITREPO)/$(BASENAME).git


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

install:
	pip install dist/*.tar.gz

######################################################################
# PYPI
######################################################################

upload:
	make -f Makefile pip
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
	pep8 ./$(GITREPO)/virtual/cluster/
	pylint ./$(GITREPO)/virtual/cluster/ | less
	pyflakes ./$(GITREPO)/virtual/cluster/

# #####################################################################
# CLEAN
# #####################################################################


clean:
	find . -name "*~" -exec rm {} \;  
	find . -name "*.pyc" -exec rm {} \;  
	rm -rf build dist *.egg-info *~ #*
	cd doc; make clean
	rm -rf *.egg-info
	rm -f user.* local.* mongod.lock

cleanmongo:
	rm -rf mongodb.?
	rm -rf mongodb.ns


#############################################################################
# SETUP SPHINX BUILD ENVIRONMENT
###############################################################################

setupbuild_ubuntu:
	#essential system packages/libraries required
	sudo apt-get install g++ python-dev python-pip python-virtualenv git libfreetype6-dev libpng-dev mercurial make
	#manually install sphinxcontrib-autorun
	mkdir -p ~/hg
	cd ~/hg; hg clone http://bitbucket.org/birkenfeld/sphinx-contrib/; cd sphinx-contrib/autorun; python setup.py install
	#setting up essential building requirements
	cd $(MANUALDIR)
	pip install -r requirements_pre.txt
	easy_install -U distribute
	pip install -r requirements.txt
	pip uninstall PIL

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
	make pages

######################################################################
# TAGGING
######################################################################


tag:
	make clean
	python bin/util/next_tag.py
	git tag $(TAG)
	echo $(TAG) > VERSION.txt
	git add .
	git commit -m "adding version $(TAG)"
	git push


######################################################################
# ONLY RUN ON GH-PAGES
######################################################################

PROJECT=`basename $(PWD)`
DIR=/tmp/$(PROJECT)
DOC=$(DIR)/doc

pages: ghphtml ghpgit
	echo done

ghphtml:
	cd /tmp
	rm -rf $(DIR)
	cd /tmp; git clone git://github.com/$(GITREPO)/$(PROJECT).git
	cp $(DIR)/Makefile .
	cd $(DOC); ls; make html
	rm -fr _static
	rm -fr _source
	rm -fr *.html
	cp -r $(DOC)/build/html/* .

ghpgit:
	git add . _sources _static   
	git commit -a -m "updating the github pages"
	git push
	git checkout master

