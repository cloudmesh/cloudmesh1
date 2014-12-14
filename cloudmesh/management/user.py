from __future__ import print_function
from cloudmesh.config.cm_config import get_mongo_db, DBConnFactory
from cloudmesh.management.cloudmeshobject import CloudmeshObject
from cloudmesh.config.ConfigDict import ConfigDict
from cloudmesh_install import config_file
from mongoengine import *
import datetime
import json
from tabulate import tabulate

__docformat__ = 'restructuredtext en'


class User(CloudmeshObject):

    # Get a connection to Mongo

    get_mongo_db("manage", DBConnFactory.TYPE_MONGOENGINE)

    # Field that represent a User Object i.e. the fields
    # seen on the Web UI

    username = StringField(required=True, max_length=50, unique=True)  # Available
    status = StringField(required=True, default='pending')
    email = EmailField(required=True)
    password = StringField(required=True)
    title = StringField(required=True)
    first_name = StringField(required=True, max_length=50)
    last_name = StringField(required=True, max_length=50)
    phone = StringField(required=True)
    url = StringField(required=True)
    citizenship = StringField(required=True)
    bio = StringField(required=True)
    institution = StringField(required=True)
    institution_role = StringField(required=True)
    department = StringField(required=True)
    address = StringField(required=True)
    advisor = StringField(required=True)
    country = StringField(required=True)

    # Field hidden from the User

    date_created = DateTimeField(default=datetime.datetime.now())
    date_activated = DateTimeField(default=datetime.date(1900, 01, 01))
    date_removed = DateTimeField(default=datetime.date(1900, 01, 01))
    date_approved = DateTimeField(default=datetime.date(1900, 01, 01))

    def add(self, user):
        """
        Function to add the user object to Mongo
        :param user: User object
        """
        usr = User.objects(username=user.username)
        valid = usr.count() == 0
        if not valid:
            print("User name exists")
        else:
            print("User name does not exist")
            user.save()

    def remove(self, username):
        pass

    def list_all(self):
        """
        Function used to list details of all users
        """
        req_fields = ["username", "title", "first_name", "last_name", "email", "phone", "url", "citizenship", "bio",
                      "institution", "institution_role", "department", "advisor", "address", "status"]

        users_json = User.objects.only(*req_fields).to_json()
        users_dict = json.loads(users_json)
        self.display(users_dict)

    # Remove all users from mongo

    def clear(self):
        pass

    # Find a user from mongo

    def find(self, username=None):

        """
        :param username:
        :return: none
        """

        """
        Function used to find and display the details of the user
        if no name is specified, lists the details of all the users
        :param username: username
        """
        req_fields = ["username", "title", "first_name", "last_name", "email", "phone", "url", "citizenship", "bio",
                      "institution", "institution_role", "department", "advisor", "address", "status"]
        try:
            if username is None:
                user_json = User.objects.only(*req_fields).to_json()
                users_dict = json.loads(user_json)
                self.display(users_dict)
            else:
                user_json = User.objects(username=username).only(*req_fields).to_json()
                users_dict = json.loads(user_json)
                self.display(users_dict)
        except:
            print("Something went wrong")
        pass

    def display(self, dicts):

        """
        Function used to display a dict in tabular format.
        Works for a single dict or a list of dicts
        :param dicts: Dict of user details
        :return: None
        """

        values = []
        for entry in dicts:
            items = []
            headers = []
            for key, value in entry.iteritems():
                items.append(value)
                headers.append(key.replace('_', '').title())
            values.append(items)
        table_fmt = "orgtbl"
        table = tabulate(values, headers, table_fmt)
        try:
            separator = table.split("\n")[1].replace("|", "+")
        except:
            separator = "-" * 50
        print(separator)
        print(table)
        print(separator)


class Users(object):
    """
    Object to manage multiple users
    """

    def __init__(self):
        config = ConfigDict(filename=config_file("/cloudmesh_server.yaml"))
        # port = config['cloudmesh']['server']['mongo']['port']

        get_mongo_db("manage", DBConnFactory.TYPE_MONGOENGINE)
        self.users = User.objects()

    def get_unique_username(self, proposal):

        """
        Suggest a unique username from a proposal, achieved by appending a number at the end.
        :param proposal: Proposed username
        :return: String
        """

        new_proposal = proposal.lower()
        num = 1
        username = User.objects(username=new_proposal)
        while username.count() > 0:
            new_proposal = proposal + str(num)
            username = User.objects(username=new_proposal)
            num = num + 1
        return new_proposal

    def validate_email(self, email):

        """
        Check if the user's email is already used in the database
        :param email: user's email
        :return: boolean
        """

        user = User.objects(email=email)
        valid = user.count() == 0
        return valid

    def find(self, email=None):

        """
        Returns the user based on given email. If email is specified, search for the user with the specified
        email, else return details of all users
        :param email: email
        :return: User object or User objects
        """

        if email:
            found = User.objects(email=email)
            if found.count() > 0:
                return User.objects()[0]
            else:
                return None
        else:
            return User.objects()

    def add(self, user):

        """
        Add a user to the database
        :param user: User object
        :return:
        """

        user.username = self.get_unique_username(user.username)
        user.set_date_deactivate()
        if self.validate_email(user.email):
            user.save()
        else:
            print("ERROR: a user with the e-mail `{0}` already exists".format(user.email))

    def clear(self):
        """
        Remove all the users from the database
        :return:
        """

        for user in User.objects:
            user.delete()