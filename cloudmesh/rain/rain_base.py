
class RainBase:

    """
    Base abstract class for rain provision
    """

    def __init__(self):
        pass

    def not_implemented(self):
        print "NOT Implemented"

    def provision(self, host, *args, **kwargs):
        """baremtal provision
        """
        self.not_implemented()

    def power(self, host, flag_on=True):
        self.not_implemented()
