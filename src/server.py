'''
'''

import json
import pymongo
from pymongo import Connection
import commands
import random

'''for testing remove if not required later'''

hostname = 'localhost'
port = 27017

class server(object):
    '''Class variables'''
       
    dictdata = {}
    '''it is the data obtained from json object'''
    
    db = ''
    collection = ''
    '''Handle for the database to be used by all the functions'''
    
    def __init__(self):
        '''
        Constructor
        '''
        self.connectmdb(hostname, port)
        
    def writelog(self, uniqueID):
        with open('server.log', 'a') as log:
            log.write(uniqueID+"\n")
        #return "Write the current unique ID's in a log file"
    
    
    ''' This approach is really bad, to delete a record among n uid's you need to rewrite n-1 uid's to file again (worst case) '''
        
    def removelog(self, uniqueID):
        log =  open('server.log', 'r')
        lines = log.readlines()
        log.close()
        
        log = open('server.log' , 'w')
        for line in lines:
            if line != uniqueID:
                log.write(uniqueID+"\n")
        log.close()
        return "Remove the uniqueID from the file"
        
    def connectmdb(self,hostname, port):
        try:
            self.connection = Connection(hostname, port)
            self.db = self.connection.fg_inventorydbase
            self.collection = (self.db).entry
       
        except:
            print "Error, cannot connect to the database"
        
        #print self.collection.find_one()
        #print "Connected to mongodb database"

    def disconnectmdb(self):
        self.connection.close()
        print "Connection is closed."
    
    """Clear this with Gregor, right now assuming only attribute would be uid""" 
    
    def read_JSON(self, attribute, value):
        server_attribute = 'server'+'.'+attribute
        
        cursor = self.collection.find({server_attribute : value})
        self.dictdata = dict((record['_id'], record) for record in cursor)
        print self.dictdata
        
    def write_server(self ,data = 'empty'): 
        if (data is 'empty'):
            data = self.server
        self.collection.insert(data)
        print data
        #self.writelog(data["server"]["uid"])
        return "Write the dict structure in mongodb collection"

    
    def add_server(self , attribute, value):
        
        return "Add a server with the data"
    
    def update_server(self, uid ,attribute, value):
        self.read_JSON('uid', uid)
        updateentry = self.collection.find({'uid' : uid})
        self.collection.update({},{attribute : value}, updateentry)
        self.dictdata[attribute] = value
        del self.dictdata['_id']
        #self.write_server(self.dictdata)
        print self.dictdata
        return "update the server with the updated values"
    
    def delete_server(self, uid):
        self.collection.remove({'uid' : uid}) 
        return "Delete the server with given uid"
    
    def list_server(self, uid):
        suid = 'server' + '.' + 'uid'
        self.collection.find({suid:uid})
        self.collection.find({'server.uid':'GMWa2j:127.0.0.1'})
        return "List the server with given uid"
    
    '''************************************Testing data will be  deleted later *************************************'''
    
    def flush(self):
        self.collection.remove()
        return "Empty the existing mongodb collection"
    
    server = {}
    test = {} 
    ''' It is the random generated data '''
    
    def get_random_word(self,wordLen):
        word = ''
        for i in range(wordLen):
            word += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
        return word
   
   
    '''Returns a dict object for testing purposes'''
    def populatedata(self):
    
        '''
        To insert the dummy data into the dict data structure.
        
        To get the IP address, I am getting it by using the command
        
        " ifconfig lo | grep 'inet addr' | cut -d: -f2 | awk '{print $1}' "
        
        Currently I am getting the data from system by using commands.getoutput on linux commands but it is deprecated since python 2.6 
        So might want to check if or not to use it
        
        '''
        get_ip =  " ifconfig lo | grep 'inet addr' | cut -d: -f2 | awk '{print $1}' "
        self.test['ip_address'] = commands.getoutput(get_ip)
        get_server_name = "hostname"
        #self.test['name'] =  commands.getoutput(get_server_name)
        self.test['name'] =  self.get_random_word(6)
        '''Server UID is HostName - IP address'''
        self.test['uid'] = str(self.test['name']) + ':' + str(self.test['ip_address'])
        
        '''For now both start time and stop time are one and the same'''
        time = "date +\"%T\" "
        self.test['start_time'] =  commands.getoutput(time)
        
        self.test['stop_time'] =  commands.getoutput(time)
        
        
        '''Populate the remaining fields with random entries for now'''
        self.test['type'] = self.get_random_word(6)
        self.test['label'] = self.get_random_word(6)
        self.test['keyword'] = self.get_random_word(6)
        self.server['server'] = self.test
        #print self.server
        '''
        name_list = ['eucalyptus', 'openstack', 'EC2']
        
        self.test['services'][0]['name'] = random.choice(name_list)
        self.test['services'][0]['type'] = self.get_random_word(3)
        self.test['services'][0]['version'] = random.randint(1,9)
        self.test['services'][0]['keyword'] = self.get_random_word(3)
        self.test['services'][0]['start_time'] = commands.getoutput(time)
        self.test['services'][0]['stop_time'] = commands.getoutput(time)
        self.test['services'][0]['status'] = self.get_random_word(3)
        '''
        self.write_server()
        return server

    
    
if __name__ == "__main__":
    myserver = server()   
    
    
    #myserver.flush()
    
    #myserver.populatedata()
    myserver.list_server('u1sR2J:127.0.0.1')
    '''
    #myserver.read_JSON( "name" , "jXXIJL") 
    myserver.update_server('GMWa2j:127.0.0.1', 'name' , 'viplav')
    #myserver.disconnectmdb()
    '''