"""Cloudmesh install util functions.

This file contains basic utility functions that must not need any
import from cloudmesh OR any other non-standard python
modules. Everything in this file must execute on a clean python 2.7.x
environment.

"""
import platform

from string import Template
import os
import sys

def get_system():
    if is_ubuntu():
        return "ubuntu"
    elif is_centos():
        return "centos"
    elif is_osx():
        return"osx"
    else:
        return "unsupported"


def is_ubuntu():
    """test sif the platform is ubuntu"""
    (dist, version, release) = platform.dist()
    if dist == "ubuntu" and version not in ["14.04"]:
        print("ERROR: %s %s is not tested" % (dist, version))
    return dist == 'Ubuntu'


def is_centos():
    """test if the platform is centos"""
    (dist, version, release) = platform.dist()
    if dist == "centos" and version not in ["6.5"]:
        print("WARNING: %s %s is not tested" % (dist, version))
    return dist == "centos"


def is_osx():
    osx = platform.system().lower() == 'darwin'
    if osx:
        os_version = platform.mac_ver()[0]
        if os_version not in ['10.9.5', '10.10']:

            osx = False
            print("WARNING: %s %s is not tested" % ('OSX', os_version))
    return osx


def banner(txt=None, c="#", debug=True):
    """prints a banner of the form with a frame of # arround the txt::

      ############################
      # txt
      ############################

    .

    :param txt: a text message to be printed
    :type txt: string
    :param c: thecharacter used instead of c
    :type c: character
    """
    if debug:
        print
        print "#", 70 * c
        if txt is not None:
            print "#", txt
            print "#", 70 * c


def path_expand(text):
    """ returns a string with expanded variable.

    :param text: the path to be expanded, which can include ~ and $ variables
    :param text: string

    """
    template = Template(text)
    result = template.substitute(os.environ)
    result = os.path.expanduser(result)
    return result


def yn_choice(message, default='y', tries=None):
    """asks for a yes/no question.
    :param message: the message containing the question
    :param default: the default answer
    """
    # http://stackoverflow.com/questions/3041986/python-command-line-yes-no-input"""
    choices = 'Y/n' if default.lower() in ('y', 'yes') else 'y/N'
    if tries == None:
        choice = raw_input("%s (%s) " % (message, choices))
        values = ('y', 'yes', '') if default == 'y' else ('y', 'yes')
        return True if choice.strip().lower() in values else False
    else:
        while tries > 0:
            choice = raw_input("%s (%s) (%s)" %
                               (message, choices, "'q' to discard"))
            choice = choice.strip().lower()
            if choice in ['y', 'yes']:
                return True
            elif choice in ['n', 'no', 'q']:
                return False
            else:
                print "Invalid input..."
                tries = tries - 1


def grep(pattern, filename):
    """Very simple grep that returns the first matching line in a file.

    String matching only, does not do REs as currently implemented.
    """
    try:
        return (L for L in open(filename) if L.find(pattern) >= 0).next()
    except StopIteration:
        return ''
