

#
# from webui/module/cloud.py
#

# ============================================================
# ROUTE: SAVE
# ============================================================


@cloud_module.route('/save/')
@login_required
def save():
    print "Saving the cloud status"
    # clouds.save()
    return redirect('/mesh/servers')

# ============================================================
# ROUTE: LOAD
# ============================================================


@cloud_module.route('/load/')
@login_required
def load():
    print "Loading the cloud status"
    # clouds.load()
    return redirect('/mesh/servers')
