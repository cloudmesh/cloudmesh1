from fabric.api import task, local
import sys
import os

browser = "firefox"

if sys.platform == 'darwin':
    browser = "open"

@task
def view():
    """view the documentation in a browser"""
    local("{browser} doc/build/html/index.html".format(browser=browser))

@task
def html():
    # disable Flask RSTPAGES due to sphins incompatibility
    os.environ['RSTPAGES'] = 'FALSE'
    api()
    man()
    """build the doc locally and view"""
    local("cd doc; make html")


@task
def publish():
    """deploy the documentation on gh-pages"""
    html()
    local("cd docs/build/html && git add .  && git commit -m "site generated" && git push origin gh-pages")
    local("git commit -a -m "build site")
    local("git push origin master")

@task
def man():
    """deploy the documentation on gh-pages"""
    #TODO: match on "Commands"
    local("cm man | grep -A10000 \"Commands\"  | sed \$d  > doc/source/man/man.rst")

@task
def api():
    for modulename in ["cloudmesh", "cloudmesh_common", "cloudmesh_install", "cloudmesh_cmd3", "cloudmesh_web"]:
        print 70 * "="
        print "Building API Doc:", modulename 
        print 70 * "="        
        local("sphinx-apidoc -f -o doc/source/api/{0} {0}".format(modulename))



