from mongoengine import *
import datetime, time
import hashlib, uuid
from pprint import pprint
#    mongod --noauth --dbpath . --port 27777
from cloudmeshobject import CloudmeshObject
import yaml

STATUS = ('pending', 'approved', 'blocked', 'denied')

port=27777

def IMPLEMENT():
    print "IMPLEMENT ME"
'''
def generate_password_hash(password)
    # maybe using passlib https://pypi.python.org/pypi/passlib
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512(password + salt).hexdigest()
    return hashed_password'''

def read_user(filename):
        stream = open(filename, 'r')
        data = yaml.load(stream)
        user = User(
                status = data["status"],            
                username = data["username"],
                title = data["title"],
                firstname = data["firstname"],
                lastname = data["lastname"],
                email = data["email"],
                url = data["url"],
                citizenship = data["citizenship"],
                bio = data["bio"],
                password = data["password"],
                userid = data["userid"],
                phone = data["phone"],
                projects = data["projects"],
                institution = data["institution"],
                department = data["department"],
                address = data["address"],
                country = data["country"],
                advisor = data["advisor"],
                message = data["message"],
        )
        return user

    
class User(CloudmeshObject):
    """This class is sued to represent a user"""

    def order(self):
        try:
            return [
                ("username", self.username),
                ("status", self.status),                
                ("title", self.title),
                ("firstname", self.firstname),
                ("lastname", self.lastname),
                ("email", self.email),
                ("url", self.url),
                ("citizenship", self.citizenship),
                ("bio", self.bio),
                ("password", self.password),
                ("phone", self.phone),
                ("projects", self.projects),
                ("institution", self.institution),
                ("department", self.department),
                ("address", self.address),
                ("country", self.country),                
                ("advisor", self.advisor),
                ("date_modified", self.date_modified),
                ("date_created", self.date_created),
                ("date_approved", self.date_approved),
                ("date_deactivated", self.date_deactivated),
            ]
        except:
            return None
    
    def hidden(self):
        return [
            "userid",
            "active",
            "message",
            ]
    #
    # User Information
    #
    status = StringField(required=True, default='pending')
    username = StringField(required=True)
    title = StringField()
    firstname = StringField(required=True)
    lastname = StringField(required=True)
    email = EmailField(required=True)
    url = StringField()
    citizenship = StringField(required=True)
    bio = StringField(required=True)
    password = StringField(required=True)
    userid = UUIDField()
    phone = StringField(required=True)
    
    projects = StringField() 
    #
    # Affiliation
    #
    institution = StringField(required=True)
    department = StringField(required=True)
    address = StringField(required=True)
    country = StringField(required=True)
    advisor = StringField()
    # advisor = pointer to another user
    
    #
    # Message received from either reviewers, 
    # committee or other users. It is a list because 
    # there might be more than one message
    #
    message = ListField(StringField())
    

    '''
    def save(self,db):
    	db.put({"firname":user.firname,...}_)
    '''


    def is_active(self):
        """finds if a user is active or not"""
        d1 = datetime.datetime.now()
        return (self.active == True) and (datetime.datetime.now() < self.date_deactivate)
        
    def set_password(self, password):
        #self.password_hash = generate_password_hash(password)
        pass
        
    def check_password(self, password):
        #return check_password_hash(self.password_hash, password)
        pass
        
    def json(self):
        """prints the user as a json object"""
        d = {}
        for (field, value) in self.order():
            try:
                d[field] = value
            except:
                pass
        return d
    
    def yaml(self):
        """prints the user as a json object"""
        return self.__str__(fields=True, all=True)
    """
    def __str__(self, fields=False, all=False):
        content = ""
        for (field, value)  in self.order():
            try:
                if not (value is None or value == "") or all:
                    if fields:
                        content = content + field + ": "
                    content = content + value + "\n"
            except:
                pass
        return content
    """
    
class Users(object):

    def __init__(self):
        db = connect('user', port=port)
        self.users = User.objects()
        
        meta = {"db_alias": "default"}

    def objects(self):
        return self.users
    
    def get_unique_username(self, proposal):
        """sets the username to the proposed username. if this name is taken, a
        number is added and checked if this new name is tacken, the first name
        with added number is used as a username
        """
        proposal = proposal.lower()
        num = 1
        same = True
        while (same == True):
            _username = User.objects(username=proposal)
            if _username.count() > 0:
                proposal = proposal + str(num)
                num = num + 1
            else:
                return proposal
                
    def add(self, user):
        """adds the specified user to mongodb, as well as activates the users' account
        as well as set's the deactivation date"""
        user.username = self.get_unique_username(user.username)
        user.set_date_deactivate()
        if self.validate(user):
            user.save()
        else:
            print "ERROR: a user with the e-mail `{0}` already exists".format(user.email)
            
    def validate(self, user):
        """verifies if the user can be added. Checks if the e-mail is unique. Returns true."""
        user = User.objects(email=user.email)
        valid = user.count() == 0
        return valid

    def find(self, email=None):
        """returns the users based on the given query"""
        if email == None:
            return User.objects()
    	else:
            found = User.objects(email=email)
            if found.count() > 0:
                return User.objects()[0]
            else:
                return None
            
    def find_user(self, username):
    	"""returns a user based on the username"""
        return User.object(username=username)
    	    	
    def clear(self):
        """removes all elements form the mongo db that are users"""
        for user in User.objects:
            user.delete()

def verified_email_domain(email):

    domains = ["indiana.edu"]

    for domain in domains:
        if email.endswith():
            return True
    return False
    
