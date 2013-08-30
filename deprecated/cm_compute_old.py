#! /usr/bin/env pytho

#
# see also http://docs.openstack.org/cli/quick-start/content/nova-cli-reference.html
#

import iso8601
import sys
sys.path.insert(0, '../..')

from datetime import datetime
import pprint
pp = pprint.PrettyPrinter(indent=4)
import json
import os

from sh import fgrep
import novaclient
from sh import nova

# from cm_credential import credentials
from cloudmesh.util.cm_table import cm_table
from cloudmesh.config.cm_config import cm_config

from novaclient.v1_1 import client


class openstack:

    type = "openstack"   # global var
    flavors = {}         # global var
    images = {}          # global var
    servers = {}         # global var
    credential = None    # global var
    label = None         # global var

    cloud = None         # internal var
    user_id = None       # internal var

    _nova = nova

    def vms(self):
        return self.servers

    def credentials(self, cred):
        self.credential = cred

    #
    # initialize
    #
    def __init__(self,
                 label,
                 authurl=None,
                 project=None,
                 username=None,
                 password=None):
        """
        initializes the openstack cloud from a defould novaRC file
        locates at ~/.futuregrid.org/openstack. However if the
        parameters are provided it will instead use them
        """

        self.clear()
        self.label = label
        self.config(label,
                    authurl=authurl,
                    project=project,
                    username=username,
                    password=password)
        self.connect()

    def clear(self):
        """
        clears the data of this openstack instance, a new connection
        including reading the credentials and a refresh needs to be
        called to obtain again data.
        """
        self.type = "openstack"
        self.flavors = {}
        self.images = {}
        self.servers = {}
        self.credential = None
        self.cloud = None
        self.user_id = None

    def connect(self):
        """
        establishes a connection to the OpenStack cloud,
        e.g. initializes the needed components to conduct subsequent
        queries.
        """
        self.cloud = client.Client(
            self.credential['OS_USERNAME'],
            self.credential['OS_PASSWORD'],
            self.credential['OS_TENANT_NAME'],
            self.credential['OS_AUTH_URL']
        )

    def config(self, label,
               authurl=None,
               project=None,
               username=None,
               password=None):
        """
        reads in the configuration file if specified, and does some
        internal configuration.
        """
        self.label = label
        if username is None:
            config = cm_config()
            self.credential = config.get(label)
            print self.credential
            self.user_id = self.credential['OS_USER_ID']
            # self.credential = credentials(label)
        else:
            self.credential = {}
            self.credential['OS_USERNAME'] = username
            self.credential['OS_PASSWORD'] = password
            self.credential['OS_AUTH_URL'] = authurl
            self.credential['label'] = label
            self.credential['OS_TENANT_NAME'] = project
        """
        self._nova = nova.bake("--os-username",    self.credential.username,
                               "--os-password",    self.credential.password,
                               "--os-auth-url",    self.credential.url,
                               "--os-tenant-name", self.credential.project)
        """

    #
    # find userid
    #

    def intro(self, what):
        """ usde to find some methods form novaclient"""
        import inspect

        print 70 * "="
        print "class ", what.__class__.__name__, ":"
        list = inspect.getmembers(what, predicate=inspect.ismethod)
        for element in list:
            print "    ", element[0]
        try:
            pp.pprint(what.__dict__)
        except:
            return

    def novaclient_dump(self):

        # playing around to discover methods
        self.intro(self.cloud)
        self.intro(self.cloud.services)
        self.intro(self.cloud.servers)
        self.intro(self.cloud.client)

        self.intro(self.cloud.agents)
        self.intro(self.cloud.aggregates)
        self.intro(self.cloud.availability_zones)
        self.intro(self.cloud.certs)
        self.intro(self.cloud.client)
        self.intro(self.cloud.cloudpipe)
        self.intro(self.cloud.coverage)
        self.intro(self.cloud.dns_domains)
        self.intro(self.cloud.dns_entries)
        self.intro(self.cloud.fixed_ips)
        self.intro(self.cloud.flavor_access)
        self.intro(self.cloud.flavors)
        self.intro(self.cloud.floating_ip_pools)
        self.intro(self.cloud.floating_ips)
        self.intro(self.cloud.floating_ips_bulk)
        self.intro(self.cloud.fping)
        self.intro(self.cloud.hosts)
        self.intro(self.cloud.hypervisors)
        self.intro(self.cloud.images)
        self.intro(self.cloud.keypairs)
        self.intro(self.cloud.limits)
        self.intro(self.cloud.networks)
        self.intro(self.cloud.os_cache)
        self.intro(self.cloud.project_id)
        self.intro(self.cloud.quota_classes)
        self.intro(self.cloud.quotas)
        self.intro(self.cloud.security_group_rules)
        self.intro(self.cloud.security_groups)
        self.intro(self.cloud.servers)
        self.intro(self.cloud.services)
        self.intro(self.cloud.usage)
        self.intro(self.cloud.virtual_interfaces)
        self.intro(self.cloud.volume_snapshots)
        self.intro(self.cloud.volume_types)
        self.intro(self.cloud.volumes)

        now = datetime.now()

    def find_user_id(self):
        """
        this method returns the user id and stores it for later use.
        """
        # As i do not know how to do this properly, we just create a
        # VM and than get the userid from there

        self.cloud.ensure_service_catalog_present(self.cloud)
        catalog = self.cloud.client.service_catalog.catalog
        pp.pprint(catalog['access']['user'], "User Credentials")
        pp.pprint(catalog['access']['token'], "Token")

        print(result)

        sys.exit()
        if self.user_id is None:
            sample_flavor = self.cloud.flavors.find(name="m1.tiny")
            sample_image = self.cloud.images.find(
                id="6d2bca76-8fff-4d57-9f29-50378539b4fa")
            sample_vm = self.cloud.servers.create(
                "%s-id" % self.credential["OS_USERNAME"],
                flavor=sample_flavor,
                image=sample_image)
            self.user_id = sample_vm.user_id
            sample_vm.delete()
        return self.user_id

    #
    # print
    #

    def __str__(self):
        """
        print everything but the credentials that is known about this
        cloud in json format.
        """
        information = {
            'label': self.label,
            'flavors': self.flavors,
            'vms': self.servers,
            'images': self.images}
        return json.dumps(information, indent=4)

    #
    # get methods
    #

    def type():
        return self.type

    #
    # refresh
    #

    """
        def _get_image_dict():
                return _self.cloud.images.list(detailed=True)

        def _update_image_dict(image):
                del image.manager
                del image._info
                del image._loaded
                # del information.links
                return (image.id, image)

    """

    def refresh(self, type=None):

        time_stamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%SZ')
        selection = ""
        if type:
            selection = type.lower()[0]
            all = selection == 'a'
        else:
            all = True

        if selection == 'i' or all:
            # list = _get_image_dict()
            list = self.cloud.images.list(detailed=True)
            for information in list:
                # (id, image) = _update_image_dict(information)
                image = information.__dict__
                del image.manager
                del image._info
                del image._loaded
                # del information.links
                self.images[information.id] = image
                self.images[information.id]['cm_refresh'] = time_stamp

        if selection == 'f' or all:
            # list = _get_floavors_list()
            list = self.cloud.flavors.list()
            for information in list:
                # flavor = _update_flavors_dict(information)
                flavor = information.__dict__
                # clean not neaded info
                del flavor.manager
                del flavor._info
                del flavor._loaded
                # del information.links
                self.flavors[information.name] = flavor
                self.flavors[information.name]['cm_refresh'] = time_stamp

        if selection == 'v' or selection is None or all:
            # list = _get_servers_list()
            list = self.cloud.servers.list(detailed=True)

            for information in list:
                # vm = _update_servers_dict(information)
                vm = information.__dict__
                # pp.pprint(vm)
                delay = vm['id']
                del vm['manager']
                del vm['_info']
                del vm['_loaded']
                # del information.links

                self.servers[information.id] = vm
                self.servers[information.id]['cm_refresh'] = time_stamp

    #
    # create a vm
    #
    def vm_create(self, name, flavor_name, image_id):
        """
        create a vm
        """

        vm_flavor = self.cloud.flavors.find(name=flavor_name)
        vm_image = self.cloud.images.find(id=image_id)
        vm = self.cloud.servers.create(name,
                                       flavor=vm_flavor,
                                       image=vm_image
                                       )
        delay = vm.user_id  # trick to hopefully get all fields
        data = vm.__dict__
        del data['manager']
        # data['cm_name'] = name
        # data['cm_flavor'] = flavor_name
        # data['cm_image'] = image_id
        return {str(data['id']):  data}

    #
    # delete vm(s)
    #

    def vm_delete(self, id):
        """
        delete a single vm and returns the id
        """

        vm = self.cloud.servers.delete(id)
        # return just the id or None if its deleted
        return vm

    def vms_delete(self, ids):
        """
        delete many vms by id. ids is an array
        """
        for id in ids:
            print "Deleting %s" % self.servers[id]['name']
            vm = self.vm_delete(id)

        return ids

    #
    # list user images
    #

    def vms_user(self, refresh=False):
        """
        find my vms
        """
        user_id = self.find_user_id()

        time_stamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%SZ')
        if refresh:
            self.refresh("images")

        result = {}
        for (key, vm) in self.servers.items():
            if vm['user_id'] == self.user_id:
                result[key] = vm

        return result

    #
    # list project vms
    #

    def vms_project(self, refresh=False):
        """
        find my vms
        """
        user_id = self.find_user_id()

        time_stamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%SZ')
        if refresh:
            self.refresh("images")

        result = {}
        for (key, vm) in self.servers.items():
            result[key] = vm

        return result

    #
    # delete images from a user
    #

    def vms_delete_user(self):
        """
        find my vms and delete them
        """

        ids = cloud.find('user_id')
        cloud.vms_delete(ids)

        return

    #
    # find
    #

    def find(self, key, value=None):
        ids = []
        if key == 'user_id' and value is None:
            value = self.user_id
        for (id, vm) in self.servers.items():
            if vm[str(key)] == value:
                ids.append(str(vm['id']))

        return ids

    #
    # rename
    #

    def rename(self, old, new, id=None):
        all = self.find('name', old)
        print all
        if len(all) > 0:
            id = all[0]
            vm = self.cloud.servers.update(id, new)
        return

    def reindex(self, prefixold, prefix, index_format):
        all = self.find('user_id')
        counter = 1
        for id in all:
            old = self.servers[id]['name']
            new = prefix + index_format % counter
            print "Rename %s -> %s, %s" % (old, new, self.servers[id]['key_name'])
            if old != new:
                vm = self.cloud.servers.update(id, new)
            counter += 1

    def reindex(self, prefix, index_format):
        all = self.find('user_id')
        counter = 1
        for id in all:
            old = self.servers[id]['name']
            new = prefix + index_format % counter
            print "Rename %s -> %s, %s" % (old, new, self.servers[id]['key_name'])
            # if old != new:
            #    vm = self.cloud.servers.update(id, new)
            counter += 1

    #
    # TODO
    #
    """
    refresh just a specific VM
    delete all images that follow a regualr expression in name
    look into sort of images, flavors, vms
    """

    #
    # EXTRA
    #

    def table_col_to_dict(self, body):
        result = {}
        for element in body:
            key = element[0]
            value = element[1]
            result[key] = value
        return result

    def Table_matrix(self, text, format=None):
        lines = text.splitlines()
        headline = lines[0].split("|")
        headline = headline[1:-1]
        for i in range(0, len(headline)):
            headline[i] = str(headline[i]).strip()

        lines = lines[1:]

        body = []

        for l in lines:
            line = l.split("|")
            line = line[1:-1]
            entry = {}
            for i in range(0, len(line)):
                line[i] = str(line[i]).strip()
                if format == "dict":
                    key = headline[i]
                    entry[key] = line[i]
            if format == "dict":
                body.append(entry)
            else:
                body.append(line)
        if format == 'dict':
            return body
        else:
            return (headline, body)

    #
    # CLI call of ussage
    #
    def parse_isotime(self, timestr):
        """Parse time from ISO 8601 format"""
        try:
            return iso8601.parse_date(timestr)
        except iso8601.ParseError as e:
            raise ValueError(e.message)
        except TypeError as e:
            raise ValueError(e.message)

    def usage(self, start, end, format='dict'):
        """ returns the usage information of the tennant"""

        # print 70 * "-"
        # print self.cloud.certs.__dict__.get()
        # print 70 * "-"

        tenantid = "member"  # not sure how to get that
        iso_start = self.parse_isotime(start)
        iso_end = self.parse_isotime(end)
        print ">>>>>", iso_start, iso_end
        info = self.cloud.usage.get(tenantid, iso_start, iso_end)

        # print info.__dict__
        sys.exit()

        result = fgrep(nova("usage", "--start", start, "--end", end), "|")
        (headline, matrix) = self.table_matrix(result)
        headline.append("Start")
        headline.append("End")
        matrix[0].append(start)
        matrix[0].append(end)

        if format == 'dict':
            result = {}
            for i in range(0, len(headline)):
                result[headline[i]] = matrix[0][i]
            return result
        else:
            return (headline, matrix[0])

    #
    # CLI call of absolute-limits
    #
    def limits(self):
        """ returns the usage information of the tennant"""

        list = []

        info = self.cloud.limits.get()
        del info.manager
        rates = info.__dict__['_info']['rate']

        for rate in rates:
            limit_set = rate['limit']
            print limit_set
            for limit in limit_set:
                list.append(limit)

        return list


