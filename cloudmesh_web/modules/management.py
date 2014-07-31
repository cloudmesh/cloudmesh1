from datetime import timedelta
from wtforms.csrf.session import SessionCSRF
import re
from wtforms.validators import ValidationError
from cloudmesh.management.project import STATUS as ProjectSTATUS
from cloudmesh_common.logger import LOGGER
from flask import Blueprint, render_template, request
from flask.ext.login import login_required
from pprint import pprint, pprint
from mongoengine import connect
from cloudmesh.management.user import User as MongoUser, Users
from cloudmesh.management.project import Project as MongoProject, Projects
from cloudmesh.management.cloudmeshobject import order, make_form_list


log = LOGGER(__file__)

management_module = Blueprint('management_module', __name__)

from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired

from wtforms import Form, validators
from wtforms.fields import BooleanField, TextField, TextAreaField, PasswordField, RadioField
from flask import flash,redirect

exclude_email_domains = ["@verizon.net","@123.com"]

@management_module.route('/m/project/apply', methods=['GET','POST'])
@login_required
def project_apply():

    return "HALO"

    '''
    form = ProjectRegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        
        print "POSTING"
        data = dict(request.form)
        action = str(data['button'][0])
        
        for key in data:
            data[key] = data[key][0]
        del data['button']

        if action == 'save':
            projects = Projects()            
            project = MongoProject()
            for d in data:
                print d, ":", data[d]
                project[d] = data[d]
            
            projects.add(project)

        flash('Thanks for registering')
        return redirect('/')
    else:
        if request.method == "POST":
            print "ERROR POST"
            print request.form
            print form.validate()
            print_errors(form)
           
        
            
    print "RENDER"
    return render_template('management/project_apply.html',
                            title="Project Application",
                            states=['save', 'cancel'],                           
                            form=form,
                            fields=ProjectRegistrationForm.keys)

    '''

class ProjectRegistrationForm(Form):

    def validate_url_in_form(form, field):
        if not field.data.startswith("http"):
            raise ValidationError('The url is not valid')            

    """
    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = b'REPLACE ME WITH A SECRET'
        csrf_time_limit = timedelta(minutes=20)

    # put this in the html form:  {{ form.csrf_token }}
    """

    keys=["title",     
          "abstract",
          "intellectual_merit",  
          "broader_impact",  
          "use_of_fg",  
          "scale_of_use", 
          # "categories", 
          # "keywords", 
          "primary_discipline", 
          "orientation",  
          "contact",  
          "url", 
          "comment", 
          "active", 
          "projectid", 
          # "lead",       
          # "managers",   
          # "members",    
          # "alumnis",    
          # "grant_orgnization", 
          # "grant_id", 
          # "grant_url", 
          "results", 
          "aggreement_use", 
          "aggreement_slides", 
          "aggreement_support", 
          "aggreement_sotfware", 
          "aggreement_documentation", 
          "comments",
          "join_open", 
          "join_notification", 
          # "resources_services",
          # "resources_software", 
          # "resources_clusters", 
          #"resources_provision"
          ]
        
    title = TextField('title')
    abstract= TextField('abstract')
    intellectual_merit  = TextField('intellectual_merit')
    broader_impact  = TextField('broader_impact')
    use_of_fg  = TextField('use_of_fg')
    scale_of_use = TextField('scale_of_use')
    categories = TextField('categories')
    keywords = TextField('keywords')
    primary_discipline = TextField('primary_discipline')
    orientation  = TextField('orientation')
    contact  = TextField('contact')
    url = TextField('url', [validators.Length(min=6, max=50), validate_url_in_form])
    comment = TextField('comment')
    active = BooleanField('active')
    projectid = TextField('projectid')
    lead       = TextField('lead')
    managers   = TextField('managers')
    members    = TextField('members')
    alumnis    = TextField('alumnis')
    grant_orgnization = TextField('grant_orgnization')
    grant_id = TextField('grant_id')
    grant_url = TextField('grant_url')
    results = TextField('results')
    aggreement_use = BooleanField('aggreement_use')
    aggreement_slides = BooleanField('aggreement_slides')
    aggreement_support = BooleanField('aggreement_support')
    aggreement_sotfware = BooleanField('aggreement_sotfware')
    aggreement_documentation = BooleanField('aggreement_documentation')
    comments= TextField('comments')
    join_open = BooleanField('join_open')
    join_notification = BooleanField('join_notification')
    resources_services= TextField('resources_services')
    resources_software = TextField('resources_software')
    resources_clusters = TextField('resources_clusters')
    resources_provision= TextField('resources_provision')


