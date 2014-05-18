from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

domain_name = "futuregrid.org"

@task
def download(host_ids):
    for host_id in host_ids:
        host = env.host.split(".")
        host = host[0]
        if host_id.split("_")[0] == host:
            with settings(warn_only=True):
                if get("~/.futuregrid/openstack/novarc", "~/.futuregrid/clouds/%s/" %
                       env.host.split("_")[0]).failed:
                    get("~/.futuregrid/novarc", "~/.futuregrid/clouds/%s/" %
                        env.host.split("_")[0])

            # Task 4. write cloudmesh.yaml based on the credentials

