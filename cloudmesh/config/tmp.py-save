
        self._userdata_handler = None
        self._serverdata = None



# pyaml.dump(self.config, f, vspacing=[2, 1, 1])
        # text = yaml.dump(self.config, default_flow_style=False)
        # this is a potential bug
        if configuration is None:
            configuration = self
        template_path = os.path.expanduser("~/.futuregrid/etc/cloudmesh.yaml")
        template = cm_template(template_path)

        # Set up a dict to pass to the template
        template_vars = {}
        template_vars['portalname'] = configuration['cloudmesh']['profile']['username']
        template_vars['password'] = {}
        for cloudname, cloudattrs in configuration['cloudmesh']['clouds'].iteritems():
            template_vars['password'][cloudname] = cloudattrs['credentials']['OS_PASSWORD']
        template_vars['projects'] = copy.deepcopy(configuration['cloudmesh']['projects'])
        template_vars['keys'] = copy.deepcopy(configuration['cloudmesh']['keys'])
        template_vars['profile'] = copy.deepcopy(configuration['cloudmesh']['profile'])

        # print custom_print(template_vars, 4)

        # content = template.replace(format="text", **template_vars)
        # changed otherwise it throws unexpected keyword error

@deprecated
    def _initialize_user(self, username):
        """Loads user config, including profile, projects, and credentials"""
        user = self.userdata_handler(username)

        self.init_config['cloudmesh']['prefix'] = username
        self.init_config['cloudmesh']['index'] = "001"

        self.init_config['cloudmesh']['profile'] = {
            'username': username,
            'uid': user.uid,
            'gid': user.gid,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'phone': user.phone,
            'email': user.email,
            'address': user.address
        }

        keys = {'default': None, 'keylist': {}}
        if user.keys:
            for key in user.keys.keys():
                if keys['default'] is None:
                    keys['default'] = key
                keys['keylist'][key] = user.keys[key]
        self.init_config['cloudmesh']['keys'] = keys

        self.init_config['cloudmesh']['projects'] = {
            'active': user.activeprojects,
            'completed': user.completedprojects,
            'default': user.defaultproject
        }

        self.init_config['cloudmesh']['active'] = user.activeclouds
        self.init_config['cloudmesh']['default'] = user.defaultcloud

    @deprecated
    def _initialize_clouds(self):
        """Creates cloud credentials for the user"""
        self.init_config['cloudmesh']['clouds'] = {}
        cloudlist = self.init_config['cloudmesh']['active']
        for cloud in cloudlist:
            cloud_handler = self._get_cloud_handler(cloud, as_admin=True)
            cloud_handler.initialize_cloud_user()
            self.init_config['cloudmesh']['clouds'][cloud] = copy.deepcopy(cloud_handler.credentials)

    @deprecated
    def initialize(self, username):
        """Creates or resets the config for a user.  Note that the
        userdata_handler property must be set with appropriate handler class."""
        self.init_config = collections.OrderedDict()
        self.init_config['cloudmesh'] = collections.OrderedDict()
        self._initialize_user(username)
        self._initialize_clouds()

    @deprecated
    def change_own_password(self, cloudname, oldpass, newpass):
        cloud_handler = self._get_cloud_handler(cloudname)
        cloud_handler.change_own_password(oldpass, newpass)
        # Save the yaml file so the new password is saved
        self.write()

    @deprecated
    def get_own_passwords(self):
        cloudlist = self.active()
        passwords = {}
        for cloud in cloudlist:
            cloud_handler = self._get_cloud_handler(cloud)
            passwords[cloud] = cloud_handler.get_own_password()
        return passwords

    # ======================================================================
    # NOT SURE WHY THESE METHODS ARE NEEDED
    # ======================================================================

    @property
    def userdata_handler(self):
        """Plug-in class that knows how to get all the user/project config"""
        return self._userdata_handler

    @userdata_handler.setter
    def userdata_handler(self, value):
        self._userdata_handler = value

    @property
    def serverdata(self):
        if self._serverdata is None:
            self._serverdata = yaml.safe_load(open(self.cloudmesh_server_path, "r"))
        return self._serverdata
    
    # ----------------------------------------------------------------------
    # Internal helper methods
    # ----------------------------------------------------------------------
    @deprecated
    def _get_cloud_handler(self, cloud, as_admin=False):
        """This gets a class that knows how to handle the specific type of
        cloud (how to provision users, etc)"""
        handler_args = { 'username': self.init_config['cloudmesh']['profile']['username'],
                         'email':  self.init_config['cloudmesh']['profile']['e_mail'],
                         'defaultproj': self.init_config['cloudmesh']['projects']['default'],
                         'projectlist': self.init_config['cloudmesh']['projects']['active'],
                         'cloudname': cloud,
                         'cloudcreds': self.get_data(cloud),
                         'cloudadmincreds': self.serverdata['keystone'][cloud] }
        cloud_handler_class = cloudmesh_cloud_handler(cloud)
        cloud_handler = cloud_handler_class(**handler_args)
        return cloud_handler

