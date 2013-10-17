
# ============================================================
# ROUTE: sitemap
# ============================================================

"""
@app.route("/site-map/")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        print"PPP>",  rule, rule.methods, rule.defaults, rule.endpoint, rule.arguments
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        try:
            if "GET" in rule.methods and len(rule.defaults) >= len(rule.arguments):
                url = url_for(rule.endpoint)
                links.append((url, rule.endpoint))
                print "Rule added", url, links[url]
        except:
            print "Rule not activated"
    # links is now a list of url, endpoint tuples
"""



# ============================================================
# ROUTE: FLAVOR
# ============================================================

# @cloud_module.route('/flavors/<cloud>/' )


@cloud_module.route('/flavors/', methods=['GET', 'POST'])
@login_required
def display_flavors(cloud=None):

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")

    if request.method == 'POST':
        for cloud in config.active():
            config['cloudmesh']['clouds'][cloud]['default'][
                'flavor'] = request.form[cloud]
            config.write()

    return render_template(
        'flavor.html',
        updated=time_now,
        cloudmesh=clouds,
        clouds=clouds.clouds,
        config=config)


# ============================================================
# ROUTE: IMAGES
# ============================================================
# @cloud_module.route('/images/<cloud>/')
@login_required
@cloud_module.route('/images/', methods=['GET', 'POST'])
def display_images():
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")

    if request.method == 'POST':
        for cloud in config.active():
            config['cloudmesh']['clouds'][cloud][
                'default']['image'] = request.form[cloud]
            config.write()

    return render_template(
        'images.html',
        updated=time_now,
        clouds=clouds.clouds,
        cloudmesh=clouds,
        config=config)
