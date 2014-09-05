import json
from cloudmesh_common.util import HEADING
from cloudmesh_common.logger import LOGGER

# ----------------------------------------------------------------------
# SETTING UP A LOGGER
# ----------------------------------------------------------------------

log = LOGGER(__file__)


# import shelve
from cloudmesh.config.cm_config import cm_config
# from openstack.cm_compute import openstack as os_client

# Error Cannot Import Openstack
from cloudmesh.iaas.openstack.cm_compute import openstack

from cloudmesh.iaas.eucalyptus.eucalyptus import eucalyptus
from cloudmesh.iaas.ec2.cm_compute import ec2
from cloudmesh.iaas.aws.cm_compute import aws
try:
    from cloudmesh.iaas.azure.cm_compute import azure
except:
    log.warning("AZURE NOT ENABLED")


class cm_mesh:

    # ----------------------------------------------------------------------
    # global variables that define the information managed by this class
    # ----------------------------------------------------------------------

    # dict that holds vms, flavors, images for al iaas
    clouds = {}

    # array with keys from the user
    keys = []

    configuration = {}

    # ----------------------------------------------------------------------
    # initialization methods
    # ----------------------------------------------------------------------

    def __init__(self):
        self.clear()
        # Read Yaml File to find all the cloud configurations present
        self.config()

    def clear(self):
        self.clouds = {}
        self.keys = []

    # ----------------------------------------------------------------------
    # the configuration method that must be called to get the cloud info
    # ----------------------------------------------------------------------

    def config(self):
        """
        reads the cloudmesh yaml file that defines which clouds build
        the cloudmesh
        """
        # print "CONFIG"

        self.configuration = cm_config()

        # pprint (configuration)

        active_clouds = self.configuration.active()
        # print active_clouds

        for cloud_name in active_clouds:
            try:
                credential = self.configuration.credential(cloud_name)
                cloud_type = self.configuration.cloud(cloud_name)['cm_type']

                if cloud_type in ['openstack', 'eucalyptus', 'azure', 'aws', 'ec2']:
                    self.clouds[cloud_name] = {'name': cloud_name,
                                               'cm_type': cloud_type,
                                               'credential': credential}
                # if cloud_type in ['openstack']:
                #    self.clouds[cloud_name] = {'states': "HALLO"}

            except:  # ignore
                pass
                # print "ERROR: could not initialize cloud %s" % cloud_name
                # sys.exit(1)

        return

    # ----------------------------------------------------------------------
    # importnat get methods
    # ----------------------------------------------------------------------

    def get(self):
        """returns the dict that contains all the information"""
        return self.clouds

    def active(self):
        active_clouds = self.configuration.active()
        return active_clouds

    def prefix(self):
        return self.configuration.prefix

    def index(self):
        return self.configuration.index

    def profile(self):
        return self.configuration.profile()

    def default(self, cloudname):
        return self.configuration.default(cloudname)

    def states(self, cloudname):
        cloud_type = self.clouds[cloudname]['cm_type']
        if cloud_type in ['openstack']:
            provider = self.cloud_provider(cloud_type)
            cloud = provider(cloudname)
            return cloud.states

    def state_filter(self, cloudname, states):
        cloud_type = self.clouds[cloudname]['cm_type']
        if cloud_type in ['openstack']:
            provider = self.cloud_provider(cloud_type)
            cloud = provider(cloudname)
            cloud.refresh()
            cloud.display(states, None)
            self.clouds[cloudname]['servers'] = cloud.servers

    def all_filter(self):
        for cloudname in self.active():
            self.state_filter(cloudname, self.states(cloudname))

    # ----------------------------------------------------------------------
    # important print methods
    # ----------------------------------------------------------------------

    def __str__(self):
        return str(self.clouds)

    def dump(self):
        print json.dumps(self.clouds, indent=4)

    # ----------------------------------------------------------------------
    # find
    # ----------------------------------------------------------------------
    #
    # returns dicts of a particular type
    #
    # ----------------------------------------------------------------------
    def find(self, cloud=["all"], type="servers", project=["all"]):
        """
        Returns a dict with matching elements

        cloud = specifies an array of cloud names that are defined in
        our configuration and returns matching elements in a dict. The
        first level in the dict is the cloud, the second level are the
        elements. If all is specified we serach in all clouds

        type = "servers", "images", "flavors"

        The type specifies the kind of element that we look for
        (we only look for the first character e.g. s, i, f)

        project = an array of projects we search for. This only
        applies for servers for now. Till we have introduced the
        profile that restricts available images and flavors for a
        project.

        In all cases None can be used as an alternative to ["all"]

        """
        result = {}
        return result

    # ----------------------------------------------------------------------
    # the refresh method that gets upto date information for cloudmesh
    # If cloudname is provided only that cloud will be refreshed
    # else all the clouds will be refreshed
    # ----------------------------------------------------------------------

    def cloud_provider(self, type):
        provider = None
        if type == 'openstack':
            provider = openstack
        elif type == 'eucalyptus':
            provider = eucalyptus
        elif type == 'aws':
            provider = aws
        elif type == 'azure':
            provider = azure
        elif type == 'ec2':
            provider = ec2
        return provider

    def info(self):
        HEADING("CLOUD MESH INFO")
        try:
            for name in self.clouds.keys():
                cloud_type = self.clouds[name]['cm_type']
                provider = self.cloud_provider(cloud_type)
                cloud = provider(name)
                HEADING("Info " + name)
                cloud.refresh("all")
                cloud.info()

        except Exception, e:
            log.error(str(e))

    def refresh(self, names=["all"], types=["all"]):
        """
        This method obtians information about servers, images, and
        flavours that build the cloudmesh. The information is held
        internally after a refresh. Than the find method can be used
        to query form this information. To pull new information into
        this data structure a new refresh needs to be called.

        Usage is defined through arrays that are passed along.

        type = "servers", "images", "flavors"

        The type specifies the kind of element that we look for
        (we only look for the first character e.g. s, i, f)

        In all cases None can be used as an alternative to ["all"]

        if cloud name  is None and type = none update everything

        if cloud name !=None and type = none update everything in the
        specified clouds

        if cloud name != None and type != none
           refresh the given types for the given clouds

        """
        if types == ['all'] or types is None:
            types = ['servers', 'flavors', 'images']

        if names == ['all'] or names is None:
            names = self.clouds.keys()

        # at one point use a threadpool.
        try:
            for name in names:
                try:
                    cloud_display = self.clouds[name]['cm_display']
                except:
                    cloud_display = False
                cloud_type = self.clouds[name]['cm_type']
                provider = self.cloud_provider(cloud_type)
                cloud = provider(name)
                log.info("Refresh cloud {0}".format(name))
                for type in types:
                    log.info("    Refresh {0}".format(type))
                    cloud.refresh(type=type)
                    result = cloud.get(type)
                    self.clouds[name][type] = cloud.get(type)
                    # maye be need to use dict update ...
                    self.clouds[name].update(
                        {'name': name, 'cm_type': cloud_type, 'cm_display': cloud_display})

        except Exception, e:
            log.error(str(e))

    def refresh_user_id(self, names=["all"]):
        if names == ['all'] or names is None:
            names = self.clouds.keys()
        try:
            for name in names:
                cloud_type = self.clouds[name]['cm_type']
                provider = self.cloud_provider(cloud_type)
                cloud = provider(name)
                if 'user_id' not in self.clouds[name]:
                    self.clouds[name]['user_id'] = cloud.find_user_id()
        except Exception, e:
            log.error(str(e))

    def add(self, name, type):
        try:
            self.clouds[name]
            log.error("Cloud {0} already exists".format(name))
        except:
            self.refresh(name, type)

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

    # ----------------------------------------------------------------------
    # saves and reads the dict to and from a file
    # ----------------------------------------------------------------------
    def save(self):
        log.error("save() not implemented")

    def load(self):
        log.error("load() not implemented")

    # ----------------------------------------------------------------------
    # TODO: convenient +, += functions to add dicts with cm_type
    # ----------------------------------------------------------------------

    def delete(self, cloud_name, server_id):
        try:
            cloud_type = self.clouds[cloud_name]['cm_type']
            provider = self.cloud_provider(cloud_type)
            cloud = provider(cloud_name)
            cloud.vm_delete(server_id)
        except:
            log.error("could not delete {0} {1}".format(cloud_name, server_id))

    def add_key_pairs(self, cloud_names=None):
        print "not implemented"

        '''
        activates a specific host by name. to be queried

        :param names: the array with the names of the clouds in the
                      yaml file to be activated.
        '''
        if cloud_names is None:
            names = self.config.active()
        else:
            names = cloud_names

        for cloud_name in names:
            print "Uploading keys to ->", cloud_name

            try:
                credential = self.config.cloud(cloud_name)
                cm_type = credential['cm_type']
                cm_type_version = credential['cm_type_version']
                if cm_type in ['openstack',
                               'eucalyptus',
                               'azure',
                               'aws',
                               'ec2']:
                    self.clouds[cloud_name] = {
                        'name': cloud_name,
                        'cm_type': cm_type,
                        'cm_type_version': cm_type_version}
    #                   'credential': credential}
                    provider = self.cloud_provider(cm_type)
                    cloud = provider(cloud_name)
                    # try to see if the credential works if so, update
                    # the 'manager' so the cloud is successfully
                    # activated otherwise log error message and skip
                    # this cloud
                    if not force_auth_verify:
                        self.clouds[cloud_name].update({'manager': cloud})
                    else:
                        tryauth = cloud.get_token()
                        if 'access' in tryauth:
                            self.clouds[cloud_name].update({'manager': cloud})
                        else:
                            log.error("Credential not working, "
                                      "cloud is not activated")

                    if cm_type == 'openstack':
                        keys = self.config.userkeys()['keylist']
                        username = self.config.username()
                        for keyname, keycontent in keys.iteritems():
                            keynamenew = "{0}_{1}".format(username,
                                                          keyname.replace('.', '_').replace('@', '_'))
                            # print "Transformed key name: %s" % keynamenew
                            log.info("Adding a key for user <%s> in cloud <%s>"
                                     % (username, cloud_name))
                            keypart = keycontent.split(" ")
                            keycontent = "%s %s" % (keypart[0], keypart[1])
                            cloud.keypair_add(keynamenew, keycontent)
                        # pprint(keys)
            except Exception, e:
                print "ERROR: can not activate cloud", cloud_name
                print e
                # print traceback.format_exc()
                # sys.exit()

    def del_key_pairs(self, cloud_names=None):
        print "not implemented"

    def add_key_pair(self, cloud_name, key, name):
        try:
            cloud_type = self.clouds[cloud_name]['cm_type']
            provider = self.cloud_provider(cloud_type)
            cloud = provider(cloud_name)
            return cloud.upload_key_pair(key, name)
        except:
            log.error("could not update keypair {0}".format(cloud_name))

    def del_key_pair(self, cloud_name, name):
        try:
            cloud_type = self.clouds[cloud_name]['cm_type']
            provider = self.cloud_provider(cloud_type)
            cloud = provider(cloud_name)
            return cloud.delete_key(name)
        except:
            log.error("could not delete keypair {0}".format(cloud_name))

    def assign_public_ip(self, cloud_name, vm_id):
        cloud_type = self.clouds[cloud_name]['cm_type']
        # for now its only for openstack
        if cloud_type in "openstack":
            provider = self.cloud_provider(cloud_type)
            cloud = provider(cloud_name)
            cloud.assign_public_ip(vm_id, cloud.get_public_ip().ip)
        # code review: GVL
        # else:
        # print "BUG: assigning ip addresses from other clouds such as azure,
        # and eucalyptus not implemented yet."

    def vm_set_meta(self, cloud_name, serverid, meta):

        cloud_type = self.clouds[cloud_name]['cm_type']
        provider = self.cloud_provider(cloud_type)

        cloud = provider(cloud_name)

        cloud.wait(serverid, 'ACTIVE')
        cloud.set_meta(serverid, meta)

    def create(self, cloud_name, prefix, index,
               image_id,
               flavor_name,
               key=None,
               security_group=None):

        # print ">>>>>>",  cloud_name, prefix, index, image_id, flavor_name,
        # key

        security_groups = []
        name = prefix + "-" + "%s" % str(index).zfill(4)

        cloud_type = self.clouds[cloud_name]['cm_type']
        log.info(cloud_type)
        provider = self.cloud_provider(cloud_type)

        cloud = provider(cloud_name)

        if security_group is None:
            security_group = cloud.checkSecurityGroups()

        #
        # TODO: else
        #
        if security_group is not None:
            security_groups.append(security_group)
        else:
            #
            # TODO: this can never be reached
            #
            security_groups = None
        return cloud.vm_create(name,
                               flavor_name,
                               image_id,
                               security_groups,
                               key)

        """
        keyname = ''
        try:
            cloud_type = self.clouds[cloud_name]['cm_type']

            if cloud_type in "openstack":
                config = cm_config()
                yamlFile= config.get()
                if yamlFile[cloud_name]['cm_type'] in 'openstack':
                    if yamlFile[cloud_name].has_key('keypair') :
                        keyname = yamlFile[cloud_name]['keypair']['keyname']

            provider = self.cloud_provider(cloud_type)
            cloud = provider(cloud_name)
            if cloud_name == "india-openstack":
                flavor_name = "m1.tiny"
                # this is a dummy and must be retrieved from flask
                image_id = "6d2bca76-8fff-4d57-9f29-50378539b4fa"
                name = prefix + "-" + index
                if (len(keyname) > 0) :
                    cloud.vm_create(name, flavor_name, image_id,keyname )
                else :
                    cloud.vm_create(name, flavor_name, image_id)
                # this is a dummy and must be retrieved from flask
        except Exception , e:
            log.error("could not create {0} {1} {2} {3} {4}".format(cloud_name,
                       prefix, index, image_id, e}
        """

    # ----------------------------------------------------------------------
    # TODO: convenient +, += functions to add dicts with cm_type
    # ----------------------------------------------------------------------

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
            log.error("TODO: not implemented yet")
            return
        elif other.cm_type == "vm":
            log.error("TODO: not implemented yet")
            return
        elif other.cm_type == "flavor":
            log.error("TODO: not implemented yet")
            return
        elif other.cm_type == "cloudmesh":
            log.error("TODO: not implemented yet")
            return
        else:
            log.error("{0} type does not exist".format(other.cm_type))
            log.error("Error: Ignoring add")
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
            log.error("TODO: not implemented yet")
            return
        elif other.cm_type == "vm":
            log.error("TODO: not implemented yet")
            return
        elif other.cm_type == "flavor":
            log.error("TODO: not implemented yet")
            return
        elif other.cm_type == "cloudmesh":
            log.error("TODO: not implemented yet")
            return
        else:
            log.error("%s type does not exist".format(other.cm_type))
            log.error("Error: Ignoring add")
            return

    def address_string(self, content, labels=False):
        """content is a dict of the form {u'private': [{u'version':
        4,u'addr': u'10.35.23.30',u'OS-EXT-IPS:type':u'fixed'},
        {u'version': 4, u'addr': u'198.202.120.194',
        u'OS-EXT-IPS:type': u'floating'}]}

        it will return

           "fixed: 10.35.23.30, floating: 198.202.120.194'
        """
        try:
            result = ""
            for address in content['private']:
                if labels:
                    result = result + address['OS-EXT-IPS:type'] + "="
                result = result + address['addr']
                result = result + ", "
            result = result[:-2]
        except:
            # THIS SEEMS WRONG
            {u'vlan102': [{u'version': 4, u'addr': u'10.1.2.104'}, {
                u'version': 4, u'addr': u'149.165.158.34'}]}
            try:
                position = 0
                for address in content['vlan102']:
                    if position == 0:
                        type = "fixed"
                    else:
                        type = "floating"
                    if labels:
                        result = result + type
                    result = result + address['addr']
                    result = result + ", "
                    position = position + 1
                result = result[:-2]
            except:
                result = content
        return result

    def status_color(self, status):
        if status == 'ACTIVE':
            return "green"
        if status == 'BUILDING':
            return "blue"
        if status in ['ERROR']:
            return "red"
        return "black"


# ----------------------------------------------------------------------
# MAIN METHOD FOR TESTING
# ----------------------------------------------------------------------

if __name__ == "__main__":

    c = cm_mesh()
    print c.clouds
    """
    c.config()

    c.dump()


    c = cloud_mesh()

    c.refresh()
    c.add('india', 'openstack')
    c.add('sierra', 'openstack')
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


    (attribute, passwd) = fgrep("OS_PASSWORD",
                                config_file("openstack/novarc"))
                                .replace("\n","").split("=")

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

    """
        content = {u'private': [
        {u'version': 4,
         u'addr': u'10.35.23.30',
         u'OS-EXT-IPS:type':
         u'fixed'},
        {u'version': 4,
         u'addr': u'198.202.120.194',
         u'OS-EXT-IPS:type':
         u'floating'}]}

    print content
    print address_string(content)
    """