class UserRegistrationForm(Form):

    """
    class Meta:
        csrf = True
        csrf_class = SessionCSRF
        csrf_secret = b'REPLACE ME WITH A SECRET'
        csrf_time_limit = timedelta(minutes=20)

    # put this in the html form:  {{ form.csrf_token }}
    """
    keys = ["username",
            "title",
            "firstname",
            "lastname",
            "phone",
            "email",
            "url",
            "citizenship",
            "bio",
            "password",
            "confirm",
            "institution",
            "department",
            "address",
            "advisor",
            "country",
            "confirm"]

    organization_keys = \
           ["institution",
            "department",
            "address",
            "advisor",
            "country"]
         
    profile_keys = \
           ["username",
            "title",
            "firstname",
            "lastname",
            "phone",
            "email",
            "url",
            "citizenship",
            "bio",
            "password",
            "confirm"]

    def validate_email_in_form(form, field):
        if ("@" not in field.data) or ("." not in field.data):
            raise ValidationError('The email address is not valid')            

        for domain in exclude_email_domains:
            if domain in field.data:
                raise ValidationError('Email form the domain {0} are not alloed'.format(field.data))            
        connect ('user', port=27777)
        users = Users()
        if not users.validate_email(field.data):
            raise ValidationError('A user with this email already exists')
            
    def validate_username_in_form(form, field):
        if not re.match("^[a-z0-9]*$", field.data):
            raise ValidationError('Only lower case characters a-z and numbers 0-9 allowed.')

        if not field.data.islower():
            raise ValidationError('The username must be lower case')

        connect ('user', port=27777)
        username = MongoUser.objects(username=field.data)  
        if username.count() > 0:
            users = Users()
            proposal =  users.get_unique_username(field.data)
            raise ValidationError('A user with name already exists. Suggestion: {0}'.format(proposal))
            
    username = TextField('Username', [validators.Length(min=6, max=25), validate_username_in_form])
    title = TextField('Title', [validators.Length(min=6, max=40)])    
    firstname = TextField('Firstname', [validators.Length(min=1, max=35)])
    lastname = TextField('Lastname', [validators.Length(min=1, max=35)])        
    email = TextField('Email', [validators.Length(min=6, max=35), validate_email_in_form])
    phone = TextField('Phone', [validators.Length(min=6, max=35)])
    url = TextField('Url',[validators.DataRequired()])
    citizenship = TextField('citizenship',[validators.DataRequired()])
    institution = TextAreaField('Institution')
    department = TextAreaField('Department')            
    address = TextAreaField('Address',[validators.DataRequired()])
    country = TextField('Country',[validators.DataRequired()])    
    advisor = TextAreaField('Advisor')    
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    #agreement = BooleanField('I accept the usage agreement', [validators.Required()])
    bio = TextAreaField('Bio',[validators.DataRequired()])


