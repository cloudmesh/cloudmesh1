"""Common methods and classes used at the intall time."""
import sys
from cloudmesh_install.util import path_expand


__config_dir_prefix__ = "~/.cloudmesh"

__config_dir__ = path_expand(__config_dir_prefix__)


def config_file(filename):
    return __config_dir__ + filename


def config_file_raw(filename):
    return __config_dir_prefix__ + filename


def config_file_prefix():
    return __config_dir_prefix__
