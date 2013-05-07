class mock_user:
    """ Provides a mock class for testing. Represents the user/project
    data that will come from LDAP and/or Portal. """

    def __init__(self, username):
        self._username = username
        self._data = None

    def _load_data(self):
        self._data = {
            'profile': {
                'username': self._username,
                'firstname': 'Gregor',
                'lastname': 'von Laszewski',
                'phone': '812 ...',
                'e-mail': 'laszewski@gmail.com',
                'address': ['Indiana University', 'Bloomington, IN 47408']
                },
            'keys': {
                'name 1': 'file $HOME/.ssh/id_rsa.pub',
                'name 2': 'file $HOME/.ssh/id_rsa2.pub',
                'bla': 'key ssh-rsa AAAAB3.....zzzz keyname'
                },
            'projects': {
                'active': ['fg-82', 'fg-101'],
                'completed': ['fg-81', 'fg-102'],
                'default': 'fg-82'
                },
            'active': ['sierra-openstack-grizzly', 'india-openstack'],
            'default': 'sierra-openstack-grizzly'
            }

    @property
    def data(self):
        if self._data is None:
            self._load_data()
        return self._data

    @property
    def firstname(self):
        return self.data['profile']['firstname']

    @property
    def lastname(self):
        return self.data['profile']['lastname']

    @property
    def phone(self):
        return self.data['profile']['phone']

    @property
    def email(self):
        return self.data['profile']['e-mail']

    @property
    def address(self):
        return self.data['profile']['address']

    @property
    def keys(self):
        return self.data['keys']

    @property
    def projects(self):
        return self.data['projects']

    @property
    def activeclouds(self):
        return self.data['active']

    @property
    def defaultcloud(self):
        return self.data['default']

    @property
    def activeprojects(self):
        return self.data['projects']['active']

    @property
    def completedprojects(self):
        return self.data['projects']['completed']

    @property
    def defaultproject(self):
        return self.data['projects']['default']



















