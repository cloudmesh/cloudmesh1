#!/usr/bin/env python

"""Example of program with many options using docopt.
::

  Usage:
    cobbler_client.py list --object=OBJECT_TYPE [--format=FORMAT]
    cobbler_client.py list --object=OBJECT_TYPE
    cobbler_client.py get --object=OBJECT_TYPE --name=ITEM_NAME
    cobbler_client.py add --object=OBJECT_TYPE --data=DATA_FILE
    cobbler_client.py child --object=OBJECT_TYPE --name=ITEM_NAME
    cobbler_client.py profile --ks=ITEM_NAME
    cobbler_client.py update --object=OBJECT_TYPE --data=DATA_FILE
    cobbler_client.py remove --object=OBJECT_TYPE --name=ITEM_NAME
    cobbler_client.py remove interface --system=SYSTEM_NAME --name=ITEM_NAME
    cobbler_client.py deploy --name=SYSTEM_NAME [options]
    cobbler_client.py power --name=SYSTEM_NAME [options]
    cobbler_client.py test [options]

  Arguments:
    PATH  destination path

  Options:
    -h --help            show this help message and exit
    --version            show version and exit
    -v --verbose         print status messages
    -q --quiet           report only file names
    -f --force           force remove the object and its sub-objects
    -o --off             power off the system
    --object=OBJECT_TYPE    specifies the object type: distro, profile, system, kickstart
    --name=ITEM_NAME        specifies the item's name
    --data=DATA_FILE      specifies the filename containing the data
    --system=SYSTEM_NAME   specifies the name of system from which some interfaces will be deleted
    --onoff=ONOFF    specifies the power status, on or off
    --format=FORMAT   the format of the table is either json, html, list,
                      or ascii [default: ascii]
  Description:

    describe here what the commands do

    cobbler_client.py list object_type

      list names in object type ...

    cobbler_client.py get object_type item_name

      get the detail report of item_name in object_type

    cobbler_client.py add object_type data_file
    cobbler_client.py update object_type data_file

      add the data object in data_file belongs to object_type to cobbler.
        examples:
          profile: data_file
          { "name": "test-profile-140318",
            "distro": "test-x86_64",
            "kickstart": "ktanaka.ks"
          }

          system: data_file
          { "name": "test-sys-140318",
            "profile": "test-profile-140318",
            "power": {
                       "power-address": "1.2.3.4",
                       "power-user": "test",
                       "power-pass": "nopassword",
                       "power-type": "ipmilan",
                       "power-id": 1
                      },
            "interfaces": [
                            {
                              "name": "ee1",
                              "ip-address": "192.168.1.23",
                              "mac-address": "aa:bb:cc:dd:ee:ff",
                              "static": true,
                              "management": true,
                              "netmask": "255.255.255.0"
                             },
                             {
                               "name": "ee2",
                               "ip-address": "192.168.1.123",
                               "mac-address": "aa:bb:cc:ee:dd:ff",
                               "static": true,
                               "management": false,
                               "netmask": "255.255.255.0"
                              }
                            ]
             }
    cobbler_client.py remove object_type item_name

        remove an item_name in object_type

    cobbler_client.py remove interface system_name item_name

        remove the interface item_name form system system_name
"""
from __future__ import print_function

from prettytable import PrettyTable
from cloudmesh_common.tables import table_printer
from docopt import docopt
from multiprocessing.pool import ThreadPool
from datetime import datetime
import requests
import pprint
import json
import time
import sys


