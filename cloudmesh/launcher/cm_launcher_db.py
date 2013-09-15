from cloudmesh.util.logger import LOGGER

# ----------------------------------------------------------------------
# SETTING UP A LOGGER
# ----------------------------------------------------------------------

log = LOGGER(__file__)

class cm_launcher_db(cm_MongoBase):

    def __init__(self):
        self.cm_type = "launcher"
        self.connect()



