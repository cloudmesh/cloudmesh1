#! /usr/bin/env python
"""
::

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
# from __future__ import dict
from __future__ import print_function
from docopt import docopt
from cloudmesh_base.hostlist import Parameter
from datetime import datetime, timedelta
from pytimeparse.timeparse import timeparse
# from timestring import Range
# from timestring import Date
# from cloudmesh.util.util import parse_time_interval


def not_implemented():
    print("ERROR: not yet implemented")


def yn_choice(message, default='y'):
    """http://stackoverflow.com/questions/3041986/python-command-line-yes-no-input"""
    choices = 'Y/n' if default.lower() in ('y', 'yes') else 'y/N'
    choice = raw_input("%s (%s) " % (message, choices))
    values = ('y', 'yes', '') if default == 'y' else ('y', 'yes')
    return True if choice.strip().lower() in values else False


def parse_time_interval(time_start, time_end):
    t_end = time_end
    t_start = time_start

    if t_start is not None:
        if t_start in ["current_time", "now"]:
            t_start = str(datetime.now())

    if t_end is not None:
        if t_end.startswith("+"):
            duration = t_end[1:]
            delta = timeparse(duration)
            t_start = datetime.strptime(t_start, "%Y-%m-%d %H:%M:%S.%f")
            t_end = t_start + timedelta(seconds=delta)

    return (str(t_start), str(t_end))


def rain_command(arguments):

    for list in ["HOSTS", "USERS", "PROJECTS", "--project", "--user"]:
        try:
            expanded_list = Parameter.expand(arguments[list])
            arguments[list] = expanded_list
        except:
            pass

    print(arguments)

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

        elif arguments["on"]:
            """rain admin on HOSTS"""

            print("switch on")
            print((arguments["HOSTS"]))
            not_implemented()

        elif arguments["off"]:
            """rain admin off HOSTS"""

            print("switch off")
            print((arguments["HOSTS"]))
            not_implemented()

        elif arguments["delete"] or arguments["rm"]:
            """rain admin [-i] delete HOSTS"""
            """rain admin [-i] rm HOSTS"""

            interactive = arguments["-i"]

            print("delete", interactive)

            for host in arguments["HOSTS"]:
                if interactive:
                    keep = yn_choice(
                        "Do you want to delete the host %s?" % host)
                    if keep:
                        print("delete %s" % host)
                    else:
                        print("keeping %s" % host)
            not_implemented()

        elif arguments["list"]:

            if arguments["users"]:
                print("list users")
                not_implemented()

            elif arguments["projects"]:
                print("list projects")
                not_implemented()

            elif arguments["roles"]:
                print("list roles")
                not_implemented()

            elif arguments["hosts"]:
                print("list hosts")
                not_implemented()

                (time_start, time_end) = parse_time_interval(arguments["--start"],
                                                             arguments["--end"])
                print("From:", time_start)
                print("To  :", time_end)

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
            print("policy")

            (time_start, time_end) = parse_time_interval(arguments["--start"],
                                                         arguments["--end"])

            print("From:", time_start)
            print("To  :", time_end)

            if ["--users"] is not None:
                not_implemented()
            elif arguments["--projects"] is not None:
                not_implemented()
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
        not_implemented()

    elif arguments["list"]:
        print("user list")

        (time_start, time_end) = parse_time_interval(arguments["--start"],
                                                     arguments["--end"])

        print("From:", time_start)
        print("To  :", time_end)

        not_implemented()


if __name__ == '__main__':
    arguments = docopt(__doc__)

    rain_command(arguments)
