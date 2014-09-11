import cloudmesh

from pprint import pprint
import sys


t = cloudmesh.ssh_vm_with_command(
    "ubuntu", "149.165.159.37", "ls -la", key="~/.ssh/id_rsa")

print t
