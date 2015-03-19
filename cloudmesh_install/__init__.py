<<<<<<< HEAD
=======
"""Common methods and classes used at the intall time."""
import sys
from cloudmesh_base.util import path_expand


__config_dir_prefix__ = "~/.cloudmesh"

__config_dir__ = path_expand(__config_dir_prefix__)


def config_file(filename):
    return __config_dir__ + filename


def config_file_raw(filename):
    return __config_dir_prefix__ + filename


def config_file_prefix():
    return __config_dir_prefix__
>>>>>>> 064ba72f1b3aa55be61ad705ca2a066e2731232e
