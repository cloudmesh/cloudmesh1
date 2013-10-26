from cloudmesh.config.ConfigDict import ConfigDict
from cloudmesh.util.logger import LOGGER
from pprint import pprint

log = LOGGER(__file__)

class CredentialBaseClass (dict):

    def __init__(self, username, cloud, datasource):
        dict.__init__({'username': username,
                       'cloud': cloud,
                       'datasource': datasource})

    def read(self, username, cloud):
        raise NotImplementedError()

    def save(self):
        raise NotImplementedError()

    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = {}
            return value
    '''
    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            log.error('key does not exist: {0}'.format(key))
            return
    '''



class CredentialFromYaml(CredentialBaseClass):

    def clean_cm(self):
        '''temporary so we do not have to modify yaml files for now'''
        for key in self.keys():
            if key.startswith('cm_'):
                new_key = key.replace('cm_', '')
                self['cm'][new_key] = self[key]
                del self[key]
        del self['filename']

    def read(self, username, cloud):
        kind = self['cm']['kind']
        if kind == "clouds":
            self['cm']['filename'] = "~/.futuregrid/cloudmesh.yaml"
            self.update(self.config.get("cloudmesh.clouds.{0}".format(cloud)))

        elif kind == "server":
            self['cm']['filename'] = "~/.futuregrid/cloudmesh_server.yaml"
            self.update(self.config.get("cloudmesh.server.keystone.{0}".format(cloud)))
        else:
            log.error("kind wrong {0}".format(kind))
        self['cm']['username'] = username
        self['cm']['cloud'] = cloud

    def __init__(self, username, cloud, datasource=None):
        """datasource is afilename"""
        CredentialBaseClass.__init__(self, username, cloud, datasource)
        self['cm']['source'] = 'yaml'
        if datasource != None:
            self.filename = datasource
        else:
            self['filename'] = "~/.futuregrid/cloudmesh.yaml"

        self.config = ConfigDict(prefix="cloudmesh.server",
                            filename=self['filename'])



        self['cm']['kind'] = self.config.get("meta.kind")

        self.read(username, cloud)
        self.clean_cm()


class CredentialFromMongo(CredentialBaseClass):

    def __init__(self, user, cloud, datasource=None):
        """data source is a collectionname in cloudmesh_server.yaml"""
        """if day=tasource is none than use the default on which is ?"""
        raise NotImplementedError()

if __name__ == "__main__":
    credential = CredentialFromYaml("gvonlasz", "sierra_openstack_grizzly")

    pprint (credential)

    print credential['credentials']['OS_USERNAME']

    print credential.keys()

    credential.read("gvonlasz", "hp")





