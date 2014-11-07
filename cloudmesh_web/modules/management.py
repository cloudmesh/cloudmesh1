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

from wtforms.validators import ValidationError

from flask.ext.login import login_required


log = LOGGER(__file__)

management_module = Blueprint('management_module', __name__)

discipline_choices=[
    ('Aerospace Engineering (101)', 'Aerospace Engineering (101)'),
    ('Agricultural Economics (901)', 'Agricultural Economics (901)'),
    ('Agricultural Engineering (102)', 'Agricultural Engineering (102)'),
    ('Agricultural Sciences (501)', 'Agricultural Sciences (501)'),
    ('Anatomy (601)', 'Anatomy (601)'),
    ('Anesthesiology (701)', 'Anesthesiology (701)'),
    ('Anthropology (902)', 'Anthropology (902)'),
    ('Astronomy (201)', 'Astronomy (201)'),
    ('Atmospheric Sciences (301)', 'Atmospheric Sciences (301)'),
    ('Biochemistry (602)', 'Biochemistry (602)'),
    ('Biology (603)', 'Biology (603)'),
    ('Biomedical Engineering (103)', 'Biomedical Engineering (103)'),
    ('Biometry and Epidemiology (604)', 'Biometry and Epidemiology (604)'),
    ('Biophysics (605)', 'Biophysics (605)'),
    ('Biosciences, n.e.c. (617)', 'Biosciences, n.e.c. (617)'),
    ('Botany (606)', 'Botany (606)'),
    ('Cardiology (702)', 'Cardiology (702)'),
    ('Cell and Molecular Biology (607)', 'Cell and Molecular Biology (607)'),
    ('Chemical and Related Engineering (104)', 'Chemical and Related Engineering (104)'),
    ('Chemistry (202)', 'Chemistry (202)'),
    ('Civil and Related Engineering (105)', 'Civil and Related Engineering (105)'),
    ('Clinical Medicine, n.e.c. (717)', 'Clinical Medicine, n.e.c. (717)'),
    ('Communication Disorders Sciences (723)', 'Communication Disorders Sciences (723)'),
    ('Computer Science (401)', 'Computer Science (401)'),
    ('Dental Sciences (718)', 'Dental Sciences (718)'),
    ('Earth, Atmospheric, and Ocean Sciences, n.e.c. (304)', 'Earth, Atmospheric, and Ocean Sciences, n.e.c. (304)'),
    ('Ecology (608)', 'Ecology (608)'),
    ('Economics (903)', 'Economics (903)'),
    ('Electrical and Related Engineering (106)', 'Electrical and Related Engineering (106)'),
    ('Endocrinology (704)', 'Endocrinology (704)'),
    ('Engineering Science and Engineering Physics (107)', 'Engineering Science and Engineering Physics (107)'),
    ('Engineering, n.e.c. (114)', 'Engineering, n.e.c. (114)'),
    ('Entomology and Parasitology (609)', 'Entomology and Parasitology (609)'),
    ('Gastroenterology (705)', 'Gastroenterology (705)'),
    ('Genetics (610)', 'Genetics (610)'),
    ('Geography (904)', 'Geography (904)'),
    ('Geosciences (302)', 'Geosciences (302)'),
    ('Health-related, n.e.c. (722)', 'Health-related, n.e.c. (722)'),
    ('Hematology (706)', 'Hematology (706)'),
    ('History and Philosophy of Science (905)', 'History and Philosophy of Science (905)'),
    ('Industrial/Manufacturing Engineering (108)', 'Industrial/Manufacturing Engineering (108)'),
    ('Linguistics (906)', 'Linguistics (906)'),
    ('Mathematics and Applied Mathematics (402)', 'Mathematics and Applied Mathematics (402)'),
    ('Mechanical and Related Engineering (109)', 'Mechanical and Related Engineering (109)'),
    ('Metallurgical and Materials Engineering (110)', 'Metallurgical and Materials Engineering (110)'),
    ('Microbiology, Immunology, and Virology (611)', 'Microbiology, Immunology, and Virology (611)'),
    ('Mining and Related Engineering (111)', 'Mining and Related Engineering (111)'),
    ('Neurology (707)', 'Neurology (707)'),
    ('Nuclear Engineering (112)', 'Nuclear Engineering (112)'),
    ('Nursing (719)', 'Nursing (719)'),
    ('Nutrition (612)', 'Nutrition (612)'),
    ('Obstetrics and Gynecology (708)', 'Obstetrics and Gynecology (708)'),
    ('Ocean Sciences (303)', 'Ocean Sciences (303)'),
    ('Oncology/Cancer Research (703)', 'Oncology/Cancer Research (703)'),
    ('Ophthalmology (709)', 'Ophthalmology (709)'),
    ('Otorhinolaryngology (710)', 'Otorhinolaryngology (710)'),
    ('Pathology (613)', 'Pathology (613)'),
    ('Pediatrics (711)', 'Pediatrics (711)'),
    ('Petroleum Engineering (113)', 'Petroleum Engineering (113)'),
    ('Pharmaceutical Sciences (720)', 'Pharmaceutical Sciences (720)'),
    ('Pharmacology (614)', 'Pharmacology (614)'),
    ('Physical Sciences, n.e.c. (204)', 'Physical Sciences, n.e.c. (204)'),
    ('Physics (203)', 'Physics (203)'),
    ('Physiology (615)', 'Physiology (615)'),
    ('Political Science/Public Administration (907)', 'Political Science/Public Administration (907)'),
    ('Preventive Medicine and Community Health (712)', 'Preventive Medicine and Community Health (712)'),
    ('Psychiatry (713)', 'Psychiatry (713)'),
    ('Psychology (except Clinical) (802)', 'Psychology (except Clinical) (802)'),
    ('Psychology, Clinical (803)', 'Psychology, Clinical (803)'),
    ('Psychology, Combined (801)', 'Psychology, Combined (801)'),
    ('Pulmonary Disease (714)', 'Pulmonary Disease (714)'),
    ('Radiology (715)', 'Radiology (715)'),
    ('Social Sciences, n.e.c. (910)', 'Social Sciences, n.e.c. (910)'),
    ('Sociology (908)', 'Sociology (908)'),
    ('Sociology and Anthropology (909)', 'Sociology and Anthropology (909)'),
    ('Statistics (403)', 'Statistics (403)'),
    ('Surgery (716)', 'Surgery (716)'),
    ('Veterinary Sciences (721)', 'Veterinary Sciences (721)'),
    ('Zoology (616)', 'Zoology (616)')
]

