import sys
import os
import yaml

sys.path.insert(0, '..')

from cloudmesh.inventory.old_inventory import FabricImage, FabricServer, \
    FabricService, Inventory
from mongoengine import *

# ============================================================
# INVENTORY
# ============================================================

# db = connect ("nosetest")

inventory = Inventory("nosetest")

# inventory.config("server.yaml")


# print inventory.configuration


"""

server_config = SafeConfigParser(
    {'name': 'flasktest'})  # Default database name
server_config.read("server.config")

inventory_db = server_config.get("mongo", "dbname")
if server_config.has_option("mongo", "host"):
    inventory = Inventory(inventory_db,
                          server_config.get("mongo", "host"),
                          server_config.getint("mongo", "port"),
                          server_config.get("mongo", "user"),
                          server_config.get("mongo", "pass"))
else:
    inventory = Inventory(inventory_db)
"""

inventory.clean()

inventory.create_cluster("bravo", "b-[001-016]", "101.102.203.[11-26]", "b-[001]")
inventory.create_cluster("delta", "d-[001-016]", "102.202.204.[1-16]", "d-[001]")
inventory.create_cluster("gamma", "g-[001-016]", "302.202.204.[1-16]", "g-[001]")
inventory.create_cluster("india", "i[1-128]", "101.52.206.[1-128]", "i[130,001]")
inventory.create_cluster("sierra", "s-[001-128]", "502.202.204.[1-128]", "s-[001]")



centos = FabricImage(
    name="centos6",
    osimage='/path/to/centos0602v1-2013-06-11.squashfs',
    os='centos6',
    extension='squashfs',
    partition_scheme='mbr',
    method='put',
    kernel='vmlinuz-2.6.32-279.19.1.el6.x86_64',
    ramdisk='initramfs-2.6.32-279.19.1.el6.x86_64.img',
    grub='grub',
    rootpass='reset'
)
centos.save()

redhat = FabricImage(
    name="ubuntu",
    osimage='/BTsync/ubuntu1304/ubuntu1304v1-2013-06-11.squashfs',
    os='ubuntu',
    extension='squashfs',
    partition_scheme='mbr',
    method='btsync',
    kernel='vmlinuz-2.6.32-279.19.1.el6.x86_64',
    ramdisk='initramfs-2.6.32-279.19.1.el6.x86_64.img',
    grub='grub2',
    rootpass='reset'
)
redhat.save()

inventory.refresh()

for cluster in inventory.clusters:
    cluster.images = [centos, redhat]
    cluster.save(cascade=True)


c = inventory.get("cluster", "bravo")

# print "LLLL", [image.name for image in c.images]

inventory.print_info()

