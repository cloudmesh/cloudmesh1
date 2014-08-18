import platform
from cloudmesh_common.logger import LOGGER

log = LOGGER(__file__)


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
        log.error("ERROR: %s %s is not tested" % (dist, version))
    return dist == 'Ubuntu'


def is_centos():
    """test if the platform is centos"""
    (dist, version, release) = platform.dist()
    if dist == "centos" and version not in ["6.5"]:
        log.error("WARNING: %s %s is not tested" % (dist, version))
    return dist == "centos"


def is_osx():
    osx = platform.system().lower() == 'darwin'
    if osx:
        os_version = platform.mac_ver()[0]
        if os_version not in ['10.9.4']:
            osx = False
            log.error("WARNING: %s %s is not tested" % ('OSX', os_version))
    return osx
