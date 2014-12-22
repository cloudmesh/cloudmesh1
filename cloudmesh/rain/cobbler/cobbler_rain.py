#! /usr/bin/env python
# from __future__ import dict
from __future__ import print_function

from docopt import docopt
import hostlist
from datetime import datetime, timedelta
from pytimeparse.timeparse import timeparse
from cloudmesh.provisioner.rain_cobbler_wrapper import RainCobblerWrapper
# from timestring import Range
# from timestring import Date
from datetime import datetime, timedelta
import sys
from cloudmesh_common.tables import parse_time_interval
from cloudmesh_common.util import not_implemented


def print_policys(policys, flag_merge=True):
    if not policys:
        print("Cannot find policy")
        return
    if flag_merge:
        for user in policys:
            print("{0}\t{1}".format(user, policys[user]))
    else:
        for puser in policys:
            policy = [(p["_id"], p["policy"]) for p in policys[puser]]
            print("{0}\t{1}".format(puser, policy))


def print_progress(label, hosts, data):
    print("Status of host --{0}-- ({1}): ".format(label, len(hosts)))
    if len(hosts) == 0:
        print("\tEmpty records.")
    else:
        if label in ["failed", "unknown"]:
            print("\thost list: ", hostlist.collect_hostlist(hosts))
        else:
            for host in hosts:
                print("\t{0}\t{1}%".format(host, data[host]["progress"]))


def filtered_hosts_based_baremetal(raw_hosts):
    """filtered hosts based on baremetal computers
    """
    # wrapper
    wrapper = RainCobblerWrapper()
    input_hosts = hostlist.expand_hostlist(raw_hosts)
    bm_hosts = wrapper.baremetal_computer_host_list()
    return [h for h in input_hosts if h in bm_hosts] if bm_hosts else []


def filtered_hosts_based_policy(user, projects, hosts):
    """filtered hosts based on policy of the user and his/her projects
    """
    # wrapper
    wrapper = RainCobblerWrapper()
    policy = wrapper.get_policy_based_user_or_its_projects(user, projects)
    policy_hosts = hostlist.expand_hostlist(policy) if policy else None
    return [h for h in hosts if h in policy_hosts] if policy_hosts else []


def filtered_access_hosts(raw_hosts):
    """filter hosts that user can access
    :return: a dict with the formation {"access": [], "unaccess": []}
    """
    valid_bm_hosts = filtered_hosts_based_baremetal(raw_hosts)
    user = "XXX"  # FIXME, try to get username
    projects = ["XXX"]  # FIXME, try to get projcts that user belongs to
    #policy_hosts = filtered_hosts_based_policy(user, projects, valid_bm_hosts)
    # ONLY for test, MUST be replaced by the above line
    policy_hosts = valid_bm_hosts
    all_hosts = hostlist.expand_hostlist(raw_hosts)
    unaccess_hosts = [h for h in all_hosts if h not in policy_hosts]
    return {"access": policy_hosts, "unaccess": unaccess_hosts, }


