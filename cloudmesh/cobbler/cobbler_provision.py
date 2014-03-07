#!/usr/bin/python

import cobbler.api as capi
import subprocess
import os
import sys
import time
import logging

class CobblerProvision:
    """ Stand on top of cobbler, provide simple and easy API for deploying new OS.
    
     NOTE: As described in "https://fedorahosted.org/cobbler/wiki/CobblerApi",
     Cobbler API (BootAPI) directly modifies the config store (data file) that may not be safe.
     Furthermore the modifications made will NOT be visible to cobblerd. Because cobbler
     command line depends on cobblerd. Therefore, the modification by BootAPI is NOT visible
     through command line.
     
     The strategy used here is as follows:
         (1) BootAPI can be used in reading only;
         (2) Add/Modify/Remove operations are operated by shell command.
    """
    
    def __init__(self):
        self.handler = capi.BootAPI()
        self.logger = logging.getLogger("Mycobbler")
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        self.logger.addHandler(ch)
    
    def get_token(self, username, password):
        """ validate user, generate a token representing his rights.
        return None if user not exist or password is not correct.
         """
        return "a random valid token"
    
    def validate_token(self, user_token, access_api):
        """ validate user's token, if it is not expired, then check whether the
        user has the right to access the specific api, that is access_api, 
        if yes, return True, otherwise return False
        """
        return True
    
    def list_distro_names(self, user_token):
        """ 
        ONLY list distribution names, 
        """
        return self._list_item_names(user_token, "distro")
    
    def list_profile_names(self, user_token):
        """ 
        ONLY list profile names, 
        """
        return self._list_item_names(user_token, "profile")
    
    def list_system_names(self, user_token):
        """ 
        ONLY list system names, 
        """
        return self._list_item_names(user_token, "system")
    
    def _list_item_names(self, user_token, func_name):
        """ 
        ONLY list item names, called by distro, profile, system, and etc.
        return a list if token is valid, otherwise return None.
        """
        if not self.validate_token(user_token, "list_{0}_names".format(func_name)):
            return None
        func_item = getattr(self.handler, "{0}s".format(func_name))
        return [x.name for x in func_item()]
    
    
    def get_distro_report(self, user_token, name):
        """ 
          report the detail of the distribution with name, 
        """
        return self._get_item_report(user_token, "distro", name)
    
    def get_profile_report(self, user_token, name):
        """ 
          report the detail of the profile with name, 
        """
        return self._get_item_report(user_token, "profile", name)
    
    def get_system_report(self, user_token, name):
        """ 
          report the detail of the system with name, 
        """
        return self._get_item_report(user_token, "system", name)
    
    def _get_item_report(self, user_token, func_name, item_name):
        """
          report the specific item, called by distro, profile, system, etc.
          if user authorization failed return None, otherwise return correct item dict.
        """
        if not self.validate_token(user_token, "get_{0}_report".format(func_name)):
            return None
        func_item = getattr(self.handler, "find_{0}".format(func_name))
        result_list = []
        for item in func_item(name=item_name, return_list=True):
            data = item.to_datastruct()
            result_list.append({"type": func_name, 
                                "name": data["name"], 
                                "data": data,
                                })
        return result_list
    
    def import_distro(self, user_token, url, name):
        if not self.validate_token(user_token, "import_distro"):
            return (False, "user token authorization failed.")
        dir_base = "/tmp"
        dir_iso = "{0}/iso".format(dir_base)
        dir_mount = "{0}/mnt/".format(dir_iso)
        result = self.mkdir(dir_mount)
        if not result:
            return (False, "User does NOT have write permission in /tmp directory")
        (result, msg) = self.wget(url, dir_iso)
        if not result:
            return (False, msg)
        old_distro_names = self.list_distro_names(user_token)
        if self.mount_image(msg, dir_mount):
            args = ["cobbler", "import", "--path={0}".format(dir_mount), "--name={0}".format(name),]
            result = self.shell_command(args)
            self.umount_image(dir_mount)
            if not result:
                return (False, "Failed to import distro [{0}] from [{1}]".format(name, url))
            curr_distro_names = self.list_distro_names(user_token)
            possible_names = [x for x in curr_distro_name if x not in old_distro_names]
            distro_name = None
            for pname in possible_names:
                if pname.startswith(name):
                    distro_name = pname
                    break
            return (True, distro_name) if distro_name else (False, "Failed to import distro, unknown error.")
        return (False, "Failed to mount unsupported image [{0}].".format(url))
    
    def add_profile(self, user_token, profile_name, distro_name, kickstart_file):
        """
          add a new profile
        """
        if not self.validate_token(user_token, "add_profile"):
            return (False, "user token authorization failed.")
        if profile_name in self.list_profile_names(user_token):
            return (False, "Profile name [{0}] has already existed.")
        if not (distro_name in self.list_distro_names(user_token)
                and self.file_exist(kickstart_file)):
            return (False, "Distro [{0}] or kickstart file [{1}] does NOT exist.".format(distro_name, kickstart_file))
        args = ["cobbler", "profile", "add", 
                "--name={0}".format(profile_name),
                "--distro={0}".format(distro_name), 
                "--kickstart={0}".format(kickstart_file),
                ]
        if self.shell_command(args):
            return (True, profile_name)
        return (False, "Failed to add profile [{0}] with distro [{1}] and kickstart file [{2}]".format(profile_name, distro_name, kickstart_file))
    
    def update_profile(self, user_token, profile_name, kickstart_file):
        """
          update the kickstart file in the profile
        """
        if not self.validate_token(user_token, "update_profile"):
            return (False, "user token authorization failed.")
        if not (profile_name in self.list_profile_names(user_token)
                and self.file_exist(kickstart_file)):
            return (False, "Profile [{0}] or kickstart file [{1}] does NOT exist.".format(profile_name, kickstart_file))
        args = ["cobbler", "profile", "edit", "--name={0}".format(profile_name), "--kickstart={0}".format(kickstart_file)]
        if self.shell_command(args):
            return (True, profile_name)
        return (False, "Failed to update profile [{0}] with kickstart file [{1}]".format(profile_name, kickstart_file))
    
    def add_system(self, user_token, system_name, profile_name, contents):
        """
          add system to cobbler.
          param interfaces is a list, each of which is a dict that has the following format.
          contents has the following formation:
          {
            name: system name,
            profile: profile name,
            gateway: default gateway,
            hostname: host name of system,
            kopts: kernel command-line arguments,
            ksmeta: kickstart meta data,
            name-servers: name servers,
            owners: users and groups,
            power: power_info,
            interfaces: [interface],
          }
          power_info has the following formation:
          {
            power-address: power IP address,
            power-type: ipmilan or etc...,
            power-user: power user,
            power-pass: power password,
            power-id: power id,
          }
          interface has the following formation:
          { name: eth0,
            ip-address: ipv4 address,
            mac-address: mac address,
            static: True | False,
            netmask: netmask of this interface,
            management: True | False,
          }
        """
        if not self.validate_token(user_token, "add_system"):
            return (False, "user token authorization failed.")
        if system_name in self.list_system_names(user_token):
            return (False, "System name [{0}] has already exist.".format(system_name))
        if not (profile_name in self.list_profile_names(user_token)):
            return (False, "Profile [{0}] does NOT exist.".format(profile_name))
        args = ["cobbler", "system", "add", "--name={0}".format(system_name), "--profile={0}".format(profile_name), ]
        result = self.shell_command(args)
        if result:
            result = self._edit_system(system_name, contents)
        return (True, system_name) if result else (False, "Failed to add system, please check parameters.")
    
    def update_system(self, system_name, contents):
        if not self.validate_token(user_token, "update_system"):
            return (False, "user token authorization failed.")
        if system_name not in self.list_system_names(user_token):
            return (False, "System name [{0}] does NOT exist.".format(system_name))
        if "profile" in contents:
            if not (contents["profile"] in self.list_profile_names(user_token)):
                return (False, "Failed to update system, because profile [{0}] does NOT exist.".format(contents["profile"]))
            args = ["cobbler", "system", "edit", "--name={0}".format(system_name)]
            args += ["--profile={0}".format(contents["profile"])]
            if not self.shell_command(args):
                return (False, "Failed to update system [{0}] with unknown error.".format(system_name))
        result = self._edit_system(system_name, contents)
        return (True, system_name) if result else (False, "Failed to add system, please check parameters.")
    
    
    def _edit_system(self, system_name, contents):
        """
          edit system of system_name with contents
        """
        system_args = "gateway hostname kopts ksmeta name-servers owners".split()
        power_args = "power-type power-address power-user power-pass power-id".split()
        interface_args = "ip-address mac-address netmask static management".split()
        args_edit = ["cobbler", "system", "edit", "--name={0}".format(system_name), ]
        args = args_edit + self._merge_arg_list(system_args, contents)
        # power
        if "power" in contents.keys():
            args += self._merge_arg_list(power_args, contents["power"])
        all_interface_args = []
        if "interfaces" in contents.keys():
            for interface in contents["interfaces"]:
                temp_if_args = ["--interface={0}".format(interface["name"])]
                temp_if_args += self._merge_arg_list(interface_args, interface)
                all_interface_args += [temp_if_args]
        result = True
        if len(all_interface_args) > 0:
            result = self.shell_command(args + all_interface_args[0])
        elif len(args) > len(args_edit):
            result = self.shell_command(args)
        if result:
            for interface in all_interface_args[1:]:
                result = self.shell_command(args_edit + interface)
                if not result:
                    break
        return result
    
    def remove_distro(self, user_token, distro_name):
        """
          remove a distro
        """
        return remove_item(user_token, "distro", distro_name)
    
    def remove_profile(self, user_token, profile_name):
        """
          remove a profile
        """
        return remove_item(user_token, "profile", profile_name)
    
    def remove_system(self, user_token, system_name):
        """
          remove a system
        """
        return remove_item(user_token, "system", system_name)
    
    def remove_item(self, user_token, item_name, object_name):
        if not self.validate_token(user_token, "remove_{0}".format(item_name)):
            return (False, "user token authorization failed.")
        args = ["cobbler", item_name, "remove", "--name={0}".format(object_name)]
        item_func = getattr(self, "get_{0}_names".format(item_name))
        result = True
        if object_name in item_func():
            result = self.shell_command(args)
        return result
    
    def remove_system_interface(self, user_token, system_name, interface_name=None):
        """
         remove an interface from a system.
        """
        if not self.validate_token(user_token, "remove_system_interface"):
            return (False, "user token authorization failed.")
        result = True
        if system_name in self.list_system_names(user_token):
            report = self.get_system_report(user_token, system_name)
            if interface_name in report[0]["data"]["interfaces"]:
                args = ["cobbler", "system", "edit", "--name={0}".format(system_name), 
                        "--interface={0}".format(interface_name), "--delete-interface", ]
                result = self.shell_command(args)
        return result
    
    def deploy_system(self, user_token, system_name):
        """
         deploy a system.
        """
        if not self.validate_token(user_token, "deploy_system"):
            return (False, "user token authorization failed.")
        result = True
        if system_name not in self.list_system_names(user_token):
            return (False, "System [{0}] dose NOT exist.".format(system_name))
        system = self.handler.find_system(name=system_name)
        if not system.netboot_enabled:
            system.netboot_enabled = True
            # save modified system
            self.handler.add_system(system)
        # monitor status
        self.handler.reboot(system)
        return (True, "deploy system")
        
    def power_system(self, user_token, system_name, power_on=True):
        """
         power on a system.
        """
        if not self.validate_token(user_token, "power_system"):
            return (False, "user token authorization failed.")
        result = True
        if system_name not in self.list_system_names(user_token):
            return (False, "System [{0}] dose NOT exist.".format(system_name))
        system = self.handler.find_system(name=system_name)
        if system.netboot_enabled:
            system.netboot_enabled = False
            # save modified system
            self.handler.add_system(system)
        self.handler.power_on(system) if power_on else self.handler.power_off(system)
        return (True, "Power {0} system.".format("on" if power_on else "off"))
    
    
    def _merge_arg_list(self, arg_list, content_dict):
        result = []
        curr_arg_list = [arg for arg in arg_list if arg in content_dict.keys()]
        for arg in curr_arg_list:
            if content_dict[arg]:
                result += ["--{0}={1}".format(arg, content_dict[arg])]
        return result
    
    def file_exist(self, filename):
        return os.path.isfile(filename)
    
    def mkdir(self, sdir):
        args = ["mkdir", "-p", sdir]
        return self.shell_command(args)
    
    def mount_image(self, image_name, location):
        args = ["mount", "-o", "loop", image_name, location]
        return self.shell_command(args)
    
    def umount_image(self, location):
        args = ["umount", "-o", "loop", location]
        return self.shell_command(args)
    
    def wget(self, url, location):
        supported_protocols = ["http", "ftp", "https",]
        supported_image = ["iso", ]
        protocol = url.split(":")[0]
        filename = url.split("/")[-1]
        filename_ext = filename.split(".")[-1]
        if protocol in supported_protocols and filename_ext in supported_image:
            args = ["wget", "-q", "-O", "{0}/{1}".format(location, filename), url,]
            if self.shell_command(args):
                result = (True, "{0}/{1}".format(location, filename))
            else:
                result = (False, "Fail to download file [{0}]".format(url))
        else:
            result = (False, "Not supported protocol [{0}] or image [{1}].".format(protocol, filename_ext))
        return result
    
    def shell_command(self, args):
        print " ".join(args)
        DEVNULL = open(os.devnull, "wb")
        return 0 == subprocess.call(args, stderr=DEVNULL, stdout=DEVNULL)

