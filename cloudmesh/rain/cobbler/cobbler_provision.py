#!/usr/bin/python
from __future__ import print_function

from cobbler import api as capi
from multiprocessing import Process, Queue
from functools import wraps
import fnmatch
import os
import subprocess

# 1: debug, 2: info, 3: warn, 4: error
MY_DEBUG_LEVEL = 1
MY_DEBUG_STRING = ["", "DEBUG", "INFO", "WARN", "ERROR", ]


def mysay(msg, level):
    if level >= MY_DEBUG_LEVEL:
        print("[{0}] {1}".format(MY_DEBUG_STRING[level], msg))


def say_debug(msg):
    return mysay(msg, 1)


def say_info(msg):
    return mysay(msg, 2)


def say_warn(msg):
    return mysay(msg, 3)


def say_error(msg):
    return mysay(msg, 4)


def authorization(func):
    """decorator. authorizate the user's action according to his token and current accessing API.
    """
    @wraps(func)
    def wrap_authorization(self, *args, **kwargs):
        """
        user_token = kwargs.get("user_token", "")
        if self.validate_token(func.__name__, user_token):
            return func(self, *args, **kwargs)
        else:
            return self._simple_result_dict(False, "Authorization failed with token {0}".format(user_token))
        """
        # ONLY for debug
        # currently, NO authorization
        # print "[TEST ONLY] Authorizate function {0}
        # ...".format(func.__name__)
        return func(self, *args, **kwargs)
    return wrap_authorization


def cobbler_object_exist(object_type, ensure_exist=True):
    """decorator. check whether one object exist or not in cobble.
    :param string object_type: a name in ["distro", "profile", "system"]
    :param boolean ensure_exist: True means the object MUST exist, otherwise must NOT exist.
    """
    def _cobbler_object_exist(func):
        @wraps(func)
        def wrap_cobbler_object_exist(self, object_name, *args, **kwargs):
            # print "args is: ", args
            # print "kwargs is: ", kwargs
            name = object_name
            flag_exist = False
            if name in self._list_item_names(object_type):
                flag_exist = True
            if ensure_exist:  # MUST exist
                if flag_exist:
                    return func(self, name, *args, **kwargs)
                else:
                    return self._simple_result_dict(False, "The name {0} in {1} does NOT exist.".format(name, object_type))
            else:  # must NOT exist
                if not flag_exist:
                    return func(self, name, *args, **kwargs)
                else:
                    return self._simple_result_dict(False, "The name {0} in {1} already exists.".format(name, object_type))
        return wrap_cobbler_object_exist
    return _cobbler_object_exist


