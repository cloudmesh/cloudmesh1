class mock_cloud:
    """ Provides a mock class for testing.  Represents the cloud
    credential data that will come from cloud API"""

    def __init__(self, username, cloudname):
        self._username = username
        self._cloudname = cloudname
        self._data = None

    def _load_data(self):
        if self.cloudname == 'india-openstack':
            self._data = {
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
                    'image': 'ktanaka/ubuntu1204-ramdisk.manifest.xml',
                    'project': 'fg-181'
                    }
                }
        elif self.cloudname == 'grizzly-openstack':
            self._data = {
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
                    'image': 'ktanaka/ubuntu1204-ramdisk.manifest.xml',
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


























