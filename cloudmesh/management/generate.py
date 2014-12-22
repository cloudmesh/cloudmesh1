# generates test users and projects

from mongoengine import *
#from other.user_dict import *
from cloudmesh.management.user import User, Users
from cloudmesh.management.project import Project, Projects
import sys
from faker import Factory
import uuid
from pprint import pprint

from cloudmesh.config.cm_config import get_mongo_db, DBConnFactory
get_mongo_db("manage", DBConnFactory.TYPE_MONGOENGINE)


#----------------------------------------------------------
#	The generate class generates 10 random users
#----------------------------------------------------------

users = Users()
projects = Projects()


# http://www.joke2k.net/faker/

fake = Factory.create()


def random_user():
    '''
    returns a random user in a dict

    :rtype: dict
    '''
    firstname = fake.first_name()
    data = User(
        status="pending",
        title=fake.prefix(),
        firstname=firstname,
        lastname=fake.last_name(),
        email=fake.safe_email(),
        username=firstname.lower(),
        active=False,
        password=fake.word(),
        phone=fake.phone_number(),
        department="IT",
        institution=fake.company(),
        institution_role="Graduate Student",
        address=fake.address(),
        country="USA",
        citizenship="US",
        bio=fake.paragraph(),
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
        print data
        users.add(data)


def random_project():
    """generates a random project

    :rtype: dict
    """
    data = Project(
        title=fake.sentence()[:-1],
        categories=['FutureGrid'],
        keywords=['sqllite'],
        contact=fake.name() + "\n" + fake.address(),
        orientation="Lot's of all make",
        primary_discipline="other",
        projectid=uuid.uuid4(),
        abstract=fake.paragraph(),
        intellectual_merit=fake.paragraph(),
        broader_impact=fake.paragraph(),
        url=fake.url(),
        results=fake.sentence(),
        grant_organization="NSF",
        grant_id="1001",
        grant_url=fake.url(),
        resources_services=['hadoop', 'openstack'],
        resources_software=['other'],
        resources_clusters=['india'],
        resources_provision=['paas'],
        comment=fake.sentence(),
        use_of_fg=fake.paragraph(),
        scale_of_use=fake.paragraph(),
        comments=fake.sentence(),
        loc_name=fake.country(),
        loc_street=fake.street_name(),
        loc_additional="None",
        loc_state=fake.state(),
        loc_country=fake.country(),
        active=False,
        status="pending"

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
        print data
        projects.save(data)


def main():
    '''
    a test function to create 10 users and 3 projects
    '''

    generate_users(10)
    generate_projects(3)

    print 70 * "="
    print users.find()
    print 70 * "="
    print 70 * "&"
    print users.find()[0]

    projects = Project.objects()
    print projects.count()
    pprint(projects[0])


if __name__ == "__main__":
    main()
