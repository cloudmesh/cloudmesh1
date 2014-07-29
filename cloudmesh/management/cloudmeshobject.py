import datetime, time
from mongoengine import Document
from mongoengine import *

from mongoengine import fields

duration_in_weeks = 24

class CloudmeshObject(Document):

    active = BooleanField(default = False) 
    date_modified = DateTimeField(default=datetime.datetime.now)
    date_created = DateTimeField()
    date_approved = None 
    date_deactivated = DateTimeField()

    meta = {'allow_inheritance': True}

    def set_attribute(self, attribute, value):
        self._data[attribute] = value 

    def set_from_dict(self, d):
        for key in d:
            self.set_attribute(key, d[key])
        
    def fields(self, kind=None):
        if kind is None or kind in ["all"]:
            return [k for k,v in self._fields.iteritems()]
        elif kind in ["optional"]:
            return [k for k,v in self._fields.iteritems() if not v.required]
        elif kind in ["required"]:
            return [k for k,v in self._fields.iteritems() if v.required]    

    def activate(self, state=True): 
    	"""activates a user"""
        self.active = state

    def deactivate(self):
    	"""deactivates a user after the date to deactivate has been reached"""
    	self.activate(state=False)
            
    def set_date_deactivate(self, weeks=duration_in_weeks): 
    	"""Sets the date for the user to be deactivated by a default time"""
    	self.date_deactivate = datetime.datetime.now() + datetime.timedelta(weeks=weeks)
        #self.activate()
    	return self.date_deactivate

    def save(self, *args, **kwargs):
        if not self.date_created:
            self.date_created = datetime.datetime.now()
        self.date_modified = datetime.datetime.now()
        return super(CloudmeshObject, self).save(*args, **kwargs)
        
