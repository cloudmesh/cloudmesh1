

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


# ============================================================
# ROUTE: KILL
# ============================================================
@cloud_module.route('/cm/kill/')
@login_required
def kill_vms():
    print "-> kill all"
    r = cm("--set", "quiet", "kill", _tty_in=True)
    return redirect('/mesh/servers')


# ============================================================
# ROUTE: Filter
# ============================================================


@cloud_module.route('/cm/filter/<cloud>/', methods=['GET', 'POST'])
@login_required
def filter(cloud=None):
    # print "-> filter", cloud

    #
    # BUG: when cloud is none
    #
    name = cloud
    if request.method == 'POST':
        query_states = []
        state_table = {}
        for state in clouds.states(name):
            state_name = "%s:%s" % (name, state)
            state_table[state] = state_name in request.form
            if state_table[state]:
                query_states.append(state)
        config.set_filter(name, state_table, 'state')

        clouds.state_filter(name, query_states)

    return redirect('/mesh/servers')
