from fabric.api import task, local
import sys
import os
from build import cursor_on

from cloudmesh_base.util import banner

browser = "firefox"

if sys.platform == 'darwin':
    browser = "open"

debug = True    



class Doc(object):

    @classmethod
    def view(cls):
        """view the documentation in a browser"""
        os.system("{browser} docs/build/html/index.html".format(browser=browser))

    @classmethod
    def html(cls):
        # disable Flask RSTPAGES due to sphins incompatibility
        os.environ['RSTPAGES'] = 'FALSE'
        banner("API Generation")
        api()
        banner("Manual Pages")
        man()
        # build the docs locally and view
        banner("Make the sphinx documentation")
        os.system("cd docs; make html")
        cursor_on()

    @classmethod
    def publish(cls):
        """deploy the documentation on gh-pages"""
        banner("publish doc to github")
        os.system("ghp-import -n -p docs/build/html")
        #html()
        #local('cd docs/build/html && git add .  && git commit -m "site generated" && git push origin gh-pages')
        #local('git commit -a -m "build site"')
        #local("git push origin master")

    @classmethod
    def man(cls):
        """deploy the documentation on gh-pages"""
        # TODO: match on "Commands"
        os.system('cm man | grep -A10000 \"Commands\"  |'
              ' sed \$d  > docs/source/man/man.rst')

    @classmethod
    def api(cls):
        """creates the api man pages"""
        for modulename in ["cloudmesh",
                           "cloudmesh_admin",
                           "cloudmesh_common",
                           "cloudmesh_install",
                           "cloudmesh_cmd3",
                           "cloudmesh_web",
                           "fabfile"]:
            print 70 * "="
            print "Building API Docs:", modulename
            print 70 * "="
            os.system("sphinx-apidoc -f -o docs/source/api/{0} {0}".format(modulename))
            print "done"


@task
def view():
    """view the documentation in a browser"""
    Doc.view()


@task
def html():
    # disable Flask RSTPAGES due to sphins incompatibility
    Doc.html()
    cursor_on()


@task
def publish():
    """deploy the documentation on gh-pages"""
    Doc.publish()


@task
def man():
    """deploy the documentation on gh-pages"""
    # TODO: match on "Commands"
    os.system('cm debug off')
    Doc.man()


@task
def api():
    """creates the api man pages"""
    Doc.api()
