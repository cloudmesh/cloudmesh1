from cloudmesh.user.cm_user import cm_user
from cloudmesh_common.util import cond_decorator
from flask import Blueprint, g, render_template, request, redirect
from flask.ext.login import login_required
from pprint import pprint
from cloudmesh.config.cm_keys import cm_keys_mongo
from cloudmesh_common.logger import LOGGER

log = LOGGER(__file__)


keys_module = Blueprint('keys_module', __name__)

#
# ROUTE: KEYS
#


@keys_module.route('/keys/', methods=['GET', 'POST'])
@login_required
def managekeys():

    idp = cm_user()
    user_mongo = idp.info(g.user.id)

    # else:
    #    user_mongo = get_ldap_user_from_yaml()

    print 70 * "-"
    pprint(user_mongo)
    if 'defaults' not in user_mongo:
        user_mongo['defaults'] = {}

    msg = ''
    """
    keys:
      default: name 1
      keylist:
         name 1: $HOME/.ssh/id_rsa.pub #  replaced with the key
         name 2: $HOME/.ssh/id_rsa2.pub #  replaced with the key
         bla: key ssh-rsa AAAAB3.....zzzz keyname
    """
    if request.method == 'POST' and request.form.has_key('keyname'):
        keyname = request.form['keyname']
        fileorstring = request.form['keyorpath']

        #
        # TODO: keys not defined
        #
        if keys.defined(keyname):
            msg = "Key name already exists. Please delete the key '{0}' before proceeding.".format(
                keyname)
        else:
            try:
                keys.set(keyname, fileorstring, expand=True)
                msg = 'Key %s added successfully' % keyname
                keys.write()
            except Exception, e:
                keys.delete(keyname)
                msg = e

    elif request.method == 'POST':
        keys['default'] = request.form['selectkeys']
        keys.write()

    return render_template('user/keys.html',
                           user=user_mongo,
                           show=msg)


@keys_module.route('/keys/delete/<name>/', methods=['GET'])
@login_required
def deletekey(name):
    #
    #  BUG cm_keys reads from config file
    #
    keys = cm_keys_mongo(g.user.id)

    try:
        keys.delete(name)
        # delete from mongo directly
        # no seperate write back needed
        # keys.write()
    except:
        print "Error: deleting the key %s" % name
    return redirect("/keys/")
