#! /usr/bin/env python
"""
Usage:
    cm-install -h | --help
    cm-install --version
    cm-install create OS
    cm-install list
    cm-install veewee

Arguments:
    OS     The operating system. [default: ubuntu]

Options:

Description:

  start the install shell with

     cm-install

   cm-install> vagrant create ubuntu

       creates an ubuntu 14.04 image with veewee and includes it in the base box list

    cm-install> vagrant list

        lists the base boxes in vagrant

"""
from docopt import docopt
import os
from cloudmesh_base.Shell import Shell

def not_implemented():
    print "ERROR: not yet implemented"


def get_boxes(kind):
    lines = Shell.vagrant("box", "list")

    boxes = []
    for line in lines:
        (OS, KIND) = line.split("(")
        OS = OS.strip()
        (KIND, rest) = KIND.split(")")
        if kind == KIND:
            boxes.append(OS)
    return boxes


def list_boxes():
    # print vagrant("box","list")
    print get_boxes("virtualbox")


def exec_script(name):
    if name is "veewee":
        os.system("./bin/install-veewee.sh")
    elif name is "ubuntu64":
        os.system("./bin/install-ubuntu64.sh")


def cm_install_command(arguments):

    print arguments

    if arguments["create"]:
        print "cm-install create"
        operating_system = arguments['OS']
        boxes = get_boxes("virtualbox")
        if operating_system not in boxes:
            print "The OS '%s' was not found in vagrant" % (operating_system)
            exec_script('./bin/install-ubuntu64.sh')
        else:
            print "The OS '%s' was found in vagrant" % (operating_system)
            exec_script('ubuntu64')

    elif arguments["veewee"]:
        exec_script('veewee')

    elif arguments["list"]:
        # cm-install vagrant list
        print "list"
        list_boxes()

if __name__ == '__main__':
    arguments = docopt(__doc__)

    cm_install_command(arguments)
