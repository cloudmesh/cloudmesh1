'''
Created on Aug 24, 2012
Improved May 2013 by Gregor
@author: Gregor von Laszewski, laszewski@gmail.com, vdkhadke
'''

#! /usr/bin/python

import json
import pymongo
from pymongo import Connection
import os
import commands
import random


class Inventory :
    '''To populate the dict data structure with relevant data'''

    hostname = 'localhost'
    port = 27017

    connection = ""
    data = {}
    db = ''

    ######################################################################
    # INITIALIZE
    ######################################################################
    
    def __init__ (self, hostname='localhost', port=27017):
        self.data = {}
        self.hostname = hostname
        self.port = port
        self.connect(self.hostname, self.port)

    ######################################################################
    # CONNECT
    ######################################################################

    def connect(self, hostname, port):
        '''connects to the database'''
        self.connection = Connection(hostname, port)
        try:
            self.db = self.connection.fg_inventorydbase
            collection = (self.db).entry
        except:
            print 'Cannot connect to the database'

    ######################################################################
    # DISCONNECT
    ######################################################################
    
    def disconnect(self):
        '''disconnects from the database'''
        self.connection.close()
    
    server = {}
    '''Removed the server field from dict structure, it is totally unnecessary since we include the contents in name,'''

    test = {        
                'ip_address':'',
                'name':'',
                'type':'',
                'label':'',
                'keyword':'',
                'uid':'',
                'start_time':'',
                'stop_time':''
                '''
                'services':[
                             {'name':'',
                              'type':'',
                              'version':'',
                              'keyword':'',
                              'start_time':'',
                              'stop_time':'',
                              'status':'',
                            }]
                '''
            }
            
    test_services = {
                      'name':'',
                      'type':'',
                      'version':'',
                      'keyword':'',
                      'start_time':'',
                      'stop_time':'',
                      'status':'',
                      } 

        

        
    def load(self, filename):
        '''loads the data from a file'''

        '''When you use "with" statement, you dont need to open and close the file streams it by default takes care of that '''
        with open(filename, 'r') as input:
            self.data = json.load(input)
    
    def write(self, filename):
        '''writes the database to a file'''
        with open(filename, 'w') as output:
            json.dump(self.data, output)
    
    def insertToDB(self):
        entry = self.db.entry
        #entry.insert(self.data)
        #Test is to insert a sample string in MongoDB
        entry.insert(self.test)
        print entry.find_one()
        
    def getServerData(self, uid):
        entry = (self.db).entry
        
        #To get individual entries from mongodb
        for each in entry.find({"uid":"PC:127.0.0.1"}):
            t = each
            print t
    
    def addAttributeUid(self, uid, attributeName, value):
        entry = db.entry
        
        for each in entry.find():
            db.entry.update({}, {'$set' : {"attribute" : "attr" }})
    
    def deleteUIDData(self, uid):
        '''Error in this data only single uid per data'''
        entry = db.entry        
        db.entry.remove({"uid" : uid})    
        print "Server deleted"
    

    ######################################################################
    # DELETE SERVER DATA
    ######################################################################
        
    def deleteServerData(self, servername):
        (self.db).entry.find()
        self.db.entry.remove({'keyword':'szt7XF'})    

    ######################################################################
    # INSERT DATA
    ######################################################################


    def insertData(self):
        '''Creating a random word generating method to populate the
        entries in the data structure.  To insert the dummy data into
        the dict data structure. To get the IP address, I am getting
        it by using the command
        
        " ifconfig lo | grep 'inet addr' | cut -d: -f2 | awk '{print $1}' "
        
        Currently I am getting the data from system by using commands.getoutput on linux commands but it is deprecated since python 2.6 
        So might want to check if or not to use it

        '''
        get_ip = " ifconfig lo | grep 'inet addr' | cut -d: -f2 | awk '{print $1}' "
        self.test['ip_address'] = commands.getoutput(get_ip)
        get_server_name = "hostname"
        self.test['name'] = commands.getoutput(get_server_name)
    
        '''Server UID is HostName - IP address'''
        self.test['uid'] = str(self.test['name']) + ':' + str(self.test['ip_address'])
        
        '''For now both start time and stop time are one and the same'''
        time = "date +\"%T\" "
        self.test['start_time'] = commands.getoutput(time)
        
        self.test['stop_time'] = commands.getoutput(time)
        
        
        '''Populate the remaining fields with random entries for now'''
        self.test['type'] = self.get_random_word(6)
        self.test['label'] = self.get_random_word(6)
        self.test['keyword'] = self.get_random_word(6)
        '''
        name_list = ['eucalyptus', 'openstack', 'EC2']
        
        self.test['services'][0]['name'] = random.choice(name_list)
        self.test['services'][0]['type'] = self.get_random_word(3)
        self.test['services'][0]['version'] = random.randint(1,9)
        self.test['services'][0]['keyword'] = self.get_random_word(3)
        self.test['services'][0]['start_time'] = commands.getoutput(time)
        self.test['services'][0]['stop_time'] = commands.getoutput(time)
        self.test['services'][0]['status'] = self.get_random_word(3)
        print self.test
        '''

    ######################################################################
    # INSERT SERVICES
    ######################################################################

    def insertServices(self, server):
        name_list = ['eucalyptus', 'openstack', 'EC2']
        self.test_services['name'] = random.choice(name_list)
        self.test_services['type'] = self.get_random_word(3)
        self.test_services['version'] = random.randint(1, 9)
        self.test_services['keyword'] = self.get_random_word(3)
        self.test_services['start_time'] = commands.getoutput("date +\"%T\" ")
        self.test_services['stop_time'] = commands.getoutput("date +\"%T\" ")
        self.test_services['status'] = self.get_random_word(3)
        
        self.test['services'].append(self.test_services)
        print self.test

    ######################################################################
    # DELETE SERVICES
    ######################################################################

    def deleteServices(self, server):
        
        for each in entry.find({'name':server}):
            print each["services"] 
            
            entry.update({ '$unset' : { 'start_time' : '14:30:25'}})
            #print "Server deleted"

    ######################################################################
    # RANDOM WORD
    ######################################################################


    def get_random_word(self, wordLen):
        '''Generates random words to fill the test data structure'''
        word = ''
        for i in range(wordLen):
            word += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
        return word
    

if __name__ == '__main__':
    
    Instance = Inventory()
    '''
    Instance.load("foo.txt")
    Instance.write("foo1.txt")
    ''',
    Instance.insertData()
    Instance.insertToDB()
    
    #Instance.getServerData("PC:127.0.0.1")
    #Instance.deleteServerData("PC")
    #Instance.deleteUIDData("PC:127.0.0.1")
    #Instance.insertData()
    #Instance.insertServices("PC")
    #Instance.insertToDB()
    #Instance.deleteServices("PC") 
    #Instance.disconnect()
