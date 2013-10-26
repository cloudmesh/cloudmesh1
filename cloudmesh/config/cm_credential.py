from cloudmesh.config.ConfigDict import ConfigDict

class CredentialBaseClass (dict):

    def __init__(self, username, cloud, datasource):
        pass

    def read(self, username, cloud):
        raise NotImplementedError()

    def save(self):
        raise NotImplementedError()

class CredentialFromYaml(dict):

    kind = "cloudmesh"

    filename = "~/.futuregrid/cloudmesh_server.yaml"

    def __init__(self, user, cloud,
                 datasource=None):
        """datasource is afilename"""
        if datasource != None:
            self.filename = datasource

        config = ConfigDict(prefix="cloudmesh.server",
                            filename=self.filename)

        print config

        kind = config.get("meta.kind")

        if kind == "user":
            self.configuration = config.get("cloudmesh.clouds.{0}".format(cloud))
        elif kind == "server":
            self.configuration = config.get("cloudmesh.server.keystone.{0}".format(cloud))
        else:
            log.error("kind wrong {0}".format(kind))


    def __getitem__(self, key):
        self.configuration[key]


class CredentialFromMongo(CredentialBaseClass):

    def __init__(self, user, cloud, datasource=None):
        """data source is a collectionname in cloudmesh_server.yaml"""
        """if day=tasource is none than use the default on which is ?"""
        raise NotImplementedError()

if __name__ == "__main__":
    credential = CredentialFromYaml("gvonlasz", "sierra_openstack_grizzly")

    print credential['OS_USERNAME']

    print credential.keys()





