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

preferred_country_choices=[
    ('United Kingdom(GB)','United Kingdom(GB)'),
    ('United States(US)','United States(US)'),
    ('Germany(DE)','Germany(DE)')]

all_country_choices=[
    ('Afghanistan(AF)','Afghanistan(AF)'),
    ('Albania(AL)','Albania(AL)'),
    ('Algeria(DZ)','Algeria(DZ)'),
    ('American Samoa(AS)','American Samoa(AS)'),
    ('Andorra(AD)','Andorra(AD)'),
    ('Angola(AO)','Angola(AO)'),
    ('Anguilla(AI)','Anguilla(AI)'),
    ('Antarctica(AQ)','Antarctica(AQ)'),
    ('Antigua and Barbuda(AG)','Antigua and Barbuda(AG)'),
    ('Argentina(AR)','Argentina(AR)'),
    ('Armenia(AM)','Armenia(AM)'),
    ('Aruba(AW)','Aruba(AW)'),
    ('Australia(AU)','Australia(AU)'),
    ('Austria(AT)','Austria(AT)'),
    ('Azerbaijan(AZ)','Azerbaijan(AZ)'),
    ('Bahamas(BS)','Bahamas(BS)'),
    ('Bahrain(BH)','Bahrain(BH)'),
    ('Bangladesh(BD)','Bangladesh(BD)'),
    ('Barbados(BB)','Barbados(BB)'),
    ('Belarus(BY)','Belarus(BY)'),
    ('Belgium(BE)','Belgium(BE)'),
    ('Belize(BZ)','Belize(BZ)'),
    ('Benin(BJ)','Benin(BJ)'),
    ('Bermuda(BM)','Bermuda(BM)'),
    ('Bhutan(BT)','Bhutan(BT)'),
    ('Bolivia(BO)','Bolivia(BO)'),
    ('Bosnia and Herzegovina(BA)','Bosnia and Herzegovina(BA)'),
    ('Botswana(BW)','Botswana(BW)'),
    ('Bouvet Island(BV)','Bouvet Island(BV)'),
    ('Brazil(BR)','Brazil(BR)'),
    ('British Antarctic Territory(BQ)','British Antarctic Territory(BQ)'),
    ('British Indian Ocean Territory(IO)','British Indian Ocean Territory(IO)'),
    ('British Virgin Islands(VG)','British Virgin Islands(VG)'),
    ('Brunei(BN)','Brunei(BN)'),
    ('Bulgaria(BG)','Bulgaria(BG)'),
    ('Burkina Faso(BF)','Burkina Faso(BF)'),
    ('Burundi(BI)','Burundi(BI)'),
    ('Cambodia(KH)','Cambodia(KH)'),
    ('Cameroon(CM)','Cameroon(CM)'),
    ('Canada(CA)','Canada(CA)'),
    ('Canton and Enderbury Islands(CT)','Canton and Enderbury Islands(CT)'),
    ('Cape Verde(CV)','Cape Verde(CV)'),
    ('Cayman Islands(KY)','Cayman Islands(KY)'),
    ('Central African Republic(CF)','Central African Republic(CF)'),
    ('Chad(TD)','Chad(TD)'),
    ('Chile(CL)','Chile(CL)'),
    ('China(CN)','China(CN)'),
    ('Christmas Island(CX)','Christmas Island(CX)'),
    ('Cocos [Keeling] Islands(CC)','Cocos [Keeling] Islands(CC)'),
    ('Colombia(CO)','Colombia(CO)'),
    ('Comoros(KM)','Comoros(KM)'),
    ('Congo - Brazzaville(CG)','Congo - Brazzaville(CG)'),
    ('Congo - Kinshasa(CD)','Congo - Kinshasa(CD)'),
    ('Cook Islands(CK)','Cook Islands(CK)'),
    ('Costa Rica(CR)','Costa Rica(CR)'),
    ('Croatia(HR)','Croatia(HR)'),
    ('Cuba(CU)','Cuba(CU)'),
    ('Cyprus(CY)','Cyprus(CY)'),
    ('Czech Republic(CZ)','Czech Republic(CZ)'),
    ('C\u00f4te d\u2019Ivoire(CI)','C\u00f4te d\u2019Ivoire(CI)'),
    ('Denmark(DK)','Denmark(DK)'),
    ('Djibouti(DJ)','Djibouti(DJ)'),
    ('Dominica(DM)','Dominica(DM)'),
    ('Dominican Republic(DO)','Dominican Republic(DO)'),
    ('Dronning Maud Land(NQ)','Dronning Maud Land(NQ)'),
    ('East Germany(DD)','East Germany(DD)'),
    ('Ecuador(EC)','Ecuador(EC)'),
    ('Egypt(EG)','Egypt(EG)'),
    ('El Salvador(SV)','El Salvador(SV)'),
    ('Equatorial Guinea(GQ)','Equatorial Guinea(GQ)'),
    ('Eritrea(ER)','Eritrea(ER)'),
    ('Estonia(EE)','Estonia(EE)'),
    ('Ethiopia(ET)','Ethiopia(ET)'),
    ('Falkland Islands(FK)','Falkland Islands(FK)'),
    ('Faroe Islands(FO)','Faroe Islands(FO)'),
    ('Fiji(FJ)','Fiji(FJ)'),
    ('Finland(FI)','Finland(FI)'),
    ('France(FR)','France(FR)'),
    ('French Guiana(GF)','French Guiana(GF)'),
    ('French Polynesia(PF)','French Polynesia(PF)'),
    ('French Southern Territories(TF)','French Southern Territories(TF)'),
    ('French Southern and Antarctic Territories(FQ)','French Southern and Antarctic Territories(FQ)'),
    ('Gabon(GA)','Gabon(GA)'),
    ('Gambia(GM)','Gambia(GM)'),
    ('Georgia(GE)','Georgia(GE)'),
    ('Germany(DE)','Germany(DE)'),
    ('Ghana(GH)','Ghana(GH)'),
    ('Gibraltar(GI)','Gibraltar(GI)'),
    ('Greece(GR)','Greece(GR)'),
    ('Greenland(GL)','Greenland(GL)'),
    ('Grenada(GD)','Grenada(GD)'),
    ('Guadeloupe(GP)','Guadeloupe(GP)'),
    ('Guam(GU)','Guam(GU)'),
    ('Guatemala(GT)','Guatemala(GT)'),
    ('Guernsey(GG)','Guernsey(GG)'),
    ('Guinea(GN)','Guinea(GN)'),
    ('Guinea-Bissau(GW)','Guinea-Bissau(GW)'),
    ('Guyana(GY)','Guyana(GY)'),
    ('Haiti(HT)','Haiti(HT)'),
    ('Heard Island and McDonald Islands(HM)','Heard Island and McDonald Islands(HM)'),
    ('Honduras(HN)','Honduras(HN)'),
    ('Hong Kong SAR China(HK)','Hong Kong SAR China(HK)'),
    ('Hungary(HU)','Hungary(HU)'),
    ('Iceland(IS)','Iceland(IS)'),
    ('India(IN)','India(IN)'),
    ('Indonesia(ID)','Indonesia(ID)'),
    ('Iran(IR)','Iran(IR)'),
    ('Iraq(IQ)','Iraq(IQ)'),
    ('Ireland(IE)','Ireland(IE)'),
    ('Isle of Man(IM)','Isle of Man(IM)'),
    ('Israel(IL)','Israel(IL)'),
    ('Italy(IT)','Italy(IT)'),
    ('Jamaica(JM)','Jamaica(JM)'),
    ('Japan(JP)','Japan(JP)'),
    ('Jersey(JE)','Jersey(JE)'),
    ('Johnston Island(JT)','Johnston Island(JT)'),
    ('Jordan(JO)','Jordan(JO)'),
    ('Kazakhstan(KZ)','Kazakhstan(KZ)'),
    ('Kenya(KE)','Kenya(KE)'),
    ('Kiribati(KI)','Kiribati(KI)'),
    ('Kuwait(KW)','Kuwait(KW)'),
    ('Kyrgyzstan(KG)','Kyrgyzstan(KG)'),
    ('Laos(LA)','Laos(LA)'),
    ('Latvia(LV)','Latvia(LV)'),
    ('Lebanon(LB)','Lebanon(LB)'),
    ('Lesotho(LS)','Lesotho(LS)'),
    ('Liberia(LR)','Liberia(LR)'),
    ('Libya(LY)','Libya(LY)'),
    ('Liechtenstein(LI)','Liechtenstein(LI)'),
    ('Lithuania(LT)','Lithuania(LT)'),
    ('Luxembourg(LU)','Luxembourg(LU)'),
    ('Macau SAR China(MO)','Macau SAR China(MO)'),
    ('Macedonia(MK)','Macedonia(MK)'),
    ('Madagascar(MG)','Madagascar(MG)'),
    ('Malawi(MW)','Malawi(MW)'),
    ('Malaysia(MY)','Malaysia(MY)'),
    ('Maldives(MV)','Maldives(MV)'),
    ('Mali(ML)','Mali(ML)'),
    ('Malta(MT)','Malta(MT)'),
    ('Marshall Islands(MH)','Marshall Islands(MH)'),
    ('Martinique(MQ)','Martinique(MQ)'),
    ('Mauritania(MR)','Mauritania(MR)'),
    ('Mauritius(MU)','Mauritius(MU)'),
    ('Mayotte(YT)','Mayotte(YT)'),
    ('Metropolitan France(FX)','Metropolitan France(FX)'),
    ('Mexico(MX)','Mexico(MX)'),
    ('Micronesia(FM)','Micronesia(FM)'),
    ('Midway Islands(MI)','Midway Islands(MI)'),
    ('Moldova(MD)','Moldova(MD)'),
    ('Monaco(MC)','Monaco(MC)'),
    ('Mongolia(MN)','Mongolia(MN)'),
    ('Montenegro(ME)','Montenegro(ME)'),
    ('Montserrat(MS)','Montserrat(MS)'),
    ('Morocco(MA)','Morocco(MA)'),
    ('Mozambique(MZ)','Mozambique(MZ)'),
    ('Myanmar [Burma](MM)','Myanmar [Burma](MM)'),
    ('Namibia(NA)','Namibia(NA)'),
    ('Nauru(NR)','Nauru(NR)'),
    ('Nepal(NP)','Nepal(NP)'),
    ('Netherlands(NL)','Netherlands(NL)'),
    ('Netherlands Antilles(AN)','Netherlands Antilles(AN)'),
    ('Neutral Zone(NT)','Neutral Zone(NT)'),
    ('New Caledonia(NC)','New Caledonia(NC)'),
    ('New Zealand(NZ)','New Zealand(NZ)'),
    ('Nicaragua(NI)','Nicaragua(NI)'),
    ('Niger(NE)','Niger(NE)'),
    ('Nigeria(NG)','Nigeria(NG)'),
    ('Niue(NU)','Niue(NU)'),
    ('Norfolk Island(NF)','Norfolk Island(NF)'),
    ('North Korea(KP)','North Korea(KP)'),
    ('North Vietnam(VD)','North Vietnam(VD)'),
    ('Northern Mariana Islands(MP)','Northern Mariana Islands(MP)'),
    ('Norway(NO)','Norway(NO)'),
    ('Oman(OM)','Oman(OM)'),
    ('Pacific Islands Trust Territory(PC)','Pacific Islands Trust Territory(PC)'),
    ('Pakistan(PK)','Pakistan(PK)'),
    ('Palau(PW)','Palau(PW)'),
    ('Palestinian Territories(PS)','Palestinian Territories(PS)'),
    ('Panama(PA)','Panama(PA)'),
    ('Panama Canal Zone(PZ)','Panama Canal Zone(PZ)'),
    ('Papua New Guinea(PG)','Papua New Guinea(PG)'),
    ('Paraguay(PY)','Paraguay(PY)'),
    ('People\'s Democratic Republic of Yemen(YD)','People\'s Democratic Republic of Yemen(YD)'),
    ('Peru(PE)','Peru(PE)'),
    ('Philippines(PH)','Philippines(PH)'),
    ('Pitcairn Islands(PN)','Pitcairn Islands(PN)'),
    ('Poland(PL)','Poland(PL)'),
    ('Portugal(PT)','Portugal(PT)'),
    ('Puerto Rico(PR)','Puerto Rico(PR)'),
    ('Qatar(QA)','Qatar(QA)'),
    ('Romania(RO)','Romania(RO)'),
    ('Russia(RU)','Russia(RU)'),
    ('Rwanda(RW)','Rwanda(RW)'),
    ('R\u00e9union(RE)','R\u00e9union(RE)'),
    ('Saint Barth\u00e9lemy(BL)','Saint Barth\u00e9lemy(BL)'),
    ('Saint Helena(SH)','Saint Helena(SH)'),
    ('Saint Kitts and Nevis(KN)','Saint Kitts and Nevis(KN)'),
    ('Saint Lucia(LC)','Saint Lucia(LC)'),
    ('Saint Martin(MF)','Saint Martin(MF)'),
    ('Saint Pierre and Miquelon(PM)','Saint Pierre and Miquelon(PM)'),
    ('Saint Vincent and the Grenadines(VC)','Saint Vincent and the Grenadines(VC)'),
    ('Samoa(WS)','Samoa(WS)'),
    ('San Marino(SM)','San Marino(SM)'),
    ('Saudi Arabia(SA)','Saudi Arabia(SA)'),
    ('Senegal(SN)','Senegal(SN)'),
    ('Serbia(RS)','Serbia(RS)'),
    ('Serbia and Montenegro(CS)','Serbia and Montenegro(CS)'),
    ('Seychelles(SC)','Seychelles(SC)'),
    ('Sierra Leone(SL)','Sierra Leone(SL)'),
    ('Singapore(SG)','Singapore(SG)'),
    ('Slovakia(SK)','Slovakia(SK)'),
    ('Slovenia(SI)','Slovenia(SI)'),
    ('Solomon Islands(SB)','Solomon Islands(SB)'),
    ('Somalia(SO)','Somalia(SO)'),
    ('South Africa(ZA)','South Africa(ZA)'),
    ('South Georgia and the South Sandwich Islands(GS)','South Georgia and the South Sandwich Islands(GS)'),
    ('South Korea(KR)','South Korea(KR)'),
    ('Spain(ES)','Spain(ES)'),
    ('Sri Lanka(LK)','Sri Lanka(LK)'),
    ('Sudan(SD)','Sudan(SD)'),
    ('Suriname(SR)','Suriname(SR)'),
    ('Svalbard and Jan Mayen(SJ)','Svalbard and Jan Mayen(SJ)'),
    ('Swaziland(SZ)','Swaziland(SZ)'),
    ('Sweden(SE)','Sweden(SE)'),
    ('Switzerland(CH)','Switzerland(CH)'),
    ('Syria(SY)','Syria(SY)'),
    ('Sao Tom and Principe(ST)','Sao Tom and Principe(ST)'),
    ('Taiwan(TW)','Taiwan(TW)'),
    ('Tajikistan(TJ)','Tajikistan(TJ)'),
    ('Tanzania(TZ)','Tanzania(TZ)'),
    ('Thailand(TH)','Thailand(TH)'),
    ('Timor-Leste(TL)','Timor-Leste(TL)'),
    ('Togo(TG)','Togo(TG)'),
    ('Tokelau(TK)','Tokelau(TK)'),
    ('Tonga(TO)','Tonga(TO)'),
    ('Trinidad and Tobago(TT)','Trinidad and Tobago(TT)'),
    ('Tunisia(TN)','Tunisia(TN)'),
    ('Turkey(TR)','Turkey(TR)'),
    ('Turkmenistan(TM)','Turkmenistan(TM)'),
    ('Turks and Caicos Islands(TC)','Turks and Caicos Islands(TC)'),
    ('Tuvalu(TV)','Tuvalu(TV)'),
    ('U.S. Minor Outlying Islands(UM)','U.S. Minor Outlying Islands(UM)'),
    ('U.S. Miscellaneous Pacific Islands(PU)','U.S. Miscellaneous Pacific Islands(PU)'),
    ('U.S. Virgin Islands(VI)','U.S. Virgin Islands(VI)'),
    ('Uganda(UG)','Uganda(UG)'),
    ('Ukraine(UA)','Ukraine(UA)'),
    ('Union of Soviet Socialist Republics(SU)','Union of Soviet Socialist Republics(SU)'),
    ('United Arab Emirates(AE)','United Arab Emirates(AE)'),
    ('United Kingdom(GB)','United Kingdom(GB)'),
    ('United States(US)','United States(US)'),
    ('Unknown or Invalid Region(ZZ)','Unknown or Invalid Region(ZZ)'),
    ('Uruguay(UY)','Uruguay(UY)'),
    ('Uzbekistan(UZ)','Uzbekistan(UZ)'),
    ('Vanuatu(VU)','Vanuatu(VU)'),
    ('Vatican City(VA)','Vatican City(VA)'),
    ('Venezuela(VE)','Venezuela(VE)'),
    ('Vietnam(VN)','Vietnam(VN)'),
    ('Wake Island(WK)','Wake Island(WK)'),
    ('Wallis and Futuna(WF)','Wallis and Futuna(WF)'),
    ('Western Sahara(EH)','Western Sahara(EH)'),
    ('Yemen(YE)','Yemen(YE)'),
    ('Zambia(ZM)','Zambia(ZM)'),
    ('Zimbabwe(ZW)','Zimbabwe(ZW)'),
    ('Aland Islands(AX)','Aland Islands(AX)')
]

