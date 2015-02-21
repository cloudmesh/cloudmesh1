from cloudmesh.config.cm_config import get_mongo_db, get_mongo_dbname_from_collection, DBConnFactory
from cloudmesh.management.cloudmeshobject import CloudmeshObject
from cloudmesh.config.ConfigDict import ConfigDict
from cloudmesh_install import config_file
from mongoengine import *
from tabulate import tabulate
import datetime
import json
import sys
import pprint
import yaml


STATUS = ('pending', 'approved', 'blocked', 'denied')


def IMPLEMENT():
    print "IMPLEMENT ME"
'''
def generate_password_hash(password)
    # maybe using passlib https://pypi.python.org/pypi/passlib
    salt = uuid.uuid4().hex
    hashed_password = hashlib.sha512(password + salt).hexdigest()
    return hashed_password'''


def read_user(filename):
    '''
    reads user data from a yaml file

    :param filename: The file anme
    :type filename: String of the path
    '''
    stream = open(filename, 'r')
    data = yaml.load(stream)
    user = User(
        status=data["status"],
        username=data["username"],
        title=data["title"],
        firstname=data["firstname"],
        lastname=data["lastname"],
        email=data["email"],
        url=data["url"],
        citizenship=data["citizenship"],
        bio=data["bio"],
        password=data["password"],
        userid=data["userid"],
        phone=data["phone"],
        projects=data["projects"],
        institution=data["institution"],
        department=data["department"],
        address=data["address"],
        country=data["country"],
        advisor=data["advisor"],
        message=data["message"],
    )
    return user


class User(CloudmeshObject):

    """
    This class is used to represent a Cloudmesh User
    """

    dbname = get_mongo_dbname_from_collection("manage")
    if dbname:
        meta = {'db_alias': dbname}
    #
    # defer the connection to where the object is instantiated
    # get_mongo_db("manage", DBConnFactory.TYPE_MONGOENGINE)

    """
    User fields
    """

    username = StringField(required=True)
    email = EmailField(required=True)
    password = StringField(required=True)
    confirm = StringField(required=True)
    title = StringField(required=True)
    firstname = StringField(required=True)
    lastname = StringField(required=True)
    phone = StringField(required=True)
    url = StringField(required=True)
    citizenship = StringField(required=True)
    bio = StringField(required=True)
    institution = StringField(required=True)
    institutionrole = StringField(required=True)
    department = StringField(required=True)
    address = StringField(required=True)
    advisor = StringField(required=True)
    country = StringField(required=True)

    """
    Hidden fields
    """

    status = StringField(required=True, default='pending')
    userid = UUIDField()
    projects = StringField()

    """
    Message received from either reviewers,
    committee or other users. It is a list because
    there might be more than one message
    """

    message = ListField(StringField())

    def order(self):
        """
        Order the attributes to be printed in the display
        method
        """
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

    @classmethod
    def hidden(cls):
        """
        Hidden attributes
        """
        return [
            "userid",
            "active",
            "message",
        ]


    # def save(self,db):
    # 	db.put({"firname":user.firname,...})

    def is_active(self):
        '''
        check if the user is active
        '''
        """finds if a user is active or not"""
        d1 = datetime.datetime.now()
        return (self.active == True) and (datetime.datetime.now() < self.date_deactivate)

    @classmethod
    def set_password(cls, password):
        '''
        not implemented

        :param password:
        :type password:
        '''
        #self.password_hash = generate_password_hash(password)
        pass

    @classmethod
    def check_password(cls, password):
        '''
        not implemented

        :param password:
        :type password:
        '''
        # return check_password_hash(self.password_hash, password)
        pass

    def json(self):
        '''
        returns a json representation of the object
        '''
        """prints the user as a json object"""
        d = {}
        for (field, value) in self.order():
            try:
                d[field] = value
            except:
                pass
        return d

    def yaml(self):
        '''
        returns the yaml object of the object.
        '''
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

    """
    convenience object to manage several users
    """

    def __init__(self):
        config = ConfigDict(filename=config_file("/cloudmesh_server.yaml"))
        port = config['cloudmesh']['server']['mongo']['port']

        #db = connect('manage', port=port)
        self.users = User.objects()

        dbname = get_mongo_dbname_from_collection("manage")
        if dbname:
            meta = {'db_alias': dbname}

