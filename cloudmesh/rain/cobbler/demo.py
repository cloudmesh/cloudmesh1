#!/usr/bin/python
from __future__ import print_function

import cobbler.api as capi
import subprocess
import sys
import time


def deploy_server(server_name):
    handle = capi.BootAPI()
    msystem = handle.find_system(name=server_name)
    # msystem = handle.systems().find(name=server_name)
    # print "system {0} status: netboot_enabled {1}".format(msystem.name, msystem.netboot_enabled)
    # print "*"*50
    # pprint(msystem.to_datastruct())
    # enable Netboot
    if not msystem.netboot_enabled:
        msystem.netboot_enabled = True
        # save modified system
        handle.add_system(msystem)
    server_ip = get_interface_ip(msystem)
    print("Depoly new OS on server {0}, please wait ...".format(server_name))
    print("  the status of server {0} is monitored on IP : {1}".format(server_name, server_ip))
    handle.reboot(msystem)
    if is_server_deployed(server_ip):
        print("\nDeploy server {0} successfully, now you can power on it.".format(server_name))
    else:
        print("\nDeploy server {0} failed, please contact your administrator.".format(server_name))


def get_interface_ip(csystem, exclude_loop=True):
    dict_interfaces = csystem.interfaces
    list_ip = [(name, dict_interfaces[name]["ip_address"])
               for name in dict_interfaces]
    if exclude_loop:
        list_ip = [(name, address)
                   for (name, address) in list_ip if not address.startswith("127")]
    # sort with name ascending
    sorted_list_ip = sorted(list_ip, key=lambda ipp: ipp[0])
    return sorted_list_ip[0][1]


def poweron_server(server_name):
    handle = capi.BootAPI()
    msystem = handle.find_system(name=server_name)
    # msystem = handle.systems().find(name=server_name)
    # print "system {0} status: netboot_enabled {1}".format(msystem.name, msystem.netboot_enabled)
    # print "*"*50
    # pprint(msystem.to_datastruct())
    # disable Netboot
    if msystem.netboot_enabled:
        msystem.netboot_enabled = False
        # save modified system
        handle.add_system(msystem)
    # msystem = handle.find_system(name=server_name)
    # print "system {0} status: netboot_enabled {1}".format(msystem.name,
    # msystem.netboot_enabled)
    server_ip = get_interface_ip(msystem)
    if is_server_on(server_ip, 1):
        print("INFO: server {0} is already ON.".format(server_name))
    else:
        print("Power on server {0}, please wait ...".format(server_name))
        print("  the status of server {0} is monitored on IP : {1}".format(server_name, server_ip))
        handle.power_on(msystem)
        if is_server_on(server_ip):
            print("\nCongradulation, server {0} is now ON.".format(server_name))
            print("    Login to {0} with command ssh root@{1}".format(server_name, server_ip))
        else:
            print("\nError. Server {0} cannot power on, please contact your administrator.".format(server_name))


def print_waiting_symbol(total, sym=".", line_count=10):
    str_sym = sym + " "
    if total % line_count == 0:
        str_sym += "\n"
        if total / line_count % 5 == 0:
            str_sym += "\n"
    sys.stdout.write(str_sym)
    sys.stdout.flush()
    return total + 1


def ping_server(ip_address):
    return subprocess.call(['ping', '-c', '1', '-W', '3', ip_address], stderr=subprocess.STDOUT, stdout=subprocess.PIPE)


def is_server_deployed(server_ip, prewait_num=100, max_num=1200, interval=6):
    count = 1
    # wait till power off
    while (count < prewait_num):
        count = print_waiting_symbol(count, "o")
        time.sleep(interval)
        ret_code = ping_server(server_ip)
        if ret_code != 0:
            break
    # wait till power on
    while (count < max_num):
        count = print_waiting_symbol(count)
        time.sleep(interval)
        ret_code = ping_server(server_ip)
        if ret_code == 0:
            break
    # wait till power off
    while (count < max_num):
        count = print_waiting_symbol(count, "+")
        ret_code = ping_server(server_ip)
        if ret_code != 0:
            break
        time.sleep(interval)
    return True if count < max_num else False


def is_server_on(server_ip, max_num=300, interval=6):
    ret_code = ping_server(server_ip)
    if ret_code == 0:
        return True
    if max_num <= 1:
        return False

    count = 1
    while (ret_code != 0):
        count = print_waiting_symbol(count)
        time.sleep(interval)
        ret_code = ping_server(server_ip)

    return True if ret_code == 0 else False


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("\n  Usage: sudo ./demo deploy|power hostname\n")
        sys.exit(1)
    # print sys.argv
    action = sys.argv[1]
    if action not in ["deploy", "power"]:
        print("\n  Usage: sudo ./demo deploy|power hostname\n")
        sys.exit(1)
    server_name = sys.argv[2]
    print("Demo how to {0} server {1} ...".format(action, server_name))
    if sys.argv[1] == "power":
        poweron_server(server_name)
    elif sys.argv[1] == "deploy":
        deploy_server(server_name)
    elif sys.argv[1] == "ping":
        ret_code = ping_server("192.168.131.2",)
        print("ret code is ", ret_code)
    else:
        print("Usage sudo ./deploy deploy|power")
    print("test git")
