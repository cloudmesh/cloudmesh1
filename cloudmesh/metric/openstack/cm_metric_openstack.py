from cloudmesh.config.cm_config import get_mongo_db


class cm_metric_openstack:

    def __init__(self, collection=None):

        if collection is None:
            collection = "metric"

        self.db_qstat = get_mongo_db(collections)

    def update(self, query, values=None):
        '''
        executes a query and updates the results from mongo db.
        :param query:
        '''
        if values is None:
            return self.db_qstat.update(query, upsert=True)
        else:
            print query
            print values
            return self.db_qstat.update(query, values, upsert=True)

    def insert(self, element):
        self.db_qstat.insert(element)

    def clear(self):
        self.db_qstat.remove({"cm_type": "metric"})

    def find(self, query):
        '''
        executes a query and returns the results from mongo db.
        :param query:
        '''
        return self.db_qstat.find(query)

    def find_one(self, query):
        '''
        executes a query and returns the results from mongo db.
        :param query:
        '''
        return self.db_qstat.find_one(query)

    def create_id(self, cluster, vm):
        return "cm-metric-{0}-{1}".format(cluster, vm)

    def cm_insert(self, element):
        e = cm_element(element)
        self.db_qstat.insert(e)

    def cm_element(self, d):
        element = dict(d)

        cluster = "pass me?"
        vm = "pass me?"
        refresh = "time when the element was refreshed"
        element = element.upodate({'cm_cluster': name,
                                   'cm_id': self.create(cluster, vm),
                                   'cm_type': "metric",
                                   'cm_kind': 'vm',
                                   'cm_refersh': refresh,
                                   })
        return element
