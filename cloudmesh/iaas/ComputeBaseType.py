from datetime import datetime

def donotchange(fn):
    return fn

class ComputeBaseType:

    """
    flavors = {}         # global var
    images = {}          # global var
    servers = {}         # global var
    credential = None    # global var
    label = None         # global var
    """

    def _clear(self):
        self.flavors = {}         # global var
        self.images = {}          # global var
        self.servers = {}         # global var
        self.credential = None    # global var
        self.label = None         # global var
        self.type = None
        self.user_id = None
        self.auth_token = None

    def info(self):
        print "Label:", self.label
        print "Type:", self.type
        print "Flavors:", len(self.flavors)
        print "Servers:", len(self.servers)
        print "Images:", len(self.images)
 
    def connect(self):
        raise NotImplementedError()

    def config (self, dict):
        raise NotImplementedError()

    def find_user_id(self, force=False):
        raise NotImplementedError()


    def dump(self, type="server", with_manager=False):
        selection = type.lower()[0]
        if selection == 'i':
            d = self.images.copy()
        elif selection == 'f':
            d = self.flavors.copy()
        elif selection == 's':
            d = self.servers.copy()
        elif type != None:
            print "refresh type not supported"
            assert False
        else:
            d = {}
            with_manager = True
        if with_manager == False:
            for element in d.keys():
                del d[element]['manager']
        return d

    def get(self,type="server"):
        selection = type.lower()[0]
        list_function = self._get_servers_dict
        d = {}
        if selection == 'i':
            d = self.images
        elif selection == 'f':
            d = self.flavors
        elif selection == 's':
            d = self.servers
        elif type != None:
            print "refresh type not supported"
            assert False
        return d
    
    def _get_image_dict(self):
        raise NotImplementedError()

    def _update_image_dict(self,information):
        raise NotImplementedError()

    def _get_flavors_dict(self):
        raise NotImplementedError()

    def _update_flavors_dict(self,information):
        raise NotImplementedError()

    def _get_servers_dict(self):
        raise NotImplementedError()


    def _update_servers_dict(self,information):
        raise NotImplementedError()

    def vm_create(self, name=None,
                  flavor_name=None,
                  image_id=None,
                  security_groups = None,
                  key_name = None,
                  meta=None):
        raise NotImplementedError()
    def vm_delete(self, id):
        raise NotImplementedError()

    def vms_project(self, refresh=False):
        raise NotImplementedError()
        
    def rename(self, old, new, id=None):
        raise NotImplementedError()

    def usage(self, start, end, format='dict'):
        raise NotImplementedError()
        
    def limits(self):
        raise NotImplementedError()

    def status(self, vm_id):
        raise NotImplementedError()

    def wait(self, vm_id, vm_status, seconds=2):
        print 'refersh', vm_id
        self.refresh()
        
        new_status = self.status(vm_id)
        print new_status
        while str(new_status) != str(vm_status):
            time.sleep(seconds)
            self.refresh()
            new_status = self.status(vm_id)


    ######################################################################
    # print
    ######################################################################

    def __str__(self):
        """
        print everything but the credentials that is known about this
        cloud in json format.
        """
        information = {
            'label': self.label,
            'flavors': self.flavors,
            'servers': self.servers,
            'images': self.images}
        return json.dumps(information, indent=4)



    ######################################################################
    # get methods
    ######################################################################

    def type():
        return self.type

    def vms(self):
        return self.servers

    def status(self, vm_id):
        return self.servers[vm_id]['status']


    ######################################################################
    # set credentials
    ######################################################################

    def credentials(self, cred):
        self.credential = cred

    ######################################################################
    # set credentials
    ######################################################################

    def refresh(self, type=None):
        time_stamp = datetime.now().strftime('%Y-%m-%dT%H-%M-%SZ')
        selection = ""
        if type:
            selection = type.lower()[0]

        list_function = self._get_servers_dict
        update_function = self._update_servers_dict
        d = self.servers
        if selection == 'a' or type == None:
            self.refresh("images")
            self.refresh("flavors")
            self.refresh("servers")
            return
        elif selection == 'i':
            list_function = self._get_images_dict
            update_function = self._update_images_dict
            d = self.images
        elif selection == 'f':
            list_function = self._get_flavors_dict
            update_function = self._update_flavors_dict
            d = self.flavors
        elif selection == 's':
            list_function = self._get_servers_dict
            update_function = self._update_servers_dict
            d = self.servers
        elif type != None:
            print "refresh type not supported"
            assert False

        list = list_function()

        if len(list)  == 0:
           if selection == 'i':
               self.images = {}
           elif selection == 'f':
               self.flavors = {}
           elif selection == 's':
               self.servers = {}

        else:
            
            for information in list:
                (id, element) = update_function(information)
                d[id] = element
                d[id]['cm_refresh'] = time_stamp
