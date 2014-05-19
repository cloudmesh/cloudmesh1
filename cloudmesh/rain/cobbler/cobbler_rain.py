#! /usr/bin/env python
#from __future__ import dict
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
    if flag_merge:
        for user in policys:
            print "{0}\t{1}".format(user, policys[user])
    else:
        for puser in policys:
            policy = [(p["_id"], p["policy"]) for p in policys[puser]]
            print "{0}\t{1}".format(puser, policy)

def print_progress(label, hosts, data):
    print "Status of host --{0}-- ({1}): ".format(label, len(hosts))
    if len(hosts) == 0:
        print "\tEmpty records."
    else:
        if label in ["failed", "unknown"]:
            print "host list: ", hostlist.collect_hostlist(hosts)
        else:
            for host in hosts:
                print "\t{0}\t{1}%".format(host, data[host]["progress"])

def rain_command(arguments):
    """
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
        rain list [--project=PROJECTS] [HOSTS]    
        rain list hosts [--start=TIME_START]
                        [--end=TIME_END]
                        [--format=FORMAT]
        rain status [--short|--summary][--kind=KIND] [HOSTS]
        rain provision --profile=PROFILE HOSTS
        rain provision list (--distro=DISTRO|--kickstart=KICKSTART)
        rain provision --distro=DITRO --kickstart=KICKSTART HOSTS
        rain provision add (--distro=URL|--kickstart=KICk_CONTENT) NAME
        rain provision power [--off] HOSTS
        rain provision monitor HOSTS

    Arguments:
        HOSTS     the list of hosts passed
        LABEL     the label of a host
        COUNT     the count of the bare metal provisioned hosts
        KIND      the kind

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
    #print(arguments)
    wrapper = RainCobblerWrapper()

    """
    rain admin on HOSTS
    rain admin off HOSTS
    """
    if arguments["admin"]:
        
        if arguments["add"]:
            print "add"

            if arguments["LABEL"] is not None:
                """admin add LABEL --file=FILE"""
                
                print(arguments["LABEL"])
                print(arguments["--file"])
                not_implemented()
                
            else:
                """admin add --file=FILE"""

                print(arguments["--file"])
                not_implemented()


        elif arguments["baremetals"]:
            """rain admin baremetals"""
            
            print "list all baremetals"
            result = wrapper.baremetal_computer_host_list()
            print result
            
        elif arguments["on"]:
            """rain admin on HOSTS"""
            
            print "switch on"
            print (arguments["HOSTS"])
            result = wrapper.baremetal_computer_host_on(arguments["HOSTS"])
            print "success" if result else "failed"
            
        elif arguments["off"]:
            """rain admin off HOSTS"""

            print "switch off"
            print (arguments["HOSTS"])
            result = wrapper.baremetal_computer_host_off(arguments["HOSTS"])
            print "success" if result else "failed"
            
        elif arguments["delete"] or arguments["rm"] :
            """rain admin [-i] delete HOSTS"""
            """rain admin [-i] rm HOSTS"""            

            interactive = arguments["-i"]
            
            print "delete", interactive

            for host in arguments["HOSTS"]:
                if interactive:
                    answer = raw_input("Do you want to delete the host %s? (y)es/(n)o: " % host)
                    if answer in ["yes","y","Y", "YES"]:
                        print "delete %s" % host
                    else:
                        print "keeping %s" % host
            not_implemented()

        elif arguments["list"]:

            if arguments["users"]:
                print "list users"
                flag_merge = arguments["--merge"]
                policys = wrapper.list_all_user_group_hosts(True, flag_merge)
                print_policys(policys, flag_merge)
                

            elif arguments["projects"]:
                print "list projects"
                flag_merge = arguments["--merge"]
                policys = wrapper.list_all_user_group_hosts(False, flag_merge)
                print_policys(policys, flag_merge)

            elif arguments["roles"]:
                print "list roles"
                not_implemented()

            elif arguments["hosts"]:
                print "list hosts"
                # comment by H. C
                """
                not_implemented()

                (time_start, time_end) = parse_time_interval(arguments["--start"],
                                                           arguments["--end"])
                print "From:", time_start
                print "To  :", time_end
                """
                if arguments["--users"] is not None:
                    policys = wrapper.list_user_hosts(arguments["--users"])
                    print_policys(policys)
                elif arguments["--projects"] is not None:
                    policys = wrapper.list_project_hosts(arguments["--projects"])
                    print_policys(policys)
                elif arguments["--role"] is not None:
                    not_implemented()
                else:
                    print ("all users, projects, roles")
                    not_implemented()

                                        
        elif arguments["policy"]:
            print "policy"
            # comment by H. C
            """
            (time_start, time_end) = parse_time_interval(arguments["--start"],
                                                         arguments["--end"])

            print "From:", time_start
            print "To  :", time_end
            """
            if arguments["--users"] is not None:
                policy_id = wrapper.add_user_policy(arguments["--users"], arguments["HOSTS"])
                print "success" if policy_id else "failed"
            elif arguments["--projects"] is not None:
                policy_id = wrapper.add_project_policy(arguments["--projects"], arguments["HOSTS"])
                print "success" if policy_id else "failed"
            elif arguments["--role"] is not None:
                not_implemented()
            else:
                print ("all users, projects, roles")
                not_implemented()

        elif arguments["list"]:
            print "list"

            not_implemented()
            
    elif arguments["status"]:
            print "status"
            if arguments["--short"]:
                status_dict = wrapper.get_status_short(arguments[HOSTS])
                if status_dict:
                    for host in sorted(status_dict.keys()):
                        print "{0}\t{1}".format(host, status_dict[host])
                else:
                    print "Empty"
            if arguments["--summary"]:
                status_dict = wrapper.get_status_short(arguments[HOSTS])
                if status_dict:
                    for deploy_status in ["deployed", "deploying", "failed", "total", ]:
                        print "{0}\t{1}".format(deploy_status, status_dict[deploy_status])
                
    elif arguments["list"]:
            print "user list"

            (time_start, time_end) = parse_time_interval(arguments["--start"],
                                                         arguments["--end"])

            print "From:", time_start
            print "To  :", time_end

            not_implemented()
    ###
    # provisioning
    ###
    elif arguments["provision"]:
        print "provision a node..."
        if arguments["list"]:
            #print "this will list distro or kickstart info"
            print "this will servers based on distro or kickstart info"
            servers = wrapper.list_system_based_distro_kickstart(arguments["DISTRO"], arguments["KICKSTART"])
            print "matched servers: {0}".format(servers)
        elif arguments["add"]:
            print "add a new distro or kickstart"
            not_implemented()
        elif arguments["power"]:
            print "power ON/OFF a host..."
            result = wrapper.power_host(arguments["HOSTS"], not arguments["--off"])
            power_hosts = [h for h in sorted(result.keys()) if result[h]]
            unknown_hosts = [h for h in sorted(result.keys()) if not result[h]]
            print "power hosts: ", power_hosts
            print "unknow hosts, must deploy first: ", unknow_hosts
        elif arguments["monitor"]:
            print "monitor progress of a host..."
            result = wrapper.monitor_host(arguments["HOSTS"])
            poweron_hosts = [h for h in sorted(result.keys()) if result[h]["status"] == "poweron"]
            poweroff_hosts = [h for h in sorted(result.keys()) if result[h]["status"] == "poweroff"]
            deploy_hosts = [h for h in sorted(result.keys()) if result[h]["status"] == "deploy"]
            failed_hosts = [h for h in sorted(result.keys()) if result[h]["status"] == "failed"]
            unknown_hosts = [h for h in sorted(result.keys()) if result[h]["status"] == "unknown"]
            print_progress("deploy", deploy_hosts, result)
            print_progress("poweron", poweron_hosts, result)
            print_progress("poweroff", poweroff_hosts, result)
            print_progress("failed", failed_hosts, result)
            print_progress("unknown", unknown_hosts, result)
        else:
            if arguments["--profile"]:
                wrapper.provision_host_with_profile(arguments["PROFILE"], arguments["HOSTS"])
            elif arguments["--distro"] and arguments["--kickstart"]:
                wrapper.provision_host_with_distro_kickstart(arguments["DISTRO"], arguments["KICKSTART"], arguments["HOSTS"])

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

    
