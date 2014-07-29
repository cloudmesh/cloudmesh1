import datetime, time
from mongoengine import Document
from mongoengine import *

from mongoengine import fields

duration_in_weeks = 24

class CloudmeshObject(Document):
    '''
    An Object for managing users and projects that includes default methods for
    activation, cration and modification dates.
    
    In future we will have a modification trace record here also. Arbitrary
    attributes can be added and modified with the set_attribute method
    '''

    active = BooleanField(default = False) 
    date_modified = DateTimeField(default=datetime.datetime.now)
    date_created = DateTimeField()
    date_approved = None 
    date_deactivated = DateTimeField()

    meta = {'allow_inheritance': True}

    def set_attribute(self, attribute, value):
        '''
        sets the attribute to the given value
        
        :param attribute: the attribute name
        :type attribute: String
        :param value: the value
        :type value: String
        '''
        self._data[attribute] = value 

    def set_from_dict(self, d):
        '''
        sets a number of attributes contained within a key, value dict
        
        :param d:
        :type d:
        '''
        for key in d:
            self.set_attribute(key, d[key])
        
    def fields(self, kind=None):
        '''
        lists the attributes. One can select optional, required and all attributes
        
        :param kind: optional, required, all
        :type kind: String
        '''
        if kind is None or kind in ["all"]:
            return [k for k,v in self._fields.iteritems()]
        elif kind in ["optional"]:
            return [k for k,v in self._fields.iteritems() if not v.required]
        elif kind in ["required"]:
            return [k for k,v in self._fields.iteritems() if v.required]    

    def activate(self, state=True): 
        '''
        activates the object
        
        :param state: the state. True if active
        :type state: Boolean
        '''
    	"""activates a user"""
        self.active = state

    def deactivate(self):
        '''
        deactivates an object.         
        '''
    	self.activate(state=False)
            
    def set_date_deactivate(self, weeks=duration_in_weeks): 
        '''
        deactivates the object after some duration specified as parameter.
        
        TODO: use readable times ... not just weeks
        
        :param weeks: number of weeks
        :type weeks: integer
        '''
    	self.date_deactivate = datetime.datetime.now() + datetime.timedelta(weeks=weeks)
        #self.activate()
    	return self.date_deactivate

    def save(self, *args, **kwargs):
        '''
        saves the object to the database
        '''
        if not self.date_created:
            self.date_created = datetime.datetime.now()
        self.date_modified = datetime.datetime.now()
        return super(CloudmeshObject, self).save(*args, **kwargs)
        
