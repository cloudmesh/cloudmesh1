from cloudmesh.config.cm_config import get_mongo_db, get_mongo_dbname_from_collection, DBConnFactory
from pprint import pprint
import re
from cloudmesh.management.project import CLUSTERS as ProjectCLUSTERS, \
    PROVISIONING as ProjectPROVISIONING, Project as MongoProject, Projects, \
    SERVICES as ProjectSERVICES, STATUS as ProjectSTATUS
from cloudmesh.management.user import User as MongoUser, Users
from cloudmesh_common.logger import LOGGER
from flask import Blueprint, render_template, request, flash, redirect
from mongoengine import connect
from wtforms import Form, validators, widgets
from wtforms.fields import BooleanField, TextField, TextAreaField, PasswordField, \
    SelectMultipleField, StringField, RadioField
from cloudmesh.config.ConfigDict import ConfigDict
from cloudmesh_install import config_file
from wtforms.validators import ValidationError
from flask.ext.login import login_required
import yaml


log = LOGGER(__file__)

management_module = Blueprint('management_module', __name__)

def country_list():
    filename = config_file("/cloudmesh_country.yaml")
    data = yaml.load(open(filename))
    countries = []
    for key, value in data.items():
        item = ''
        item = item + str(value.encode(encoding='UTF-8', errors='strict')) + "(" + str(key) + ")"
        countries.append(item)
    countries.sort()
    countries.insert(0, 'United States(US)')
    return countries


def states_list():
    filename = config_file("/cloudmesh_states.yaml")
    data = yaml.load(open(filename))
    states = []
    for key, value in data.items():
        item = ''
        item = item + str(value['name']) + "("+str(key)+")"
        states.append(item)
    states.sort()
    states.insert(0,'Other (OTH)')
    return states


def disciplines_list():
    filename = config_file("/cloudmesh_disciplines.yaml")
    data = yaml.load(open(filename))
    disciplines = []
    for key, value in data.items():
        item = ''
        item += str(value['name'])
        disciplines.append(item)
    disciplines.sort()
    disciplines.insert(0,'Other (OTH)')
    return disciplines


def get_choices_for_form(services):
    choices = []
    for service in services:
        choices.append((service, service))
    return choices


institutionrole_choices=[
    ('Undergraduate','Undergraduate'),
    ('Graduate Masters','Graduate Masters'),
    ("Graduate PhD",'Graduate PhD'),
    ('Student Other', 'Student Other'),
    ('Faculty','Faculty'),
    ('Staff','Staff'),
    ('Other','Other')
]

roles=['Undergraduate', 'Graduate Masters', 'Graduate PhD', 'Student Other', 'Faculty', 'Staff', 'Other']


class RadioSelectField(RadioField):
    widget = widgets.Select(multiple=False)
    option_widget = widgets.Select


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.

    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = widgets.TableWidget(with_table_tag=True)
    option_widget = widgets.CheckboxInput()

exclude_email_domains = ["@verizon.net", "@123.com"]

