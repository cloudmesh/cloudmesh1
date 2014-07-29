from mongoengine import *
from mongoengine.context_managers import switch_db
from datetime import datetime
import hashlib, uuid
from user import User, Users
# from comittee import Committee
from pprint import pprint
from cloudmeshobject import CloudmeshObject

port = 27777
db_name = 'project'


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
            'other', 'None')

SOFTWARE = ('other')

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

class Project(CloudmeshObject):
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
    title = StringField(required=True)
    abstract = StringField(required=True)
    intellectual_merit = StringField(required=True)
    broader_impact = StringField(required=True)
    use_of_fg = StringField(required=True)
    scale_of_use = StringField(required=True)
    categories = ListField(StringField(choices=CATEGORY), required=True)
    # example search in a list field
    # Project.objects(categories__contains='education')
    keywords = ListField(StringField(), required=True)
    primary_discipline = StringField(choices=DISCIPLINE, required=True)
    orientation = StringField(required=True)
    contact = StringField(required=True)
    url = URLField(required=True)
    comment = StringField()
    active = BooleanField(required=True)
    projectid = UUIDField()

    status = StringField(choices=STATUS, required=True)
    # maybe we do not need active as this may be covered in status

    # -------------------------------------------------------------------
    # Project Comittee: contains all the information about the projects committee
    # -------------------------------------------------------------------
    # comittee = ReferenceField(Committee)

    # -------------------------------------------------------------------
    # Member Fields
    # -------------------------------------------------------------------
    lead = ReferenceField(User)
    # lead_institutional_role =  StringField(choices=INSTITUTE_ROLE, required=True)
    managers = ListField(StringField())
    members = ListField(ReferenceField(User))
    alumnis = ListField(StringField())

    # active_members = lead u managers u members - alumnis
    # if not active : active_members = None

    # -------------------------------------------------------------------
    # Grant Information
    # -------------------------------------------------------------------
    grant_orgnization = StringField(choices=GRANT_ORG)
    grant_id = StringField()
    grant_url = URLField()


    # -------------------------------------------------------------------
    # Results
    # -------------------------------------------------------------------
    results = StringField()

    # -------------------------------------------------------------------
    # Aggrements
    # -------------------------------------------------------------------
    aggreement_use = BooleanField()
    aggreement_slides = BooleanField()
    aggreement_support = BooleanField()
    aggreement_sotfware = BooleanField()
    aggreement_documentation = BooleanField()

    # -------------------------------------------------------------------
    # Comments
    # -------------------------------------------------------------------
    comments = StringField()

    # -------------------------------------------------------------------
    # Join
    # -------------------------------------------------------------------
    join_open = BooleanField()
    join_notification = BooleanField()

    # -------------------------------------------------------------------
    # Resources
    # -------------------------------------------------------------------
    resources_services = ListField(StringField(choices=SERVICES), required=True)
    resources_software = ListField(StringField(choices=SOFTWARE), required=True)
    resources_clusters = ListField(StringField(choices=CLUSTERS), required=True)
    resources_provision = ListField(StringField(choices=PROVISIONING), required=True)

    # BUG how can we add also arbitray info in case of other, mabe ommit choices

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
        db = connect(db_name, port=port)
        self.projects = Project.objects()
        db = connect('user', port=port)
        self.users = User.objects()


    def __str__(self):
        '''
        not implemented
        '''
        IMPLEMENT()

    def update(self):
        '''
        updates the project
        '''
        self.projects = Project.objects()

    def objects(self):
        '''
        returns the projects
        '''
        self.update()
        return self.projects

    def save(self, project):
        '''adds a project to the database but only after it has been verifie
        
        :param project: the project id
        :type project: uuid
        '''
        project.save()

    def add(self, user_name, project, role):
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

    def find_all(self, project, role):
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


    def clear(self):
        """removes all projects from the database"""
        for project in Project.objects:
            project.delete()


