#! /usr/bin/env python
"""
Usage:
    rain -h | --help
    rain --version
    rain admin add [LABEL] --file=FILE
    rain admin on HOSTS
    rain admin off HOSTS
    rain admin [-i] delete HOSTS
    rain admin [-i] rm HOSTS
    rain admin list users
    rain admin list projects
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
    --role=ROLE                Specify predefined role
    --start=TIME_START        Start time of the reservation, in 
                           YYYY/MM/DD HH:MM:SS format. [default: current_time]
    --end=TIME_END              End time of the reservation, in 
                           YYYY/MM/DD HH:MM:SS format. [default: +1d]
    --kind=KIND           Format of the output -png, jpg, pdf. [default:png]
    --format=FORMAT  the format. [default:json]


"""
from docopt import docopt
import hostlist
from datetime import datetime

def not_implemented():
    print "ERROR: not yet implemented"

def rain_command(arguments):

    for list in ["HOSTS", "USERS", "PROJECTS","--project", "--user"]:
        try:
            expanded_list = hostlist.expand_hostlist(arguments[list])
            arguments[list]=expanded_list
        except:
            pass
        
    print(arguments)

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


        elif arguments["on"]:
            """rain admin on HOSTS"""
            
            print "switch on"
            print (arguments["HOSTS"])
            not_implemented()
            
        elif arguments["off"]:
            """rain admin off HOSTS"""

            print "switch off"
            print (arguments["HOSTS"])
            not_implemented()
            
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
                not_implemented()

            elif arguments["projects"]:
                print "list projects"
                not_implemented()

            elif arguments["roles"]:
                print "list roles"
                not_implemented()

            elif arguments["hosts"]:
                print "list hosts"
                not_implemented()
                
                if arguments["--start"] is not None:
                    if arguments["--start"] in ["current_time","now"]:
                        arguments["--start"] = str(datetime.now())
                    print "start %s" % arguments["--start"]

                if arguments["--end"] is not None:
                    t_end = arguments["--end"]
                    if t_end.startswith("+"):
                        print "duration: %s" % t_end
                    
                if ["--users"] is not None:
                    not_implemented()
                elif arguments["--projects"] is not None:
                    not_implemented()
                elif arguments["--role"] is not None:
                    not_implemented()
                else:
                    print ("all users, projects, roles")
                    not_implemented()

                                        
        elif arguments["policy"]:
            print "policy"
            not_implemented()

        elif arguments["list"]:
            print "admin list"
            not_implemented()
            
    elif arguments["status"]:
            print "status"
            not_implemented()
            
    elif arguments["list"]:
            print "user list"
            not_implemented()


if __name__ == '__main__':
    arguments = docopt(__doc__)

    rain_command(arguments)
    
    """

        --duration=DURATION   format. [default: +1d]




"""
