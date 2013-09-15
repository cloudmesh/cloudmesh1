from cloudmesh.config.cm_config import cm_config_server
from cloudmesh.config.cm_config import get_mongo_db
from cloudmesh.util.logger import LOGGER


from pymongo import MongoClient
import pprint

# ----------------------------------------------------------------------
# SETTING UP A LOGGER
# ----------------------------------------------------------------------

log = LOGGER(__file__)

class cm_launcher_db(cm_MongoBase):

    def __init__(self):
        self.cm_type = "launcher"
        self.connect()



