from cloudmesh_base.util import banner
from cloudmesh_base.locations import config_file
import os
from cloudmesh_base.Shell import Shell


class Clean(object):
    @classmethod
    def dir(cls):
        """clean the dirs"""
        banner("clean the directory")
        commands = '''
            find . -name \"#*\" -exec rm {} \\;
            find . -name \"*~\" -exec rm {} \\;
            find . -name \"*.pyc\" -exec rm {} \\;
        '''.split("\n")
        for command in commands:
            command = command.strip()
            if command != "":
                print "Executing:", command
                os.system(command)
        Shell.rm("-rf", "build", "dist", "*.egg-info")
        Shell.rm("-rf", "docs/build", "dist", "*.egg-info")
        Shell.rm("-f", "celeryd@*")
        Shell.rm("-f", "*.dump")
        Shell.rm("-f", "*.egg")

    @classmethod
    def cmd3(cls):
        d = config_file("/cmd3local")
        print("rm -rf", d)
        Shell.rm("-rf", "{0}".format(d))

    @classmethod
    def delete_package(cls, name):
        try:
            banner("CLEAN PREVIOUS {0} INSTALLS".format(name))
            r = int(local("pip freeze |fgrep {0} | wc -l".format(name), capture=True))
            while r > 0:
                local('echo "y" | pip uninstall {0}'.format(name))
                r = int(
                    local("pip freeze |fgrep {0} | wc -l".format(name), capture=True))
        except:
            print "ERROR: uninstalling", name

    @classmethod
    def all(cls):
        """clean the dis and uninstall cloudmesh"""
        cls.dir()
        cls.cmd3()
        banner("CLEAN PREVIOUS CLOUDMESH INSTALLS")
        cls.delete_package("cloudmesh")
        cls.delete_package("cmd3")
        cls.delete_package("cloudmesh_base")
