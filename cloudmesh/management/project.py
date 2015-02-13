from mongoengine import *
from mongoengine.context_managers import switch_db
from datetime import datetime
import hashlib
import uuid
from user import User, Users
# from comittee import Committee
from pprint import pprint
from cloudmeshobject import CloudmeshObject
from cloudmesh.config.ConfigDict import ConfigDict
from cloudmesh_install import config_file
from cloudmesh.config.cm_config import get_mongo_db, get_mongo_dbname_from_collection, DBConnFactory


def IMPLEMENT():
    print "IMPLEMENT ME"

STATUS = ('pending',
          'approved',
          'completed',
          'denied')

CATEGORY = ('Database', 'FutureGrid', 'other')

DISCIPLINE = ('other')
# see https://ncsesdata.nsf.gov/nsf/srs/webcasp/data/gradstud.htm
# put in discipline.txt and initialize from there through reading the file and codes
#

INSTITUTE_ROLE = ('gaduate student',
                  'undergraduate student',
                  'staff',
                  'faculty',
                  'visitor',
                  'other')

CLUSTERS = ('india',
            'bravo',
            'echo',
            'delta',
            'other', 'None')

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
                'other', 'None')

GRANT_ORG = ('NSF',
             'DOE',
             'DoD',
             'NIH',
             'other', 'None')


REQUIRED = False


class Project(CloudmeshObject):
    # named connection (not 'default')
    dbname = get_mongo_dbname_from_collection("manage")
    if dbname:
        meta = {'db_alias': dbname}

    '''
    The project object with its fields. The current fields include

    Attributes:

        title
        abstract
        intellectual_merit
        broader_impact
        use_of_fg
        scale_of_use
        categories
        keywords
        primary_discipline
        orientation
        contact
        url
        comment
        active
        projectid
        status
        lead
        managers
        members
        alumnis
        grant_orgnization
        grant_id
        grant_url
        results
        aggreement_use
        aggreement_slides
        aggreement_support
        aggreement_sotfware
        aggreement_documentation
        comments
        join_open
        join_notification
        resources_services
        resources_software
        resources_clusters
        resources_provision

    '''

    # -------------------------------------------------------------------
    # Project Information
    # -------------------------------------------------------------------
    title = StringField(required=REQUIRED)

    # -------------------------------------------------------------------
    # Project Vocabulary
    # -------------------------------------------------------------------

    categories = ListField(StringField(choices=CATEGORY), required=REQUIRED)
    keywords = ListField(StringField(), required=REQUIRED)

    # -------------------------------------------------------------------
    # Project Contact
    # -------------------------------------------------------------------

    # lead_institutional_role =  StringField(choices=INSTITUTE_ROLE, required=REQUIRED)
    lead = ReferenceField(User)
    managers = ListField(StringField())
    members = ListField(ReferenceField(User))
    alumnis = ListField(StringField())
    contact = StringField(required=REQUIRED)
    # active_members = lead u managers u members - alumnis
    # if not active : active_members = None

    # -------------------------------------------------------------------
    # Project Details
    # -------------------------------------------------------------------

    orientation = StringField(required=REQUIRED)
    primary_discipline = StringField(choices=DISCIPLINE, required=REQUIRED)
    abstract = StringField(required=REQUIRED)
    intellectual_merit = StringField(required=REQUIRED)
    broader_impact = StringField(required=REQUIRED)
    url = URLField(required=REQUIRED)
    results = StringField()

    # -------------------------------------------------------------------
    # Agreements
    # -------------------------------------------------------------------
    agreement_use = BooleanField()
    agreement_slides = BooleanField()
    agreement_support = BooleanField()
    agreement_software = BooleanField()
    agreement_documentation = BooleanField()

    # -------------------------------------------------------------------
    # Grant Information
    # -------------------------------------------------------------------
    grant_organization = StringField(choices=GRANT_ORG)
    grant_id = StringField()
    grant_url = URLField()

    # -------------------------------------------------------------------
    # Resources
    # -------------------------------------------------------------------
    resources_services = ListField(
        StringField(choices=SERVICES), required=REQUIRED)
    resources_software = ListField(
        StringField(choices=SOFTWARE), required=REQUIRED)
    resources_clusters = ListField(
        StringField(choices=CLUSTERS), required=REQUIRED)
    resources_provision = ListField(
        StringField(choices=PROVISIONING), required=REQUIRED)
    comment = StringField()
    use_of_fg = StringField(required=REQUIRED)
    scale_of_use = StringField(required=REQUIRED)

    # -------------------------------------------------------------------
    # Other
    # -------------------------------------------------------------------

    comments = StringField()

    # -------------------------------------------------------------------
    # Project Membership Management
    # -------------------------------------------------------------------
    join_open = BooleanField()
    join_notification = BooleanField()

    # -------------------------------------------------------------------
    # Location
    # -------------------------------------------------------------------

    loc_name = StringField()
    loc_street = StringField()
    loc_additional = StringField()
    loc_state = StringField()
    loc_country = StringField()

    # example search in a list field
    # Project.objects(categories__contains='education')

    active = BooleanField(required=REQUIRED)
    projectid = UUIDField()

    status = StringField(choices=STATUS, required=REQUIRED)
    # maybe we do not need active as this may be covered in status

    # -------------------------------------------------------------------
    # Project Comittee: contains all the information about the projects committee
    # -------------------------------------------------------------------
    # comittee = ReferenceField(Committee)



    # BUG how can we add also arbitray info in case of other, mabe ommit
    # choices

    def to_json(self):
        """prints the project as a json object"""

        d = {
            "title": self.title,
            "abstract": self.abstract,
            "intellectual_merit": self.intellectual_merit,
            "broader_impact": self.broader_impact,
            "use_of_fg": self.use_of_fg,
            "scale_of_use": self.scale_of_use,
            "categories": self.categories,
            "keywords": self.keywords,
            "primary_discipline": self.primary_discipline,
            "orientation": self.orientation,
            "contact": self.contact,
            "url": self.url,
            "active": self.active,
            "status": self.status,
            "lead": self.lead,
            "members": self.members,
            "resources_services": self.resources_services,
            "resources_software": self.resources_software,
            "resources_clusters": self.resources_clusters,
            "resources_provision": self.resources_provision
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
    convenience opbject to manage multiple prpojects
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
        '''adds a project to the database but only after it has been verifie

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
                project.members.append(user)
            elif role == "lead":
                project.lead.append(user)
            elif role == "lead":
                project.alumni.append(user)
        else:
            print "ERROR: The user `{0}` has not registered with FutureGrid".format(user_name)

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
        found = Project.objects(projectid=id)
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
        print "PPPPPP", project
        if not project.status:
            project.status = 'pending'
        if (project.projectid is None) or (project.projectid == ""):
            found = False
            proposedid = None

            # while not found:
            #    proposedid = uuid.uuid4()
            #    result = Project.objects(projectid=proposedid)
            #    print "PPPPP", result
            #    found = result.count() > 0
            #    print result.count()

            project.projectid = proposedid
        else:
            print "UUUUUU -{0}-".format(project.projectid)
        print "UUID", project.projectid
        project.save()

    def clear(self):
        """removes all projects from the database"""
        for project in Project.objects:
            project.delete()
