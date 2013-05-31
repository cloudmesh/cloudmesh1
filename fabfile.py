from fabric.api import *
from fabric.contrib.console import confirm
from sh import git as _git
import os
import webbrowser
import platform
import sys

#
# SETTING THE BROWSER BASED ON PLATFORM
#
browser = "firefox"

if sys.platform == 'darwin':
    browser = "open"

#
# VERSION MANAGEMENT
#

#
# we are no longer doing version management with the VERSION.txt file,
# but instead including it in setup.py we need to change the code
# here, so do not use the version increment
#

#filename = "VERSION.txt"
#version = open(filename).read()

SERVER = "server"

"""
def _next_version(version):
    numbers = version.split(".")
    numbers[-1] = str(int(numbers[-1]) + 1)
    newversion = ".".join(numbers)
    return newversion


def _write_version(version):
    file = open(filename, 'w')
    print >> file, version
    file.close()
"""

def _cleantest():
    """wipe out the database and rerun the test. not recommended."""
    local("python cloud_mesh.py")
    cm()


def cm():
    """run the server and look at the output with the browser"""
    file = open("Makefile~", "w")
    print >> file, """
all: server view

server:
	python flask_cm/server.py

view:
	sleep 10
	 %s http://127.0.0.1:5000/table/
""" % browser
    #webbrowser.open("http://127.0.0.1:5000")
    file.close()
    os.system("make -j -f Makefile~ all")

def deltag(tag):
    local("git tag -d %s" % tag)
    local("git push origin :refs/tags/%s" % tag)


def view():
    """run the browser"""
    local("sleep 1")
    local("%s http://localhost:5000/table" % browser)


def clean():
    """clean the directory"""
    local("find . -name \"#*\" -exec rm {} \\;")
    local("find . -name \"*~\" -exec rm {} \\;")
    local("find . -name \"*.pyc\" -exec rm {} \\;")
    local("rm -rf build dist *.egg-info")
    local("rm -rf doc/build ")


def git():
    """upload the changes to git"""
    clean()
    _git("add", ".")
    os.system("git commit")
    _git("push")


'''
def tag():
    """introduce a new tag and upload it to git. run fab changes first and
       add that to CHANGES.txt"""
    global version
    local("make clean")
    new_version = _next_version(version)
    _write_version(new_version)
    _git("add", ".")
    _git("tag", "%s" % new_version)
    _git("commit", "-m", "adding version %s" % new_version)
    _git("push")
    changes()
'''

def changes():
    """look at the changes in github since the last taged version"""
    gitversion = _git("describe", "--abbrev=0", "--tags").strip()
    tags = _git("tag").split("\n")
    tags = tags[:-1]

    versions = {'previous': tags[-1],
                'head': 'HEAD',
                'next': _next_version(tags[-1])}

    print versions
    headline = "CHANGES %(previous)s -> %(next)s" % versions
    print headline
    print len(headline) * "="
    print
    change = _git("log",
                  "%(previous)s...%(head)s" % versions,
                  "--no-merges", "--format=* %B")
    change = change.replace("\n\n", "\n")
    print change


def dist():
    clean()
    local("python setup.py sdist")


def force():
    dist()
    local("pip install -U dist/*.tar.gz")


def pypi():
    force()
    #	python setup.py register
    local("python setup.py sdist upload")


def install():
    """install Flask Frozen-Flask Flask-FlatPages"""
    local("pip install Flask Frozen-Flask Flask-FlatPages")
    local(
        "pip install --upgrade -e git://github.com/openstack/python-novaclient.git#egg=python-novaclient")


def installmongodb():
    local('ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"')
    local('brew update')
    local('brew install mongodb')


def installmongodb_ubuntu():
    local('sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10')
    local(
        'sudo sh -c "echo \'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen\' > /etc/apt/sources.list.d/10gen.list"')
    local('sudo apt-get update')
    local('sudo apt-get install mongodb-10gen')