def rain_command(arguments):
    """
    ::

      Usage:
          rain -h | --help
          rain --version
          rain admin add [LABEL] --file=FILE
          rain admin baremetals
          rain admin on HOSTS
          rain admin off HOSTS
          rain admin [-i] delete HOSTS
          rain admin [-i] rm HOSTS
          rain admin list users [--merge]
          rain admin list projects [--merge]
          rain admin list roles
          rain admin list hosts [--user=USERS|--project=PROJECTS|--role=ROLE]
                                [--start=TIME_START]
                                [--end=TIME_END]
                                [--format=FORMAT]
          rain admin policy [--user=USERS|--project=PROJECTS|--role=ROLE]
                            (-l HOSTS|-n COUNT)
                            [--start=TIME_START]
                            [--end=TIME_END]
          rain user list [--project=PROJECTS] [HOSTS]
          rain user list hosts [--start=TIME_START]
                          [--end=TIME_END]
                          [--format=FORMAT]
          rain status [--short|--summary][--kind=KIND] [HOSTS]
          rain provision --profile=PROFILE HOSTS
          rain provision list [--type=TYPE] (--distro=DISTRO|--kickstart=KICKSTART)
          rain provision --distro=DITRO --kickstart=KICKSTART HOSTS
          rain provision add (--distro=URL|--kickstart=KICk_CONTENT) NAME
          rain provision power [--off] HOSTS
          rain provision monitor HOSTS

      Arguments:
          HOSTS     the list of hosts passed
          LABEL     the label of a host
          COUNT     the count of the bare metal provisioned hosts
          KIND      the kind
          TYPE      the type of profile or server

      Options:
          -n COUNT     count of teh bare metal hosts to be provisined
          -p PROJECTS  --projects=PROJECTS
          -u USERS     --user=USERS        Specify users
          -f FILE, --file=FILE  file to be specified
          -i           interactive mode adds a yes/no
                       question for each host specified
          --role=ROLE            Specify predefined role
          --start=TIME_START     Start time of the reservation, in
                                 YYYY/MM/DD HH:MM:SS format. [default: current_time]
          --end=TIME_END         End time of the reservation, in
                                 YYYY/MM/DD HH:MM:SS format. In addition a duration
                                 can be specified if the + sign is the first sign.
                                 The duration will than be added to
                                 the start time. [default: +1d]
          --kind=KIND            Format of the output -png, jpg, pdf. [default:png]
          --format=FORMAT        Format of the output json, cfg. [default:json]
          --type=TYPE            Format of the output profile, server. [default:server]


    """

    # comment by H. C, we need the raw list for policy
    """
    for list in ["HOSTS", "USERS", "PROJECTS","--project", "--user"]:
        try:
            expanded_list = hostlist.expand_hostlist(arguments[list])
            arguments[list]=expanded_list
        except:
            pass
    """
    # print(arguments)
    # wrapper
    wrapper = RainCobblerWrapper()

    """
    rain admin on HOSTS
    rain admin off HOSTS
    """
    if arguments["admin"]:

        if arguments["add"]:
            print("add")

            if arguments["LABEL"] is not None:
                """admin add LABEL --file=FILE"""

                print((arguments["LABEL"]))
                print((arguments["--file"]))
                not_implemented()

            else:
                """admin add --file=FILE"""

                print((arguments["--file"]))
                not_implemented()

        elif arguments["baremetals"]:
            """rain admin baremetals"""

            print("list all baremetals")
            result = wrapper.baremetal_computer_host_list()
            print(result if result else "No Baremetals")

        elif arguments["on"]:
            """rain admin on HOSTS"""

            print("switch on")
            print((arguments["HOSTS"]))
            result = wrapper.baremetal_computer_host_on(arguments["HOSTS"])
            print("success" if result else "failed")

        elif arguments["off"]:
            """rain admin off HOSTS"""

            print("switch off")
            print((arguments["HOSTS"]))
            result = wrapper.baremetal_computer_host_off(arguments["HOSTS"])
            print("success" if result else "failed")

        elif arguments["delete"] or arguments["rm"]:
            """rain admin [-i] delete HOSTS"""
            """rain admin [-i] rm HOSTS"""

            interactive = arguments["-i"]

            print("delete", interactive)

            for host in arguments["HOSTS"]:
                if interactive:
                    answer = raw_input(
                        "Do you want to delete the host %s? (y)es/(n)o: " % host)
                    if answer in ["yes", "y", "Y", "YES"]:
                        print("delete %s" % host)
                    else:
                        print("keeping %s" % host)
            not_implemented()

        elif arguments["list"]:

            if arguments["users"]:
                print("list users")
                flag_merge = arguments["--merge"]
                policys = wrapper.list_all_user_group_hosts(True, flag_merge)
                print_policys(policys, flag_merge)

            elif arguments["projects"]:
                print("list projects")
                flag_merge = arguments["--merge"]
                policys = wrapper.list_all_user_group_hosts(False, flag_merge)
                print_policys(policys, flag_merge)

            elif arguments["roles"]:
                print("list roles")
                not_implemented()

            elif arguments["hosts"]:
                print("list hosts")
                # comment by H. C
                """
                not_implemented()

                (time_start, time_end) = parse_time_interval(arguments["--start"],
                                                           arguments["--end"])
                print "From:", time_start
                print "To  :", time_end
                """
                if arguments["--user"] is not None:
                    policys = wrapper.list_user_hosts(arguments["--user"])
                    print_policys(policys)
                elif arguments["--project"] is not None:
                    policys = wrapper.list_project_hosts(
                        arguments["--project"])
                    print_policys(policys)
                elif arguments["--role"] is not None:
                    not_implemented()
                else:
                    print ("all users, projects, roles")
                    not_implemented()

        elif arguments["policy"]:
            print("policy")
            # comment by H. C
            """
            (time_start, time_end) = parse_time_interval(arguments["--start"],
                                                         arguments["--end"])

            print "From:", time_start
            print "To  :", time_end
            """
            if arguments["--user"] is not None:
                policy_id = wrapper.add_user_policy(
                    arguments["--user"], arguments["HOSTS"])
                print("success" if policy_id else "failed")
            elif arguments["--project"] is not None:
                policy_id = wrapper.add_project_policy(
                    arguments["--project"], arguments["HOSTS"])
                print("success" if policy_id else "failed")
            elif arguments["--role"] is not None:
                not_implemented()
            else:
                print ("all users, projects, roles")
                not_implemented()

        elif arguments["list"]:
            print("list")

            not_implemented()

    elif arguments["status"]:
        print("status")
        if arguments["--short"]:
            status_dict = wrapper.get_status_short(arguments["HOSTS"])
            if status_dict:
                for host in sorted(status_dict.keys()):
                    print("{0:16}\t{1}".format(host, status_dict[host]))
            else:
                print("Empty")
        if arguments["--summary"]:
            status_dict = wrapper.get_status_summary(arguments["HOSTS"])
            if status_dict:
                for deploy_status in ["deployed", "deploying", "failed", "total", ]:
                    print("{0:16}\t{1}".format(deploy_status, status_dict[deploy_status]))

    elif arguments["user"]:
        if arguments["list"]:
            print("user list")

            (time_start, time_end) = parse_time_interval(arguments["--start"],
                                                         arguments["--end"])

            print("From:", time_start)
            print("To  :", time_end)

            not_implemented()
    ###
    # provisioning
    ###
    elif arguments["provision"]:
        # print "provision a node..."
        if arguments["list"]:
            # print "this will list distro or kickstart info"
            if arguments["--type"] == "profile":
                print("this will list profiles based on distro or kickstart info")
                profiles = wrapper.list_profile_based_distro_kickstart(
                    arguments["--distro"], arguments["--kickstart"])
                print("matched profiles: {0}".format(profiles))
            else:
                print("this will list servers based on distro or kickstart info")
                servers = wrapper.list_system_based_distro_kickstart(
                    arguments["--distro"], arguments["--kickstart"])
                print("matched servers: {0}".format(servers))
        elif arguments["add"]:
            print("add a new distro or kickstart")
            not_implemented()
        elif arguments["power"]:
            print("power ON/OFF a host...")
            # pre-process hosts which user can access
            if arguments["HOSTS"]:
                all_hosts = filtered_access_hosts(arguments["HOSTS"])
                access_hosts = all_hosts["access"]
                unaccess_hosts = all_hosts["unaccess"]
            if unaccess_hosts:
                print("You can NOT access these hosts: {0}, please contact your admin.".format(hostlist.collect_hostlist(unaccess_hosts)))
            result = wrapper.power_host(access_hosts, not arguments["--off"])
            power_hosts = [h for h in sorted(result.keys()) if result[h]]
            unknown_hosts = [h for h in sorted(result.keys()) if not result[h]]
            if unknown_hosts:
                print("unknow hosts, must deploy first: ", hostlist.collect_hostlist(hostlist.collect_hostlist(unknown_hosts)))
            if power_hosts:
                print("call [rain provision monitor {0}] to monitor power progress.".format(hostlist.collect_hostlist(power_hosts)))
        elif arguments["monitor"]:
            print("monitor progress of a host...")
            # pre-process hosts which user can access
            if arguments["HOSTS"]:
                all_hosts = filtered_access_hosts(arguments["HOSTS"])
                access_hosts = all_hosts["access"]
                unaccess_hosts = all_hosts["unaccess"]
            if unaccess_hosts:
                print("You can NOT access these hosts: {0}, please contact your admin.".format(hostlist.collect_hostlist(unaccess_hosts)))
            result = wrapper.monitor_host(access_hosts)
            poweron_hosts = [
                h for h in sorted(result.keys()) if result[h]["status"] == "poweron"]
            poweroff_hosts = [
                h for h in sorted(result.keys()) if result[h]["status"] == "poweroff"]
            deploy_hosts = [
                h for h in sorted(result.keys()) if result[h]["status"] == "deploy"]
            failed_hosts = [
                h for h in sorted(result.keys()) if result[h]["status"] == "failed"]
            unknown_hosts = [
                h for h in sorted(result.keys()) if result[h]["status"] == "unknown"]
            print_progress("deploy", deploy_hosts, result)
            print_progress("poweron", poweron_hosts, result)
            print_progress("poweroff", poweroff_hosts, result)
            print_progress("failed", failed_hosts, result)
            print_progress("unknown", unknown_hosts, result)
        else:
            # pre-process hosts which user can access
            if arguments["HOSTS"]:
                all_hosts = filtered_access_hosts(arguments["HOSTS"])
                access_hosts = all_hosts["access"]
                unaccess_hosts = all_hosts["unaccess"]
            if unaccess_hosts:
                print("You can NOT access these hosts: {0}, please contact your admin.".format(hostlist.collect_hostlist(unaccess_hosts)))
            if arguments["--profile"]:
                if access_hosts:
                    wrapper.provision_host_with_profile(
                        arguments["--profile"], access_hosts)
                    print("call [rain provision monitor {0}] to monitor depoy progress.".format(hostlist.collect_hostlist(access_hosts)))
            elif arguments["--distro"] and arguments["--kickstart"]:
                if access_hosts:
                    wrapper.provision_host_with_distro_kickstart(
                        arguments["--distro"], arguments["--kickstart"], access_hosts)
                    print("call [rain provision monitor {0}] to monitor deploy progress.".format(hostlist.collect_hostlist(access_hosts)))


def main():
    arguments = docopt(rain_command.__doc__)
    rain_command(arguments)

if __name__ == '__main__':
    main()

    """
    timeparse('1.2 minutes')32m

2h32m
3d2h32m
1w3d2h32m
1w 3d 2h 32m
1 w 3 d 2 h 32 m
4:13
4:13:02
4:13:02.266
2:04:13:02.266
2 days,  4:13:02 (uptime format)
2 days,  4:13:02.266
5hr34m56s
5 hours, 34 minutes, 56 seconds
5 hrs, 34 mins, 56 secs
2 days, 5 hours, 34 minutes, 56 seconds
1.2 m
1.2 min
1.2 mins
1.2 minute
1.2 minutes
172 hours
172 hr
172 h
172 hrs
172 hour
1.24 days
5 d
5 day
5 days
5.6 wk
5.6 week
5.6 weeks
"""
