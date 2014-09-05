from fabric.api import task, local, warn_only


@task
def pylint():
    """running pylint"""
    local("mkdir -p doc/build/html/qc/pylint")
    for modulename in ["cloudmesh_common",
                       "cloudmesh_install",
                       "cloudmesh",
                       "cmd3local",
                       "cloudmesh_web"]:
        print 70 * "="
        print "Building Pylint:", modulename
        print 70 * "="
        with warn_only():
            local("pylint --output-format=html {0} > "
                  "doc/build/html/qc/pylint/{0}.html"
                  .format(modulename))
