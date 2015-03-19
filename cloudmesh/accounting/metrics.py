import pickle
from sh import fgrep
from sh import nova
from sh import tail
from datetime import datetime
import json
import sys
import os
import pprint
pp = pprint.PrettyPrinter(indent=4)

# import shelve
from cloudmesh.config.cm_config import cm_config
# from openstack.cm_compute import openstack as os_client

# Error Cannot Import Openstack
from cloudmesh.iaas.openstack.cm_compute import openstack

from cloudmesh.iaas.eucalyptus.eucalyptus_new import eucalyptus
from cloudmesh.iaas.azure.cm_azure import cm_azure as azure

from cloudmesh_base.locations import config_file

try:
    # from sh import fgmetric
    from fgmetric.FGMetricsAPI import FGMetricsAPI
    # OR
    # from sh import fgmetric
except:
    # TODO THIS IS NOT HOW WE DO IT, SETUP CONTAINS ALL REQUEMENTS
    # FIX SETUP
    print "---------------------"
    print "fgmetric not imported"
    print "---------------------"
    pass
try:
    from bson import json_util
except:
    # TODO THIS IS NOT HOW WE DO IT, SETUP CONTAINS ALL REQUEMENTS
    # FIX SETUP
    print "--------------------------------"
    print "Please run 'pip install pymongo'"
    print "--------------------------------"

    #

# WHY ARE WE NOT MORE CLEANLY SEPARATING METRIC FROM THIS?