if __name__ == "__main__":
    cp = CobblerProvision()
    user_token = cp.get_token("username", "password")
    """
    distro_names = cp.list_distro_names(token)
    print "distros names: ", distro_names
    profile_names = cp.list_profile_names(token)
    print "profiles names: ", profile_names
    system_names = cp.list_system_names(token)
    print "systems names: ", system_names
    name = "*x86_64"
    distros = cp.get_profile_report(token, name)
    if len(distros) > 0:
        for distro in distros:
            print "profile report: {0}".format( distro)
    else:
        print "Cannot find profile with name {0}".format(name)
    url = "http://ftp.ussg.iu.edu/linux/ubuntu-releases/13.04/ubuntu-13.04-server-amd64.iso"
    name = "test"
    (result, msg) = cp.add_distro(token, url, name)
    print "after add distro, result is {0}, msg is {1}".format(result, msg)
    profile_name = "test-x86_64"
    kickstart_file = "/var/lib/cobbler/kickstarts/ktanaka.ks"
    result = cp.update_profile(user_token, profile_name, kickstart_file)
    print result
    profile_name = "abcdef_test"
    distro_name = "test-x86_64"
    kickstart_file = "/var/lib/cobbler/kickstarts/ktanaka.ks"
    result = cp.add_profile(user_token, profile_name, distro_name, kickstart_file)
    print result
    """
    my_sys = {
               "name": "mytestsys",
               "profile": "test-x86_64",
               "power": {
                           "power-address": "1.2.3.4",
                           "power-user": "test",
                           "power-pass": "nopassword",
                           "power-type": "ipmilan",
                           "power-id": 1,
                         },
               "interfaces": [
                               {
                                 "name": "ee1",
                                 "ip-address": "192.168.1.23",
                                 "mac-address": "aa:bb:cc:dd:ee:ff",
                                 "static": True,
                                 "management": True,
                                 "netmask": "255.255.255.0",
                                },
                              {
                                 "name": "ee2",
                                 "ip-address": "192.168.1.123",
                                 "mac-address": "aa:bb:cc:ee:dd:ff",
                                 "static": True,
                                 "management": False,
                                 "netmask": "255.255.255.0",
                                },
                              ],
              }
    #(result, msg) = cp.add_system(user_token, my_sys["name"], my_sys["profile"], my_sys)
    #print result, msg
    result = cp.remove_system_interface(user_token, my_sys["name"], my_sys["interfaces"][0]["name"])
    print result