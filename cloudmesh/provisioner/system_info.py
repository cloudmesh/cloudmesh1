from fabric.api import *
from fabric.context_managers import settings


@task
def memory_usage():
    run('free -m')


def main():
    hosts = 'localhost,india.futuregrid.org'
    with settings(host_string=hosts):
        memory_usage()

if __name__ == '__main__':
    memory_usage()

'''
class SystemInfo:


    def __init__(self):
        pass

    def get(self, ips, refresh=True):
        """gets the system info from the host with the given ips.
        if the info is not there it is loaded from the machine.
        the result is a dict with attribute tuples. the first element in the tuple is the valu, the second is a unit.
        if no unit is avalable or needed None is used as unit."""
        pass

    def _get(self,ip):
        """gets the systme information from the machine with the given ip"""
        pass
'''
