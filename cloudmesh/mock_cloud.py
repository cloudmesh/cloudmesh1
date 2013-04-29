class mock_cloud:
    """ Provides a mock class for testing.  Represents the cloud
    credential data that will come from cloud API"""

    def __init__(self, username, cloudname):
        self._username = username
        self._cloudname = cloudname
        self._data = None

    def _load_data(self):
        self._data = { cloudname: {} }
        if self.cloudname == 'india-openstack':
            self._data[cloudname] = {
                'cm_label': 'ios',
                'cm_host': 'india.futuregrid.org',
                'cm_type': 'openstack',
                'credentials': {
                    'OS_AUTH_URL': 'url',
                    'OS_PASSWORD': 'password',
                    'OS_TENANT_NAME': 'member',
                    'OS_USERNAME': 'username',
                    'OS_VERSION': 'essex',
                    'OS_CACERT': '$HOME/.futuregrid/india/openstack/cacert.pem'
                    },
                'default': {
                    'flavor': 'm1.tiny',
                    'image': 'ktanaka/ubuntu1204-ramdisk.manifest.xml ',
                    'project': 'fg-181'
                    }
                }
        elif self.cloudname == 'grizzly-openstack':
            self._data[cloudname] = {
                'cm_label': 'ios',
                'cm_host': 'abc.futuregrid.org',
                'cm_type': 'openstack',
                'credentials': {
                    'OS_AUTH_URL': 'url',
                    'OS_PASSWORD': 'password',
                    'OS_TENANT_NAME': 'member',
                    'OS_USERNAME': 'username',
                    'OS_VERSION': 'grizzly',
                    'OS_CACERT': '$HOME/.futuregrid/india/openstack/cacert.pem'
                    },
                'default': {
                    'flavor': 'm1.tiny',
                    'image': 'ktanaka/ubuntu1204-ramdisk.manifest.xml ',
                    'project': 'fg-181'
                    }
                }


    @property
    def cloudname(self):
        return self._cloudname

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

