def print_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        print "HHHHHH", field
        for error in errors:
            print(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')
            
@management_module.route('/m/user/apply', methods=['GET','POST'])
@login_required
def user_apply():

    form = UserRegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        
        print "POSTING"
        data = dict(request.form)
        action = str(data['button'][0])
        
        for key in data:
            data[key] = data[key][0]
        del data['button']

        if action == 'save':
            users = Users()            
            user = MongoUser()
            del data['confirm']            
            for d in data:
                print d, ":", data[d]
                user[d] = data[d]
            
            users.add(user)

        flash('Thanks for registering')
        return redirect('/')
    else:
        if request.method == "POST":
            print "ERROR POST"
            print request.form
            print form.validate()
            print_errors(form)
           
        
            
    print "RENDER"
    return render_template('management/user_apply.html',
                            title="Project Application",
                            states=['save', 'cancel'],                           
                            form=form,
                            fields=UserRegistrationForm.keys,
                            profile_fields=UserRegistrationForm.profile_keys,                          
                            organization_fields=UserRegistrationForm.organization_keys)



@management_module.route('/project/edit/<projectid>/', methods=['GET','POST'])
@login_required
def project_edit(projectid):
    connect ('user', port=27777)

    try:
        project = MongoProject.objects(projectid=projectid)
    except:
        print "Error: pojectid not found"
        return render_template('management/error.html',
                                error="The project does not exist")

    if request.method == 'GET':
        print "GETTING"

        return render_template('management/project_edit.html',
                                project=project[0], states=['save', 'cancel'],                
                                title="Project Management")

        
    elif request.method == 'POST':

        print "POSTING"
        data = dict(request.form)
        action = str(data['button'][0])
        #del data['button']
        for key in data:
            data[key] = data[key][0]
    
        print ">>>>ACTION", action
        #project = Project.objects(projectid=projectid)[0]
        project = project[0]        
            
        if action == 'save':
            for d in data:
                print d, ":", data[d]
            try:
                project.title = data["title"]
                project.abstract = data["abstract"]
                project.intellectual_merit = data["intellectual_merit"]
                project.broader_impact = data["broader_impact"]
                project.use_of_fg = data["use_of_fg"]
                project.scale_of_use = data["scale_of_use"]
                """

                #
                # things that should not be changed
                #
                #project.active = data["active"]
                #project.status = data["status"]
                #project.projectid = data["projectid"]

                #
                # after apoproval this should not be changed either
                #
                project.aggreement_use = data["aggreement_use"]
                project.aggreement_slides = data["aggreement_slides"]
                project.aggreement_support = data["aggreement_support"]
                project.aggreement_sotfware = data["aggreement_sotfware"]
                project.aggreement_documentation = data["aggreement_documentation"]
                                                                
                project.categories = data["categories"]
                project.keywords = data["keywords"]
                project.primary_discipline = data["primary_discipline"]
                project.orientation = data["orientation"]
                project.contact = data["contact"]
                project.url = data["url"]
                project.comment = data["comment"]


                project.lead = data["lead"]
                project.managers = data["managers"]
                project.members = data["members"]
                project.alumnis = data["alumnis"]
                project.grant_orgnization = data["grant_orgnization"]
                project.grant_id = data["grant_id"]
                project.grant_url = data["grant_url"]
                project.results = data["results"]
                project.comments = data["comments"]
                project.join_open = data["join_open"]
                project.join_notification = data["join_notification"]
                project.resources_services = data["resources_services"]
                project.resources_software = data["resources_software"]
                project.resources_clusters = data["resources_clusters"]
                project.resources_provision = data["resources_provision"]
                """
                project.save()                
                print "SAVING"
                
            except Exception, e:
                print "ERROR",e 
                


        return render_template('management/project_edit.html',
                                project=project, states=['save', 'cancel'],                
                                title="Project Management")


@management_module.route('/project/profile/<projectid>', methods=['GET'])
@login_required
def project_profile(projectid):
    print projectid 
    connect ('user', port=27777)
    try:
        project = MongoProject.objects(projectid=projectid)
        if project.count() == 1:

            return render_template('management/project_profile.html',
                                    project=project[0],
                                    title="Project Management")
        else:
            raise Exception
    except:
        print "Error: Project not found"
        return render_template('management/error.html',
                                error="The project does not exist")


@management_module.route('/m/project/manage', methods=['GET', 'POST'])
@login_required
def management_project_manage():

    print "AAAA"
    connect ('user', port=27777)
    projects = MongoProject.objects()


    if request.method == 'POST':
        #
        # check for selection
        #
        if 'selectedprojects' in request.form:
            data = dict(request.form)
            print data
            project_ids = data['selectedprojects']
            action = str(data['button'][0])
            print "ACTION", action, action in ProjectSTATUS, 'approved' in ProjectSTATUS
            print "PROJECTS", project_ids
            
            for projectid in project_ids:
                project = MongoProject.objects(projectid=projectid)[0]
                project.status = action                
                project.save()

    connect ('user', port=27777)
    projects = MongoProject.objects()
    print projects

    print "PPP"    
    print "COUNT", projects.count()
    pprint(projects)

            
    return render_template('management/project_manage.html',
                           projects=projects, with_edit="True",
                           title="Project Management",
                           states=ProjectSTATUS)

    


@management_module.route('/m/project/list')
@login_required
def management_project_list():

    print "IIIII"
    connect ('user', port=27777)
    projects = MongoProject.objects()

    print "PPP"    
    print "COUNT", projects.count()
    pprint(projects)
    
    return render_template('management/project_list.html', projects=projects, with_edit="False", title="Project List")


@management_module.route('/m/user/manage')
@login_required
def management_user_manage():

    connect ('user', port=27777)
    users = MongoUser.objects()
    print "COUNT", users.count()
    return render_template('management/user_manage.html', users=users, with_edit="True", title="User Management")

@management_module.route('/m/user/list')
@login_required
def management_user_list():

    connect ('user', port=27777)
    users = MongoUser.objects()
    print "COUNT", users.count()
        
    return render_template('management/user_manage.html', users=users, with_edit="False", title="User List")

@management_module.route('/user/profile/<username>')
def management_user_profile(username):
    connect ('user', port=27777)
    try:
        user = MongoUser.objects(username=username)
        print user
        print user.count()
        if user.count() == 1:
            pprint (user[0])
            print user[0].username
            print user[0].firstname
            print user[0].lastname                        
            
            return render_template('management/user_profile.html', user=user[0])
        
        else:
            raise Exception
    except:
        print "Error: Username not found"
        return render_template('error.html', form=None, type="exists", msg="The user does not exist")                    

@management_module.route('/user/edit/<username>/', methods=['GET', 'POST'])
@login_required
def management_user_edit(username):
    connect ('user', port=27777)

    try:
        user = MongoUser.objects(username=username)
    except:
        print "Error: Username not found"
        return render(request, 'error.html', {"error": "The user does not exist"}) 
    
    if request.method == 'GET':

        return render_template('management/user_edit.html', user=user[0], states=['save', 'cancel'])                    

    elif request.method == 'POST':

        print request.form
        
        data = dict(request.form)
        
        action = str(data['button'][0])
        del data['button']
        for key in data:
            data[key] = data[key][0]

        user = MongoUser.objects(username=username)[0]
        if action == 'save':

            keys = ["bio",
                    "citizenship",
                    "firstname",
                    "lastname",
                    "title",
                    "url",
                    "address",
                    "institution",
                    "phone",
                    "advisor",
                    "department",
                    "country",
                    "email"]

                    
            for key in keys:
                user[key] = data[key]


            user.save()

        return render_template('management/user_edit.html', user=user, states=['save', 'cancel'])            
        