@management_module.route('/m/project/apply', methods=['GET', 'POST'])
@login_required
def project_apply():

    form = ProjectRegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        data = dict(request.form)
        action = str(data['button'][0])

        print "Project Data"
        print data

        for key in data:
            if key in ['agreement_use','agreement_slides','agreement_support',
                       'agreement_software','agreement_documentation', 'join_open',
                       'join_notification']:
                if str(data[key][0]) == 'y':
                    data[key] = True
                elif str(data[key][0]) == 'n':
                    data[key] = False
            elif key in ['category', 'managers', 'resources_clusters', 'alumni',
                         'resources_provision', 'resources_services', 'members',
                         'keywords']:
                print data[key][0]
            else:
                 data[key] = data[key][0]
            print str(key)+" - "+str(data[key])+"\n"

        del data['button']

        if action == 'save':
            projects = Projects()
            project = MongoProject()
            for d in data:
                project[d] = data[d]
            print project
            projects.add(project)

        flash('Thanks for registering')
        return redirect('/')
    project_config = ConfigDict(filename=config_file("/cloudmesh_project_intf.yaml"))
    project_fields = project_config.get("cloudmesh.project")
    return render_template('management/project_apply.html',
                           title="Project Application",
                           states=['save', 'cancel'],
                           fields=project_fields,
                           countries_list=[c for c in country_list()],
                           states_list = [c for c in states_list()],
                           disciplines_list = [c for c in disciplines_list()])

    # return render_template('management/project_apply.html',
    # title="Project Application",
    #                        states=['save', 'cancel'],
    #                        form=form,
    #                        fields=ProjectRegistrationForm.keys)

    # return render_template('management/project_apply.html',
    #                        title="Project Application",
    #                        states=['save', 'cancel'],
    #                        form=form,
    #                        fields=ProjectRegistrationForm.keys,
    #                        profile_fields=ProjectRegistrationForm.profile_keys,
    #                        vocab_fields=ProjectRegistrationForm.vocab_keys,
    #                        contact_fields=ProjectRegistrationForm.project_contact_keys,
    #                        project_details_fields=ProjectRegistrationForm.project_details_keys,
    #                        agreements_fields=ProjectRegistrationForm.agreements_keys,
    #                        grant_fields=ProjectRegistrationForm.grant_keys,
    #                        resource_fields=ProjectRegistrationForm.resource_keys,
    #                        membership_fields=ProjectRegistrationForm.membership_keys,
    #                        other_fields=ProjectRegistrationForm.other_keys,
    #                        loc_fields=ProjectRegistrationForm.loc_keys)


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

    # keys = [("profile", ["title",
    #                      "abstract",
    #                      "intellectual_merit",
    #                      "broader_impact",
    #                      "use_of_fg",
    #                      "scale_of_use",
    #                      # "categories",
    #                      # "keywords",
    #                      # "primary_discipline",
    #                      "orientation",
    #                      "contact",
    #                      "url",
    #                      "comment",
    #                      # "active",
    #                      # "projectid",
    #                      # "lead",
    #                      # "managers",
    #                      # "members",
    #                      # "alumnis",
    #                      # "grant_orgnization",
    #                      # "grant_id",
    #                      # "grant_url",
    #                      "results"]),
    #         ("agreements", ["agreement_use",
    #                         "agreement_slides",
    #                         "agreement_support",
    #                         "agreement_software",
    #                         "agreement_documentation"]),
    #         ("other", ["comments",
    #                    "join_open",
    #                    "join_notification",
    #                    "resources_services",
    #                    # "resources_software",
    #                    "resources_clusters",
    #                    "resources_provision"
    #         ])
    # ]

    keys = [\
        "title",
        "category",
        "keywords",
        "contact",
        "primary_discipline"
        "orientation",
        "abstract",
        "intellectual_merit",
        "broader_impact",
        "use_of_fg",
        "scale_of_use",
        "url",
        "comment",
        "results",
        "agreement_use",
        "agreement_slides",
        "agreement_support",
        "agreement_software",
        "agreement_documentation",
        "comments",
        "join_open",
        "join_notification",
        "resources_services",
        # "resources_software",
        "resources_clusters",
        "resources_provision",
        "grant_organization",
        "grant_id",
        "grant_url",
        "loc_name",
        "loc_street",
        "loc_additional",
        "loc_state",
        "loc_country"]

    profile_keys = [\
        "title"]


    vocab_keys = [\
        "category",
        "keywords"]

    project_contact_keys = [\
        "lead",
        "managers",
        "members",
        "alumni",
        "contact"]

    project_details_keys = [\
        "orientation",
        "primary_discipline",
        "abstract",
        "intellectual_merit",
        "broader_impact",
        "url",
        # "active",
        # "projectid",
        # "lead",
        # "managers",
        # "members",
        # "alumnis",
        "results"]

    agreements_keys= [\
        "agreement_use",
        "agreement_slides",
        "agreement_support",
        "agreement_software",
        "agreement_documentation"]

    grant_keys = [\
        "grant_organization",
        "grant_id",
        "grant_url"
        ]

    loc_keys = [\
        "loc_name",
        "loc_street",
        "loc_additional",
        "loc_state",
        "loc_country"]

    resource_keys = [\
        "resources_services",
        # "resources_software",
        "resources_clusters",
        "resources_provision",
        "comment",
        "use_of_fg",
        "scale_of_use"]

    other_keys = [\
        "comments"]

    membership_keys = [\
        "join_open",
        "join_notification"
        ]

    title = StringField('Title')
    category = RadioSelectField('Project Category', choices=[('None','None'),('Computer Science','Computer Science'),\
                                                             ('Education','Education'),\
                                                             ('Interoperability','Interoperability'),\
                                                             ('Life Sciences','Life Sciences'),\
                                                             ('Non Life Sciences','Non Life Sciences'),\
                                                             ('Technology Development','Technology Development'),\
                                                             ('Technology Evaluation','Technology Evaluation')])
    keywords = StringField('Project Keywords')
    abstract = TextAreaField('Abstract')
    intellectual_merit = TextAreaField('Intellectual merit')
    broader_impact = TextAreaField('Broader impact')
    use_of_fg = TextAreaField('Use of Future Systems')
    scale_of_use = TextAreaField('Scale of use')
    categories = StringField('Categories')
    # orientation = StringField('Orientation')
    orientation = RadioSelectField('Orientation', choices=[('research','Research'),('education','Education'),\
                                                           ('industry','Industry'),('government','Government')])
    # primary_discipline = RadioSelectField('Primary discipline', choices=discipline_choices)
    primary_discipline = RadioSelectField('Primary discipline')
    primary_discipline.choices = [c for c in disciplines_list()]
    url = StringField(
        'URL', [validators.Length(min=6, max=50), validate_url_in_form])
    comment = TextAreaField('Comment')
    active = BooleanField('Active')
    projectid = StringField('Projectid')
    contact = StringField('Contact')
    lead = StringField('Project Lead')
    managers = TextAreaField('Project Managers')
    members = TextAreaField('Project Members')
    alumni = TextAreaField('Project Alumni')
    grant_organization = StringField('Grant Organization')
    grant_id = StringField('Grant ID')
    grant_url = StringField('Grant URL')
    results = TextAreaField('Results')
    agreement_use = BooleanField('NSF Agreement to use Future Systems')
    agreement_slides = BooleanField('Slide Collection')
    agreement_support = BooleanField('Support')
    agreement_software = BooleanField('Software Contributions')
    agreement_documentation = BooleanField('Documentation Contributions')
    agreement_images = BooleanField('Images')
    comments = TextAreaField('Comments')
    join_open = BooleanField('Allow users to request to join')
    join_notification = BooleanField('Send an email notification when a user joins')
    resources_services = MultiCheckboxField(
        'Resource Services',
        choices=get_choices_for_form(ProjectSERVICES))
    # resources_software = MultiCheckboxField('resources_software',
    #                         choices=get_choices_for_form(ProjectSOFTWARE))
    resources_clusters = MultiCheckboxField(
        'Resource Clusters', choices=get_choices_for_form(ProjectCLUSTERS))
    resources_provision = MultiCheckboxField(
        'Resource Provisioning', choices=get_choices_for_form(ProjectPROVISIONING))
    loc_name = StringField('Name')
    loc_street = StringField('Street')
    loc_additional = StringField('Additional')
    # loc_state= RadioSelectField("State",[validators.DataRequired()], choices=state_choices)
    # loc_country = RadioSelectField("Country", [validators.DataRequired()], choices=country_choices)
    loc_country = RadioSelectField("Country", [validators.DataRequired()])
    loc_state= RadioSelectField("State",[validators.DataRequired()])
    loc_country.choices = [c for c in country_list()]
    loc_state.choices = [c for c in states_list()]


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
            "email",
            "password",
            "confirm",
            "title",
            "firstname",
            "lastname",
            "phone",
            "url",
            "citizenship",
            "bio",
            "institution",
            "institutionrole",
            "department",
            "address",
            "advisor",
            "country",
            "confirm"]

    organization_keys = \
        ["institution",
         "institutionrole",
         "department",
         "address",
         "advisor",
         "country"]

    profile_keys = \
        ["username",
         "email",
         "password",
         "confirm",
         "title",
         "firstname",
         "lastname",
         "phone",
         "url",
         "citizenship",
         "bio"]

    def validate_email_in_form(form, field):
        if ("@" not in field.data) or ("." not in field.data):
            raise ValidationError('The email address is not valid')

        for domain in exclude_email_domains:
            if domain in field.data:
                raise ValidationError(
                    'Email form the domain {0} are not alloed'.format(field.data))
        dbname = get_mongo_dbname_from_collection("manage")
        print "Database Name: ", dbname
        if dbname:
            meta = {'db_alias': dbname}
