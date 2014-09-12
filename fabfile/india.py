from fabric.api import task
from util import ec2secgroup_openport, yaml_file_replace


@task
def configure():
    """configure india environment for cloudmesh rapid deployment"""
    yaml_file_replace(filename='/cloudmesh_server.yaml',
                      replacements={
                                    'browser: True': 'browser: False',
                                    'host: 127.0.0.1': 'host: 0.0.0.0'
                                    }
                      )
    ec2secgroup_openport('india', 5000)
    print "Configuration changes have been made successfully"
