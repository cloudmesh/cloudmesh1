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
        if os_version not in ['10.9.5', '10.10', '10.10.1', '10.10.2']:
            osx = False
            print("WARNING: %s %s is not tested" % ('OSX', os_version))
    return osx