#         connect('user', port=27777)
        users = Users()
        if not users.validate_email(field.data):
            raise ValidationError('A user with this email already exists')

    def validate_username_in_form(form, field):
        if not re.match("^[a-z0-9]*$", field.data):
            raise ValidationError(
                'Only lower case characters a-z and numbers 0-9 allowed.')

        if not field.data.islower():
            raise ValidationError('The username must be lower case')

        dbname = get_mongo_dbname_from_collection("manage")
        print "Database Name: ", dbname
        if dbname:
            meta = {'db_alias': dbname}
#         connect('user', port=27777)
        username = MongoUser.objects(username=field.data)
        if username.count() > 0:
            users = Users()
            proposal = users.get_unique_username(field.data)
            raise ValidationError(
                'A user with name already exists. Suggestion: {0}'.format(proposal))

    username = StringField(
        'Username', [validators.Length(min=6, max=25), validate_username_in_form])
    title = StringField('Title', [validators.Length(min=2, max=40)])
    firstname = StringField('Firstname', [validators.Length(min=1, max=35)])
    lastname = StringField('Lastname', [validators.Length(min=1, max=35)])
    email = StringField(
        'Email', [validators.Length(min=6, max=35), validate_email_in_form])
    phone = StringField('Phone', [validators.Length(min=6, max=35)])
    url = StringField('URL')
    # citizenship = RadioSelectField("Citizenship", [validators.DataRequired()], choices=all_country_choices)
    citizenship = RadioSelectField("Citizenship", [validators.DataRequired()])
    institution = TextAreaField('Institution')
    institutionrole = RadioSelectField("Institution Role", [validators.DataRequired()], choices=institutionrole_choices)
    # institutionrole = StringField('Institution role')
    department = TextAreaField('Department')
    address = TextAreaField('Address', [validators.DataRequired(message="Address required")])
    # country = RadioSelectField("Country", [validators.DataRequired()], choices=country_choices)
    country = RadioSelectField("Country", [validators.DataRequired()])
    advisor = TextAreaField('Advisor')
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])

    confirm = PasswordField('Confirm Password')
    # agreement = BooleanField('I accept the usage agreement', [validators.Required()])
    bio = TextAreaField('Bio', [validators.DataRequired()])
    citizenship.choices = [c for c in country_list()]
    country.choices = [c for c in country_list()]

