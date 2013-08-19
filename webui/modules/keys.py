from flask import Blueprint
from flask import render_template, request, redirect
from cloudmesh.config.cm_keys import cm_keys

keys_module = Blueprint('keys_module', __name__)

#
# ROUTE: KEYS
#


@keys_module.route('/keys/', methods=['GET', 'POST'])
def managekeys():
    keys = cm_keys()

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

        if keys.defined(keyname):
            msg = "Key name already exists. Please delete the key '{0}' before proceeding.".format(keyname)
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

    return render_template('keys.html',
                           keys=keys,
                           show=msg)


@keys_module.route('/keys/delete/<name>/')
def deletekey(name):
    keys = cm_keys()

    try:
        keys.delete(name)
        keys.write()
    except:
        print "Error: deleting the key %s" % name
    return redirect("/keys/")
