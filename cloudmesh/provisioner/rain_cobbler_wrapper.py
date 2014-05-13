from cloudmesh.rain.cobbler.cobbler_rest_api import CobblerRestAPI
from hostlist import expand_hostlist
from cloudmesh.util.logger import LOGGER
#
# SETTING UP A LOGGER
#

log = LOGGER(__file__)

class RainCobblerWrapper:
    """
    provide API for CM command or Web Interface.
    """
    def __init__(self):
        self.rest_api = CobblerRestAPI()
        
    def provision_host_with_profile(self, profile, raw_hosts):
        """
        baremetal provision host in raw_hosts with profile defined in cobbler
        ..return:: a dict, formation is {"result": True|False, "description": "details"}
        """
        FIELD_DESC = "description"
        result_data = {"result": False, FIELD_DESC: ""}
        # check the exist of the profile
        profiles = self.baremetal.get_cobbler_profile_list()
        if profile in profiles:
            hosts = expand_hostlist(raw_hosts)
            print "after expand, hosts is: ", hosts
            systems = self.baremetal.get_cobbler_system_list()
            # check the system named host exist in cobbler
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
    
    def create_system_with_profile(self, name, profile):
        """
        create a new system in cobbler with host information stored in inventory and profile
        ..param:: name the unique name of host
        ..param:: profile the profile name in cobbler, the profile MUST be exist
        ..return:: True means create system sucefully, False means failed.
        """
        # get all the necessary host information stored in inventory
        host_info = self.baremetal.get_host_info(name)
        host_info["profile"] = profile
        return self.baremetal.add_cobbler_system(host_info)
    
    def update_system_with_profile(self, name, profile):
        """
        update profile in a system
        ..return:: True means update system sucefully, False means failed.
        """
        data = {"name": name, "profile": profile}
        return self.baremetal.update_cobbler_system(data)
    
# test
if __name__ == "__main__":
    rcb = RainCobblerWrapper()
    result_data = rcb.cra.get_cobbler_distro_list()
    print result_data
    