def print_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            print(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')


@management_module.route('/m/user/apply', methods=['GET', 'POST'])
@login_required
def user_apply():

    form = UserRegistrationForm(request.form)

    if request.method == 'POST': #and form.validate():
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
                user[d] = data[d]

            users.add(user)

        flash('Thanks for registering')
        return redirect('/')

    user_config = ConfigDict(filename=config_file("/cloudmesh_user_intf.yaml"))
    user_fields = user_config.get("cloudmesh.user")
    return render_template('management/user_apply.html',
                           title="User Application",
                           states=['save', 'cancel'],
                           fields=user_fields,
                           countries_list=[c for c in country_list()],
                           roles_list=roles)



@management_module.route('/project/edit/<projectid>/', methods=['GET', 'POST'])
@login_required
def project_edit(projectid):
    dbname = get_mongo_dbname_from_collection("manage")
    print "Database Name: ", dbname
    if dbname:
        meta = {'db_alias': dbname}
#     connect('user', port=27777)

    try:
        project = MongoProject.objects(projectid=projectid)
    except:
        print "Error: pojectid not found"
        return render_template('management/error.html',
                               error="The project does not exist")

    if request.method == 'GET':

        return render_template('management/project_edit.html',
                               project=project[0], states=['save', 'cancel'],
                               title="Project Management")

    elif request.method == 'POST':

        data = dict(request.form)
        action = str(data['button'][0])
        # del data['button']
        for key in data:
            data[key] = data[key][0]

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
                project.agreement_use = data["agreement_use"]
                project.agreement_slides = data["agreement_slides"]
                project.agreement_support = data["agreement_support"]
                project.agreement_software = data["agreement_software"]
                project.agreement_documentation = data["agreement_documentation"]

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
                project.alumni = data["alumni"]
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

            except Exception, e:
                print "ERROR", e

        return render_template('management/project_edit.html',
                               project=project, states=['save', 'cancel'],
                               title="Project Management")


@management_module.route('/project/profile/<projectid>', methods=['GET'])
@login_required
def project_profile(projectid):
    dbname = get_mongo_dbname_from_collection("manage")
    print "Database Name: ", dbname
    if dbname:
        meta = {'db_alias': dbname}
#     connect('user', port=27777)
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
    dbname = get_mongo_dbname_from_collection("manage")
    print "Database Name: ", dbname
    if dbname:
        meta = {'db_alias': dbname}
#     connect('user', port=27777)
    projects = MongoProject.objects()

    if request.method == 'POST':
        #
        # check for selection
        #
        if 'selectedprojects' in request.form:
            data = dict(request.form)
            project_ids = data['selectedprojects']
            action = str(data['button'][0])

            for projectid in project_ids:
                project = MongoProject.objects(projectid=projectid)[0]
                project.status = action
                project.save()
    dbname = get_mongo_dbname_from_collection("manage")
    print "Database Name: ", dbname
    if dbname:
        meta = {'db_alias': dbname}
#     connect('user', port=27777)
    projects = MongoProject.objects()

    return render_template('management/project_manage.html',
                           projects=projects, with_edit="True",
                           title="Project Management",
                           states=ProjectSTATUS)


@management_module.route('/m/project/list')
@login_required
def management_project_list():
    dbname = get_mongo_dbname_from_collection("manage")
    print "Database Name: ", dbname
    if dbname:
        meta = {'db_alias': dbname}
#     connect('user', port=27777)
    projects = MongoProject.objects()

    return render_template('management/project_list.html', projects=projects, with_edit="False", title="Project List")


@management_module.route('/m/user/manage', methods=['GET', 'POST'])
@login_required
def management_user_manage():
    dbname = get_mongo_dbname_from_collection("manage")
    print "Database Name: ", dbname
    if dbname:
        meta = {'db_alias': dbname}
#     connect('user', port=27777)
    users = MongoUser.objects()

    if request.method == 'POST':
        #
        # check for selection
        #
        if 'selectedusers' in request.form:
            data = dict(request.form)
            usernames = data['selectedusers']
            action = str(data['button'][0])

            if action == 'delete':

                for username in usernames:
                    user = MongoUser.objects(username=username)[0]
                    user.delete()

            else:

                for username in usernames:
                    user = MongoUser.objects(username=username)[0]
                    user.status = action
                    user.save()

    users = MongoUser.objects()
    return render_template('management/user_manage.html',
                           users=users,
                           with_edit="True",
                           states=['approve', 'pending', 'deny', 'block', 'delete'],
                           title="User Management")


@management_module.route('/m/user/list')
@login_required
def management_user_list():
    dbname = get_mongo_dbname_from_collection("manage")
    print "Database Name: ", dbname
    if dbname:
        meta = {'db_alias': dbname}
#     connect('user', port=27777)
    users = MongoUser.objects()
    return render_template('management/user_manage.html', users=users, with_edit="False", title="User List")


@management_module.route('/user/profile/<username>')
def management_user_profile(username):
    dbname = get_mongo_dbname_from_collection("manage")
    print "Database Name: ", dbname
    if dbname:
        meta = {'db_alias': dbname}
#     connect('user', port=27777)
    try:
        user = MongoUser.objects(username=username)
        if user.count() == 1:
            for item in user:
                print item
            pprint(user[0])
            print user[0].username
            print user[0].firstname
            print user[0].lastname
            print user[0].country

            return render_template('management/user_profile.html', user=user[0])

        else:
            raise Exception
    except:
        print "Error: Username not found"
        return render_template('error.html',
                               form=None,
                               type="exists",
                               msg="The user does not exist")


@management_module.route('/user/edit/<username>/', methods=['GET', 'POST'])
@login_required
def management_user_edit(username):
    dbname = get_mongo_dbname_from_collection("manage")
    print "Database Name: ", dbname
    if dbname:
        meta = {'db_alias': dbname}
#     connect('user', port=27777)

    try:
        user = MongoUser.objects(username=username)
    except:
        print "Error: Username not found"
        return render_template('error.html',
                               form=None,
                               type="exists",
                               msg="The user does not exist")

    if request.method == 'GET':

        return render_template('management/user_edit.html', user=user[0], states=['save', 'cancel'])

    elif request.method == 'POST':

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