class CobblerClient:

    def __init__(self, server, argdict):
        self.server_url = "http://{0}:5000".format(server)
        self.arg_dict = argdict
        self.pp = pprint.PrettyPrinter(indent=4)

    def run(self):
        if self.arg_dict["list"]:
            self.list_object(self.arg_dict["--object"])
        elif self.arg_dict["get"]:
            self.get_object(self.arg_dict["--object"], self.arg_dict["--name"])
        elif self.arg_dict["add"]:
            self.add_object(self.arg_dict["--object"], self.arg_dict["--data"])
        elif self.arg_dict["child"]:
            self.get_child(self.arg_dict["--object"], self.arg_dict["--name"])
        elif self.arg_dict["profile"]:
            self.get_ks_profile(self.arg_dict["--ks"])
        elif self.arg_dict["update"]:
            self.update_object(
                self.arg_dict["--object"], self.arg_dict["--data"])
        elif self.arg_dict["remove"]:
            if not self.arg_dict["interface"]:
                self.remove_object(
                    self.arg_dict["--object"], self.arg_dict["--name"])
            else:
                self.remove_interface(
                    self.arg_dict["--system"], self.arg_dict["--name"])
        elif self.arg_dict["deploy"]:
            self.deploy_system(
                self.arg_dict["--name"], self.arg_dict["--verbose"])
        elif self.arg_dict["power"]:
            self.power_system(
                self.arg_dict["--name"], self.arg_dict["--off"], self.arg_dict["--verbose"])
        elif self.arg_dict["test"]:
            print("test is: {0}, force is: {1}, verbose is: {2}".format(self.arg_dict["test"], self.arg_dict["--force"], self.arg_dict["--verbose"]))

    def render_result(self, slabel, data):
        if data["result"]:
            if self.arg_dict["--format"] in ["json"]:
                self.pp.pprint(data)
            elif self.arg_dict["--format"] in ["list"]:
                self.pp.pprint(data["data"])
            elif self.arg_dict["--format"] in ["html"]:
                print(table_printer(data["data"]))
            elif self.arg_dict["--format"] in ["ascii"]:
                x = PrettyTable()
                x.add_column(slabel, data["data"])
                x.align = "l"
            print(x)
            """
            datas = data["data"]
            print "[Succeed] {0}{1}.".format(slabel, ", description is: {0}".format(data["description"]) if data["description"] else "")
            print "    There is {0} records satisfy query, data is: ".format(len(datas) if datas else 0)
            if datas:
                count = 0
                data_type = type(datas[0])
                for single_data in datas:
                    count += 1
                    print "-" * 40
                    if data_type is unicode or data_type is str:
                        print "  Record [{0}]: {1}".format(count, single_data)
                    elif data_type is dict:
                        print "  Record [{0}]: name is {1}".format(count, single_data["name"])
                        self.pp.pprint(single_data)
                    else:
                        self.pp.pprint(single_data)
            """
        else:
            print("[Failed] {0}, description is: {1}.".format(slabel, data["description"]))

    def read_dict(self, filename):
        s = ""
        with open(filename) as f:
            for line in f:
                sline = line.strip()
                if sline:
                    s += sline + " "
        try:
            data = json.loads(s)
        except:
            data = None
        return data

    def read_kickstart_data(self, filename):
        with open(filename) as f:
            lines = [line.rstrip("\n") for line in f]
        return {
            "name": lines[0][5:],
            "contents": lines[1:],
        }

    def list_object(self, object_type):
        surl = "/cm/v1/cobbler/{0}s".format(object_type)
        result_dict = self.request_rest_api("get", surl)
        self.render_result("{0} {1}".format("list", object_type), result_dict)

    def get_object(self, object_type, name):
        surl = "/cm/v1/cobbler/{0}s/{1}".format(object_type, name)
        result_dict = self.request_rest_api("get", surl)
        self.render_result(
            "{0} {1} {2}".format("get", object_type, name), result_dict)

    def add_object(self, object_type, data):
        data_dict = self.read_dict(
            data) if object_type != "kickstart" else self.read_kickstart_data(data)
        if data_dict is None:
            print("Error. File {0} is NOT a valid json formation data file.".format(data))
            return 1
        name = data_dict["name"]
        surl = "/cm/v1/cobbler/{0}s/{1}".format(object_type, name)
        result_dict = self.request_rest_api("post", surl, data_dict)
        self.render_result("{0} {1} {2} with data file {3}".format(
            "add", object_type, name, data), result_dict)

    def get_child(self, object_type, name):
        surl = "/cm/v1/cobbler/{0}s/{1}/child".format(object_type, name)
        result_dict = self.request_rest_api("get", surl)
        self.render_result(
            "{0} {1} {2}".format("child", object_type, name), result_dict)

    def get_ks_profile(self, name):
        surl = "/cm/v1/cobbler/kickstarts/{0}/profile".format(name)
        result_dict = self.request_rest_api("get", surl)
        self.render_result("{0} {1} ".format("profile", name), result_dict)

    def update_object(self, object_type, data):
        data_dict = self.read_dict(
            data) if object_type != "kickstart" else self.read_kickstart_data(data)
        if data_dict is None:
            print("Error. File {0} is NOT a valid json formation data file.".format(data))
            return 1
        name = data_dict["name"]
        surl = "/cm/v1/cobbler/{0}s/{1}".format(object_type, name)
        result_dict = self.request_rest_api("put", surl, data_dict)
        self.render_result("{0} {1} {2} with data file {3}".format(
            "update", object_type, name, data), result_dict)

    def remove_object(self, object_type, name):
        surl = "/cm/v1/cobbler/{0}s/{1}".format(object_type, name)
        result_dict = self.request_rest_api("delete", surl)
        self.render_result(
            "{0} {1} {2}".format("remove", object_type, name), result_dict)

    def remove_interface(self, system_name, if_name):
        surl = "/cm/v1/cobbler/systems/{0}/{1}".format(system_name, if_name)
        result_dict = self.request_rest_api("delete", surl)
        self.render_result(
            "{0} {1} {2}".format("remove interface", system_name, if_name), result_dict)

    def deploy_system(self, name, flag_monitor):
        print("  Send command [deploy] to {0}, please wait ...".format(name))
        surl = "/cm/v1/cobbler/baremetal/{0}".format(name)
        result_dict = self.request_rest_api("post", surl)
        self.render_result("{0} {1}".format("deploy", name), result_dict)
        if flag_monitor:
            self.monitor_deploy(name)

    def power_system(self, name, flag_off, flag_monitor):
        print("  Send command [power {1}] to {0}, please wait ...".format(name, "off" if flag_off else "on"))
        surl = "/cm/v1/cobbler/baremetal/{0}".format(name)
        data = {"power_on": not flag_off}
        result_dict = self.request_rest_api("put", surl, data)
        self.render_result(
            "{0} {1} {2}".format("power", name, "off" if flag_off else "on"), result_dict)
        if flag_monitor:
            self.monitor_power(name, not flag_off)

    def get_server_status(self, name):
        surl = "/cm/v1/cobbler/baremetal/{0}".format(name)
        result_dict = self.request_rest_api("get", surl)
        return result_dict["result"]

    def set_server_status(self, status):
        self.server_status = status
        self.server_status_ok = True

    def print_symbol(self, status, count):
        sym = "+" if status else "."
        str_sym = sym + " "
        if count % 10 == 0:
            str_sym += "\n"
        sys.stdout.write(str_sym)
        sys.stdout.flush()

    def async_get_server_status(self, name, dest_status, total_count, interval=5):
        pool = ThreadPool(processes=1)
        count = total_count
        while True:
            self.server_status_ok = False
            # tuple of args for get_server_status
            pool.apply_async(
                self.get_server_status, (name), callback=self.set_server_status)
            while not self.server_status_ok:
                time.sleep(interval)
                self.print_symbol(not dest_status, count)
                count += 1
            if self.server_status == dest_status:
                break
        return count

    def sync_get_server_status(self, name, dest_status, total_count, interval=6, flag_sleep_first=False):
        count = total_count
        min_interval = 1
        interval = min_interval if interval < min_interval else interval
        # usually, it is enabled between the status switch phase
        if flag_sleep_first:
            time.sleep(interval)
        while True:
            start_time = datetime.now()
            result = self.get_server_status(name)
            # print "start time is: {0}, result is: {1}".format(start_time,
            # result)
            self.print_symbol(result, count)
            count += 1
            if result == dest_status:
                break
            diff_time = datetime.now() - start_time
            once_sleep = interval - diff_time.total_seconds()
            curr_delay = min_interval if min_interval > once_sleep else once_sleep
            # print "current delay is: ", curr_delay
            time.sleep(curr_delay)
        return count

    def waiting_server(self, name, arr_status):
        count = 1
        for status in arr_status:
            count = self.sync_get_server_status(
                name, status, count, 12, True if count > 1 else False)

    def monitor_deploy(self, name):
        server_status_pattern = [False, True, False]
        self.waiting_server(name, server_status_pattern)
        print("\nServer {0} deployed successfully.".format(name))

    def monitor_power(self, name, flag_on):
        server_status_pattern = [True if flag_on else False]
        self.waiting_server(name, server_status_pattern)
        print("\nServer {0} power {1} successfully.".format(name, "on" if flag_on else "off"))

    def get_data(self, req_json):
        return req_json["cmrest"]["data"]

    def request_rest_api(self, method, url, data=None):
        """
          method = [get, post, put, delete]
        """
        headers = {"content-type": "application/json",
                   "accept": "application/json", }
        req_api = getattr(requests, method)
        req_url = self.server_url + url
        if method == "get":
            r = req_api(req_url)
        else:
            if data:
                data["user_token"] = ""
            else:
                data = {"user_token": ""}
            r = req_api(req_url, data=json.dumps(
                data), headers=headers) if data else req_api(req_url)
        return self.get_data(r.json())


if __name__ == '__main__':
    arguments = docopt(__doc__, version='1.0')
    with open("server.cfg") as f:
        while True:
            data = f.readline()
            if (data.strip()):
                server = data.strip()
                break
    cclient = CobblerClient(server, arguments)
    cclient.run()