#         get_mongo_db("manage", DBConnFactory.TYPE_MONGOENGINE)

    @classmethod
    def objects(cls):
        """
        returns the users
        """
        return cls.users

    @classmethod
    def get_unique_username(cls, proposal):
        """
        gets a unique username form a proposal. This is achieved whil appending a number at the end. if the

        :param proposal: the proposed username
        :type proposal: String
        """
        new_proposal = proposal.lower()
        num = 1
        username = User.objects(username=new_proposal)
        while username.count() > 0:
            new_proposal = proposal + str(num)
            username = User.objects(username=new_proposal)
            num = num + 1
        return new_proposal

    @classmethod
    def add(cls, user):
        """
        adds a user

        :param user: the username
        :type user: String
        """
        user.username = cls.get_unique_username(user.username)
        user.set_date_deactivate()
        if cls.validate_email(user.email):
            user.save()
        else:
            print "ERROR: a user with the e-mail `{0}` already exists".format(user.email)

    @classmethod
    def delete_user(cls, user_name=None):
        if user_name:
            try:
                user=User.objects(username=user_name)
                if user:
                    user.delete()
                else:
                    print "Error: User with the name '{0}' does not exist.".format(user_name)
            except:
                print "Oops! Something went wrong while trying to remove a user", sys.exc_info()[0]
        else:
            print "Error: Please specity the user to be removed"
    
    @classmethod
    def amend_user_status(self, user_name=None, status=None):
        if user_name:
            try:
                user=User.objects(username=user_name)
                if user:
                    user.status=status
                    user.save()
            except:
                print "Oops! Something went wrong while trying to amend user status", sys.exc_info()[0]
        else:
            print "Error: Please specity the user to be amended"

    @classmethod
    def validate_email(cls, email):
        """
        verifies if the email of the user is not already in the users.

        :param user: user object
        :type user: User
        :rtype: Boolean
        """
        user = User.objects(email=email)
        valid = user.count() == 0
        return valid

    @classmethod
    def find(cls, email=None):
        """
        returns the users based on the given query.
        If no email is specified all users are returned.
        If the email is specified we search for the user with the given e-mail.

        :param email: email
        :type email: email address
        """
        if email is None:
            return User.objects()
        else:
            found = User.objects(email=email)
            if found.count() > 0:
                return User.objects()[0]
            else:
                return None

    @classmethod
    def find_user(cls, username):
        """
        returns a user based on the username

        :param username:
        :type username:
        """
        return User.object(username=username)

    @classmethod
    def clear(cls):
        """removes all elements form the mongo db that are users"""
        for user in User.objects:
            user.delete()
            

    @classmethod
    def list_users(cls, disp_fmt=None, username=None):
        req_fields = ["username", "title", "firstname", "lastname",
                      "email", "phone", "url", "citizenship",
                      "institution", "institutionrole", "department",
                      "advisor", "address", "status"]
        try:
            if username is None:
                user_json = User.objects.only(*req_fields).to_json()
                user_dict = json.loads(user_json)
                if disp_fmt != 'json':
                    cls.display(user_dict, username)
                else:
                    cls.display_json(user_dict, username)
            else:
                user_json = User.objects(username=username).only(*req_fields).to_json()
                user_dict = json.loads(user_json)
                if disp_fmt != 'json':
                    cls.display(user_dict, username)
                else:
                    cls.display_json(user_dict, username)
        except:
            print "Oops.. Something went wrong in the list users method", sys.exc_info()[0]
        pass

    @classmethod
    def display(cls, user_dicts=None, user_name=None):
        if bool(user_dicts):
            values = []
            for entry in user_dicts:
                items = []
                headers = []
                for key, value in entry.iteritems():
                    items.append(value)
                    headers.append(key.replace('_',' ').title())
                values.append(items)
            table_fmt = "orgtbl"
            table = tabulate(values, headers, table_fmt)
            separator = ''
            try:
                seperator = table.split("\n")[1].replace("|", "+")
            except:
                separator = "-" * 50
            print separator
            print table
            print separator
        else:
            if user_name:
                print "Error: No user in the system with name '{0}'".format(user_name)
                
                
    @classmethod
    def display_json(cls, user_dict=None, user_name=None):
        if bool(user_dict):
            # pprint.pprint(user_json)
            print json.dumps(user_dict, indent=4)
        else:
            if user_name:
                print "Error: No user in the system with name '{0}'".format(user_name)


def verified_email_domain(email):
    """
    not yet implemented. Returns true if the a-mail is in a specified domain.

    :param email:
    :type email:
    """
    domains = ["indiana.edu"]

    for domain in domains:
        if email.endswith():
            return True
    return False
