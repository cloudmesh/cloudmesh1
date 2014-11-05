from __future__ import print_function
from cloudmesh.rain.cobbler.cobbler_rest_api import CobblerRestAPI
from cloudmesh.rain.cobbler.queue.tasks import deploy_system, power_system
from baremetal_computer import BaremetalComputer
from baremetal_status import BaremetalStatus
from baremetal_policy import BaremetalPolicy
from hostlist import expand_hostlist, collect_hostlist
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
        self.policy = BaremetalPolicy()

    def baremetal_computer_host_list(self):
        """list computers for baremetal provisioning
        provided for **rain admin baremetals**
        :return: a list of baremetal computers
        """
        return self.baremetal.get_baremetal_computers()

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

    def list_all_user_group_hosts(self, flag_user=True, flag_merge=False):
        """list all baremetal computers that can be used by each user/project.
        provided for **rain admin list users/projects**
        :param boolean flag_user: True means user, False means projects
        :return: a dict with the formation {"user1": "hostlist", "user2": "hostlist2"}
        """
        if flag_user:
            return self.policy.get_all_user_policy(flag_merge)
        return self.policy.get_all_group_policy(flag_merge)

    def list_user_hosts(self, raw_users):
        """list all baremetal computers that can be used by each user.
        provided for **rain admin list hosts --user=USERS**
        :param string raw_users: one or more users with the valid formation of hostlist
        :return: a dict with the formation {"user1": "hostlist", "user2": "hostlist2"}
        """
        return self.policy.get_policy_based_user(raw_users)

    def list_project_hosts(self, raw_projects):
        """list all baremetal computers that can be used by each project/group.
        provided for **rain admin list hosts --project=PROJECTS**
        :param string raw_projects: one or more projects with the valid formation of hostlist
        :return: a dict with the formation {"project1": "hostlist", "project2": "hostlist2"}
        """
        return self.policy.get_policy_based_group(raw_projects)

    def get_policy_based_user_or_its_projects(self, user, projects):
        """get the merged policy based on the username and his/her related projects
        """
        return self.policy.get_policy_based_user_or_its_projects(user, projects)

    def add_user_policy(self, raw_users, raw_hosts):
        """add a new policy for user
        provided for **rain admin policy --user=USERS -l HOSTS**
        :param string raw_users: one or more users with the valid formation of hostlist
        :param string raw_hosts: one or more hosts with the valid formation of hostlist
        :return: None if add failed, otherwise the UUID of this policy
        :rtype: string
        """
        return self.policy.add_user_policy(raw_users, raw_hosts)

    def add_project_policy(self, raw_projects, raw_hosts):
        """add a new policy for project
        provided for **rain admin policy --project=PROJECTS -l HOSTS**
        :param string raw_projects: one or more projects with the valid formation of hostlist
        :param string raw_hosts: one or more hosts with the valid formation of hostlist
        :return: None if add failed, otherwise the UUID of this policy
        :rtype: string
        """
        return self.policy.add_group_policy(raw_projects, raw_hosts)

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

    def provision_host_with_profile(self, profile, hosts):
        """
        baremetal provision host in raw_hosts with profile defined in cobbler.
        provided for **rain provision --profile=PROFILE HOSTS**
        :param string profile: the name of cobbler profile
        :param list hosts: a list of host ["host1", "host2",]
        :return: a dict, formation is {"result": True|False, "description": "details"}
        """
        FIELD_DESC = "description"
        result_data = {"result": False, FIELD_DESC: ""}
        # check the exist of the profile
        profiles = self.rest_api.get_cobbler_profile_list()
        if profile in profiles:
            #hosts = expand_hostlist(raw_hosts)
            #log.debug("after expand, raw_hosts {0} is: {1}".format(raw_hosts, hosts))
            systems = self.rest_api.get_cobbler_system_list()
            # check the system named host exist in cobbler or not
            not_exist_hosts = [h for h in hosts if h not in systems]
            already_exist_hosts = [h for h in hosts if h in systems]
            log.debug("hosts is: {0}, systems is: {1}, not_exist_hosts is {2}, already_exist is {3}".format(
                hosts, systems, not_exist_hosts, already_exist_hosts))
            result = True
            # create system with profile for host in not_exist_hosts
            for host in not_exist_hosts:
                result = self.create_system_with_profile(host, profile)
                if not result:
                    result_data[FIELD_DESC] = "Create system for host {0} with profile {1} failed.".format(
                        host, profile)
            if result:
                # update system with profile for host in already_exist_hosts
                for host in already_exist_hosts:
                    result = self.update_system_with_profile(host, profile)
                    if not result:
                        result_data[FIELD_DESC] = "Update system for host {0} with profile {1} failed.".format(
                            host, profile)
            if result:
                # provision/deploy each host
                for host in hosts:
                    log.info(
                        "call celery deploy_system on host {0} ...".format(host))
                    deploy_system.apply_async([host], queue='cobbler')
            result_data["result"] = result
        else:
            result_data[
                FIELD_DESC] = "profile {0} NOT exist in cobbler.".format(profile)
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

    def list_profile_based_distro_kickstart(self, distro=None, kickstart=None):
        """list all possible profiles based on distro and kickstart
        provided for **rain provision list --type=profile (--distro=DISTRO|--kickstart=KICKSTART)**
        :param string distro: the name of cobbler distro
        :param string kickstart: the name of kickstart file (ONLY filename)
        :return: a list of profiles name
        """
        profiles = None
        if distro:
            profiles_distro = self.rest_api.get_cobbler_distro_children(distro)
            profiles_ks = None
            if kickstart:
                profiles_ks = self.rest_api.get_cobbler_profile_based_kickstart(
                    kickstart)
            if profiles_distro and profiles_ks:
                profiles = [p for p in profiles_distro if p in profiles_ks]
            else:
                profiles = profiles_distro if profiles_distro else profiles_ks
        else:
            if kickstart:
                profiles = self.rest_api.get_cobbler_profile_based_kickstart(
                    kickstart)
            else:
                profiles = self.rest_api.get_cobbler_profile_list()
        return profiles

    def provision_host_with_distro_kickstart(self, distro, kickstart, hosts):
        """
        baremetal provision host in hosts with distro defined in cobbler and kickstart file.
        provided for **rain provision --distro=DITRO --kickstart=KICKSTART HOSTS**
        :param string distro: the name of cobbler distro
        :param string kickstart: the filename of kickstart
        :param list hosts: a list of host ["host1", "host2",]
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
            data = {
                "name": profile_name, "distro": distro, "kickstart": kickstart, }
            result = self.rest_api.add_cobbler_profile(data)
            profile = profile_name if result else None
        if profile:
            return self.provision_host_with_profile(profile, hosts)
        return {"result": False, "description": "create profile with distro and kickstart failed.", }

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
            distro_data = self.rest_api.add_cobbler_distro(
                {"name": name, "url": distro_url, })
            if distro_data:
                # remove the original profile
                result = self.rest_api.remove_cobbler_profile(
                    distro_data["profile"])
                if result:
                    # create a new profile
                    result = self.rest_api.add_cobbler_profile(
                        {"name": name, "distro": distro_data["distro"], "kickstart": ks_name, })
        return result

    def power_host(self, hosts, flag_on=True):
        """power ON/OFF hosts
        provided for **rain provision power [--off] HOSTS**
        :param list hosts: a list of host ["host1", "host2",]
        :param boolean flag_on: True means power ON, False means OFF
        :return: a dict of {"host1": True, "host2": False}, in which True means send power command, False means hosts MUST deploy before power
        """
        result = {}
        for host in hosts:
            result[host] = False
        hosts_status = self.status.get_status_short(hosts)
        for host in hosts_status:
            if hosts_status[host] == "deployed":
                result[host] = True
                #self.rest_api.power_cobbler_system(host, flag_on)
                power_system.apply_async([host, flag_on], queue='cobbler')
        return result

    def monitor_host(self, hosts):
        """monitor the progress of deploying/powering ON/OFF of hosts
        provided for **rain provision monitor HOSTS**
        :param list hosts: a list of host ["host1", "host2",]
        :return: a dict of {"host1": {"status": "deploying", "progress": 25, }, "host2": {"status": "poweron", "progress": 100,}, "host3": {"status": "poweroff", "progress": 10,},}
        """
        result = {}
        for host in hosts:
            result[host] = self.status.get_host_progress(host)
        return result

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
        data = {"name": name, "contents": contents, }
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
    #result_data = rcb.baremetal_computer_host_on("i003")
    #result_data = rcb.baremetal_computer_host_on("i0[06-10]")
    #result_data = rcb.baremetal_computer_host_off("i003,i189")
    #result_data = rcb.list_all_user_group_hosts()
    #result_data = rcb.list_all_user_group_hosts(False)
    #result_data = rcb.list_user_hosts("chen")
    #result_data = rcb.list_project_hosts("fg1")
    #result_data = rcb.add_user_policy("chen", "i008")
    #result_data = rcb.add_project_policy("fg1", "i008")
    #result_data = rcb.get_status_short()
    #result_data = rcb.get_status_summary()
    #result_data = rcb.list_system_based_distro_kickstart()
    #result_data = rcb.provision_host_with_profile("centos6-x86_64", "i072")
    #result_data = rcb.rest_api.monitor_deploy_power_status("i072", "deploy")
    result_data = rcb.baremetal_computer_host_list()
    print(result_data)