class CobblerProvision:

    """ Stand on top of cobbler, provide simple and easy API for deploying new OS.

     NOTE: As described in "https://fedorahosted.org/cobbler/wiki/CobblerApi",
     Cobbler API (BootAPI) directly modifies the config store (data file) that may not be safe.
     Furthermore the modifications made will NOT be visible to cobblerd. Because cobbler
     command line depends on cobblerd. Therefore, the modification by BootAPI is NOT visible
     through command line.

     The strategy used here is as follows:
         (1) BootAPI can be used in reading only, MUST use multiprocessing;
         (2) Add/Modify/Remove operations are operated by shell command.
    """
    # default kickstart location
    KICKSTART_LOCATION = "/var/lib/cobbler/kickstarts"

    def __init__(self):
        pass

    def get_token(self, username, password):
        """validate user, generate a token representing his rights.
        return None if user not exist or password is not correct.
        :param username: the username
        :type username: string
        :param password: the password
        :type password: string
        """
        return "a random valid token"

    def validate_token(self, access_api, user_token):
        """ validate user's token, if it is not expired, then check whether the
        user has the right to access the specific api, that is access_api,
        if yes, return True, otherwise return False

        :param access_api: the access_api
        :type access_api: string
        :param user_token: the user_token
        :type user_token: string
        """
        print("user_token = {0}, access_api = {1}".format(user_token, access_api))
        return True

    @authorization
    def list_distro_names(self, **kwargs):
        """list distribution names,
        :return: a list of distro names
        """
        return self._simple_result_dict(True, data=self._list_item_names("distro"))

    @authorization
    def list_profile_names(self, **kwargs):
        """list profile names,
        :return: a list of profile names
        """
        return self._simple_result_dict(True, data=self._list_item_names("profile"))

    @authorization
    def list_system_names(self, **kwargs):
        """list system names,
        :return: a list of system names
        """
        return self._simple_result_dict(True, data=self._list_item_names("system"))

    @authorization
    def list_kickstart_names(self, **kwargs):
        """list kickstart filenames with extension,
        :return: a list of kickstart filenames
        """
        return self._simple_result_dict(True, data=self.list_kickstart_filenames(self.KICKSTART_LOCATION))

    @authorization
    def list_iso_names(self, **kwargs):
        """list iso filenames with extension **iso**,
        :return: a list of iso filenames
        """
        filenames = self.list_dir_filenames(self.get_temp_dir_iso())
        return self._simple_result_dict(True, data=[f for f in filenames if f.endswith(".iso")])

    def list_kickstart_filenames(self, dir_name):
        """list the kickstart file under **dir_name** directory that has an extension **ks** or **seed**.
        :param string dir_name: the directory that stores kickstart files
        :return: a list of valid kickstart filename with path information
        """
        files = self.list_dir_filenames(dir_name, False)
        return [f for f in files if f.endswith(".ks") or f.endswith(".seed")]

    def _call_cobbler_process(self, func_name, *args):
        """Provide multiple process support.
        The cobbler REST service depends on this API **heavily** since the inherent characteristics of cobbler
        """
        q = Queue()
        p = Process(target=getattr(self, func_name), args=(q,) + args)
        p.start()
        result = q.get()
        p.join()
        return result

    def _wrap_process_list_item_names(self, q, objects):
        """Call cobbler API **distros**, **profiles**, **systems** to get the corresponding objects
        :return: a list of name of objects
        """
        cobbler_handler = capi.BootAPI()
        func = getattr(cobbler_handler, objects)
        q.put([x.name for x in func()])

    def _list_item_names(self, object_type):
        """ONLY list item names
        :param string object_type: an cobbler object type in distro, profile, system, and etc.
        :return: a list of name of object_type
        """
        return self._call_cobbler_process("_wrap_process_list_item_names", "{0}s".format(object_type))

    def _wrap_report_result(self, object_type, name):
        """get the detail report of *name* of cobbler object **object_type**
        :return: the data field in result dict can refer :py:func:`._wrap_process_get_item_report`
        """
        data = self._get_item_report(object_type, name)
        result = True if len(data) else False
        msg = "Success" if result else "Object {0} does NOT exist in {1}s.".format(
            name, object_type)
        return self._simple_result_dict(result, msg, data)

    @authorization
    def get_distro_report(self, name, **kwargs):
        """report the detail of the distribution with name,
        :return: refer the function :py:func:`._wrap_report_result`
        """
        return self._wrap_report_result("distro", name)

    @authorization
    def get_profile_report(self, name, **kwargs):
        """report the detail of the profile with name,
        :return: refer the function :py:func:`._wrap_report_result`
        """
        return self._wrap_report_result("profile", name)

    @authorization
    def get_system_report(self, name, **kwargs):
        """report the detail of the system with name,
        :return: refer the function :py:func:`._wrap_report_result`
        """
        return self._wrap_report_result("system", name)

    @authorization
    def get_kickstart_report(self, name, **kwargs):
        """report the detail of the kickstart with filename,
        :return: refer the function :py:func:`._wrap_report_result`
        """
        return self._wrap_report_result("kickstart", name)

    def get_object_child_count(self, object_type, name, handler):
        """get the count of child list of a cobbler object
        :return: the count of children
        :rtype: int
        """
        result = self._get_object_child_list(object_type, name, handler)
        return len(result) if result else 0

    def _get_object_child_list(self, object_type, name, handler=None):
        """get the child list of a cobbler object **distro** and **profile**
        :param string object_type: a type in ['distro', 'profile']
        :param string name: the specific name in an object_type
        :param BootAPI handler: the Cobbler API handler
        :returns: None if object_type is NOT in ['distro', 'profile'], empty list if there is no child, otherwise return ['child', 'child',]
        :rtype: list
        """
        pobjects = {"distro": "profile",
                    "profile": "system",
                    }
        result = None
        if object_type in pobjects:
            if not handler:
                handler = capi.BootAPI()
            func = getattr(handler, "find_{0}".format(pobjects[object_type]))
            kwargs = {}
            kwargs[object_type] = name
            # find_profile(distro=distro_name)
            child_list = func(return_list=True, **kwargs)
            result = [v.name for v in child_list]
        return result

    @authorization
    def get_object_child_list(self, object_type, name, handler=None):
        data = self._get_object_child_list(object_type, name, handler)
        if data is not None:
            return self._simple_result_dict(True, data=data)
        return self._simple_result_dict(False, "NOT Supported Object {0}".format(object_type))

    @authorization
    def get_profile_match_kickstart(self, name):
        """get the profile matching the name of kickstart file
        :param string name: the name of kickstart file, supports UNIX wildcard
        :return: a list of profile name
        """
        profiles = self.get_profile_report("*")
        result = None
        if profiles:
            result = []
            for profile in profiles["data"]:
                data = profile["data"]
                kickstart = data["kickstart"]
                filename_kickstart = kickstart.split("/")[-1]
                if fnmatch.fnmatch(filename_kickstart, name):
                    result.append(data["name"])
        if result is not None:
            return self._simple_result_dict(True, data=result)
        return self._simple_result_dict(False, "Cannot find profiles mathching {0}".format(name))

    def _wrap_process_get_item_report(self, q, object_type, name):
        """get the detail report of *name* of cobbler object **object_type**.
        :param string object_type: a type in ['distro', 'profile', 'system', 'kickstart',]
        :param string name: the name that user specified, it supports UNIX wildcard
        :return: a list of report that has the formation [{"name": name, data": data,}, {}]
        """
        result_list = []
        if object_type == "kickstart":
            allfiles = self.list_kickstart_filenames(self.KICKSTART_LOCATION)
            for filename in allfiles:
                if fnmatch.fnmatch(filename, name):
                    result_list.append({
                        "type": "kickstart",
                        "name": filename,
                        "data": {"name": filename,
                                 "contents": self.read_file_to_list("{0}/{1}".format(self.KICKSTART_LOCATION, filename)),
                                 },
                    })
        else:
            cobbler_handler = capi.BootAPI()
            func = getattr(cobbler_handler, "find_{0}".format(object_type))
            for item in func(name=name, return_list=True):
                data = item.to_datastruct()
                if object_type == "system":
                    data["child_count"] = len(data["interfaces"])
                else:
                    data["child_count"] = self.get_object_child_count(
                        object_type, data["name"], cobbler_handler)
                result_list.append({"type": object_type,
                                    "name": data["name"],
                                    "data": data,
                                    })
        q.put(result_list)

    def _get_item_report(self, object_type, name):
        """report the specific item, called by distro, profile, system, etc.
        """
        return self._call_cobbler_process("_wrap_process_get_item_report", object_type, name)

    def get_temp_dir_base(self):
        """get the parent directory that stores iso files
        """
        return "/tmp"

    def get_temp_dir_iso(self):
        """get the directory that stores iso files
        """
        return "{0}/iso".format(self.get_temp_dir_base())

    def get_temp_dir_mount(self):
        """get the mount directory that mount iso files
        """
        return "{0}/mnt/".format(self.get_temp_dir_iso())

    @authorization
    def import_distro(self, udistro_name, **kwargs):
        """Add a distribution to cobbler with import command. The import distro will rename the udistro_name by adding suffix which is "-x86_64" in generall.
        At the same time, the import also generate a profile with the same name automatically. Both of them can be obtained through **data** field in return dict.
        The first step is to fetch image file given by parameter url with wget, the url MUST be http, ftp, https.
        Then, moust the image, finally import iso with cobbler import command
        :param string udistro_name: the distro name that user specified
        :param dict kwargs: a dict contains the following {"url": "iso url",}, url can only have a filename
        :returns: a dict defined in :py:func:`_simple_result_dict`, the data field in dict is {"distro":"name", "profile":"name"}
        """
        url = kwargs.get("url", "")
        dir_iso = self.get_temp_dir_iso()
        dir_mount = self.get_temp_dir_mount()
        flag_result = self.mkdir(dir_mount)
        if not flag_result:
            return self._simple_result_dict(False, "User does NOT have write permission in /tmp directory.")
        # fetch image iso
        (flag_result, iso_filename) = self.iso_exist(url, dir_iso)
        if not flag_result:    # if has NOT downloaded, then do it now.
            (flag_result, msg) = self.wget(url, dir_iso)
            if not flag_result:
                return self._simple_result_dict(False, msg)
            iso_filename = msg
        old_distro_names = self._list_item_names("distro")
        # mount image
        # check mount location is idle or not
        if len(os.listdir(dir_mount)) > 0:
            self.umount_image(dir_mount)    # must umount first
        if self.mount_image(iso_filename, dir_mount):
            cmd_args = [
                "cobbler", "import", "--path={0}".format(dir_mount), "--name={0}".format(udistro_name), ]
            flag_result = self.shell_command(cmd_args)
            self.umount_image(dir_mount)
            if not flag_result:
                return self._simple_result_dict(False, "Failed to import distro [{0}] from [{1}]".format(udistro_name, url))
            curr_distro_names = self._list_item_names("distro")
            # double check the result of import distro
            possible_names = [
                x for x in curr_distro_names if x not in old_distro_names and x.startswith(udistro_name)]
            distro_name = possible_names[0] if len(possible_names) else None
            # import a distribution will generate a profile with the same name
            # automatically
            distro_return_data = {
                "distro": distro_name, "profile": distro_name, }
            return self._simple_result_dict(True if distro_name else False, "Add distro {0} {1}successfully.".format(udistro_name, "" if distro_name else "un"), data=distro_return_data)
        return self._simple_result_dict(False, "Failed to mount unsupported image [{0}] in add distro {1}.".format(url, udistro_name))

    @cobbler_object_exist("distro")
    @authorization
    def update_distro(self, distro_name, *args, **kwargs):
        """update the distro, typical fields are comment, owners.
        :param string distro_name: the name of a distro
        :param dict kwargs: a sub dict of {"comment": "string", "owners":"string",}
        :returns: a dict defined in :py:func:`_simple_result_dict`
        """
        # fields that allow update, if a field is not state in common_args,
        # just ignore it
        common_args = "comment owners".split()
        cmd_args_edit = [
            "cobbler", "distro", "edit", "--name={0}".format(distro_name), ]
        # common distro parameters
        cmd_args = cmd_args_edit + self._merge_arg_list(common_args, kwargs)
        flag_result = True
        if len(cmd_args) > len(cmd_args_edit):
            flag_result = self.shell_command(cmd_args)
        return self._simple_result_dict(flag_result, "Update distro {0} {1}successfully.".format(distro_name, "" if flag_result else "un"))

    @cobbler_object_exist("profile", False)
    @authorization
    def add_profile(self, profile_name, *args, **kwargs):
        """Add a new profile
        :param string profile_name: the profile name that user specified
        :param dict kwargs: a sub dict of {"distro": "name", "kickstart":"filename","comment":"string", "owners":"string",}
        :returns: a dict defined in :py:func:`_simple_result_dict`
        """
        # check the validation of distro
        distro_name = kwargs.get("distro", None)
        if distro_name and distro_name in self._list_item_names("distro"):
            # check the validation of kickstart file
            kickstart_file = kwargs.get("kickstart", None)
            if kickstart_file:
                if not self.file_exist(kickstart_file):
                    return self._simple_result_dict(False, "Must provide a valid kickstart file.")
            cmd_args = ["cobbler", "profile", "add",
                        "--name={0}".format(profile_name),
                        "--distro={0}".format(distro_name),
                        ]
            flag_result = self.shell_command(cmd_args)
            if flag_result:
                kwargs.pop("distro")
                flag_result = self._edit_profile(profile_name, kwargs)
            return self._simple_result_dict(flag_result, "Add profile {0} {1}successfully.".format(profile_name, "" if flag_result else "un"))
        return self._simple_result_dict(False, "Must provide a valid distro name.")

    @cobbler_object_exist("profile")
    @authorization
    def update_profile(self, profile_name, *args, **kwargs):
        """update a profile
        :param string profile_name: the profile name that user specified
        :param dict kwargs: a sub dict of {"distro": "name", "kickstart":"filename","comment":"string", "owners":"string",}
        :returns: a dict defined in :py:func:`_simple_result_dict`
        """
        # check the validation of distro
        distro_name = kwargs.get("distro", None)
        if distro_name:
            if distro_name not in self._list_item_names("distro"):
                return self._simple_result_dict(False, "Must provide a valid distro name.")
        # check the validation of kickstart file
        kickstart_file = kwargs.get("kickstart", None)
        if kickstart_file:
            if not self.file_exist(kickstart_file):
                return self._simple_result_dict(False, "Must provide a valid kickstart file.")

        flag_result = self._edit_profile(profile_name, kwargs)
        return self._simple_result_dict(flag_result, "Update profile {0} {1}successfully.".format(profile_name, "" if flag_result else "un"))

    def _edit_profile(self, profile_name, contents):
        """edit a profile, a inner function called by add_profile and update_profile
        :return: True means edit profile success, othewise failed.
        """
        # fields that allow update, if a field is not state in common_args,
        # just ignore it
        common_args = "distro kickstart comment owners".split()
        cmd_args_edit = [
            "cobbler", "profile", "edit", "--name={0}".format(profile_name), ]
        # common profile parameters
        cmd_args = cmd_args_edit + self._merge_arg_list(common_args, contents)
        flag_result = True
        if len(cmd_args) > len(cmd_args_edit):
            flag_result = self.shell_command(cmd_args)
        return flag_result

    @cobbler_object_exist("system", False)
    @authorization
    def add_system(self, system_name, **kwargs):
        """Add a system
          add system to cobbler with 2 steps.
          1. add a new system ONLY with system name and profile name.
          2. add other contents of system.
          param interfaces is a list, each of which is a dict that
          has the following format.

          ::

            {
                name: system name,
                profile: profile name,
                gateway: default gateway,
                hostname: host name of system,
                kopts: kernel command-line arguments,
                ksmeta: kickstart meta data,
                name-servers: name servers,
                comment: user comment,
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
        contents = kwargs
        # profile must be provided to add a system
        flag_result = False
        profile_name = None
        if "profile" in contents:
            profile_name = contents["profile"]
            if profile_name in self._list_item_names("profile"):
                flag_result = True
        if not flag_result:
            return self._simple_result_dict(False, "Profile [{0}] does NOT exist.".format(profile_name) if profile_name else "Must provide a profile to add system.")
        cmd_args = ["cobbler", "system", "add",
                    "--name={0}".format(system_name),
                    "--profile={0}".format(profile_name),
                    ]
        flag_result = self.shell_command(cmd_args)
        say_info("Create system {0}, step 1 {1}".format(
            system_name, "success" if flag_result else "failed"))
        if flag_result:
            contents.pop("profile")
            flag_result = self._edit_system(system_name, contents)
        # add others of system failed, MUST remove the added new system
        # completely
        if not flag_result:
            self._remove_item("system", system_name)
        return self._simple_result_dict(flag_result, "Add system {0} {1}successfully.".format(system_name, "" if flag_result else "un"))

    @cobbler_object_exist("system")
    @authorization
    def update_system(self, system_name, **kwargs):
        """Update a system.
        update system with 2 steps. The first step is checking the validation of profile if needed.
        The second step is to update the attributes in system.
        :param string system_name: the system name that user specified
        :param dict kwargs: a sub dict of system dict
        """
        contents = kwargs
        profile_name = contents.get("profile", None)
        if profile_name:
            if profile_name not in self._list_item_names("profile"):
                return self._simple_result_dict(False, "Failed to update system, because profile [{0}] does NOT exist.".format(profile_name))
        # update other objects in system
        flag_result = self._edit_system(system_name, contents)
        return self._simple_result_dict(flag_result, "Update system {0} {1}successfully.".format(system_name, "" if flag_result else "un"))

    def _edit_system(self, system_name, contents):
        """
          edit system of system_name with contents
        """
        system_args = "profile gateway hostname kopts ksmeta name-servers name-servers-search owners comment".split()
        power_args = "power-type power-address power-user power-pass power-id".split()
        interface_args = "ip-address mac-address netmask static management".split()
        cmd_args_edit = [
            "cobbler", "system", "edit", "--name={0}".format(system_name), ]
        # common system parameters
        cmd_args = cmd_args_edit + self._merge_arg_list(system_args, contents)
        # power parameters
        if "power" in contents.keys():
            cmd_args += self._merge_arg_list(power_args, contents["power"])
        all_interface_args = []
        if "interfaces" in contents:
            for interface in contents["interfaces"]:
                temp_if_args = ["--interface={0}".format(interface["name"])]
                temp_if_args += self._merge_arg_list(interface_args, interface)
                all_interface_args += [temp_if_args]
        flag_result = True
        if len(all_interface_args) > 0:
            flag_result = self.shell_command(cmd_args + all_interface_args[0])
        elif len(cmd_args) > len(cmd_args_edit):
            flag_result = self.shell_command(cmd_args)
        say_info("_edit system {0}, step 1 {1}".format(
            system_name, "success" if flag_result else "failed"))
        if flag_result:
            for interface in all_interface_args[1:]:
                flag_result = self.shell_command(cmd_args_edit + interface)
                say_info("_edit system {0}, step 2, interfaces {1}".format(
                    system_name, "success" if flag_result else "failed"))
                if not flag_result:
                    break
        return flag_result

    @authorization
    def update_kickstart(self, kickstart_name, lines, **kwargs):
        """update kickstart file with list of lines.
        :param string kickstart_name: filename of kickstart file
        :param list lines: contents of a kickstart file, each line of the file is a elment in list
        """
        # update profile firstly
        with open("{0}/{1}".format(self.KICKSTART_LOCATION, kickstart_name), "w") as f:
            f.write("\n".join(lines))
        return self._simple_result_dict(True, "Update kickstart {0} successfully.".format(kickstart_name))

    @authorization
    def remove_distro(self, distro_name, **kwargs):
        """remove a distro
        """
        return self._remove_item("distro", distro_name)

    @authorization
    def remove_profile(self, profile_name, **kwargs):
        """remove a profile
        """
        return self._remove_item("profile", profile_name)

    @authorization
    def remove_system(self, system_name, **kwargs):
        """remove a system
        """
        return self._remove_item("system", system_name)

    @authorization
    def remove_kickstart(self, kickstart_name, **kwargs):
        """remove a kickstart file
        """
        filename = "{0}/{1}".format(self.KICKSTART_LOCATION, kickstart_name)
        if self.file_exist(filename):
            flag_result = True
            try:
                os.remove(filename)
            except:
                flag_result = False
            return self._simple_result_dict(flag_result, "The object {0} in kickstart removed {1}successfully.".format(kickstart_name, "" if flag_result else "un"))
        return self._simple_result_dict(True, "The name {0} in kickstart does NOT exist. Not need to remove.".format(kickstart_name))

    def _remove_item(self, object_type, name):
        """remove a cobbler object
        """
        cmd_args = [
            "cobbler", object_type, "remove", "--name={0}".format(name)]
        if name in self._list_item_names(object_type):
            flag_result = self.shell_command(cmd_args)
            return self._simple_result_dict(flag_result, "The object {0} in {1} removed {2}successfully.".format(name, object_type, "" if flag_result else "un"))
        return self._simple_result_dict(True, "The name {0} in {1} does NOT exist. Not need to remove.".format(name, object_type))

    @cobbler_object_exist("system")
    @authorization
    def remove_system_interface(self, system_name, *args, **kwargs):
        """remove one interface from a system named system_name.
        If param args contains one interface name, then this interface will be removed from system.
        """
        report = self._get_item_report("system", system_name)
        all_interfaces = [x for x in report[0]["data"]["interfaces"]]
        user_delete_interfaces = list(args) if len(args) > 0 else []
        if len(user_delete_interfaces) == 0:
            return self._simple_result_dict(False, "To remove an interface, you MUST give the name of the interface.")
        result = {}
        for interface_name in user_delete_interfaces:
            if interface_name in all_interfaces:
                cmd_args = ["cobbler", "system", "edit",
                            "--name={0}".format(system_name),
                            "--interface={0}".format(interface_name),
                            "--delete-interface",
                            ]
                flag_result = self.shell_command(cmd_args)
                result = self._simple_result_dict(flag_result,
                                                  "Interface {0} removed {1}succefully.".format(interface_name, "" if flag_result else "un"))
            else:
                result = self._simple_result_dict(
                    True, "Interface {0} does NOT exist. Not need to remove.".format(interface_name))
            break   # ONLY remove the first interface name
        return result

    # find system in cobbler
    def _wrap_cobbler_find_system(self, q, name):
        cobbler_handler = capi.BootAPI()
        func = getattr(cobbler_handler, "find_system")
        system = func(name)
        q.put(system.to_datastruct())

    # power system
    def _wrap_cobbler_power_system(self, q, name, flag_netboot, power_status):
        """wrap cobbler power action
        """
        options = {
            "on": "power_on",
            "off": "power_off",
            "reboot": "reboot",
        }
        cobbler_handler = capi.BootAPI()
        func = getattr(cobbler_handler, "find_system")
        system = func(name)
        system.netboot_enabled = flag_netboot
        cobbler_handler.add_system(system)
        # default action is power_on
        power_action = options.get(power_status.lower(), "power_on")
        func = getattr(cobbler_handler, power_action)
        try:
            func(system)
        except:
            power_action = "failed"
        q.put(power_action)

    def cobbler_find_system(self, system_name):
        return self._call_cobbler_process("_wrap_cobbler_find_system", system_name)

    def cobbler_power_system(self, name, flag_netboot, power_status):
        return self._call_cobbler_process("_wrap_cobbler_power_system", name, flag_netboot, power_status)

    @cobbler_object_exist("system")
    @authorization
    def deploy_system(self, system_name, **kwargs):
        """deploy a system.
        """
        result = self.cobbler_power_system(system_name, True, "reboot")
        if result == "failed":
            return self._simple_result_dict(False, "Deploy failed, contact your admin.")
        return self._simple_result_dict(True, "Start to deploy system ...")

    @cobbler_object_exist("system")
    def power_system(self, system_name, **kwargs):
        """power on/off a system.
        """
        # get the value of 'power_on' set by user, default value is True or
        # power ON
        power_status = "on" if kwargs.get("power_on", True) else "off"
        result = self.cobbler_power_system(system_name, False, power_status)
        if result == "failed":
            return self._simple_result_dict(False, "Power failed, contact your admin.")
        return self._simple_result_dict(True, "Start to power {0} system ...".format(power_status))

    @authorization
    def monitor_system(self, system_name, **kwargs):
        """monitor server's status with Ping. True means the server is on, False means down.
        """
        system = self.cobbler_find_system(system_name)
        """
        interfaces = system["interfaces"]
        manage_ip = interfaces[interfaces.keys()[0]]["ip_address"]
        for if_name in interfaces:
            if interfaces[if_name]["management"]:
                manage_ip = interfaces[if_name]["ip_address"]
                break
        """
        manage_ip = self.get_system_manage_ip(system)
        # print "manage ip is: ", manage_ip
        cmd_args = ['ping', '-c', '1', '-W', '3', manage_ip]
        result = self.shell_command(cmd_args)
        # print "result is: ", result
        return self._simple_result_dict(result, "Ping {0} {1}successfully.".format(system_name, "" if result else "un"))

    def get_system_manage_ip(self, csystem, exclude_loop=True):
        """get IP address of the management interface,
        Currently, choose the management interface by the name that the lower name is management
        FIXME, TODO, Maybe we can add a field in mongodb later
        """
        dict_interfaces = csystem["interfaces"]
        list_ip = [(name, dict_interfaces[name]["ip_address"])
                   for name in dict_interfaces]
        if exclude_loop:
            list_ip = [(name, address)
                       for (name, address) in list_ip if not address.startswith("127")]
        # sort with name ascending
        sorted_list_ip = sorted(list_ip, key=lambda ipp: ipp[0])
        return sorted_list_ip[0][1]

    def _simple_result_dict(self, result, msg="", data=None):
        return {"result": result, "description": msg, "data": data, }

    def _merge_arg_list(self, arg_list, content_dict):
        result = []
        curr_arg_list = [arg for arg in arg_list if arg in content_dict.keys()]
        for arg in curr_arg_list:
            if content_dict[arg]:
                result += ["--{0}={1}".format(arg, content_dict[arg])]
        return result

    def iso_exist(self, url, dir_iso):
        arr = url.split("/")
        filename = "{0}/{1}".format(dir_iso, arr[-1])
        return (self.file_exist(filename), filename)

    def read_file_to_list(self, name):
        with open(name) as f:
            lines = [line.rstrip("\n") for line in f]
        return lines

    def list_dir_filenames(self, dir_name, flag_include_link=False):
        home_dir, sub_dirs, files = os.walk(dir_name).next()
        return files if flag_include_link else [f for f in files if not os.path.islink(os.path.join(home_dir, f))]

    def file_exist(self, filename):
        return os.path.isfile(filename)

    def mkdir(self, sdir):
        args = ["mkdir", "-p", sdir]
        return self.shell_command(args)

    def mount_image(self, image_name, location):
        args = ["mount", "-o", "loop", image_name, location]
        return self.shell_command(args)

    def umount_image(self, location):
        args = ["umount", "-f", location]
        return self.shell_command(args)

    def wget(self, url, location):
        supported_protocols = ["http", "ftp", "https", ]
        supported_image = ["iso", ]
        protocol = url.split(":")[0]
        filename = url.split("/")[-1]
        filename_ext = filename.split(".")[-1]
        if protocol in supported_protocols and filename_ext in supported_image:
            args = [
                "wget", "-q", "-O", "{0}/{1}".format(location, filename), url, ]
            if self.shell_command(args):
                result = (True, "{0}/{1}".format(location, filename))
            else:
                result = (False, "Fail to download file [{0}]".format(url))
        else:
            result = (False, "Not supported protocol [{0}] or image [{1}].".format(
                protocol, filename_ext))
        return result

    def shell_command(self, args):
        # print "==Command> ", " ".join(args)
        say_debug("shell command: {0}".format(" ".join(args)))
        DEVNULL = open(os.devnull, "wb")
        return 0 == subprocess.call(args, stderr=DEVNULL, stdout=DEVNULL)

# TEST TEST TEST
if __name__ == "__main__":
    debug_status = {
        "list_names": True,
        "report_distro": False,
        "report_profile": True,
        "report_system": False,
        "add_distro": False,
        "add_profile": True,
        "update_profile": True,
        "add_system": False,
        "update_system": False,
        "remove_system_interface": False,
        "remove_system": False,
        "remove_profile": False,
        "remove_distro": False,
    }
    my_sys = {
        "name": "mysys140313",
        "profile": "test-profile-140313",
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
    my_sys_update = {
        "name": "mysys140313",
        "interfaces": [
            {
                "name": "ee3",
                "ip-address": "192.168.1.234",
                "mac-address": "aa:bb:dd:dd:ee:ff",
                "static": True,
                "management": False,
                "netmask": "255.255.255.0",
            },
        ],
    }
    cp = CobblerProvision()
    user_token = cp.get_token("username", "password")
    kwargs = {"user_token": user_token}

    # list objects
    if debug_status["list_names"]:
        distro_names = cp.list_distro_names(**kwargs)
        print("distros names: ", distro_names["data"])
        profile_names = cp.list_profile_names(**kwargs)
        print("profiles names: ", profile_names["data"])
        system_names = cp.list_system_names(**kwargs)
        print("systems names: ", system_names["data"])
    # get object reports
    if debug_status["report_distro"]:
        # distro
        distro_name = "*x86_64"
        reports = cp.get_distro_report(distro_name)
        distros = reports["data"] if reports["result"] else []
        if len(distros) > 0:
            for distro in distros:
                print("{0} {1} {0}".format("=" * 10, distro["name"]))
                print("distro report: {0}".format(distro))
        else:
            print("Cannot find distro with name {0}".format(distro_name))
    if debug_status["report_system"]:
        # system
        system_name = "gra*"
        reports = cp.get_system_report(system_name)
        systems = reports["data"] if reports["result"] else []
        if len(systems) > 0:
            for system in systems:
                print("{0} {1} {0}".format("=" * 10, system["name"]))
                print("system report: {0}".format(system))
        else:
            print("Cannot find system with name {0}".format(system_name))

    distro_name = "test-distro-140313"
    profile_name = my_sys["profile"]
    system_name = my_sys["name"]
    # clean the test
    # cp.remove_system(system_name)
    # cp.remove_profile(profile_name)
    # cp.remove_distro(distro_name)

    # following is a clean test  ...

    # add distro
    if debug_status["add_distro"]:
        #url = "http://ftp.ussg.iu.edu/linux/ubuntu-releases/13.04/ubuntu-13.04-server-amd64.iso"
        # CentOS
        url = "http://mirrors.usc.edu/pub/linux/distributions/centos/6.5/isos/x86_64/CentOS-6.5-x86_64-bin-DVD1.iso"
        result = cp.add_distro(distro_name, url)
        print("add_distro result is: ", result)
    # add profile
    if debug_status["add_profile"]:
        distro_name = "test-x86_64"
        kickstart_file = "/var/lib/cobbler/kickstarts/ktanaka.ks"
        result = cp.add_profile(profile_name, distro_name, kickstart_file)
        print("add profile, result is: ", result)
    # report profile
    if debug_status["report_profile"]:
        reports = cp.get_profile_report(profile_name)
        profiles = reports["data"] if reports["result"] else []
        if len(profiles) > 0:
            for profile in profiles:
                print("{0} {1} {0}".format("=" * 10, profile["name"]))
                print("profile report: {0}".format(profile))
        else:
            print("Cannot find profile with name {0}".format(profile_name))
    # update profile
    if debug_status["update_profile"]:
        kickstart_file = "/var/lib/cobbler/kickstarts/sample.ks"
        result = cp.update_profile(profile_name, kickstart_file)
        print("update profile, result is: ", result)
    # report profile
    if debug_status["report_profile"]:
        reports = cp.get_profile_report(profile_name)
        profiles = reports["data"] if reports["result"] else []
        if len(profiles) > 0:
            for profile in profiles:
                print("{0} {1} {0}".format("=" * 10, profile["name"]))
                print("profile report: {0}".format(profile))
        else:
            print("Cannot find profile with name {0}".format(profile_name))
    # add system
    if debug_status["add_system"]:
        result = cp.add_system(my_sys["name"], my_sys)
        print("add system, result is: ", result)
    # update system
    if debug_status["update_system"]:
        result = cp.update_system(my_sys_update["name"], my_sys_update)
        print("update system, result is: ", result)
    # remove a interface
    if debug_status["remove_system_interface"]:
        system_name = my_sys_update["name"]
        interface_name = my_sys_update["interfaces"][0]["name"]
        result = cp.remove_system_interface(system_name, interface_name)
        print("remove system interface, result is: ", result)
    # remove system
    if debug_status["remove_system"]:
        system_name = my_sys["name"]
        result = cp.remove_system(system_name)
        print("remove system, result is: ", result)
    # remove profile
    if debug_status["remove_profile"]:
        result = cp.remove_profile(profile_name)
        print("remove profile, result is: ", result)
    # remove distro
    if debug_status["remove_distro"]:
        result = cp.remove_distro(distro_name)
        print("remove distro, result is: ", result)
