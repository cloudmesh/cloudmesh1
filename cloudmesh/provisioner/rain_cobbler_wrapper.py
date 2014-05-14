from cloudmesh.rain.cobbler.cobbler_rest_api import CobblerRestAPI
from baremetal_computer import BaremetalComputer
from baremetal_status import BaremetalStatus
from hostlist import expand_hostlist
from datetime import datetime
from cloudmesh_common.logger import LOGGER
#
# SETTING UP A LOGGER
#

log = LOGGER(__file__)

class RainCobblerWrapper:
    """
    provide API for CM rain command or Web Interface.
    """
    def __init__(self):
        self.rest_api = CobblerRestAPI()
        self.baremetal = BaremetalComputer()
        self.status = BaremetalStatus()
    
    def baremetal_computer_host_on(self, raw_hosts):
        """Enable/ON computers for baremetal provisioning
        provided for **rain admin on HOSTS**
        :param string raw_hosts: ne or more hosts with the valid formation of hostlist
        :return: True means successfully, otherwise False
        """
        hosts = expand_hostlist(raw_hosts) if raw_hosts else None
        return self.baremetal.enable_baremetal_computers(hosts)
    
    def baremetal_computer_host_off(self, raw_hosts):
        """Disable/OFF computers for baremetal provisioning
        provided for **rain admin off HOSTS**
        :param string raw_hosts: ne or more hosts with the valid formation of hostlist
        :return: True means successfully, otherwise False
        """
        hosts = expand_hostlist(raw_hosts) if raw_hosts else None
        return self.baremetal.disable_baremetal_computers(hosts)
    
    def list_all_user_hosts(self):
        """list all baremetal computers that can be used by each user.
        provided for **rain admin list users**
        :return: a dict with the formation {"user1": "hostlist", "user2": "hostlist2"}
        """
        pass
    
    def get_status_short(self, raw_hosts=None):
        """get status of baremetal computer
        provided for **rain status --short [HOSTS]**
        :param string raw_hosts: one or more hosts with the valid formation of hostlist
        :return: a dict of the formation {"host1": "deployed", "host2": "deploying", "host3": "failed"}
        """
        hosts = expand_hostlist(raw_hosts) if raw_hosts else None
        return self.status.get_status_short(hosts)
    
    def get_status_summary(self, raw_hosts=None):
        """get status summary of baremetal computer
        provided for **rain status --summary [HOSTS]**
        :param string raw_hosts: one or more hosts with the valid formation of hostlist
        :return: a dict of the formation {"deployed": 1, "deploying":2, "failed":2, "total": 5}
        """
        hosts = expand_hostlist(raw_hosts) if raw_hosts else None
        return self.status.get_status_summary(hosts)
    
    def provision_host_with_profile(self, profile, raw_hosts):
        """
        baremetal provision host in raw_hosts with profile defined in cobbler. 
        provided for **rain provision --profile=PROFILE HOSTS**
        :param string profile: the name of cobbler profile
        :param string raw_hosts: one or more hosts with the valid formation of hostlist
        :return: a dict, formation is {"result": True|False, "description": "details"}
        """
        FIELD_DESC = "description"
        result_data = {"result": False, FIELD_DESC: ""}
        # check the exist of the profile
        profiles = self.rest_api.get_cobbler_profile_list()
        if profile in profiles:
            hosts = expand_hostlist(raw_hosts)
            print "after expand, hosts is: ", hosts
            systems = self.rest_api.get_cobbler_system_list()
            # check the system named host exist in cobbler or not
            not_exist_hosts = [h for h in hosts if h not in systems]
            already_exist_hosts = [h for h in hosts if h in systems]
            result = True
            # create system with profile for host in not_exist_hosts
            for host in not_exist_hosts:
                result = self.create_system_with_profile(host, profile)
                if not result:
                    result_data[FIELD_DESC] = "Create system for host {0} with profile {1} failed.".format(host, profile)
            if result:
                # update system with profile for host in already_exist_hosts
                for host in already_exist_hosts:
                    result = self.update_system_with_profile(host, profile)
                    if not result:
                        result_data[FIELD_DESC] = "Update system for host {0} with profile {1} failed.".format(host, profile)
            if result:
                # provision/deploy each host
                for host in hosts:
                    result = self.deploy_cobbler_system(host)
            result_data["result"] = result
        else:
            result_data[FIELD_DESC] = "profile {0} NOT exist in cobbler.".format(profile)
        return result_data
    
    def list_system_based_distro_kickstart(self, distro=None, kickstart=None):
        """list all possible systems/hosts based on distro and kickstart
        provided for **rain provision list (--distro=DISTRO|--kickstart=KICKSTART)**
        :param string distro: the name of cobbler distro
        :param string kickstart: the name of kickstart file (ONLY filename)
        :return: a list of systems/hosts name
        """
        profiles = self.list_profile_based_distro_kickstart(distro, kickstart)
        systems = []
        if profiles:
            for profile in profiles:
                result = self.rest_api.get_cobbler_profile_children(profile)
                if result:
                    systems.extend(result)
        return systems
    
    def provision_host_with_distro_kickstart(self, distro, kickstart, raw_hosts):
        """
        baremetal provision host in raw_hosts with distro defined in cobbler and kickstart file. 
        provided for **rain provision --distro=DITRO --kickstart=KICKSTART HOSTS**
        :param string distro: the name of cobbler distro
        :param string kickstart: the filename of kickstart
        :param string raw_hosts: one or more hosts with the valid formation of hostlist
        :return: a dict, formation is {"result": True|False, "description": "details"}
        """
        # step 1, try to find an existed profile matching distro and kickstart
        profiles = self.list_profile_based_distro_kickstart(distro, kickstart)
        if profiles:
            profile = profiles[0]
        # step 2, create a new profile based on distro and kickstart
        else:
            # create a temporary name for profile
            profile_name = "pt_{0}".format(self.get_current_time_str())
            data = {"name": profile_name, "distro": distro, "kickstart": kickstart,}
            result = self.rest_api.add_cobbler_profile(data)
            profile = profile_name if result else None
        if profile:
            return self.provision_host_with_profile(profile, raw_hosts)
        return False
    
    def add_profile_based_distro_kickstart(self, distro_url, kickstart, name):
        """add/create a new profile based a url of distro and a kickstart file
        provided for **rain provision add (--distro=URL|--kickstart=kickstart) NAME**
        :param string distro_url: the url for the user specified iso
        :param string kickstart: the absolute filename of kickstart in local computer
        :param string name: the name of destination profile
        :return: True means add/create profile successfully, otherwise failed
        """
        result = False
        # step 1, upload local kickstart file to cobbler
        ks_name = self.upload_kickstart_to_cobbler(kickstart, name)
        if ks_name:
            # step 2, add distro to cobbler
            distro_data = self.rest_api.add_cobbler_distro({"name": name, "url": distro_url,})
            if distro_data:
                # remove the original profile
                result = self.rest_api.remove_cobbler_profile(distro_data["profile"])
                if result:
                    # create a new profile
                    result = self.rest_api.add_cobbler_profile({"name": name, "distro": distro_data["distro"], "kickstart": ks_name,})
        return result
    
    def list_profile_based_distro_kickstart(self, distro=None, kickstart=None):
        """list all possible profiles based on distro and kickstart
        :param string distro: the name of cobbler distro
        :param string kickstart: the name of kickstart file (ONLY filename)
        :return: a list of profiles name
        """
        profiles = None
        if distro:
            profiles_distro = self.rest_api.get_cobbler_distro_children(distro)
            profiles_ks = None
            if kickstart:
                profiles_ks = self.rest_api.get_cobbler_profile_based_kickstart(kickstart)
            if profiles_distro and profiles_ks:
                profiles = [p for p in profiles_distro if p in profiles_ks]
            else:
                profiles = profiles_distro if profiles_distro else profiles_ks
        else:
            if kickstart:
                profiles = self.rest_api.get_cobbler_profile_based_kickstart(kickstart)
            else:
                profiles = self.rest_api.get_cobbler_profile_list()
        return profiles
    
    def upload_kickstart_to_cobbler(self, filename, name=None):
        """add a local kickstart file to cobbler
        :param string filename: the local filename of kickstart file, please use the absolute path
        :param string name: the destination name of kickstart in cobbler
        :return: the name of kickstart in cobbler if added success, otherwise None
        """
        if not name:
            name = filename.split("/")[-1]
        ext = name.split(".")[-1]
        if ext not in ["ks", "seed"]:
            name += ".ks"
        # read from local kickstart
        with open(filename) as f:
            lines = [line.rstrip("\n") for line in f]
        return self.save_kickstart_to_cobbler(lines, name)
    
    def save_kickstart_to_cobbler(self, contents, name):
        """save a list of string as a kickstart file to cobbler
        :param list contents: list of string, the conent of a kickstart file, ["line1", "line2"]
        :param string name: the destination name of kickstart in cobbler
        :return: the name of kickstart in cobbler if added success, otherwise None
        """
        data = {"name": name, "contents": contents,}
        result = self.rest_api.add_cobbler_kickstart(data)
        return name if result else None
    
    def create_system_with_profile(self, name, profile):
        """
        create a new system in cobbler with host information stored in inventory and profile
        :param string name: the unique name of host
        :param string profile: the profile name in cobbler, the profile MUST be exist
        :return:: True means create system sucefully, False means failed.
        """
        # get all the necessary host information stored in inventory
        host_info = self.baremetal.get_host_info(name)
        if host_info:
            host_info["profile"] = profile
            return self.rest_api.add_cobbler_system(host_info)
        return False
    
    def update_system_with_profile(self, name, profile):
        """
        update profile in a system
        :param string name: the unique name of host
        :param string profile: the profile name in cobbler, the profile MUST be exist
        :return:: True means update system sucefully, False means failed.
        """
        data = {"name": name, "profile": profile}
        return self.rest_api.update_cobbler_system(data)
    
    def get_current_time_str(self):
        """current time, format is YYYYMMDDHHmmSSfffff
        """
        t = datetime.now()
        return t.strftime("%Y%m%d%H%M%S%f")
    
# test
if __name__ == "__main__":
    rcb = RainCobblerWrapper()
    result_data = rcb.list_system_based_distro_kickstart()
    print result_data
    