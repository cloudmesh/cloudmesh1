import sys
import os
import yaml

sys.path.insert(0, '..')

from cloudmesh.inventory.resources import FabricImage, FabricServer, \
    FabricService, Inventory
    
# ============================================================
# INVENTORY
# ============================================================

inventory = Inventory("test")

# inventory.config("server.yaml")

        
print inventory.configuration


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

inventory.create_cluster("bravo", "101.102.203.[11-26]", "b{0:03d}", 1,
                         "b001", "b")
inventory.create_cluster("delta", "102.202.204.[1-16]", "d-{0:03d}", 1,
                         "d-001", "d")
inventory.create_cluster("gamma", "302.202.204.[1-16]", "g-{0:03d}", 1,
                         "g-001", "g")
inventory.create_cluster("india", "402.202.204.[1-128]", "i-{0:03d}", 1,
                         "i-001", "i")
inventory.create_cluster("sierra", "502.202.204.[1-128]", "s-{0:03d}", 1,
                         "s-001", "s")


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
).save()

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
).save()