country_choices=preferred_country_choices + all_country_choices

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
                           vocab_fields=ProjectRegistrationForm.vocab_keys,
                           contact_fields=ProjectRegistrationForm.project_contact_keys,
                           project_details_fields=ProjectRegistrationForm.project_details_keys,
                           agreements_fields=ProjectRegistrationForm.agreements_keys,
                           nsf_fields=ProjectRegistrationForm.nsf_keys,
                           resource_fields=ProjectRegistrationForm.resource_keys,
                           membership_fields=ProjectRegistrationForm.membership_keys,
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
        "resources_provision",
        "grant_organization",
        "grant_id",
        "grant_url"]

    profile_keys = [\
        "title"]


    vocab_keys = [\
        "category",
        "keywords"]

    project_contact_keys = [\
        "lead",
        "managers",
        "members",
        "alumnis",
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

    nsf_keys = [\
        "grant_organization",
        "grant_id",
        "grant_url"
        ]


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
    keywords = StringField('Keywords')
    # orientation = StringField('Orientation')
    orientation = RadioSelectField('Orientation', choices=[('research','Research'),('education','Education'),\
                                                           ('industry','Industry'),('government','Government')])
    primary_discipline = RadioSelectField('Primary discipline', choices=discipline_choices)
    url = StringField(
        'URL', [validators.Length(min=6, max=50), validate_url_in_form])
    comment = TextAreaField('Comment')
    active = BooleanField('Active')
    projectid = StringField('Projectid')
    contact = StringField('Contact')
    lead = StringField('Project Lead')
    managers = TextAreaField('Project Managers')
    members = TextAreaField('Project Members')
    alumnis = TextAreaField('Project Alumni')
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