institutionrole_choices=[
    ('Undergraduate','Undergraduate'),
    ('Graduate Masters','Graduate Masters'),
    ("Graduate PhD",'Graduate PhD'),
    ('Student Other', 'Student Other'),
    ('Faculty','Faculty'),
    ('Staff','Staff'),
    ('Other','Other')
]

prefered_country_choices=[
    ('GB','United Kingdom'),
    ('US','United States'),
    ('DE','Germany')
    ]

all_country_choices=[
    ('AF','Afghanistan'),
    ('AL','Albania'),
    ('DZ','Algeria'),
    ('AS','American Samoa'),
    ('AD','Andorra'),
    ('AO','Angola'),
    ('AI','Anguilla'),
    ('AQ','Antarctica'),
    ('AG','Antigua and Barbuda'),
    ('AR','Argentina'),
    ('AM','Armenia'),
    ('AW','Aruba'),
    ('AU','Australia'),
    ('AT','Austria'),
    ('AZ','Azerbaijan'),
    ('BS','Bahamas'),
    ('BH','Bahrain'),
    ('BD','Bangladesh'),
    ('BB','Barbados'),
    ('BY','Belarus'),
    ('BE','Belgium'),
    ('BZ','Belize'),
    ('BJ','Benin'),
    ('BM','Bermuda'),
    ('BT','Bhutan'),
    ('BO','Bolivia'),
    ('BA','Bosnia and Herzegovina'),
    ('BW','Botswana'),
    ('BV','Bouvet Island'),
    ('BR','Brazil'),
    ('BQ','British Antarctic Territory'),
    ('IO','British Indian Ocean Territory'),
    ('VG','British Virgin Islands'),
    ('BN','Brunei'),
    ('BG','Bulgaria'),
    ('BF','Burkina Faso'),
    ('BI','Burundi'),
    ('KH','Cambodia'),
    ('CM','Cameroon'),
    ('CA','Canada'),
    ('CT','Canton and Enderbury Islands'),
    ('CV','Cape Verde'),
    ('KY','Cayman Islands'),
    ('CF','Central African Republic'),
    ('TD','Chad'),
    ('CL','Chile'),
    ('CN','China'),
    ('CX','Christmas Island'),
    ('CC','Cocos [Keeling] Islands'),
    ('CO','Colombia'),
    ('KM','Comoros'),
    ('CG','Congo - Brazzaville'),
    ('CD','Congo - Kinshasa'),
    ('CK','Cook Islands'),
    ('CR','Costa Rica'),
    ('HR','Croatia'),
    ('CU','Cuba'),
    ('CY','Cyprus'),
    ('CZ','Czech Republic'),
    ('CI','C\u00f4te d\u2019Ivoire'),
    ('DK','Denmark'),
    ('DJ','Djibouti'),
    ('DM','Dominica'),
    ('DO','Dominican Republic'),
    ('NQ','Dronning Maud Land'),
    ('DD','East Germany'),
    ('EC','Ecuador'),
    ('EG','Egypt'),
    ('SV','El Salvador'),
    ('GQ','Equatorial Guinea'),
    ('ER','Eritrea'),
    ('EE','Estonia'),
    ('ET','Ethiopia'),
    ('FK','Falkland Islands'),
    ('FO','Faroe Islands'),
    ('FJ','Fiji'),
    ('FI','Finland'),
    ('FR','France'),
    ('GF','French Guiana'),
    ('PF','French Polynesia'),
    ('TF','French Southern Territories'),
    ('FQ','French Southern and Antarctic Territories'),
    ('GA','Gabon'),
    ('GM','Gambia'),
    ('GE','Georgia'),
    ('DE','Germany'),
    ('GH','Ghana'),
    ('GI','Gibraltar'),
    ('GR','Greece'),
    ('GL','Greenland'),
    ('GD','Grenada'),
    ('GP','Guadeloupe'),
    ('GU','Guam'),
    ('GT','Guatemala'),
    ('GG','Guernsey'),
    ('GN','Guinea'),
    ('GW','Guinea-Bissau'),
    ('GY','Guyana'),
    ('HT','Haiti'),
    ('HM','Heard Island and McDonald Islands'),
    ('HN','Honduras'),
    ('HK','Hong Kong SAR China'),
    ('HU','Hungary'),
    ('IS','Iceland'),
    ('IN','India'),
    ('ID','Indonesia'),
    ('IR','Iran'),
    ('IQ','Iraq'),
    ('IE','Ireland'),
    ('IM','Isle of Man'),
    ('IL','Israel'),
    ('IT','Italy'),
    ('JM','Jamaica'),
    ('JP','Japan'),
    ('JE','Jersey'),
    ('JT','Johnston Island'),
    ('JO','Jordan'),
    ('KZ','Kazakhstan'),
    ('KE','Kenya'),
    ('KI','Kiribati'),
    ('KW','Kuwait'),
    ('KG','Kyrgyzstan'),
    ('LA','Laos'),
    ('LV','Latvia'),
    ('LB','Lebanon'),
    ('LS','Lesotho'),
    ('LR','Liberia'),
    ('LY','Libya'),
    ('LI','Liechtenstein'),
    ('LT','Lithuania'),
    ('LU','Luxembourg'),
    ('MO','Macau SAR China'),
    ('MK','Macedonia'),
    ('MG','Madagascar'),
    ('MW','Malawi'),
    ('MY','Malaysia'),
    ('MV','Maldives'),
    ('ML','Mali'),
    ('MT','Malta'),
    ('MH','Marshall Islands'),
    ('MQ','Martinique'),
    ('MR','Mauritania'),
    ('MU','Mauritius'),
    ('YT','Mayotte'),
    ('FX','Metropolitan France'),
    ('MX','Mexico'),
    ('FM','Micronesia'),
    ('MI','Midway Islands'),
    ('MD','Moldova'),
    ('MC','Monaco'),
    ('MN','Mongolia'),
    ('ME','Montenegro'),
    ('MS','Montserrat'),
    ('MA','Morocco'),
    ('MZ','Mozambique'),
    ('MM','Myanmar [Burma]'),
    ('NA','Namibia'),
    ('NR','Nauru'),
    ('NP','Nepal'),
    ('NL','Netherlands'),
    ('AN','Netherlands Antilles'),
    ('NT','Neutral Zone'),
    ('NC','New Caledonia'),
    ('NZ','New Zealand'),
    ('NI','Nicaragua'),
    ('NE','Niger'),
    ('NG','Nigeria'),
    ('NU','Niue'),
    ('NF','Norfolk Island'),
    ('KP','North Korea'),
    ('VD','North Vietnam'),
    ('MP','Northern Mariana Islands'),
    ('NO','Norway'),
    ('OM','Oman'),
    ('PC','Pacific Islands Trust Territory'),
    ('PK','Pakistan'),
    ('PW','Palau'),
    ('PS','Palestinian Territories'),
    ('PA','Panama'),
    ('PZ','Panama Canal Zone'),
    ('PG','Papua New Guinea'),
    ('PY','Paraguay'),
    ('YD','People\'s Democratic Republic of Yemen'),
    ('PE','Peru'),
    ('PH','Philippines'),
    ('PN','Pitcairn Islands'),
    ('PL','Poland'),
    ('PT','Portugal'),
    ('PR','Puerto Rico'),
    ('QA','Qatar'),
    ('RO','Romania'),
    ('RU','Russia'),
    ('RW','Rwanda'),
    ('RE','R\u00e9union'),
    ('BL','Saint Barth\u00e9lemy'),
    ('SH','Saint Helena'),
    ('KN','Saint Kitts and Nevis'),
    ('LC','Saint Lucia'),
    ('MF','Saint Martin'),
    ('PM','Saint Pierre and Miquelon'),
    ('VC','Saint Vincent and the Grenadines'),
    ('WS','Samoa'),
    ('SM','San Marino'),
    ('SA','Saudi Arabia'),
    ('SN','Senegal'),
    ('RS','Serbia'),
    ('CS','Serbia and Montenegro'),
    ('SC','Seychelles'),
    ('SL','Sierra Leone'),
    ('SG','Singapore'),
    ('SK','Slovakia'),
    ('SI','Slovenia'),
    ('SB','Solomon Islands'),
    ('SO','Somalia'),
    ('ZA','South Africa'),
    ('GS','South Georgia and the South Sandwich Islands'),
    ('KR','South Korea'),
    ('ES','Spain'),
    ('LK','Sri Lanka'),
    ('SD','Sudan'),
    ('SR','Suriname'),
    ('SJ','Svalbard and Jan Mayen'),
    ('SZ','Swaziland'),
    ('SE','Sweden'),
    ('CH','Switzerland'),
    ('SY','Syria'),
    ('ST','Sao Tom and Principe'),
    ('TW','Taiwan'),
    ('TJ','Tajikistan'),
    ('TZ','Tanzania'),
    ('TH','Thailand'),
    ('TL','Timor-Leste'),
    ('TG','Togo'),
    ('TK','Tokelau'),
    ('TO','Tonga'),
    ('TT','Trinidad and Tobago'),
    ('TN','Tunisia'),
    ('TR','Turkey'),
    ('TM','Turkmenistan'),
    ('TC','Turks and Caicos Islands'),
    ('TV','Tuvalu'),
    ('UM','U.S. Minor Outlying Islands'),
    ('PU','U.S. Miscellaneous Pacific Islands'),
    ('VI','U.S. Virgin Islands'),
    ('UG','Uganda'),
    ('UA','Ukraine'),
    ('SU','Union of Soviet Socialist Republics'),
    ('AE','United Arab Emirates'),
    ('GB','United Kingdom'),
    ('US','United States'),
    ('ZZ','Unknown or Invalid Region'),
    ('UY','Uruguay'),
    ('UZ','Uzbekistan'),
    ('VU','Vanuatu'),
    ('VA','Vatican City'),
    ('VE','Venezuela'),
    ('VN','Vietnam'),
    ('WK','Wake Island'),
    ('WF','Wallis and Futuna'),
    ('EH','Western Sahara'),
    ('YE','Yemen'),
    ('ZM','Zambia'),
    ('ZW','Zimbabwe'),
    ('AX','Aland Islands')]

