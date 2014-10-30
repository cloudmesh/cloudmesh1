from __future__ import print_function
from datetime import datetime
import time
import json


def donotchange(fn):
    return fn


class ComputeBaseType:

    # users = {}
    # tenants = {}

    # : the dict for the flavors
    flavors = {}

    # : the dict for the images
    images = {}

    # : the dict for the servers
    servers = {}

    # : the dict for the security_groups
    security_groups = {}

    # : the dict for the stacks
    stacks = {}

    # : the dict for usage data
    usage = {}

    # : the dict for the set_credentials
    credential = None

    # : the unique string identifying this cloud
    label = None

    def __init__(self, label, cred=None):
        self.credential = cred
        self.label = label

    def _clear(self):
        # self.users = {}
        # self.tenants = {}
        self.flavors = {}  # global var
        self.images = {}  # global var
        self.servers = {}  # global var
        self.security_groups = {}  # global var
        self.stacks = {}
        self.usage = {}
        self.credential = None  # global var
        self.label = None  # global var
        self.type = None
        self.user_id = None
        self.auth_token = None

    def info(self):
        """obtain some basic information about the cloud"""
        print("Label:", self.label)
        print("Type:", self.type)
        print("Flavors:", len(self.flavors))
        print("Servers:", len(self.servers))
        print("Images:", len(self.images))
        print("Security Groups:", len(self.security_groups))
        print("Stacks:", len(self.stacks))
        print("Usage:", self.usage)
        # print "Users:", len(self.users)
        # print "Tenants:", len(self.tenants)

    def connect(self):
        """connect to the cloud"""
        raise NotImplementedError()

    def config(self, dict):
        """uses the dict to conduct some configuration with the parameters passed"""
        raise NotImplementedError()

    def find_user_id(self, force=False):
        """finds the user id of a user and caches it. If a chaced
        value is ther it will use that. If you specify force, it will
        regenerate it"""
        self.user_id = "unkown"
        raise NotImplementedError()

    def dump(self, type="server", with_manager=False):
        """returns a string that contains information about the cloud. One can ste the type to 'images','flavors','servers'"""
        selection = type.lower()[0]
        if selection == 'i':
            d = self.images.copy()
        elif selection == 'f':
            d = self.flavors.copy()
        elif selection == 's':
            d = self.servers.copy()
        elif selection == 'e':
            d = self.security_groups.copy()
        elif selection == 't':
            d = self.stacks.copy()
        elif selection == 'u':
            d = self.usage.copy()
        elif type is not None:
            print("refresh type not supported")
            assert False
        else:
            d = {}
            with_manager = True
        if not with_manager:
            for element in d.keys():
                try:
                    del d[element]['manager']
                except:
                    pass
        return d

    def get(self, type="server"):
        """returns information in a dict for 'servers','flavours','images'"""
        selection = type.lower()[0]
        d = {}
        if selection == 'i':
            d = self.images
        elif selection == 'f':
            d = self.flavors
        elif selection == 's':
            d = self.servers
        elif selection == 'e':
            d = self.security_groups
        elif selection == 't':
            d = self.stacks
        elif selection == 'u':
            d = self.usage
        # elif selection == 'u':
        #    d = self.users
        # elif selection == 't':
        #    d = self.tenants
        elif type is not None:
            print("refresh type not supported")
            assert False
        return d

    # identity management moved to its dedicated class
    """
    def _get_users_dict(self):
        raise NotImplementedError()

    def _get_tenants_dict(self):
        raise NotImplementedError()
    """

    def _get_images_dict(self):
        raise NotImplementedError()

    def _get_flavors_dict(self):
        raise NotImplementedError()

    def _get_servers_dict(self):
        raise NotImplementedError()

    def _get_security_groups_dict(self):
        raise NotImplementedError()

    def vm_create(self, name=None,
                  flavor_name=None,
                  image_id=None,
                  security_groups=None,
                  key_name=None,
                  meta=None):
        """create a virtual machine with the given parameters"""
        raise NotImplementedError()

    def vm_delete(self, id):
        """delete the virtual machine with the id"""
        raise NotImplementedError()

    def vms_project(self, refresh=False):
        raise NotImplementedError()

    def rename(self, old, new, id=None):
        """rename the firtual machine with the name old to the name new"""
        raise NotImplementedError()

    def usage(self, start, end, format='dict'):
        """returns the usage data between start and end date"""
        raise NotImplementedError()

    def limits(self):
        """returns a dict of limits that the cloud will maintain for a user and/or the project"""
        raise NotImplementedError()

    def wait(self, vm_id, vm_status, seconds=2):
        """waits a number of seconds and than refreshes information form the cloud"""
        print('refersh', vm_id)
        self.refresh()

        new_status = self.status(vm_id)
        print(new_status)
        while str(new_status) != str(vm_status):
            time.sleep(seconds)
            self.refresh()
            new_status = self.status(vm_id)

    #
    # print
    #

    def __str__(self):
        """
        print everything but the set_credentials that is known about this
        cloud in json format.
        """
        information = {
            'label': self.label,
            'flavors': self.flavors,
            'servers': self.servers,
            'images': self.images,
            'security groups': self.security_groups,
            'stacks': self.stacks,
            'usage': self.usage,
            # 'users': self.users,
            # 'users': len(self.users),
            # 'tenants': self.tenants,
        }
        return json.dumps(information, indent=4)

    #
    # get methods
    #
    # TODO BUG REMOVE THIS METHOD and replace with .type
    # def type():
    #    return self.type

    def vms(self):
        """returns the dict of the servers. deprecated."""
        return self.servers

    def status(self, vm_id):
        """returns that status of a given virtual machine"""
        return self.servers[vm_id]['status']

    def set_credentials(self, cred):
        """sets the set_credentials to the dict cred"""
        self.credential = cred

    def refresh(self, type=None):
        """refreshes the information of the cache for a given type 'images', 'flavors', 'servers', or 'all' for all of them"""
        time_stamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%SZ')
        selection = ""
        if type:
            selection = type.lower()[0]

        list_function = self._get_servers_dict

        data = self.servers
        if selection == 'a' or type is None:
            self.refresh("images")
            self.refresh("flavors")
            self.refresh("servers")
            return
        elif selection == 'i':
            list_function = self._get_images_dict
            data = self.images
        elif selection == 'f':
            list_function = self._get_flavors_dict
            data = self.flavors
        elif selection == 's':
            list_function = self._get_servers_dict
            data = self.servers
        elif selection == 'e':
            list_function = self._get_security_groups_dict
            data = self.security_groups
        elif selection == 't':
            list_function = self._get_stacks_dict
            data = self.stacks
        elif selection == 'u':
            list_function = self._get_usage_dict
            data = self.usage
        # elif selection == 'u':
        #    list_function = self._get_users_dict
        #    d = self.users
        # elif selection == 't':
        #    list_function = self._get_tenants_dict
        #    d = self.tenants
        elif type is not None:
            print("refresh type not supported")
            assert False

        list_func = list_function()

        if len(list_func) == 0:
            if selection == 'i':
                self.images = {}
            elif selection == 'f':
                self.flavors = {}
            elif selection == 's':
                self.servers = {}
            elif selection == 'e':
                self.security_groups = {}
            elif selection == 't':
                self.stacks = {}
            elif selection == 'u':
                self.usage = {}
            # elif selection == 'u':
            #    self.users = {}
            # elif selection == 't':
            #    self.tenants = {}

        else:
            data_updated = {}
            for key in list_func:
                element = list_func[key]
                # id = list[element]['id']
                # d[id] = list[element]
                # d[id]['cm_refresh'] = time_stamp

                # element is a dictionary. It doesn't have to lookup the list
                # like 'list[element]...'. element[...] simply works.
                id = element['id']
                data_updated[id] = element
                data_updated[id]['cm_refresh'] = time_stamp
            data = data_updated

    def keypair_list(self):
        raise NotImplementedError()

    def keypair_add(self, keyname, keycontent):
        raise NotImplementedError()

    def keypair_remove(self, keyname):
        raise NotImplementedError()
