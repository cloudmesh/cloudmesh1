# generates test users and projects
from __future__ import print_function

from mongoengine import *
# from other.user_dict import *
from cloudmesh.management.user import User, Users
from cloudmesh.management.project import Project, Projects
import sys
from faker import Factory
import uuid
from pprint import pprint

from cloudmesh.config.cm_config import get_mongo_db, DBConnFactory

get_mongo_db("manage", DBConnFactory.TYPE_MONGOENGINE)


# ----------------------------------------------------------
# The generate class generates 10 random users
# ----------------------------------------------------------

users = Users()
projects = Projects()


# http://www.joke2k.net/faker/

fake = Factory.create()


def random_user():
    '''
    returns a random user in a dict

    :rtype: dict
    '''
    first_name = fake.first_name()
    data = User(
        username=first_name.lower(),
        email=fake.safe_email(),
        password=fake.word(),
        title=fake.prefix(),
        first_name=first_name,
        last_name=fake.last_name(),
        phone=fake.phone_number(),
        url=fake.url(),
        citizenship="US",
        bio=fake.paragraph(),
        institution=fake.company(),
        institution_role=fake.company_suffix(),
        department="IT",
        address=fake.address(),
        advisor=fake.name(),
        country="USA",
        status="pending",
        active=False,
    )
    return data


def generate_users(n):
    '''
    generates n random users in an array containing dicts for users

    :param n: number of users
    :type n: integer
    :rtype: array of dicts
    '''
    users.clear()
    for i in range(0, n):
        data = random_user()
        print(data)
        users.add(data)


def random_project():
    """generates a random project

    :rtype: dict
    """
    data = Project(
        title=fake.sentence()[:-1],
        category=['Education'],
        keywords=['sqllite'],
        leads=fake.name(),
        managers=[fake.name()],
        members=[fake.name()],
        alumni=[fake.name()],
        contact=fake.phone_number(),
        orientation="Research",
        primary_discipline="Other (000)",
        abstract=fake.paragraph(),
        intellectual_merit=fake.sentence(),
        broader_impact=fake.sentence(),
        url=fake.url(),
        results=fake.paragraph(),
        agreement_use=True,
        agreement_slide=True,
        agreement_support=True,
        agreement_software=True,
        agreement_documentation=True,
        grant_organization='NSF',
        grant_id=fake.building_number(),
        grant_url=fake.url(),
        resources_services=['hadoop', 'openstack'],
        resources_software=['other'],
        resources_clusters=['india'],
        resources_provision=['paas'],
        comment=fake.sentence(),
        use_of_fg=fake.sentence(),
        scale_of_use=fake.sentence(),
        comments=fake.sentence(),
        join_allow=True,
        join_notification=True,
        location_name=fake.name(),
        location_street=fake.street_address(),
        location_additional=fake.sentence(),
        location_state=fake.state() + "(" + fake.state_abbr() + ")",
        location_country=fake.country(),
        active=False,
        status="pending",
        project_id=uuid.uuid4(),
    )
    return data
    #projects.add_member("gregvon1", data)


def generate_projects(n):
    '''
    generates n random projects in an array containing dicts for users

    :param n: number of projects
    :type n: integer
    :rtype: array of dicts
    '''
    projects.clear()
    for i in range(0, n):
        data = random_project()
        print(data)
        projects.save(data)


def main():
    '''
    a test function to create 10 users and 3 projects
    '''

    generate_users(10)
    print(70 * "=")
    print(users.find())
    print(70 * "=")
    print(70 * "&")
    print(users.find()[0])

    generate_projects(3)
    projects_list = Project.objects()
    print(projects_list.count())
    pprint(projects_list[0])


if __name__ == "__main__":
    main()