country_choices=prefered_country_choices + all_country_choices 

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

        for key in data:
            data[key] = data[key][0]
        del data['button']

        if action == 'save':
            projects = Projects()
            project = MongoProject()
            for d in data:
                project[d] = data[d]

            projects.add(project)

        flash('Thanks for registering')
        return redirect('/')

    # return render_template('management/project_apply.html',
    #                        title="Project Application",
    #                        states=['save', 'cancel'],
    #                        form=form,
    #                        fields=ProjectRegistrationForm.keys)

    return render_template('management/project_apply.html',
                           title="Project Application",
                           states=['save', 'cancel'],
                           form=form,
                           fields=ProjectRegistrationForm.keys,
                           profile_fields=ProjectRegistrationForm.profile_keys,
                           agreements_fields=ProjectRegistrationForm.agreements_keys,
                           other_fields=ProjectRegistrationForm.other_keys)


def get_choices_for_form(services):
    choices = []
    for service in services:
        choices.append((service, service))
    return choices


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
        "resources_provision"]

    profile_keys = [\
        "title",
        "category",
        "keywords",
        "contact",
        "orientation",
        "primary_discipline",
        "abstract",
        "intellectual_merit",
        "broader_impact",
        "use_of_fg",
        "scale_of_use",
        "url",
        "comment",
        # "active",
        # "projectid",
        # "lead",
        # "managers",
        # "members",
        # "alumnis",
        # "grant_orgnization",
        # "grant_id",
        # "grant_url",
        "results"]

    agreements_keys= [\
        "agreement_use",
        "agreement_slides",
        "agreement_support",
        "agreement_software",
        "agreement_documentation"]

    other_keys = [\
        "comments",
        "join_open",
        "join_notification",
        "resources_services",
        # "resources_software",
        "resources_clusters",
        "resources_provision"]

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
    keywords = StringField('Keywords')
    # orientation = StringField('Orientation')
    orientation = RadioSelectField('Orientation', choices=[('research','Research'),('education','Education'),\
                                                           ('industry','Industry'),('government','Government')])
    primary_discipline = RadioSelectField('Primary discipline', choices=discipline_choices)
    contact = StringField('Contact')
    url = StringField(
        'URL', [validators.Length(min=6, max=50), validate_url_in_form])
    comment = TextAreaField('Comment')
    active = BooleanField('Active')
    projectid = StringField('Projectid')
    lead = StringField('Lead')
    managers = TextAreaField('Managers')
    members = TextAreaField('Members')
    alumnis = TextAreaField('Alumnis')
    grant_orgnization = StringField('Grant Orgnization')
    grant_id = StringField('Grant id')
    grant_url = StringField('Grant URL')
    results = TextAreaField('Results')
    agreement_use = BooleanField('NSF Agreement to use Future Systems')
    agreement_slides = BooleanField('Slide Collection')
    agreement_support = BooleanField('Support')
    agreement_software = BooleanField('Software Contributions')
    agreement_documentation = BooleanField('Documentation Contributions')
    agreement_images = BooleanField('Images')
    comments = TextAreaField('Comments')
    join_open = BooleanField('Join open')
    join_notification = BooleanField('Join notification')
    resources_services = MultiCheckboxField(
        'Resource Services',
        choices=get_choices_for_form(ProjectSERVICES))
    # resources_software = MultiCheckboxField('resources_software',
    #                         choices=get_choices_for_form(ProjectSOFTWARE))
    resources_clusters = MultiCheckboxField(

        'Resource Clusters', choices=get_choices_for_form(ProjectCLUSTERS))
    resources_provision = MultiCheckboxField(
        'Resource Provisioning', choices=get_choices_for_form(ProjectPROVISIONING))


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
        connect('user', port=27777)
        users = Users()
        if not users.validate_email(field.data):
            raise ValidationError('A user with this email already exists')

    def validate_username_in_form(form, field):
        if not re.match("^[a-z0-9]*$", field.data):
            raise ValidationError(
                'Only lower case characters a-z and numbers 0-9 allowed.')

        if not field.data.islower():
            raise ValidationError('The username must be lower case')

        connect('user', port=27777)
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
    citizenship = RadioSelectField("Citizenship", [validators.DataRequired()], choices=country_choices)
    institution = TextAreaField('Institution')
    institutionrole = RadioSelectField("Institution Role", [validators.DataRequired()], choices=institutionrole_choices)
    # institutionrole = StringField('Institution role')
    department = TextAreaField('Department')
    address = TextAreaField('Address', [validators.DataRequired(message="Address required")])
    country = RadioSelectField("Country", [validators.DataRequired()], choices=country_choices)
    advisor = TextAreaField('Advisor')
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])

    confirm = PasswordField('Confirm Password')
    # agreement = BooleanField('I accept the usage agreement', [validators.Required()])
    bio = TextAreaField('Bio', [validators.DataRequired()])


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

    if request.method == 'POST' and form.validate():
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

    return render_template('management/user_apply.html',
                           title="User Application",
                           states=['save', 'cancel'],
                           form=form,
                           fields=UserRegistrationForm.keys,
                           profile_fields=UserRegistrationForm.profile_keys,
                           organization_fields=UserRegistrationForm.organization_keys)


