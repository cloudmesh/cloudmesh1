from __future__ import print_function
from new_user import User
import uuid
from mongoengine import *
import json
import prettytable
from cloudmeshobject import order, make_form_list

# connect('cloudmesh', host='localhost', port=29017)

def main():
    user_object = User(
        user_id=uuid.uuid4(),
        username="aravindhvaradharaju",
        email="avaradha@indiana.edu",
        password="testing@123",
        title="Mr.",
        first_name="Aravindh",
        last_name="Varadharaju",
        phone="8123693537",
        url="google.com",
        citizenship="Indian",
        bio="Graduate student",
        institution="IUB",
        institution_role="Graduate Student",
        department="SOIC",
        address="Test Address",
        advisor="Test Advisor",
        country="India"
    )

    # print (user_object.username)
    # user_object.add(user_object)
    #user_object.save()
    user_object.list_all()
    user_object.find('avaradha')


if __name__ == "__main__":
    main()