from cloudmesh.config.cm_config import cm_config, cm_config_server
from cloudmesh.config.cm_keys import cm_keys
from cloudmesh.config.cm_projects import cm_projects
from cloudmesh.util.util import cond_decorator
from datetime import datetime
from flask import Blueprint, g, render_template, request
from flask.ext.login import login_required
import cloudmesh
from cloudmesh.user.cm_userLDAP import cm_userLDAP
from pprint import pprint

profile_module = Blueprint('profile_module', __name__)

#
# ROUTE: PROFILE
#


# @cond_decorator(cloudmesh.with_login, login_required)

@profile_module.route('/profile/', methods=['GET', 'POST'])
@login_required
def profile():
    # bug the global var of the ditc should be used

    with_ldap = cm_config_server().get("cloudmesh.server.ldap.with_ldap")


    config = cm_config()
    # username = config.get("cloudmesh.hpc.username")
    # projects = cm_projects()
    # person = config.get('cloudmesh.profile')
    # keys = cm_keys()
    # version = "tmp"

    userdata = g.user

    if with_ldap:
        idp = cm_userLDAP ()
        idp.connect("fg-ldap", "ldap")
        user_mongo = idp.find_one({'cm_user_id': userdata.id})
        print "MONGO USER"
    else:
        user_mongo = get_ldap_user_from_yaml()
    print 70 * "-"
    pprint (user_mongo)
    if 'default' not in user_mongo:
        user_mongo['default'] = {}
    print 70 * "-"

    if request.method == 'POST':
        print request.form
        print "p", projects
        # print "c", config

        projects.default = request.form['field-selected-project']


        user_mongo['default']['security'] = request.form[
            'field-selected-securityGroup']

        user_mongo['index'] = request.form['field-index']

        user_mongo['prefix'] = request.form['field-prefix']

        user_mongo['firstname'] = request.form['field-firstname']
        user_mongo['lastname'] = request.form['field-lastname']
        user_mongo['phone'] = request.form['field-phone']
        user_mongo['email'] = request.form['field-email']
        print "setting the values"
        user_mongo['default']['security'] = request.form['field-default-cloud']
        # # print request.form["field-cloud-activated-" + value]
        # print "setting the cloud values"
        # print config
        # config.write()
        # print "WRITING DONE"

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")

    address = '<br>'.join(str(x) for x in user_mongo['address'])
    return render_template('profile.html',
                           updated=time_now,
                           # clouds=clouds,
                           config=config,  # just to populate active projects
                           configuration=config['cloudmesh'],  # just to populate security groups
                           user=user_mongo,
                           userdata=userdata
                           )
