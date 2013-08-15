from config.cm_config import cm_config_server

from util.logger import LOGGER

# ----------------------------------------------------------------------
# SETTING UP A LOGGER
# ----------------------------------------------------------------------

log = LOGGER('cm_user')



class cm_userLDAP (CMUserProviderBaseType):
    
    
    provider = {}
    
    def __init__(self, collection="user"):
        super( cm_mongo, self ).__init__()

        
    def refresh(self):
        '''
        refreshes the userdatabase from the user provider
        '''
        users = self.list()
        for user in users:
            data = self.get(username)
            self.update(username, data)


    def register(self, name, type, **kwargs):
        '''
        registers a provider with som parameters specified in the dict params
        
        :param name: the name of the provider
        :param type: the type of the provider, overwrites a possibly given type in params
        :param params: a dictionary describing wht needs to be poassed to the service that provides user information
        '''
        provider = {'type': type, 
                    'name': name}
        for k,v in kwargs.iteritems():
            provider[k] = v
            
    def get(self,username):
        '''
        returns the dict associated with the username
        :param username:
        '''
        return {}
        
    def list(self):
        '''
        returns a list with all usernames
        '''
        return []
    
        
        
        
            
        
        
        
        
