import sys
from datetime import datetime
import pprint
pp = pprint.PrettyPrinter(indent=4)
import json
import os
import random


from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from libcloud.compute.types import NodeState

import libcloud.security
import time
from sh import fgrep

# from openstack.util.cm_table import table as cm_table
from cloudmesh.config.cm_config import cm_config


class eucalyptus:

    def config(self, label=None, project=None, accessKey=None, secretKey=None):
        """
        reads in the configuration file if specified, and does some
        internal configuration.
        """
        if label is None and accessKey is None:
            label = 'india-eucalyptus'
            project = 'fg-82'

        if accessKey is None:
            self.label = label

            config = cm_config()
            configuration = config.get(label)

            pp.pprint(configuration)

            basedir = configuration['BASEDIR'] = configuration[
                'BASEDIR'].replace('~', os.environ['HOME'])
            configuration[project]['EC2_PRIVATE_KEY'] = "%s/%s" % (
                basedir, configuration[project]['EC2_PRIVATE_KEY'])
            configuration[project]['EUCALYPTUS_CERT'] = "%s/%s" % (
                basedir, configuration[project]['EUCALYPTUS_CERT'])

            pp.pprint(configuration)

            self.credentials['accessKey'] = configuration[
                project]['EC2_ACCESS_KEY']
            self.credentials['secretKey'] = configuration[
                project]['EC2_SECRET_KEY']

        else:
            self.credentials['accessKey'] = accessKey
            self.credentials['secretkey'] = secretKey

    def getNodebyID(self, nodeid):
        nodes = self.cloud.list_nodes()
        for node in nodes:
            if node.id == nodeid:
                return node

    def vm_delete(self, node):
        result = self.destroy_node(self, node)
        # add result to internal cache
        print ("vm Deleted")
        return result

    def restart(self, node):
        """restarts a vm with the given name"""
        result = self.reboot_node(self, node)
        # add result to internal cache
        print result

    def vm_create(self, name, flavor_name, image_id):
        """
        create a vm
        """
        self.vm = self.cloud.create_node(
            name=vm_name, image=vm_image, size=vm_flavour)

        while 1:
            time.sleep(15)
            updatedNode = self.getNodebyID(self.vm.id)
            if updatedNode.state == 3:
                print "pending " + updatedNode.id
            if updatedNode.state == 0:
                print("successful creation of vm")
                time.sleep(60)
                break
            if updatedNode.state == 4:
                print(self.vm.id, "Has Errored out")
                # TODO: BUG clearly wrong, as remove also does not exist for a
                # dict if we change to self.
                nodes.remove(vm)
                break

        data = self.vm.__dict__
        del data['driver']
        pp.pprint(data)
        return {}
