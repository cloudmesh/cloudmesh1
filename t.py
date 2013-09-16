#
#  fab queue.start:1
#  python t.py

#
from cloudmesh.provisioner.queue.celery import celery
from cloudmesh.provisioner.queue.tasks import info, provision
from cloudmesh.inventory.inventory import FabricImage, FabricServer, \
    FabricService, Inventory

inventory = Inventory("nosetest")
import hostlist

import time
from pprint import pprint

"""
t = info.delay()

print t.status
for i in range(10):
    time.sleep(1)
    print t.status
    if t.status == 'SUCCESS':
        break


print t.get()
"""
inventory.print_cluster("bravo")
hosts = hostlist.expand_hostlist("b-[001-008]")

for host in hosts:
    print "PROVISION HOST", host
    provision.delay(host, "openstack")

    # t[host] = provision.delay(host,"openstack")

    # t[host] = provision.delay(host,"hpc")

    # i = celery.control.inspect()



# for j in range(10):
#    print chr(27) + "[2J"
#    inventory.print_cluster("bravo")
#    for host in hosts:
#        print host, t[host].status
#    pprint (i.active())
#    pprint (i.scheduled())
#    pprint (i.reserved())
#    time.sleep(1)

# for j in range(10):
#    for host in hosts:
#        print t[host].status()

