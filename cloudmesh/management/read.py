import yaml
from mongoengine import *
import datetime
import time
import hashlib
import uuid
import yaml
from pprint import pprint
from user import User, Users
from cloudmesh_management.generate import random_user
from cloudmesh_management.user import read_user


FILENAME = "/tmp/user.yaml"

connect('user', port=27777)

users = Users()

# Reads user information from file


def main():
    #    user = random_user()
    #    with open(FILENAME, "w") as f:
    #        f.write(user.yaml())

    print 70 * "="
    user = User()
    user = read_user(FILENAME)

    print 70 * "="
    pprint(user.json())
    user.save()

    user.update(**{"set__username": "Hallo"})
    user.save()
    print User.objects(username="Hallo")

if __name__ == "__main__":
    main()
