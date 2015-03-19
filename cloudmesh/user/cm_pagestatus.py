from __future__ import print_function
from cloudmesh_base.logger import LOGGER
from cloudmesh.cm_mongo import cm_MongoBase
from cloudmesh.config.ConfigDict import ConfigDict
import os
from pprint import pprint

# ----------------------------------------------------------------------
# SETTING UP A LOGGER
# ----------------------------------------------------------------------

log = LOGGER(__file__)


class cm_pagestatus(cm_MongoBase):

    """
    This methods holds some status information that is associated with a web
    page
    """

    cm_kind = 'pagestatus'

    def __init__(self):
        self.cm_type = "pagestatus"
        self.connect()

    def delete(self, user, page=None):
        '''
        Deletes the state values associated with a page. If non is specified for
        page all page state values are deleted

        :param user: the user for which the state values are recorded
        :type user: string
        :param page: the page base url
        :type page: of the form /uri (string)
        '''

        if page is None:
            self.db_mongo.remove({"cm_type": self.cm_type, "cm_user_id": user})
        else:
            self.db_mongo.remove({"cm_type": self.cm_type,
                                  "page": page,
                                  "cm_user_id": user})

    def add(self, user, page, attribute, value):
        '''
        adds the state value for a user and page

        :param user:
        :type user:
        :param page:
        :type page:
        :param attribute:
        :type attribute:
        :param value:
        :type value:
        '''

        self.update({
            'cm_kind': self.cm_kind,
            'cm_user_id': user,
            'page': page,
            'attribute': attribute
        }, {
            'cm_kind': self.cm_kind,
            'cm_user_id': user,
            'page': page,
            'attribute': attribute,
            'value': value})

    def get(self, user, page, attribute):
        '''
        get the state value for a user and a page

        :param user:
        :type user:
        :param page:
        :type page:
        :param attribute:
        :type attribute:
        '''
        result = m.find_one({'cm_user_id': user,
                             'page': page,
                             'attribute': attribute})
        return result['value']


if __name__ == "__main__":

    m = cm_pagestatus()
    m.clear()

    m.add('gregor', '/hello', 'VMs', '100')
    m.add('gregor', '/hello', 'images', '99')

    m.add('gregor', '/hello', 'dict', {"a": 1, "b": {"c": 1}})

    cursor = m.find({})
    for element in cursor:
        print('element', element)

    print(m.get('gregor', '/hello', 'VMs'))
    print(m.get('gregor', '/hello', 'images'))
    print(m.get('gregor', '/hello', 'dict'))

    pprint(m.get('gregor', '/hello', 'dict')['b'])
