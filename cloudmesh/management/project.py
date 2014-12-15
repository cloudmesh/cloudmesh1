from __future__ import print_function
from mongoengine import *
import uuid
from user import User, Users
# from comittee import Committee
from cloudmeshobject import CloudmeshObject
from cloudmesh.config.cm_config import get_mongo_db, DBConnFactory


def IMPLEMENT():
    print("IMPLEMENT ME")


STATUS = ('pending',
          'approved',
          'completed',
          'denied')

CATEGORY = ('Computer Science', 'Education',
            'Interoperability', 'Life Sciences',
            'Non Life Sciences', 'Technology Development',
            'Technology Evaluation')

DISCIPLINE = 'Other (000)'
# see https://ncsesdata.nsf.gov/nsf/srs/webcasp/data/gradstud.htm
# put in discipline.txt and initialize from there through reading the file and codes
#

INSTITUTE_ROLE = ('Undergraduate',
                  'Graduate Masters',
                  'Graduate PhD',
                  'Student Other',
                  'Faculty',
                  'Staff',
                  'Other')

CLUSTERS = ('india',
            'bravo',
            'echo',
            'delta',
            'other',
            'None')

SERVICES = ('eucalyptus',
            'openstack',
            'mpi',
            'hadoop',
            'mapreduce',
            'docker',
            'other',
            'None')

SOFTWARE = ('HPC', 'other')

PROVISIONING = ('vm',
                'baremetal',
                'container',
                'iaas',
                'paas',
                'other',
                'None')

GRANT_ORG = ('NSF',
             'DOE',
             'DoD',
             'NIH',
             'other',
             'None')

REQUIRED = False


class Project(CloudmeshObject):

    # Project Information

    title = StringField(required=REQUIRED)

    # Project vocabulary

    category = ListField(StringField(choices=CATEGORY), required=REQUIRED)
    keywords = ListField(StringField(), required=REQUIRED)

    # Project contacts

    # lead = ReferenceField(User)
    lead = StringField()
    managers = ListField(StringField())
    # members = ListField(ReferenceField(User))
    members = ListField(StringField())
    alumni = ListField(StringField())
    contact = StringField(required=REQUIRED)

    # Project Details

    orientation = StringField(required=REQUIRED)
    primary_discipline = StringField(choices=DISCIPLINE, required=REQUIRED)
    abstract = StringField(required=REQUIRED)
    intellectual_merit = StringField(required=REQUIRED)
    broader_impact = StringField(required=REQUIRED)
    url = URLField(required=REQUIRED)
    results = StringField()

    # Agreements

    agreement_use = BooleanField()
    agreement_slides = BooleanField()
    agreement_support = BooleanField()
    agreement_software = BooleanField()
    agreement_documentation = BooleanField()

    # Grant Information

    grant_organization = StringField(choices=GRANT_ORG)  # Should be a list of grants
    grant_id = StringField()
    grant_url = URLField()

    # Resource Requirements

    resources_services = ListField(
        StringField(choices=SERVICES), required=REQUIRED)
    resources_clusters = ListField(
        StringField(choices=CLUSTERS), required=REQUIRED)
    resources_provision = ListField(
        StringField(choices=PROVISIONING), required=REQUIRED)
    # resources_software = ListField(
    #     StringField(choices=SOFTWARE), required=REQUIRED)
    comment = StringField()
    use_of_fg = StringField(required=REQUIRED)
    scale_of_use = StringField(required=REQUIRED)

    # Other

    comments = StringField()

    # Project Membership Management

    join_open = BooleanField()
    join_notification = BooleanField()

    # Location

    loc_name = StringField(required=REQUIRED)
    loc_street = StringField(required=REQUIRED)
    loc_additional = StringField(required=REQUIRED)
    loc_state = StringField(required=REQUIRED)
    loc_country = StringField(required=REQUIRED)

    # Invisible fields

    active = BooleanField(required=REQUIRED)
    project_id = UUIDField()
    status = StringField(choices=STATUS, required=REQUIRED)


    def to_json(self):
        """prints the project as a json object"""

        d = {
            "title": self.title,
            "category": self.category,
            "keywords": self.keywords,  #
            "lead": self.lead,
            "managers": self.managers,
            "members": self.members,
            "alumni": self.alumni,
            "contact": self.contact,
            "orientation": self.orientation,
            "primary_discipline": self.primary_discipline,
            "abstract": self.abstract,
            "intellectual_merit": self.intellectual_merit,
            "broader_impact": self.broader_impact,
            "url": self.url,
            "results": self.results,
            "agreement_user": self.agreement_use,
            "agreement_slides": self.agreement_slides,
            "agreement_support": self.agreement_support,
            "agreement_software": self.agreement_support,
            "agreement_documentation": self.agreement_documentation,
            "grant_organization": self.grant_organization,
            "grant_id": self.grant_id,
            "grant_url": self.grant_url,
            "resources_services": self.resources_services,
            # "resources_software": self.resources_software,
            "resources_clusters": self.resources_clusters,
            "resources_provision": self.resources_provision,
            "comment": self.comment,
            "use_of_fg": self.use_of_fg,
            "scale_of_use": self.scale_of_use,
            "comments": self.comments,
            "join_open": self.join_open,
            "join_notification": self.join_notification,
            "loc_name": self.loc_name,
            "loc_street": self.loc_street,
            "loc_additional": self.loc_additional,
            "loc_state": self.loc_state,
            "loc_country": self.loc_country,

            "active": self.active,
            "status": self.status,


        }
        return d

    def __str__(self):
        '''
        printing the object as a string
        '''
        d = self.to_json()
        return str(d)


