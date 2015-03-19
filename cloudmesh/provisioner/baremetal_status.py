from __future__ import print_function
from dbhelper import DBHelper
from hostlist import expand_hostlist
from types import *
from copy import deepcopy
from cloudmesh_base.logger import LOGGER
#
# SETTING UP A LOGGER
#

log = LOGGER(__file__)


class BaremetalStatus:

    """Baremetal computer Status.
    """

    def __init__(self):
        """Init function of class BaremetalStatus
        """
        self.db_client = DBHelper()

    def get_default_query(self):
        return {"cm_kind": "baremetal", "cm_type": "status_inventory"}

    def get_full_query(self, query_elem):
        elem = self.get_default_query()
        if query_elem:
            elem.update(query_elem)
        return elem

    def init_deploy_status(self, host):
        """Init the deploy status of host
        :param string host: the host name of baremetal computer
        """
        return self.init_status(host, "deploy")

    def init_power_status(self, host, flag_on=True):
        """Init the Power ON/OFF status of the host
        :param string host: the host name of baremetal computer
        """
        return self.init_status(host, "on" if flag_on else "off")

    def init_status(self, host, action):
        """init the status of baremetal computer
        :param string action: one of values in ["on", "off", "deploy"]
        :return: True means init status successfully, otherwise failed.
        """
        query_elem = self.get_full_query({"cm_id": host})
        # status cycle for deploy, OFF --> ON --> OFF
        # status cycle for power on, ON
        # status cycle for power off, OFF
        update_elem = {"transient": {"action": "{0}...".format(action),  # deploy, on, off
                                     "status_1": "unknown",  # status phase 1
                                     "status_2": "unknown",  # status phase 2
                                     "status_3": "unknown",  # status phase 3
                                     },
                       }
        if action == "deploy":
            # unknown, deploying, deployed, failed
            update_elem["status"] = "unknown"
        result = self.db_client.atom_update(query_elem, {"$set": update_elem})
        return result["result"]

    def update_deploy_command_result(self, host, result):
        """update the deploy result
        :param string host: the unique name of host
        :param boolean result: True means deploy command success, False means failed
        :return: a flag, True means update mongodb success, otherwise failed.
        """
        query_elem = self.get_full_query({"cm_id": host})
        update_elem = {"status": "deploying" if result else "failed", }
        result = self.db_client.atom_update(query_elem, {"$set": update_elem})
        return result["result"]

    def update_power_status(self, host, status, flag_on):
        """update the status of power ON/OFF
        :param string host: the unique name of host
        :param string status: status of "ON" or "OFF"
        :param boolean flag_on: True means power on, False means power off
        :return: True means udpate successfully, otherwise failed
        """
        query_elem = self.get_full_query({"cm_id": host})
        hosts_status = self.get_status(host)
        result = False
        if hosts_status and hosts_status[0]["status"] == "deployed":
            host_status = hosts_status[0]
            trans_status = {}
            flag_update = False
            if flag_on and host_status["transient"]["action"] == "on...":
                result = True
                if status == "ON":
                    trans_status["transient.action"] = "on"
                    trans_status["transient.status_1"] = "ON"
                    flag_update = True
            elif not flag_on and host_status["transient"]["action"] == "off...":
                result = True
                if status == "OFF":
                    trans_status["transient.action"] = "off"
                    trans_status["transient.status_1"] = "OFF"
                    flag_update = True
            if flag_update:
                update_result = self.db_client.atom_update(
                    query_elem, {"$set": trans_status})
                result = update_result["result"]
        return result

    def update_deploy_status(self, host, status):
        """update the status of deploy based on the cycle OFF --> ON --> OFF
        :param string host: the unique name of host
        :param string status: status of "ON" or "OFF"
        :return: True means udpate successfully, otherwise failed
        """
        query_elem = self.get_full_query({"cm_id": host})
        hosts_status = self.get_status(host)
        result = False
        if hosts_status and hosts_status[0]["status"] == "deploying":
            host_status = hosts_status[0]
            if host_status["transient"]["action"] == "deploy...":
                result = True
                trans_status = {}
                flag_update = False
                # phase 1, unknown --> OFF
                if host_status["transient"]["status_1"] == "unknown":
                    if status == "OFF":
                        log.debug(
                            "host {0} deploy monitor, step 1 ".format(host))
                        trans_status["transient.status_1"] = "OFF"
                        flag_update = True
                elif host_status["transient"]["status_1"] == "OFF":
                    # phase 2, unknown --> ON
                    if host_status["transient"]["status_2"] == "unknown":
                        if status == "ON":
                            log.debug(
                                "host {0} deploy monitor, step 2 ".format(host))
                            trans_status["transient.status_2"] = "ON"
                            flag_update = True
                    elif host_status["transient"]["status_2"] == "ON":
                        # phase 3, unknown --> OFF
                        if host_status["transient"]["status_3"] == "unknown":
                            if status == "OFF":
                                log.debug(
                                    "host {0} deploy monitor, step 3 ".format(host))
                                trans_status["transient.status_3"] = "OFF"
                                trans_status["transient.action"] = "deploy"
                                trans_status["status"] = "deployed"
                                flag_update = True
                if flag_update:
                    update_result = self.db_client.atom_update(
                        query_elem, {"$set": trans_status})
                    result = update_result["result"]
        return result

    def get_deploy_progress(self, host, host_status=None):
        """get the progress of deploy of host baremetal computer.
        :param string host: the unique ID of host
        :param dict host_status: the status document of host in mongodb
        :return: an integer number. -1 means error. 10 means before phase 1, 25, 50, 100 means the end of phase 1, 2, 3.
        """
        result = -1
        if not host_status:
            status_list = self.get_status(host)
            if status_list:
                host_status = status_list[0]
        if host_status:
            if host_status["status"] == "deploying":
                if host_status["transient"]["status_1"] == "unknown":
                    result = 10
                elif host_status["transient"]["status_1"] == "OFF":
                    result = 25
                    if host_status["transient"]["status_2"] == "ON":
                        result = 50
            elif host_status["status"] == "deployed":
                result = 100
        return result

    def get_power_progress(self, host, flag_on, host_status=None):
        """get the progress of power ON/OFF of host baremetal computer.
        :param string host: the unique ID of host
        :param boolean flag_on: True means power ON, False means OFF
        :param dict host_status: the status document of host in mongodb
        :return: an integer number. -1 means error. 10 means before phase 1, 100 means phase 1.
        """
        result = -1
        if not host_status:
            status_list = self.get_status(host)
            if status_list:
                host_status = status_list[0]
        if host_status:
            if host_status["status"] == "deployed":
                if host_status["transient"]["status_1"] == "unknown":
                    result = 10
                elif host_status["transient"]["status_1"] == "ON" if flag_on else "OFF":
                    result = 100
        return result

    def get_host_progress(self, host):
        """get the progress of host baremetal computer.
        :param string host: the unique ID of host
        :return: a dict of {"status": "deploy", "progress": 25, }, there are 5 status of host, namely deploy, poweron, poweroff, failed, unknown
        """
        result = {"status": "unknown", "progress": -1, }
        status_list = self.get_status(host)
        if status_list:
            host_status = status_list[0]
            if host_status["status"] == "deployed":
                # maybe any status in deploy, poweron, poweroff
                action = host_status["transient"]["action"]
                if action.startswith("on"):
                    result["status"] = "poweron"
                    result["progress"] = self.get_power_progress(
                        host, True, host_status)
                elif action.startswith("off"):
                    result["status"] = "poweroff"
                    result["progress"] = self.get_power_progress(
                        host, False, host_status)
                elif action.startswith("deploy"):
                    result["status"] = "deploy"
                    result["progress"] = self.get_deploy_progress(
                        host, host_status)
            elif host_status["status"] == "deploying":
                result["status"] = "deploy"
                result["progress"] = self.get_deploy_progress(
                    host, host_status)
            elif host_status["status"] == "failed":
                result["status"] = "failed"
        return result

    def get_status(self, host=None):
        """get the status of single or all baremetal computer(s)
        :param string host: the unique ID of host, None means get status of all hosts
        :return: a list of dict with the following formation [{"cm_id": "cm_id", "status":"status", "transient":{"action": "action", "status_1":"status_1", "status_2":"status_2", "status_3":"status_3"}}]

        """
        query_elem = self.get_full_query({"cm_id": host} if host else {})
        result = self.db_client.find(query_elem)
        return result["data"] if result["result"] else None

    def get_status_short(self, hosts=None):
        """get the short status of baremetal for hosts
        :param list hosts: a list of host or None means all hosts
        :return: a dict with the formation {"host1":"deployed", "host2": "deploying", "host3": "failed", "host4": "unknown", }
        """
        status_list = self.get_status()
        valid_hosts_status = [status for status in status_list if status[
            "cm_id"] in hosts] if hosts is not None else status_list
        result = {}
        for host in valid_hosts_status:
            result[host["cm_id"]] = host["status"]
        return result

    def get_status_summary(self, hosts=None):
        """get the summary status of baremetal for hosts
        :param list hosts: a list of host or None means all hosts
        :return: a dict with the formation {"deployed": 1, "deploying":2, "failed":2, "total": 5}
        """
        status_list = self.get_status()
        valid_hosts_status = [status for status in status_list if status[
            "cm_id"] in hosts] if hosts is not None else status_list
        result = {"deployed": 0, "deploying": 0, "failed": 0, "total": 0}
        for host in valid_hosts_status:
            result["total"] += 1
            result[host["status"]] += 1
        return result

if __name__ == "__main__":
    bms = BaremetalStatus()
    result = bms.init_deploy_status("i072")
    result = bms.get_status("i072")
    print("result is: ", result)
    result = bms.update_deploy_status("i072", "OFF")
    print("deploy result is: ", result)
    result = bms.update_deploy_status("i072", "ON")
    print("deploy result is: ", result)
    result = bms.update_deploy_status("i072", "OFF")
    print("deploy result is: ", result)
    result = bms.init_power_status("i072", True)
    result = bms.update_power_status("i072", "ON", True)
    print("power on result is: ", result)
    result = bms.init_power_status("i072", False)
    result = bms.update_power_status("i072", "ON", False)
    print("power off result is: ", result)
    result = bms.update_power_status("i072", "OFF", False)
    print("power off result is: ", result)
    result = bms.get_status_short()
    print("result is: ", result)
