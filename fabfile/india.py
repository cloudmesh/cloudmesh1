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

@task
def ipython():
    IPython.lib import passwd
    from fabfile.util import yaml_file_replace


    local("ipython profile create nbserver")
    local('cp etc/ipython_notebook_config.py ~/.ipython/profile_nbserver')
    result = passwd()

    
    yaml_file_replace(filename='~/.ipython/profile_nbserver/ipython_notebook_config.py',
                      replacements={'SHAPASSWORD': result}
                      )
    
    local("openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout mycert.pem -out ~/.ipython/profile_nbserver/mycert.pem")
    local("chmod go-rw ~/.ipython/profile_nbserver/mycert.pem")


@task
def start():
    local("ipython notebook --certfile=~/.ipython/profile_nbserver/mycert.pem --profile=nbserver")
