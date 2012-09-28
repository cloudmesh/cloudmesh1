
import commands
import random
import datetime
import pprint
from pymongo import Connection
import uuid


class Server(object):
    def __init__(self):
        '''
        uniq_ID = ''
        ip_address=''
        name=''
        kind=''
        label=''
        keyword=''
        time_start=''
        time_stop=''
        time_update=''
        services=''
        '''
        self.uniq_ID = uuid.uuid4()
        self.ip_address = commands.getoutput(" ifconfig lo | grep 'inet addr' \
        | cut -d: -f2 | awk '{print $1}' ")
        self.name = commands.getoutput("hostname")
        
        #For now both start time and stop time are one and the same
        self.time_start = datetime.datetime.now().strftime("%D-%H:%M:%S.%f")
        self.time_stop = datetime.datetime.now().strftime("%D-%H:%M:%S.%f")
        self.time_update = datetime.datetime.now().strftime("%D-%H:%M:%S.%f")
        #Populate the remaining fields with random entries
        self.type = get_random_word(6)
        self.label = get_random_word(6)
        self.keyword = get_random_word(6)
        
    def insertData(self):
        '''Insert server data in the object created
        """
        self.ip_address = commands.getoutput(" ifconfig lo | grep 'inet addr'\
         | cut -d: -f2 | awk '{print $1}' ")
        self.name = commands.getoutput("hostname")'
        self.uniq_ID = uuid.uuid4()
        
        self.time_start = datetime.datetime.now().strftime("%D-%H:%M:%S.%f")
        self.time_stop = datetime.datetime.now().strftime("%D-%H:%M:%S.%f")
        self.time_update = datetime.datetime.now().strftime("%D-%H:%M:%S.%f")
        #Populate the remaining fields with random entries for now
        self.type = self.get_random_word(6)
        self.label = self.get_random_word(6)
        self.keyword = self.get_random_word(6)
        """  
        '''

    def dumpServer(self):
        '''Print the current data in server object'''
        print self.ip_address
        print self.name
        #print self.kind
        print self.label
        print self.keyword
        print self.time_start
        print self.time_stop
        print self.time_update
        #print self.services
        return
    
class Services(object):
    def __init__(self):
        '''Initialize all the class fields'''
        """
        uniq_ID = ''
        ip_address ='' 
        name = ''
        kind = ''
        label = ''
        version = ''
        keyword = ''
        time_start = ''
        time_stop = ''
        time_update = ''
        """
        name_list = ['eucalyptus', 'openstack', 'EC2']
        #initialize the server unique ID to zero, the service will be assigned 
        # to server later on.
        self.server_uniq_ID = 0
        self.uniq_ID = uuid.uuid4()
        self.ip_address = commands.getoutput(" ifconfig lo | grep 'inet addr' \
        | cut -d: -f2 | awk '{print $1}' ")
        
        self.name = random.choice(name_list)
        self.type = get_random_word(3)
        self.version = random.randint(1, 9)
        self.keyword = get_random_word(3)
        self.time_start = datetime.datetime.now().strftime("%D-%H:%M:%S.%f")
        self.time_stop = datetime.datetime.now().strftime("%D-%H:%M:%S.%f")
        self.time_update = datetime.datetime.now().strftime("%D-%H:%M:%S.%f")
        self.type = get_random_word(6)
        self.label = get_random_word(6)
        self.keyword = get_random_word(6)
    
    @classmethod
    def insertServiceData(self):

        '''Insert the services data in the object created'''
        """
        name_list = ['eucalyptus', 'openstack', 'EC2']
        self.ip_address = commands.getoutput(" ifconfig lo | grep 'inet addr' \
        | cut -d: -f2 | awk '{print $1}' ")
        self.name = random.choice(name_list)
        self.type = self.get_random_word(3)
        self.version = random.randint(1, 9)
        self.uniq_ID = uuid.uuid4()
        self.keyword = self.get_random_word(3)
        self.time_start = datetime.datetime.now().strftime("%D-%H:%M:%S.%f")
        self.time_stop = datetime.datetime.now().strftime("%D-%H:%M:%S.%f")
        self.time_update = datetime.datetime.now().strftime("%D-%H:%M:%S.%f")
        self.status = self.get_random_word(3)
        self.type = self.get_random_word(6)
        self.label = self.get_random_word(6)
        self.keyword = self.get_random_word(6)
        """
        '''Look about the services'''
        #self.test['services'].append(self.test_services)
    
