from fabric.api import task, local
from util import yaml_file_replace
import progress

@task
@task
def create():
        
    from IPython.lib import passwd
    from fabfile.util import yaml_file_replace


    local("ipython profile create nbserver")
    local('cp etc/ipython_notebook_config.py ~/.ipython/profile_nbserver')
    result = passwd()

    
    yaml_file_replace(filename='/../.ipython/profile_nbserver/ipython_notebook_config.py',
                      replacements={'SHAPASSWD': result}
                      )


    progress.off()
    filename = "~/.ipython/profile_nbserver/mycert.pem"
    local("openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout {0} -out {0}".format(filename))
    local("chmod go-rw ~/.ipython/profile_nbserver/mycert.pem")


@task
def start():
    progress.off()
    local("mkdir -p ~/notebook/")
    local("cd ~/notebook/ && ipython notebook --certfile=~/.ipython/profile_nbserver/mycert.pem --profile=nbserver")