#
# MAIN FOR TESTING
#

if __name__ == "__main__":

    credential_test = False
    flavor_test = False
    table_test = False
    image_test = False
    vm_test = True
    cloud_test = False
    usage_test = False

    if credential_test:
        credential = cm_config('india-openstack')
        # print credential

    cloud = openstack("india-openstack")

    cloud.novaclient_dump()

    if usage_test:
        # print json.dumps(cloud.usage("2000-01-01T00:00:00",
        # "2013-12-31T00:00:00"), indent=4)

        print json.dumps(cloud.limits(), indent=4)

        # print json.dumps(cloud.usage("2000-01-01", "2013-12-31"), indent=4)
        # print json.dumps(cloud.usage("2000-01-01", "2013-12-31",format=None),
        # indent=4)
        # print json.dumps(cloud.limits(format='dict'), indent=4)
        # print json.dumps(cloud.limits(format='array'), indent=4)
    if flavor_test or table_test:
        cloud.refresh('flavors')
        print json.dumps(cloud.flavors, indent=4)

    if table_test:
        table = cm_table()
        columns = ["id", "name", "ram", "vcpus"]

        table.create(cloud.flavors, columns, header=True)
        print table

        table.create(cloud.flavors, columns, format='HTML', header=True)
        print table

        table.create(cloud.flavors, columns, format='%12s', header=True)
        print table

    if image_test:
        cloud.refresh('images')
        print json.dumps(cloud.images, indent=4)

    if vm_test:
        cloud.refresh('vms')
        print json.dumps(cloud.images, indent=4)

    if cloud_test:
        cloud.refresh()
        print cloud

        # print cloud.find_user_id()

    name = "%s-%04d" % (cloud.credential["OS_USERNAME"], 1)

    out = cloud.vm_create(
        name, "m1.tiny", "6d2bca76-8fff-4d57-9f29-50378539b4fa")
    pp.pprint(out)
    print json.dumps(out, indent=4)

    """
    key = out.keys()[0]
    id = out[key]["id"]

    print ">>>", id

    vm = cloud.vm_delete(id)
    print vm


    list = cloud.vms_user()
    print json.dumps(list, indent=4)

    print cloud.find_user_id()

    list = cloud.vms_delete_user()
    print list
    """
    """
    for i in range (1,3):
        name ="%s-%04d" % (cloud.credential["OS_USERNAME"], i)
        out = cloud.vm_create(name, "m1.tiny", "6d2bca76-8fff-4d57-9f29-50378539b4fa")
        pp.pprint(out)
    """

    """
    print cloud.find('name', name)
    """

    # ids = cloud.find('user_id')

    # print ids

    # cloud.vms_delete(ids)

    # print cloud.vms_delete_user()

    # cloud.rename("gvonlasz-0001","gregor")

    # cloud.reindex("deleteme-", "%03d")