@management_module.route('/project/edit/<projectid>/', methods=['GET', 'POST'])
@login_required
def project_edit(projectid):
    connect('user', port=27777)

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

            except Exception, e:
                print "ERROR", e

        return render_template('management/project_edit.html',
                               project=project, states=['save', 'cancel'],
                               title="Project Management")


@management_module.route('/project/profile/<projectid>', methods=['GET'])
@login_required
def project_profile(projectid):

    connect('user', port=27777)
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

    connect('user', port=27777)
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

    connect('user', port=27777)
    projects = MongoProject.objects()

    return render_template('management/project_manage.html',
                           projects=projects, with_edit="True",
                           title="Project Management",
                           states=ProjectSTATUS)


@management_module.route('/m/project/list')
@login_required
def management_project_list():

    connect('user', port=27777)
    projects = MongoProject.objects()

    return render_template('management/project_list.html', projects=projects, with_edit="False", title="Project List")


@management_module.route('/m/user/manage', methods=['GET', 'POST'])
@login_required
def management_user_manage():

    connect('user', port=27777)
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
                           states=['approved', 'pending', 'denied', 'blocked', 'delete'],
                           title="User Management")


@management_module.route('/m/user/list')
@login_required
def management_user_list():

    connect('user', port=27777)
    users = MongoUser.objects()

    return render_template('management/user_manage.html', users=users, with_edit="False", title="User List")


@management_module.route('/user/profile/<username>')
def management_user_profile(username):
    connect('user', port=27777)
    try:
        user = MongoUser.objects(username=username)
        if user.count() == 1:
            pprint(user[0])
            print user[0].username
            print user[0].firstname
            print user[0].lastname

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
    connect('user', port=27777)

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
