from mongoengine import *
#from other.user_dict import *
from user import User, Users
from project import Project, Projects
import sys
from faker import Factory
import uuid

connect ('user', port=27777)

#----------------------------------------------------------
#	The generate class generates 10 random users
#----------------------------------------------------------

users = Users()
projects = Projects()


# http://www.joke2k.net/faker/

fake = Factory.create()

def random_user():
    firstname = fake.first_name()    
    data = User(
        status = "pending",
        title = fake.prefix(),
        firstname = firstname,
        lastname = fake.last_name(),
        email = fake.safe_email(),
        username = firstname.lower(),
        active = False,
        password = fake.word(),
        phone = fake.phone_number(),
        department = "IT",
        institution = fake.company(),
        address = fake.address(),
        country = "USA",
        citizenship = "US",
        bio = fake.paragraph(),
    )
    return data


def generate_users(n):
    users.clear()
    for i in range(0,n):
        data = random_user()
        print data
        users.add(data)    


def random_project():
    """generates a random project"""
    data = Project(
    	    title = fake.sentence()[:-1],
            projectid = uuid.uuid4(),
    	    abstract = fake.paragraph(),
            intellectual_merit = fake.paragraph(),
            broader_impact = fake.paragraph(),
            use_of_fg = fake.paragraph(),
            scale_of_use = fake.paragraph(),
            categories = ['FutureGrid'],
            keywords = ['sqllite'],
            primary_discipline = "other",  
            orientation = "Lot's of all make",
            contact = fake.name() +"\n" + fake.address(),
            url = fake.url(),
            active = False,
            status = "pending",
            resources_services = ['hadoop','openstack'],
            resources_software = ['other'],
            resources_clusters = ['india'],
            resources_provision = ['paas']
          )
    return data
    #projects.add_member("gregvon1", data)
    


def generate_projects(n):
    projects.clear()
    for i in range(0,n):
        data = random_project()
        print data
        projects.add(data)    
    

def main():

    generate_users(10)
    generate_projects(3)    

    print 70 * "="
    print users.find()
    print 70 * "="    
    print projects.find()

    print 70* "&"
    print users.find()[0]
        

if __name__ == "__main__":
    main()
