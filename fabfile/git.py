from fabric.api import task, local
import os

class Git(object):

    @classmethod
    def push(cls):
        """git push"""
        os.system("git commit -a ")
        os.system("git push")

    def gregor():
        """git config of name and email for gregor"""
        os.system('git config --global user.name "Gregor von Laszewski"')
        os.system('git config --global user.email laszewski@gmail.com')


@task
def push():
    """git push"""
    Git.push()


@task
def gregor():
    """git config of name and email for gregor"""
    Git.gregor()


def up():
    """upload the changes to git"""
    clean()
    local("git add .")
    local("git commit")
    local("git push")


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
    #   python setup.py register
    local("python setup.py sdist upload")


def install():
    """install Flask Frozen-Flask Flask-FlatPages"""
    local("pip install Flask Frozen-Flask Flask-FlatPages")
    local('pip install --upgrade -e '
          'git://github.com/openstack/python-novaclient.git#egg=python-novaclient')


def installmongodb():
    local('ruby -e "$(curl -fsSL https://raw.github.com/mxcl/homebrew/go)"')
    local('brew update')
    local('brew install mongodb')


def installmongodb_ubuntu():
    local('sudo apt-key adv --keyserver keyserver.ubuntu.com --recv 7F0CEB10')
    local('sudo sh -c '
        '"echo \'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen\'
        '> /etc/apt/sources.list.d/10gen.list"')
    local('sudo apt-get update')
    local('sudo apt-get install mongodb-10gen')


def _next_version(version):
    numbers = version.split(".")
    numbers[-1] = str(int(numbers[-1]) + 1)
    newversion = ".".join(numbers)
    return newversion


def _write_version(version):
    file = open(filename, 'w')
    print >> file, version
    file.close()
'''


def deltag(tag):
    local("git tag -d %s" % tag)
    local("git push origin :refs/tags/%s" % tag)
