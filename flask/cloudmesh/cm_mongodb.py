from cloudmesh.mongodb import Mongodb


def example():
    cm_mongodb = Mongodb()
    cm_mongodb.connect()
    res = {}  # dict data structure from cloud mesh
    cm_mongodb.insert("cloud_mesh", res)
