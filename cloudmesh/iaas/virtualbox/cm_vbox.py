from sh import VBoxManage
from collections import OrderedDict
from pprint import pprint
from cloudmesh.iaas.ComputeBaseType import ComputeBaseType
from cloudmesh_common.logger import LOGGER


log = LOGGER(__file__)

vbox_list = VBoxManage.bake("list", "vms", "-l")
vbox_vminfo = VBoxManage.bake("showvminfo")
vbox_controlvm = VBoxManage.bake("controlvm")
vbox_startvm = VBoxManage.bake("startvm")

#
# LIST
#


def filter_attributes(d, filterkeys=["name", "uuid", "state"]):
    """filters from the given dict just the attributed with the specified keys"""
    f = {}
    for name in d:
        m = d[name]
        f[m["name"]] = dict(zip(filterkeys, [m[k] for k in filterkeys]))
    return f


def extract_state(attribute, value):
    if attribute == "state":
        value = value.split("(")[0]
    return value


def convert_to_dict(lines, token=":", converters=None):
    """converts lines of the form 
    attribute: value
    to a dict. The : can be changed to a token.
    and array of converter functions canbe passe to transform a specific attributes value.
    the attribute will be converted to lower case
    """
    m = {}
    for line in lines:
        try:
            attribute, value = line.split(token, 1)
            if converters is not None:
                for converter in converters:
                    value = converter(attribute, value)
            m.update({attribute.lower(): value.strip()})
        except:
            pass
    return m


class virtualbox(ComputeBaseType):

    # : the type of the cloud. It is "virtualbox"
    type = "virtualbox"  # global var

    def __init__(self, label, cred=None):
        self.credential = cred
        self.label = label

    def connect(self):
        """connect to the cloud"""
        pass

    def config(self, dict):
        """uses the dict to conduct some configuration with the parameters passed"""
        pass

    def find_user_id(self, force=False):
        """finds the user id of a user and caches it. If a chaced
        value is ther it will use that. If you specify force, it will
        regenerate it"""
        # just ignore cached
        return os.getusername()

    def _get_servers_dict(self):
        return _get_vms()

    #
    #  Helper functions
    #

    def _get_vms(filter=None):
        """
        returns the dict for the vms. if simple is specified as filter only
        very few attributs ar listed. the rturned attributes can be specified in
        a list.
        """

        result = vbox_list()
        d = {}
        for info in result.split("\n\n\n"):
            lines = info.split("\n\n")[0].split("\n")
            m = convert_to_dict(lines, converters=[extract_state])
            try:
                d[m["name"]] = m
            except:
                pass

        if filter is None:
            return d

        if filter == "simple":
            filterkeys = ["name", "uuid", "state"]
        else:
            filterkeys = filter

        f = filter_attributes(d, filterkeys)
        return f

    def _get_vminfo(name, filter=None):
        """returns the info of a named vm"""
        data = vbox_vminfo(name).split("\n\n")[0].split("\n")
        m = convert_to_dict(data, converters=[extract_state])
        if filter is None:
            return m

        if filter == "simple":
            filterkeys = ["name", "uuid", "state"]
        else:
            filterkeys = filter

        f = dict(zip(filterkeys, [m[k] for k in filterkeys]))
        return f

    def _get_state(name):
        """gets the state of a named vm"""
        info = get_vminfo(name, filter=["state"])
        return info["state"]

    def vm_create(self, name=None,
                  flavor_name=None,
                  image_id=None,
                  security_groups=None,
                  key_name=None,
                  meta=None):
        """create a virtual machine with the given parameters"""
        raise NotImplementedError()

    def vm_start(self, name, mode="headless"):
        """
        mode = gui, headless
        """

        try:
            state = self._get_state(name)
        except:
            log.error(
                "can not stop VM. VM with the name {0} does not exist".format(name))
            return

        if state != "running":

            result = vbox_startvm("startvm", name, "--type", mode)

            if result:
                log.error(str(result))
                return False
            else:
                return True
        else:
            log.error("vm with the name {0} is already running".format(name))
            return False

    def vm_delete(self, id):
        """delete the virtual machine with the id"""
        """ here id is the same as name"""
        raise NotImplementedError()

    def vm_control(self, name, action):
        try:
            state = self._get_state(name)
        except:
            log.error(
                "can not stop VM. VM with the name {0} does not exist".format(name))
            return
        if state == "running":
            result = vbox_controlvm(name, action)
            log.info("exit code {0}".format(result))
        if exitcode:
            return False
        else:
            return True

    def vm_stop(self, name):
        return self.vm_control(name, "savestate")

    def vm_halt(self, name):
        return self.vm_control(name, "poweroff")

    def vm_reset(self, name):
        return self.vm_control(name, "reset")


#     print "OOOO"
#     name = "compute1.puppetlabs.lan"
#     pprint (_get_vminfo(name))
#
#     print "YYYYY"
#     pprint (_get_vminfo(name, "simple"))
#
#     print "STATE"
#     print _get_state(name)
