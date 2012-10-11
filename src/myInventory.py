
import commands
import random
import datetime
import pprint
from pymongo import Connection



class Server(object):
    def __init__(self):
        ip_address=''
        name=''
        label=''
        keyword=''
        time_start=''
        time_stop=''
        time_update=''
        services=''
        
    def insertData(self):
        #Insert server data in the object created
        
        servernamelist = ['india','sierra','alamo', 'foxtrot']
        self.ip_address = commands.getoutput(" ifconfig wlan0 | grep 'inet addr' \
        | cut -d: -f2 | awk '{print $1}' ")
        
        #self.name = commands.getoutput("hostname")
        self.name = random.choice(servernamelist)
        #For now both start time and stop time are one and the same
        self.time_start = datetime.datetime.now().strftime("%D-%H:%M:%S.%f")
        self.time_stop = datetime.datetime.now().strftime("%D-%H:%M:%S.%f")
        self.time_update = datetime.datetime.now().strftime("%D-%H:%M:%S.%f")
        #Populate the remaining fields with random entries
        self.type = 'Server'
        self.label = get_random_word(6)
        self.keyword = get_random_word(6)
       

    def dumpServer(self):
        '''Print the current data in server object'''
        print self.ip_address
        print self.name
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
        
        ip_address ='' 
        name = ''
        label = ''
        type = ''
        version = ''
        keyword = ''
        time_start = ''
        time_stop = ''
        time_update = ''
        server_name = ''
        
        
    def insertServiceData(self):

        '''Insert the services data in the object created'''
        name_list = ['Euca', 'OS', 'Euca2', 'HPC']
        self.ip_address = commands.getoutput(" ifconfig eth0 | grep 'inet addr' \
        | cut -d: -f2 | awk '{print $1}' ")
        self.name = random.choice(name_list)
        self.type = get_random_word(3)
        self.version = random.randint(1, 9)
        #self.uniq_ID = uuid.uuid4()
        self.keyword = get_random_word(3)
        self.type = 'Service'
        self.time_start = datetime.datetime.now().strftime("%D-%H:%M:%S.%f")
        self.time_stop = datetime.datetime.now().strftime("%D-%H:%M:%S.%f")
        self.time_update = datetime.datetime.now().strftime("%D-%H:%M:%S.%f")
        self.status = get_random_word(3)
        self.label = get_random_word(6)
        self.keyword = get_random_word(6)
        
        '''Look about the services'''
        #self.test['services'].append(self.test_services)
    
class myInventory():
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
        
        # Connect to the database and initialize the required parameters.
        #self.connect( port, hostname )
       
    def add(self, obj, **KWdata):
        '''add the data to the kind object specified, data right
         now is a dummy variable'''
        #Parameters\
            # **KWdata if kind is services, first field is uuid of the server'''
        if(obj.__class__.__name__ == 'Server'):
            self.Serverlist.append(Server())
            self.Serverlist[(len(self.Serverlist) - 1)].insertData()
            if 'name' in KWdata:
                self.Serverlist[(len(self.Serverlist) - 1)].name = KWdata['name']
            Serverdict = self.Serverlist[len(self.Serverlist)-1].__dict__
            pprint.pprint(Serverdict)
            
            
        elif(obj.__class__.__name__ == 'Services'):
            #create and add service object
            #data is a list with first element being the name of server
            self.Serviceslist.append(Services())
            self.Serviceslist[(len(self.Serviceslist) - 1)].insertServiceData()
            if 'name' in KWdata:
                self.Serviceslist[(len(self.Serviceslist) - 1)].server_name = KWdata['name']
            if 'service_name' in KWdata:
                self.Serviceslist[(len(self.Serviceslist) - 1)].name = KWdata['service_name']
                
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
        '''Disconnect from the Mongodb database'''
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

    def startNewService(self, servicefrom, serviceto, number):
        '''To move a service from one server to another server, just change \
        the server_Uniq_id field in services to the new server'''
        i = 0
        for k in self.Serviceslist:
            if i < number: 
                if k.name == servicefrom:
                    k.name == serviceto
                    i = i+1
       
    def dump(self):
        '''dump the contents of object array to summarize the current services\
        and the servers'''
        
        server_services_dict = {'india':[], 'sierra':[] , 'foxtrot':[]}#, 'alamo':[]}
        servers = []
        
        for each in self.Serviceslist:
            server_services_dict[each.server_name].append(each.name)

        services = ['Euca', 'OS', 'Euca2', 'HPC']
        
        print('\tEuca\t OS\t HPC\t Euca2\t')
        
        for every in server_services_dict:
            print every+'\t',
            for service in services:
                print str(server_services_dict[every].count(service)) +'\t',
            print 

#******************** Test method for putting in random data for now***********
def get_random_word(wordLen):
    '''To generate random words to fill the test data structure'''
    word = ''
    for _ in range(wordLen):
        word += random.choice('abcdefghijklmnopqrstuvwxyz')
    return word
 

if __name__ == "__main__":
    
    serverobj = Server()
    serviceobj = Services()
    serverobj.insertData()