class metrics:

    #
    # global variables that define the information managed by this class
    #

    # dict that holds vms, flavors, images for al iaas
    clouds = {}

    # array with keys from the user
    keys = []

    #
    # variables that we can most likely eliminate
    #

    # user needs to come from credential ...
    user = "gvonlasz"

    #
    # initialization methods
    #

    def __init__(self):
        self.clear()
        # Read Yaml File to find all the cloud configurations present
        self.config()
        try:
            self.metric_api = FGMetricsAPI()
        except:
            pass

    def clear(self):
        self.clouds = {}
        self.keys = []
        self.user = "gvonlasz"

    #
    # some metric methods
    #

    def get_metrics_cli(self, args):
        """ Get usage data from FG Metric CLI"""
        """ This is replica with get_metrics but using CLI instead of API """
        """
            Args:
                args (dict): parameters for CLI with option
            Return:
                (dict): output of fgmetric in a dict type
            Raise:
                n/a
        """
        try:
            res = fgmetric(
                args)  # args should be list-lized before send it out as a parameter
            return json.loads(res, object_hook=json_util.object_hook)
        except:
            pass

    def get_metrics(self, args):
        """Get usage data from FG Metrics"""

        if not self.metric_api:
            return

        try:
            args["user"] = args["user"] or self.user
            self._set_metric_api_vars(args)
            # print args
            stats = self.metric_api._set_dict_vars()
            metrics = self.metric_api.get_stats()
            stats["stats"] = metrics
            self.metrics = stats
            # print self.metrics
        except:
            print sys.exc_info()
            pass
        return self.metrics

    def get_realtime_metrics(self, args):
        """ get real-time usage data from FG Metrics"""

        # IN DEVELOPMENT
        if not self.metric_api:
            return

        try:
            print 1
        except:
            pass

    def _set_metric_api_vars(self, args):
        self.metric_api.set_date(args["s_date"], args["e_date"])
        self.metric_api.set_metric(
            "count runtime cores mem disks")  # args["metric"])
        self.metric_api.set_user(args["user"])
        self.metric_api.set_cloud(args["cloud"])
        self.metric_api.set_hostname(args["host"])
        self.metric_api.set_period(args["period"])

    #
    # the configuration method that must be called to get the cloud info
    #

    def config(self):
        """
        reads the cloudmesh yaml file that defines which clouds build
        the cloudmesh
        """

        configuration = cm_config()
        pp.pprint(configuration)

        for cloud_name in configuration.keys():
            print "--------------------"

            try:
                credential = configuration.get(key=cloud_name)
                cloud_type = credential['cm_type']

                print credential

                print ">>>>>>>", cloud_name, cloud_type

                if cloud_type in ['openstack', 'eucalyptus']:
                    print "AAAAA"
                    self.clouds[cloud_name] = {
                        'cm_type': cloud_type, 'credential': credential}
                    print "BBBB"
                    try:
                        self.update(cloud_name, cloud_type)
                        self.clouds[cloud_name] = {
                            'cm_type': cloud_type, 'credential': credential}
                    except:
                        print "ERROR: can not connect to", cloud_name
                    print "CCCC"

            except Exception, e:
                print "ERROR: Not a cloud:", cloud_name, e
        return

    #
    # importnat get methods
    #

    def get(self):
        """returns the dict that contains all the information"""
        return self.clouds

    #
    # important print methods
    #
    # includes sanitizing to remove the credentials
    #

    def __str__(self):
        tmp = self._sanitize()
        print tmp

    def _sanitize(self):
        # copy the self.cloud
        # delete the attributes called credential for all clouds

        all_keys = self.clouds.keys()
        for cloud in all_keys:
            self.clouds[cloud]['credential'] = {}

        return self.clouds

    def dump(self):
        tmp = self._sanitize()
        print json.dumps(tmp, indent=4)

    #
    # the refresh method that gets upto date information for cloudmesh
    # If cloudname is provided only that cloud will be refreshed
    # else all the clouds will be refreshed
    #

    def refresh(self, cloud_name=None):
        print "Refershing cloud %s" % cloud_name
        servers = {}
        cloud = None

        if(cloud_name is None):
            all_clouds = self.clouds.keys()
            for cloud_name in all_clouds:
                try:
                    type = self.clouds[cloud_name]['cm_type']

                    if type == 'openstack':
                        cloud = openstack(cloud_name)

                    elif type == 'eucalyptus':
                        # Where do i find the project name ? Is there a defaul
                        # one ?
                        cloud = eucalyptus(cloud_name, 'fg-82')

                    elif type == 'azure':
                        cloud = azure.cm_azure()

                    cloud.refresh()
                    self.clouds[cloud_name]['flavors'] = cloud.flavors
                    self.clouds[cloud_name]['images'] = cloud.images
                    self.clouds[cloud_name]['servers'] = cloud.servers

                except Exception, e:
                    print e
        else:
            try:
                type = self.clouds[cloud_name]['cm_type']

                if type == 'openstack':
                    cloud = openstack(cloud_name)

                elif type == 'eucalyptus':
                    # Where do i find the project name ? Is there a defaul one ?
                    # this is obvious;ly wrong as the tennent comes from profile
                    # TODO EUCALYPTUS DOES NOT YET WORK

                    cloud = eucalyptus(cloud_name, 'fg-82')

                elif type == 'azure':
                    cloud = azure.cm_azure()

                cloud.refresh()
                self.clouds[cloud_name]['flavors'] = cloud.flavors
                self.clouds[cloud_name]['images'] = cloud.images
                self.clouds[cloud_name]['servers'] = cloud.servers

            except Exception, e:
                print e
        return cloud

    def update(self, name, type):
        servers = self.refresh(name)
        self.clouds[name].update({'name': name,
                                  'cm_type': type,
                                  "servers": servers})
        return

    def add(self, name, type):
        try:
            self.clouds[name]
            print "Error: Cloud %s already exists" % name
        except:
            self.update(name, type)

    """
    def get_keys(self):
        return self.keys

    def refresh_keys(self):
        self.keys = []
        result = fgrep(tail(nova("keypair-list"), "-n", "+4"),"-v","+")
        for line in result:
            (front, name, signature, back) = line.split("|")
            self.keys.append(name.strip())
        return self.keys


    def refresh(self):
        keys = self.refresh_keys()
        for cloud in keys:
            self.refresh(cloud)

        # p = Pool(4)
        # update = self.refresh
        # output = p.map(update, keys)

    """

    #
    # saves and reads the dict to and from a file
    #

    def save(self):
        log.error("not implemented")
        """
        tmp = self._sanitize()
        file = open(self.datastore, 'wb')
        # pickle.dump(self.keys, file)
        pickle.dump(tmp, file)
        file.close()
        """

    def load(self):
        log.error("not implemented")
        """
        file = open(self.datastore, 'rb')
        # self.keys = pickle.load(file)
        self.clouds = pickle.load(file)
        ''' above returns:
        [u'gvonlasz']
         So, call pickle again to get more:
            {'india': {'name': 'india',
            'servers': {u'2731c421-d985-44ce-91bf-2a89ce4ba033': {'cloud': 'india',
            'id': u'2731c421-d985-44ce-91bf-2a89ce4ba033',
            'ip': u'vlan102=10.1.2.85, 149.165.158.7',
            'name': u'gvonlasz-001',
            'refresh': '2013-02-11 20:30:04.472583',
            'status': u'ACTIVE'},
            ...
        '''
        self.clouds = pickle.load(file)
        file.close()
        """
    #
    # TODO: convenient +, += functions to add dicts with cm_type
    #

    def __add__(self, other):
        """
        type based add function c = cloudmesh(...); b = c + other
        other can be a dict that contains information about the object
        and it will be nicely inserted into the overall cloudmesh dict
        the type will be identified via a cm_type attribute in the
        dict Nn attribute cm_cloud identifies in which cloud the
        element is stored.
        """
        if other.cm_type == "image":
            print "TODO: not implemented yet"
            return
        elif other.cm_type == "vm":
            print "TODO: not implemented yet"
            return
        elif other.cm_type == "flavor":
            print "TODO: not implemented yet"
            return
        elif other.cm_type == "cloudmesh":
            print "TODO: not implemented yet"
            return
        else:
            print "Error: %s type does not exist", cm_type
            print "Error: Ignoring add"
            return

    def __iadd__(self, other):
        """
        type based add function c = cloudmesh(...); c += other other
        can be a dict that contains information about the object and
        it will be nicely inserted into the overall cloudmesh dict the
        type will be identified via a cm_type attribute in the dict.
        Nn attribute cm_cloud identifies in which cloud the element is
        stored.
        """
        if other.cm_type == "image":
            print "TODO: not implemented yet"
            return
        elif other.cm_type == "vm":
            print "TODO: not implemented yet"
            return
        elif other.cm_type == "flavor":
            print "TODO: not implemented yet"
            return
        elif other.cm_type == "cloudmesh":
            print "TODO: not implemented yet"
            return
        else:
            print "Error: %s type does not exist", cm_type
            print "Error: Ignoring add"
            return

