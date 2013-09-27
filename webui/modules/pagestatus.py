
cm_kind = 'pagestatus'
user = 'psjoshi'
page = 'mesh/qstat'
attribute = 'openpages'
value = ['sierra.futuregrid.org', 'hotel.futuregrid.org']

userDefaults = {
                'user': 'psjoshi',
                'images': 'sierra',
                'servers': 'India',
                'qstat': 'hotel'
                }


from cloudmesh.util.logger import LOGGER
from cloudmesh.cm_mongo import cm_MongoBase
from cloudmesh.config.ConfigDict import ConfigDict
import os

# ----------------------------------------------------------------------
# SETTING UP A LOGGER
# ----------------------------------------------------------------------

log = LOGGER(__file__)

class cm_mongo_pagestatus(cm_MongoBase):
    cm_kind = 'pagestatus'

    def __init__(self):
        self.cm_type = "pagestatus"
        self.connect()

    def kill(self):
        self.db_mongo.remove({})

    def add(self, user, page, attribute, value):
        self.update({'cm_kind': cm_kind, 'user': user, 'page': page, 'attribute': attribute}, {'cm_kind': cm_kind, 'user': user, 'page': page, 'attribute': attribute, 'value': value})

    def get(self, user, page, attribute):
        result = m.find_one({'user': user, 'page': page, 'attribute': attribute})
        print 'Result:', result
        return result['value']


class cm_config_pagestatus(ConfigDict):
    """
    reads the information contained in the file
    ~/.futuregrid/cloudmesh_server.yaml
    """
    filename = os.path.expanduser("~/.futuregrid/cloudmesh_server.yaml")

    def __init__(self, filename=None):
        if filename is None:
            filename = self.filename
        ConfigDict.__init__(self, filename=filename, kind="pagestatus")


if __name__ == "__main__":

    config = cm_config_pagestatus()
    print config.get('mongo.collections.pagestatus.db')


    m = cm_mongo_pagestatus()
    m.clear()


    m.kill()


    '''
    m.update({'cm_kind': cm_kind, 'user': user, 'page': page}, {'cm_kind': cm_kind, 'user': user, 'page': page, 'attribute': value})
    cursor = m.find({})
    for element in cursor:
        print element
    
    cursor = m.find({'user': user, 'page': page})
    print cursor
    print cursor[0]
    for element in cursor:
        print element
    
    cursor = m.find_one({'user': user, 'page': page})
    print cursor
    
    
    m.kill()
    '''

    print 'done killing'

    m.add('gregor', '/hello', 'VMs', '100')
    m.add('gregor', '/hello', 'images', '99')

    cursor = m.find({})
    for element in cursor:
        print 'a', element


    print m.get('gregor', '/hello', 'VMs')
    print m.get('gregor', '/hello', 'images')