class Projects(object):
    '''
    convenience object to manage multiple projects
    '''

    def __init__(self):
        get_mongo_db("manage", DBConnFactory.TYPE_MONGOENGINE)
        self.projects = Project.objects()
        self.users = User.objects()

    def __str__(self):
        '''
        not implemented
        '''
        IMPLEMENT()

    def find(self):
        return Project.objects()

    def objects(self):
        '''
        returns the projects
        '''
        return Project.objects()

    def save(self, project):
        '''adds a project to the database but only after it has been verified

        :param project: the project id
        :type project: uuid
        '''
        project.save()

    def add_user(self, user_name, project, role):
        '''
        Adds a member to the project.

        :param role: the role of the user
        :type role: String
        :param user_name: the username
        :type user_name: String
        :param project: the project id
        :type project: uuid
        '''
        """adds members to a particular project"""
        users = User.objects(user_name=user_name)
        if users.count() == 1:
            if role == "member":
                project.members.append(users)
            elif role == "lead":
                project.lead.append(users)
            elif role == "lead":
                project.alumni.append(users)
        else:
            print("ERROR: The user `{0}` has not registered with FutureGrid".format(user_name))

    def find_users(self, project, role):
        '''returns all the members of a particular project

        :param role: the role of the user
        :type role: String
        :param project: the project id
        :type project: uuid
        '''
        if role == "member":
            return project.members
        elif role == "lead":
            return project.leads
        elif role == "lead":
            return project.alumni

    def find_by_id(self, id):
        '''
        finds projects by if

        :param id: the project id
        :type id: uuid
        '''
        """Finds a project by the given id"""
        found = Project.objects(project_id=id)
        if found.count() > 0:
            return found[0].to_json()
        else:
            return None
            # User ID or project ID

    def find_by_category(self, category):
        '''
        find the project by category

        :param category: the category
        :type category: String
        '''
        """Finds and returns all project in that category"""
        found = Project.objects(categories=category)
        if found.count() > 0:
            return found[0].to_json()
        else:
            return None

    def find_by_keyword(self, keyword):
        '''
        finds a projects matching a keyword

        :param keyword: a keyword
        :type keyword: String
        '''
        """Finds and returns all projects with the entered keyword"""
        found = Project.objects(keyword=keyword)
        if found.count() > 0:
            return found[0].to_json()
        else:
            return None

    def add(self, project):
        '''
        adds a project

        :param project: the username
        :type project: String
        '''
        print("PPPPPP", project)
        if not project.status:
            project.status = 'pending'
        if (project.project_id is None) or (project.project_id == ""):
            found = False
            proposed_id = None

            # while not found:
            # proposedid = uuid.uuid4()
            #    result = Project.objects(project_id=proposedid)
            #    print "PPPPP", result
            #    found = result.count() > 0
            #    print result.count()

            project.project_id = proposed_id
        else:
            print("UUUUUU -{0}-".format(project.project_id))
        print("UUID", project.project_id)
        project.save()

    def clear(self):
        """removes all projects from the database"""
        for project in Project.objects:
            project.delete()
