from fabric.api import task
from cloudmesh_base.util import banner
from cloudmesh_base.ConfigDict import ConfigDict
from cloudmesh.config.cm_config import cm_config
from cloudmesh.user.cm_user import cm_user
from cloudmesh.shell.Shell import Shell
from cloudmesh_base.locations import config_file


@task
def password():
    user_config = cm_config(filename=config_file("/cloudmesh.yaml"))
    user = user_config.cloud('india')['credentials']

    server_config = ConfigDict(filename=config_file("/cloudmesh_server.yaml"))
    server = server_config.get('cloudmesh.server.keystone.india')

    print(" ".join(["keystone", "--os-username", server['OS_USERNAME'],
                    "--os-password", server['OS_PASSWORD'],
                    "--os-tenant-name", server['OS_TENANT_NAME'],
                    "--os-auth-url", server['OS_AUTH_URL'],
                    "user-password-update",
                    "--pass", user['OS_PASSWORD'], user['OS_USERNAME']]))

    Shell.keystone("--os-username", server['OS_USERNAME'],
             "--os-password", server['OS_PASSWORD'],
             "--os-tenant-name", server['OS_TENANT_NAME'],
             "--os-auth-url", server['OS_AUTH_URL'],
             "user-password-update",
             "--pass", user['OS_PASSWORD'], user['OS_USERNAME'])


@task
def delete_defaults():
    filename = config_file("/cloudmesh.yaml")
    banner("reading data from {0}".format(filename))
    config = cm_config(filename=filename)
    username = config.get("cloudmesh.hpc.username")

    print username

    user = cm_user()

    user.set_defaults(username, {})
    # user.set_default_attribute(username, 'images', {})

    user.info(username)


@task
def register():
    from cloudmesh.server.database import Database
    database = Database()
    database.set_credentials()


@task
def mongo(passwd=None):
    from cloudmesh.server.database import Database

    database = Database()
    if passwd is None:
        database.set_password_local()
    else:
        database.set_password_local(passwd=passwd)

    database.set_credentials()
    database.initialize_user()
