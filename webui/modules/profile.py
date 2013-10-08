from cloudmesh.config.cm_config import cm_config, cm_config_server
from cloudmesh.config.cm_keys import cm_keys
from cloudmesh.config.cm_projects import cm_projects
from cloudmesh.util.util import cond_decorator
from datetime import datetime
from flask import Blueprint, g, render_template, request
from flask.ext.login import login_required
import cloudmesh
from pprint import pprint
# from cloudmesh.user.cm_userLDAP import get_ldap_user_from_yaml
from cloudmesh.user.cm_user import cm_user

profile_module = Blueprint('profile_module', __name__)

#
# ROUTE: PROFILE
#


# @cond_decorator(cloudmesh.with_login, login_required)

@profile_module.route('/profile/', methods=['GET', 'POST'])
@login_required
def profile():

    def upload_default(username, attribute):
        user_obj.set_default_attribute(username, attribute, user['defaults'][attribute])

    # bug the global var of the ditc should be used

    # with_ldap = cm_config_server().get("cloudmesh.server.ldap.with_ldap")


    config = cm_config()
    # username = config.get("cloudmesh.hpc.username")
    # projects = cm_projects()
    # person = config.get('cloudmesh.profile')
    # keys = cm_keys()
    # version = "tmp"

    userdata = g.user

    # if with_ldap:
    username = userdata.id
    user_obj = cm_user()
    user = user_obj.info(username)

    # else:
    #    user = get_ldap_user_from_yaml()


    print 70 * "-"
    pprint (user)
    if 'defaults' not in user:
        user['defaults'] = {}
        user.set_defaults(username, {})
    print 70 * "-"

    if request.method == 'POST':




        print "REQUEST"
        pprint(request.__dict__)
        print "OOOOOO", request.form

        if 'field-project' in request.form:
            user['defaults']['project'] = request.form['field-project']

        if 'field-securitygroup' in request.form:
            user['defaults']['securitygroup'] = request.form['field-securitygroup']

        if 'field-index' in request.form:
            user['defaults']['index'] = request.form['field-index']

        if 'field-prefix' in request.form:
            user['defaults']['prefix'] = request.form['field-prefix']

        if 'field-default-cloud' in request.form:
            user['defaults']['cloud'] = request.form['field-default-cloud']

        if 'field-key' in request.form:
            user['defaults']['key'] = request.form['field-key']


        user['defaults']['activeclouds'] = []
        for cloudname in config.cloudnames():
            form_key = 'field-cloud-activated-{0}'.format(cloudname)
            if form_key in request.form:
                user['defaults']['activeclouds'].append(cloudname)





        '''
        user['profile']['firstname'] = request.form['field-firstname']
        user['profile']['lastname'] = request.form['field-lastname']
        user['profile']['phone'] = request.form['field-phone']
        user['profile']['email'] = request.form['field-email']
        '''

        print "setting the values"
        user_obj.set_defaults(username, user['defaults'])

        # # print request.form["field-cloud-activated-" + value]
        # print "setting the cloud values"
        # print config
        # config.write()
        # print "WRITING DONE"

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")

    return render_template('profile.html',
                           updated=time_now,
                           configuration=config['cloudmesh'],  # just to populate security groups
                           user=user,
                           userdata=userdata
                           )
