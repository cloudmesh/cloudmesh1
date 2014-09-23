from fabric.api import task
from util import ec2secgroup_openport, yaml_file_replace
from cloudmesh_install import config_file
from cloudmesh.config.cm_config import yaml_attribute_replace

@task
def configure():
    """configure india environment for cloudmesh rapid deployment"""
    
    # running on server mode with external port listening
    yaml_file_replace(filename='/cloudmesh_server.yaml',
                      replacements={
                                    'browser: True': 'browser: False',
                                    'host: 127.0.0.1': 'host: 0.0.0.0'
                                    }
                      )
    # port 5000 needs to be open
    # ec2secgroup_openport('india', 5000)
    # now managed via nova before vm is started.
    
    # new way to replace an attribute in yaml
    filename = config_file("/cloudmesh.yaml")
    replacements = {
        "cloudmesh.clouds.india.cm_service_url_type": "internalURL",
    }
    yaml_attribute_replace(filename,replacements,indent_by=2)
    
    print "Configuration changes have been made successfully"
