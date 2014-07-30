from cloudmesh.management.project import STATUS as ProjectSTATUS
from cloudmesh_common.logger import LOGGER
from flask import Blueprint, render_template, request
from flask.ext.login import login_required
from pprint import pprint, pprint
from mongoengine import connect
from cloudmesh.management.user import User as MongoUser
from cloudmesh.management.project import Project as MongoProject 


log = LOGGER(__file__)

management_module = Blueprint('management_module', __name__)


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

            user.bio = data["bio"]
            user.citizenship = data["citizenship"]
            user.firstname = data["firstname"]
            user.title = data["title"]
            user.url = data["url"]
            user.lastname = data["lastname"]
            user.address = data["address"]
            user.institution = data["institution"]
            user.phone = data["phone"]
            user.advisor = data["advisor"]
            user.department = data["department"]

            user.country = data["country"]
            user.email = data["email"]

            user.save()

        return render_template('management/user_edit.html', user=user, states=['save', 'cancel'])            
        
