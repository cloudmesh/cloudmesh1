class CredentialBaseClass (dict):

    def __init__(self):
        pass

    def get(self):
        return self

    def read(self, username, cloud):
        raise NotImplementedError()

class CredentialFromYaml(CredentialBaseClass):

    kind = "cloudmesh"

    filename = "~/.futuregrid/cloudmesh_server.yaml"

    def __init__(self, user, cloud,
                 datasource=None):
        """datasource is afilename"""

        if filename == None:
            filename = self.filename
        else:
            self.filename = filename

        config = ConfigDict(prefix="cloudmesh.server",
                            filename=filename)

        kind = config.get("meta.kind")

        if kind == "user":
            self = config.get("cloudmesh.clouds.{0}".format(cloud))
        elif kind == "server":
            self = config.get("cloudmesh.server.keystone.{0}".format(cloud))
        else:
            log.error("kind wrong {0}".format(kind))

class AuthenticateFromMongo(CredentialBaseClass):

    def __init__(self, user, cloud, datasource=None):
        """data source is a collectionname in cloudmesh_server.yaml"""
        """if day=tasource is none than use the default on which is ?"""
        raise NotImplementedError()



