from cloudmesh.config.cm_config import cm_config, cm_config_server
from cloudmesh.config.cm_projects import cm_projects
from cloudmesh_common.util import cond_decorator
from datetime import datetime
from flask import Blueprint, g, render_template, request
from flask.ext.login import login_required
import cloudmesh
from pprint import pprint
# from cloudmesh.user.cm_userLDAP import get_ldap_user_from_yaml
from cloudmesh.user.cm_user import cm_user


from cloudmesh_common.logger import LOGGER

log = LOGGER(__file__)

profile_module = Blueprint('profile_module', __name__)

#
# ROUTE: PROFILE
#


@profile_module.route('/profile/', methods=['GET', 'POST'])
@login_required
def profile():

    config = cm_config()

    userdata = g.user
    username = userdata.id
    user_obj = cm_user()
    user = user_obj.info(username)

    if 'defaults' not in user:
        user['defaults'] = {}
        user.set_defaults(username, {})

    if request.method == 'POST':

        # print "REQUEST"
        # pprint(request.__dict__)
        # print "OOOOOO", request.form

        if 'field-project' in request.form:
            user['defaults']['project'] = request.form['field-project']

        if 'field-securitygroup' in request.form:
            user['defaults']['securitygroup'] = request.form[
                'field-securitygroup']

        if 'field-index' in request.form:
            user['defaults']['index'] = request.form['field-index']

        if 'field-prefix' in request.form:
            user['defaults']['prefix'] = request.form['field-prefix']

        if 'field-default-cloud' in request.form:
            user['defaults']['cloud'] = request.form['field-default-cloud']

        if 'field-key' in request.form:
            user['defaults']['key'] = request.form['field-key']

        user['defaults']['activeclouds'] = []
        regclouds = user['defaults']['registered_clouds']
        for cloudname in regclouds:
            form_key = 'field-cloud-activated-{0}'.format(cloudname)
            if form_key in request.form:
                print "ACTIVE IN FORM", cloudname
                user['defaults']['activeclouds'].append(cloudname)

        '''
        user['profile']['firstname'] = request.form['field-firstname']
        user['profile']['lastname'] = request.form['field-lastname']
        user['profile']['phone'] = request.form['field-phone']
        user['profile']['email'] = request.form['field-email']
        '''

        print "setting the values"
        user_obj.set_defaults(username, user['defaults'])

        # print request.form["field-cloud-activated-" + value]
        # print "setting the cloud values"
        # print config
        # config.write()
        # print "WRITING DONE"

        user = user_obj.info(username)
        # print "UD", user["defaults"]["activeclouds"]

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")

    return render_template('user/profile.html',
                           updated=time_now,
                           # just to populate security groups
                           configuration=config['cloudmesh'],
                           user=user,
                           userdata=userdata
                           )