#
# MAIN METHOD FOR TESTING
#

if __name__ == "__main__":

    c = cloudmesh()
    print c.clouds
    """
    c.config()

    c.dump()


    c = cloud_mesh()

    c.refresh()
    c.add('india', 'openstack')
    c.refresh_keys()
    c.dump()
    c.save()
    print 70 * "-"
    c.clear()
    c.dump()
    print 70 * "-"
    c.load()
    c.dump()
    print 70 * "-"
    """

    """
    india_os = {
        "OS_TENANT_NAME" : '',
        "OS_USERNAME" : '',
        "OS_PASSWORD" : '',
        "OS_AUTH_URL" : '',
        }


    (attribute, passwd) = fgrep("OS_PASSWORD",config_file("openstack/novarc")).replace("\n","").split("=")

    india_os['OS_PASSWORD'] = passwd



    username = india_os['OS_USERNAME']
    password = india_os['OS_PASSWORD']
    authurl = india_os['OS_AUTH_URL']
    tenant = india_os['OS_TENANT_NAME']

    print password
    '''
    username = os.environ['OS_USERNAME']
    password = os.environ['OS_PASSWORD']
    authurl = os.environ['OS_AUTH_URL']
    '''
    india = cloud_openstack("india", authurl, tenant, username, password)

    india._vm_show("gvonlasz-001")
    india.dump()
    india._vm_show("gvonlasz-001")
    india.dump()
    """
