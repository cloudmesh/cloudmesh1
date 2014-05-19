from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

domain_name = "futuregrid.org"


@task
def download(host_ids):
    # host_ids = india_openstack_havana,sierra_openstack_grizzly
    for host_id in host_ids.split(","):
        host_from_env = env.host.split(".")[0]
        host_from_input = host_id.split("_")[0]
        if host_from_input == host_from_env:
            local("mkdir -p ~/.futuregrid/clouds/%s/" % host_id)
            with settings(warn_only=True):
                if get("~/.futuregrid/openstack/novarc",
                       "~/.futuregrid/clouds/%s/novarc" %
                       host_id).failed:
                    get("~/.futuregrid/novarc", "~/.futuregrid/clouds/%s/novarc" %
                        host_id)
        else:
            pass#print host_id.split("_")[0], host

            # Task 4. write cloudmesh.yaml based on the credentials
