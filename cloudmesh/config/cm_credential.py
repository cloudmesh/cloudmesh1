from cloudmesh.config.ConfigDict import ConfigDict
from cloudmesh.util.logger import LOGGER
from pprint import pprint
from cloudmesh.util.util import banner

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


class CredentialFromYaml(CredentialBaseClass):


    def clean_cm(self):
        '''temporary so we do not have to modify yaml files for now'''
        for key in self.keys():
            if key.startswith('cm_'):
                new_key = key.replace('cm_', '')
                self['cm'][new_key] = self[key]
                del self[key]

    def read(self, username, cloud, style=2.0):
        self.style = style

        self['cm']['source'] = 'yaml'
        self['cm']['filename'] = self.filename
        self['cm']['kind'] = self.config.get("meta.kind")
        self['cm']['yaml_version'] = self.config.get("meta.yaml_version")

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
        self.clean_cm()
        self.transform_cm(self['cm']['yaml_version'], style)


    def __init__(self,
                 username,
                 cloud,
                 datasource=None,
                 yaml_version=2.0,
                 style=2.0):
        """datasource is afilename"""
        CredentialBaseClass.__init__(self, username, cloud, datasource)

        if datasource != None:
            self.filename = datasource
        else:
            self.filename = "~/.futuregrid/cloudmesh.yaml"

        self.config = ConfigDict(filename=self.filename)




        self.read(username, cloud)

    def transform_cm(self, yaml_version, style):
        if yaml_version <= 2.0 and style == 2.0:
            for key in self['cm']:
                new_key = 'cm_' + key
                self[new_key] = self['cm'][key]
            del self['cm']

class CredentialFromMongo(CredentialBaseClass):

    def __init__(self, user, cloud, datasource=None):
        """data source is a collectionname in cloudmesh_server.yaml"""
        """if day=tasource is none than use the default on which is ?"""
        raise NotImplementedError()

if __name__ == "__main__":

    # -------------------------------------------------------------------------
    banner("YAML read test")
    # -------------------------------------------------------------------------
    banner("gvonlasz - sierra_openstack_grizzly - old")
    # -------------------------------------------------------------------------
    credential = CredentialFromYaml("gvonlasz", "sierra_openstack_grizzly")
    pprint (credential)

    banner("gvonlasz - sierra_openstack_grizzly - new")
    # -------------------------------------------------------------------------
    credential = CredentialFromYaml("gvonlasz", "sierra_openstack_grizzly", style=3.0)
    pprint (credential)

    print credential['credentials']['OS_USERNAME']

    print credential.keys()

    banner("gvonlasz - hp - old")
    # -------------------------------------------------------------------------
    credential.read("gvonlasz", "hp")

    pprint (credential)

    banner("gvonlasz - hp - new")
    # -------------------------------------------------------------------------
    credential.read("gvonlasz", "hp", style=3.0)

    pprint (credential)



