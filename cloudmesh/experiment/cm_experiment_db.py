from cloudmesh_base.logger import LOGGER
from cloudmesh.cm_mongo import cm_MongoBase
from cloudmesh.config.cm_config import cm_config

# ----------------------------------------------------------------------
# SETTING UP A LOGGER
# ----------------------------------------------------------------------

log = LOGGER(__file__)


class cm_experiment_db(cm_MongoBase):

    """
    This methods holds some status information that is associated with a web
    page
    """

    cm_kind = 'experiment'

    def __init__(self):
        self.cm_kind = "experiment"
        self.connect()

    def delete(self, user, experiment=None):
        '''
        Deletes the state values associated with a experiment.
        If non is specified for experiment all experiment state
        values are deleted

        :param user: the user for which the state values are recorded
        :type user: string
        :param experiment: the experiment base url
        :type experiment: of the form /uri (string)
        '''

        if experiment is None:
            self.db_mongo.remove({"cm_kind": self.cm_kind,
                                  "cm_user_id": user})
        else:
            self.db_mongo.remove({"cm_kind": self.cm_kind,
                                  "experiment": experiment,
                                  "cm_user_id": user})

    def add(self, user, experiment, attribute, value):
        '''
        adds the state value for a user and experiment

        :param user:
        :type user:
        :param experiment:
        :type experiment:
        :param attribute:
        :type attribute:
        :param value:
        :type value:
        '''

        self.update({
            'cm_kind': self.cm_kind,
            'cm_user_id': user,
            'experiment': experiment,
            'attribute': attribute
        }, {
            'cm_kind': self.cm_kind,
            'cm_user_id': user,
            'experiment': experiment,
            'attribute': attribute,
            'value': value})

    def get(self, user, experiment, attribute):
        '''
        get the state value for a user and a experiment

        :param user:
        :type user:
        :param experiment:
        :type experiment:
        :param attribute:
        :type attribute:
        '''
        result = m.find_one({'cm_kind': self.cm_kind,
                             'cm_user_id': user,
                             'experiment': experiment,
                             'attribute': attribute})
        return result['value']


if __name__ == "__main__":

    username = cm_config().username()
    m = cm_experiment_db()
    m.clear()

    m.add(username, 'exp1', 'VMs', '100')
    m.add(username, 'exp1', 'images', '99')

    m.add(username, 'exp1', 'dict', {"a": 1, "b": {"c": 1}})

    cursor = m.find({})

    # pprint(configuration['cloudmesh']['experiment'])

    '''
    for element in cursor:
        print 'element', element


    print m.get(username, 'exp1', 'VMs')
    print m.get(username, 'exp1', 'images')
    print m.get(username, 'exp1', 'dict')

    pprint(m.get(username, 'exp1', 'dict')['b'])
    '''
