from fabric.api import task, local, execute
import clean
import os
from sys import platform
from cloudmesh.util.password import get_password, get_user, get_host

input = raw_input

__all__ = ['user','install','host','allow']

@task
def install():
    """install the rabitmq"""
    if platform == "darwin":
        local("brew install rabbitmq")
    else:
        print "ERROR: error no other install yet provided "
        sys.exit()

@task
def user(name=None):
    ''' create a user in rabit mq
    
    :param name: if the name is ommited it will be queried for it.
    '''
    if name is None: 
        user = get_user()
    password = get_password()
    local("rabbitmqctl {0} {1}".format(name,password))

@task
def host():
    """adding a host to rabitmq"""
    host = get_host()
    local("rabbitmqctl add_vhost {0}".format(host))

@task
def allow():
    """allow a user to access the host in rabitmq"""
    values = {
        'host': get_host(),
        'user': get_user()
        }
    #print('rabbitmqctl set_permissions -p {host} {user} ".*" ".*" ".*"'.format(**values))
    local('rabbitmqctl set_permissions -p {host} {user} ".*" ".*" ".*"'.format(**values))
