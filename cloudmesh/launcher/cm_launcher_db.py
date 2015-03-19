from cloudmesh_base.logger import LOGGER
from cloudmesh.cm_mongo import cm_MongoBase

# ----------------------------------------------------------------------
# SETTING UP A LOGGER
# ----------------------------------------------------------------------

log = LOGGER(__file__)


class cm_launcher_db(cm_MongoBase):

    def __init__(self):
        self.cm_type = "launcher"
        self.connect()
