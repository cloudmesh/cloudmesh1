from __future__ import print_function
from cloudmesh.config.cm_config import get_mongo_db, DBConnFactory
from cloudmesh.management.cloudmeshobject import CloudmeshObject
import mongoengine
import datetime
import json
from tabulate import tabulate


class User(CloudmeshObject):
    """
    class is used to model a user with its properties.
    """
    get_mongo_db("manage", DBConnFactory.TYPE_MONGOENGINE)

    # Field that represent a User Object i.e. the fields
    # seen on the Web UI

    username = mongoengine.StringField(required=True, max_length=50,
                                       unique=True)
    status = mongoengine.StringField(required=True, default='pending')
    email = mongoengine.EmailField(required=True)
    password = mongoengine.StringField(required=True)
    title = mongoengine.StringField(required=True)
    first_name = mongoengine.StringField(required=True, max_length=50)
    last_name = mongoengine.StringField(required=True, max_length=50)
    phone = mongoengine.StringField(required=True)
    url = mongoengine.StringField(required=True)
    citizenship = mongoengine.StringField(required=True)
    bio = mongoengine.StringField(required=True)
    institution = mongoengine.StringField(required=True)
    institution_role = mongoengine.StringField(required=True)
    department = mongoengine.StringField(required=True)
    address = mongoengine.StringField(required=True)
    advisor = mongoengine.StringField(required=True)
    country = mongoengine.StringField(required=True)

    # Field hidden from the User

    date_created = \
        mongoengine.DateTimeField(default=datetime.datetime.now())
    date_activated = \
        mongoengine.DateTimeField(default=datetime.date(1900, 01, 01))
    date_removed = \
        mongoengine.DateTimeField(default=datetime.date(1900, 01, 01))
    date_approved = \
        mongoengine.DateTimeField(default=datetime.date(1900, 01, 01))

    @classmethod
    def add(cls, user):

        """
        Function to add the user object to Mongo
        :param user: User object
        """
        usr = User.objects(username=user.username)
        valid = usr.count() == 0
        if not valid:
            print("User name exists")
        else:
            user.save()

    @classmethod
    def remove(cls, username):
        pass

    @classmethod
    def list_all(cls):
        """
        Function used to list details of all users
        """
        req_fields = ["username", "title", "first_name", "last_name",
                      "email", "phone", "url", "citizenship", "bio",
                      "institution", "institution_role", "department",
                      "advisor", "address", "status"]

        users_json = User.objects.only(*req_fields).to_json()
        users_dict = json.loads(users_json)
        cls.display(users_dict)

    @classmethod
    def clear(cls):
        pass

    # Find a user from mongo

    @classmethod
    def find(cls, username=None):

        """
        Function used to find and display the details of the user
        if no name is specified, lists the details of all the users
        :param username:
        :return: none
        """
        req_fields = ["username", "title", "first_name", "last_name",
                      "email", "phone", "url", "citizenship", "bio",
                      "institution", "institution_role", "department",
                      "advisor", "address", "status"]
        try:
            if username is None:
                user_json = User.objects.only(*req_fields).to_json()
                users_dict = json.loads(user_json)
                cls.display(users_dict)
            else:
                user_json = User.objects(username=username) \
                    .only(*req_fields).to_json()
                users_dict = json.loads(user_json)
                cls.display(users_dict)
        except:
            print("Something went wrong")

    @classmethod
    def display(cls, dicts):

        """
        Function used to display a dict in tabular format.
        Works for a single dict or a list of dicts
        :param dicts: Dict of user details
        :return: None
        """

        values = []
        headers = []
        for entry in dicts:
            items = []
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
        get_mongo_db("manage", DBConnFactory.TYPE_MONGOENGINE)
        self.users = User.objects()

    @classmethod
    def get_unique_username(cls, proposal):

        """
        Suggest a unique username from a proposal, achieved
        by appending a number at the end.
        :param proposal: Proposed username
        :return: String
        """

        new_proposal = proposal.lower()
        num = 1
        username = User.objects(username=new_proposal)
        while username.count() > 0:
            new_proposal = proposal + str(num)
            username = User.objects(username=new_proposal)
            num += 1
        return new_proposal

    @classmethod
    def validate_email(cls, email):

        """
        Check if the user's email is already used in the database
        :param email: user's email
        :return: boolean
        """

        user = User.objects(email=email)
        valid = user.count() == 0
        return valid

    @classmethod
    def find(cls, email=None):

        """
        Returns the user based on given email.
        If email is specified, search for the user with the specified
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

    @classmethod
    def add(cls, user):

        """
        Add a user to the database
        :param user: User object
        :return:
        """

        user.username = cls.get_unique_username(user.username)
        user.set_date_deactivate()
        if cls.validate_email(user.email):
            user.save()
        else:
            print("ERROR: a user with the e-mail `{0}` already exists"
                  .format(user.email))

    @classmethod
    def clear(cls):
        """
        Remove all the users from the database
        :return:
        """

        for user in User.objects:
            user.delete()
