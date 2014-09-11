# see cm_temperature


class cm_power:

    """class to conveniently switch power on and of"""

    """the hostanme is the label of the host as defined in the inventory."""

    def on(self, hostname):
        """switches the power on"""

    def off(self, hostname):
        """switches power off"""

    def status(self, hostname):
        """resturns the power state of the hostname"""

    def cluster_statue(self, cluster_label):
        """returns the powere status of all hosts in the given cluster"""

    def enabled(self, hostname):
        """returns true if the power can be set"""