class myInventory:
    '''
    Class that handles all the operations on the inventory with server\
     and services objects;
    '''
    #Create a list of server and services objects
    Serviceslist = []
    Serverlist = []
    
    #Create a dict for dumping the contents of the list
    Serverdict = {}
    Servicesdict = {}
    
    connection = ''
    db = ""
    
    def __init__(self):
        hostname = "localhost"
        port = 27017
        
        self.connect( port, hostname )
        # Connect to the database and initialize the required parameters.
        
    def add(self, kind, **KWdata):
        '''add the data to the kind object specified, data right
         now is a dummy variable'''
        #Parameters\
            # **KWdata if kind is services, first field is uuid of the server'''
         
        if(kind == 'Server'):
            self.Serverlist.append(Server())
            self.Serverlist[(len(self.Serverlist) - 1)].insertData()
            Serverdict = self.Serverlist[len(self.Serverlist)-1].__dict__
            pprint.pprint(Serverdict)
            print self.Serverlist
            #create and add server object
            
        elif(kind == 'Service'):
            #create and add service object, bind the service object to one of the\
            #servers by setting its Server_uniq_ID to the servers uniq_ID
            #data is a list with first element being the uuid of the server
            self.Serviceslist.append(Services())
            self.Serviceslist[(len(self.Serviceslist) - 1)].insertData()
            self.Serviceslist[(len(self.Serviceslist) - 1)].server_uniq_ID = KWdata[0]
            Servicesdict = self.Serviceslist[len(self.Serviceslist)-1].__dict__
            pprint.pprint(Servicesdict)

    def delete(self, kind, uid):
        '''Delete the kind object with specified data unique ID'''
        if(kind == 'Server'):
            for i in self.Serverlist: 
                if i.uniq_ID == uid:
                    self.Serverlist.remove(i)
        
        elif(kind == 'Service'):
            #Delete a service object
            for j in self.Serviceslist: 
                if j.uniq_ID == uid:
                    self.Serviceslist.remove(j)
        
    def connect(self, port, hostname):
        '''Initialization method to connect to the database'''
        self.connection = Connection(hostname, port)
        try:
            self.db = self.connection.fg_inventorydbase
            collection = self.db.entry
        except:
            print "Cannot connect to the database"
        print "Connected Successfully"

    def disconnect(self):
        '''Disconnect from the mongodb database'''
        self.connection.close()

    def modify(self, kind, **fieldnames):
        '''Modify the data to the new required field.'''
        if kind == 'Server':
            pass
        elif kind == 'Services':
            pass
        
    def updateTime(self, kind , old_time, new_time):
        '''Update the time_update, stamp for given kind of object to 
        reflect the new current time'''
        if kind == 'Server':
            pass
        elif kind == 'Services':
            pass
        
    def list(self, kind):
        '''List the given kind of objects'''
        if kind == 'Server':
            pass
        
        elif kind == 'Services':
            pass

    def move(self, serviceuID, serveruID):
        '''To move a service from one server to another server, just change \
        the server_Uniq_id field in services to the new server'''
        for k in self.Serviceslist:
            if k.uniq_ID == serviceuID:
                k.server_uniq_ID = serveruID
        
    def dumpDB(self):
        '''dump the contents of object array to database'''
        
#******************** Test method for putting in random data for now***********
def get_random_word(wordLen):
    '''To generate random words to fill the test data structure'''
    word = ''
    for _ in range(wordLen):
        word += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuv\
        wxyz0123456789')
    return word
 
if __name__ == "__main__":
    pass