'''
Created on Aug 24, 2012

@author: vdkhadke
'''

#! /usr/bin/python

import json
import pymongo
from pymongo import Connection
import os
import commands
import random

class fgInventory :

    data = {}
    
    '''To populate the dict data structure with relevant data'''
    
    '''To generate random words to fill the test data structure'''
    def get_random_word(self,wordLen):
        word = ''
        for i in range(wordLen):
            word += random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')
        return word
    
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
                'stop_time':'',
                'services':[
                             {'name':'',
                              'type':'',
                              'version':'',
                              'keyword':'',
                              'start_time':'',
                              'stop_time':'',
                              'status':'',
                            }]
            }
            
    test_services =  {
                      'name':'',
                      'type':'',
                      'version':'',
                      'keyword':'',
                      'start_time':'',
                      'stop_time':'',
                      'status':'',
                      } 

    def __init__ (self):
        self.data = {}
        
    '''When you use "with" statement, you dont need to open and close the file streams it by default takes care of that '''
        
    def load(self, filename):
        with open(filename, 'r') as input:
            self.data = json.load(input)
    
    def mongoConnectionOpen(self):
        connection = Connection('localhost', 27017)
        try:
            db = connection.fg_inventorydbase
            collection = db.inventory_collection
        except ConnectionFailure:
            print 'Cannot connect to the database'
    
    def write(self, filename):
        with open(filename, 'w') as output:
            json.dump(self.data, output)
    
    
    def insertToDB(self):
        connection = Connection('localhost', 27017)
        try:
            db = connection.fg_inventorydbase
            collection = db.inventory_collection
        except ConnectionFailure:
            print 'Cannot connect to the database'
        
        entry= db.entry
        #entry.insert(self.data)
        
        #Test is to insert a sample string in MongoDB
        entry.insert(self.test)
        print entry.find_one()
        connection.close()
    
    def getServerData(self, uid):
        connection = Connection('localhost', 27017)
        try:
            db = connection.fg_inventorydbase
            collection = db.inventory_collection
        except ConnectionFailure:
            print 'Cannot connect to the database'
        entry = db.entry
        
        #To get individual entries from mongodb
        for each in entry.find({"uid":"vdkhadke-PC:127.0.0.1"}):
            t = each
            print t
        connection.close()
    
    
    def addAttributeUid(self, uid, attributeName, value):
        connection = Connection('localhost', 27017)
        try:
            db = connection.fg_inventorydbase
            collection = db.inventory_collection
        except ConnectionFailure:
            print 'Cannot connect to the database'
        
        entry = db.entry
        
        for each in entry.find({"uid":uid}):
            db.entry.update({'uid' : uid},{'$set' : {"attribute" : "attr" }})
        
        connection.close()   
    
    
    def deleteUIDData(self, uid):
        connection = Connection('localhost', 27017)
        try:
            db = connection.fg_inventorydbase
            collection = db.inventory_collection
        except ConnectionFailure:
            print 'Cannot connect to the database'
        
        entry = db.entry
        for each in entry.find({"uid":uid}):
            db.entry.remove()    
            print "Server deleted"
        connection.close()
        
        
    def deleteServerData(self, servername):
        connection = Connection('localhost', 27017)
        try:
            db = connection.fg_inventorydbase
            collection = db.inventory_collection
        except ConnectionFailure:
            print 'Cannot connect to the database'
        
        entry = db.entry
        for each in entry.find({'name':servername}):
            db.entry.remove()    
            print "Server deleted"
        connection.close()
    
    
    '''Creating a random word generating method to populate the entries in the data structure'''
        
    
    def insertData(self):
        
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
        self.test['name'] =  commands.getoutput(get_server_name)
    
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
        
        name_list = ['eucalyptus', 'openstack', 'EC2']
        
        self.test['services'][0]['name'] = random.choice(name_list)
        self.test['services'][0]['type'] = self.get_random_word(3)
        self.test['services'][0]['version'] = random.randint(1,9)
        self.test['services'][0]['keyword'] = self.get_random_word(3)
        self.test['services'][0]['start_time'] = commands.getoutput(time)
        self.test['services'][0]['stop_time'] = commands.getoutput(time)
        self.test['services'][0]['status'] = self.get_random_word(3)
        print self.test
        
    def insertServices(self, server):
        name_list = ['eucalyptus', 'openstack', 'EC2']
        self.test_services['name'] = random.choice(name_list)
        self.test_services['type'] = self.get_random_word(3)
        self.test_services['version'] = random.randint(1,9)
        self.test_services['keyword'] = self.get_random_word(3)
        self.test_services['start_time'] = commands.getoutput("date +\"%T\" ")
        self.test_services['stop_time'] = commands.getoutput("date +\"%T\" ")
        self.test_services['status'] = self.get_random_word(3)
        
        self.test['services'].append(self.test_services)
        print self.test
        
    def deleteServices(self, server):
        connection = Connection('localhost', 27017)
        try:
            db = connection.fg_inventorydbase
            collection = db.inventory_collection
        except ConnectionFailure:
            print 'Cannot connect to the database'
        
        entry = db.entry
        for each in entry.find({'name':server}):
            print each["services"] 
            print "*" * 10
            db.entry.update({},{ $unset : { 'start_time' : '14:30:25'}})
            #print "Server deleted"
        connection.close()
        
            
if __name__ == '__main__':
    
    Instance = fgInventory()
    '''
    Instance.load("foo.txt")
    Instance.write("foo1.txt")
    '''
    
    #Instance.insertToDB()
    #Instance.getServerData("vdkhadke-PC:127.0.0.1")
    #Instance.deleteServerData("vdkhadke-PC")
    #Instance.deleteUIDData("vdkhadke-PC:127.0.0.1")
    #Instance.insertData()
    #Instance.insertServices("vdkhadke-PC")
    #Instance.insertToDB()
    Instance.deleteServices("vdkhadke-PC") 
    