""" run with

nosetests -v --nocapture test_cm.py

"""
from cloudmesh_common.util import HEADING
from cloudmesh_common.logger import LOGGER, LOGGING_ON, LOGGING_OFF

log = LOGGER(__file__)

import sys
import os



if os.path.isdir(os.path.expanduser("~/.cloudmesh")):
    print "ERROR", "you must not have a .cloudmesh dir to run this test"
    sys.exit()


class Test:

    def get_user(self):
        import cloudmesh    
        config = cloudmesh.load("user")
        self.username = config.get("cloudmesh.hpc.username")

    
    def setup(self):
        self.project_id = "fg82"

    def tearDown(self):
        pass

    
    def test_01_git(self):
        os.system("git pull")
                
    def test_02_init(self):
        HEADING()        
        #os.system("rm ~/.cloudmesh")
        os.system("./install system")
        os.system("./install requirements")

    def test_03_user(self):
        HEADING()        
        os.system("./install new")

    def test_04_cloudmesh_install(self):
        HEADING()        
        os.system("./install cloudmesh")
        
    def test_05_fetch(self):
        HEADING()        
        os.system("cm-iu user fetch")
        os.system("cm-iu user create")        

    def test_06_mongo(self):
        HEADING()
        os.system("fab mongo.reset")
        
    def test_07_key(self):
        HEADING()
        self.get_user() 
        os.system('cm "key add --keyname={0}-key ~/.ssh/id_rsa.pub"'.format(self.username))

    def test_08_project(self):
        os.system("cm project default {0}".format(self.project_id))

        
    def test_09_help(self):
        HEADING()

        import cloudmesh
        cloud_commands = [
            "cloud",
            "group",
            "inventory",
            "rain",
            "storm",
            "yaml",
            "keys",
            "defaults",
            "image",
            "list",
            "register",
            "user",
            "debug",
            "project",
            "flavor",
            "init",
            "metric",
            "security_group",
            "vm",
            "loglevel",
            ]

        success = True
        for command in cloud_commands:
            execution = "help {0}".format(command)
            print "testing", execution,
            try:
                result = cloudmesh.shell(execution)
            except Exception, e:
                success = False
                print e
            if "Usage" not in result:
                print command, "ERROR", result
                success = False
            else:
                success = success 
                print "ok"
        assert success 

        
    def test_10_cloud_on(self):
        HEADING()
        os.system("cm cloud on india")
                
