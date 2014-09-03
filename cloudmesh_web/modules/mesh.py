from ast import literal_eval
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.config.cm_config import cm_config, cm_config_server
from cloudmesh.pbs.pbs_mongo import pbs_mongo
from cloudmesh_common.logger import LOGGER
from cloudmesh_common.util import address_string, cond_decorator
from datetime import datetime
from flask import Blueprint, g, render_template, request, redirect
from flask.ext.login import login_required
from pprint import pprint
import cloudmesh
from cloudmesh.user.cm_user import cm_user
from flask.ext.principal import Permission, RoleNeed
from cloudmesh_common.util import banner
# from cloudmesh.experiment.cm_experiment_db import cm_experiment_db
import json

log = LOGGER(__file__)

admin_permission = Permission(RoleNeed('admin'))

mesh_module = Blueprint('mesh_module', __name__)

# ============================================================
# ROUTE: /mesh/images
# ============================================================

def getCurrentUserinfo():
    userinfo = cm_user().info(g.user.id)
    return userinfo

def with_active_clouds():
    ret = False
    userinfo = getCurrentUserinfo()
    if "activeclouds" in userinfo["defaults"] and\
        len(userinfo["defaults"]["activeclouds"]) > 0:
        ret = True
    return ret

@mesh_module.route('/mesh/register/clouds', methods=['GET', 'POST'])
@login_required
def mesh_register_clouds():


    config = cm_config()
    userdata = g.user
    cm_user_id = userdata.id
    user_obj = cm_user()
    user = user_obj.info(cm_user_id)


    cloudtypes = {}
    for cloud in config.get("cloudmesh.clouds"):
        cloudtypes[cloud] = config['cloudmesh']['clouds'][cloud]['cm_type']


    credentials = user_obj.get_credentials(cm_user_id)
    # pprint(credentials)

    error = {}
    registered = {}
    for cloudname in user['defaults']['registered_clouds']:
        registered[cloudname] = True
    # todo define correct actions.
    if request.method == 'POST':

        cloudname = request.form['cloudInput']



        if cloudname in credentials:
            if 'credential' in credentials[cloudname]:
                credential = credentials[cloudname]['credential']
            else:
                credentials[cloudname] = None
        else:
            credentials[cloudname] = None


        if cloudtypes[cloudname] == "openstack":

            d = {}
            if credentials[cloudname] == None:
                 d = {'OS_USERNAME' : cm_user_id,
                      'OS_PASSWORD': '',
                      'OS_TENANT_NAME': ''
                }

            user_obj.set_credential(cm_user_id, cloudname, d)

            error[cloudname] = ''

            d = {"CM_CLOUD_TYPE": cloudtypes[cloudname]}


            cloudid = 'field-{0}-{1}-text'.format(cloudname, "OS_USERNAME")

            if cloudid in request.form:
                username = request.form[cloudid]
            else:
                username = cm_user_id
            d["OS_USERNAME"] = username


            fields = ["OS_PASSWORD", "OS_TENANT_NAME"]

            for key in fields:

                if key == 'OS_PASSWORD':
                    cloudid = 'field-{0}-{1}-password'.format(cloudname, key)
                else:
                    cloudid = 'field-{0}-{1}-text'.format(cloudname, key)


                if cloudid in request.form:
                    content = request.form[cloudid]
                    d[key] = content
                elif key in credential:
                    content = credential[key]
                    d[key] = content
                if content == '':
                    error[cloudname] = error[cloudname] + "Please set " + key + "."

            if error[cloudname] == '':

                user_obj.set_credential(cm_user_id, cloudname, d)

                '''
                c = cm_mongo()
                cloud = c.get_cloud(cm_user_id=cm_user_id,cloud_name=cloudname,force=True)
                if cloud:
                    registered[cloudname] = True
                    # pprint(cloud.user_token)
                    if cloudname not in user['defaults']['registered_clouds']:
                        user['defaults']['registered_clouds'].append(cloudname)
                        user_obj.set_defaults(cm_user_id, user['defaults'])
                else:
                    registered[cloudname] = False
                '''

        elif cloudtypes[cloudname] == "ec2":

            error[cloudname] = ''

            d = {"CM_CLOUD_TYPE": cloudtypes[cloudname]}


            if credentials[cloudname] is None:
                d = {'EC2_URL' : '',
                      'EC2_ACCESS_KEY': '',
                      'EC2_SECRET_KEY': '',
                }

                user_obj.set_credential(cm_user_id, cloudname, d)


            fields = ["EC2_ACCESS_KEY", "EC2_SECRET_KEY", "EC2_URL"]

            for id in fields:
                if id in ["EC2_URL"]:
                    cloudid = 'field-{0}-{1}-text'.format(cloudname, id)
                else:
                    cloudid = 'field-{0}-{1}-password'.format(cloudname, id)

                content = ''
                if cloudid in request.form:
                    content = request.form[cloudid]
                    d[id] = content
                elif id in credential:
                    password = credential[id]
                    d[id] = content

                if content == '':
                    error[cloudname] = error[cloudname] + "please set " + id


            if error[cloudname] == '':

                user_obj.set_credential(cm_user_id, cloudname, d)


        elif cloudtypes[cloudname] == "aws":

            error[cloudname] = ''

            d = {"CM_CLOUD_TYPE": cloudtypes[cloudname]}


            if credentials[cloudname] is None:
                d = {
                      'OS_USERNAME': cm_user_id,
                      'EC2_ACCESS_KEY': '',
                      'EC2_SECRET_KEY': '',
                }

                user_obj.set_credential(cm_user_id, cloudname, d)


            fields = ["EC2_ACCESS_KEY", "EC2_SECRET_KEY"]

            cloudid = 'field-{0}-userid-text'.format(cloudname)
            if cloudid in request.form:
                username = request.form[cloudid]
            else:
                username = cm_user_id
            d["OS_USERNAME"] = username

            for id in fields:
                if id in ["EC2_URL"]:
                    cloudid = 'field-{0}-{1}-text'.format(cloudname, id)
                else:
                    cloudid = 'field-{0}-{1}-password'.format(cloudname, id)

                content = ''
                if cloudid in request.form:
                    content = request.form[cloudid]
                    d[id] = content
                elif id in credential:
                    password = credential[id]
                    d[id] = content

                if content == '':
                    error[cloudname] = error[cloudname] + "please set " + id


            if error[cloudname] == '':

                user_obj.set_credential(cm_user_id, cloudname, d)

        elif cloudtypes[cloudname] == "azure":
            error[cloudname] = ''
            azureSubscriptionid = request.form['field-azure-subscriptionid-password']

            user_obj.set_credential(cm_user_id, cloudname,
                                  {"subscriptionid": azureSubscriptionid,
                                   "CM_CLOUD_TYPE": "azure" }
                                  )

        if error[cloudname] == '':
            c = cm_mongo()
            cloud = c.get_cloud(cm_user_id=cm_user_id, cloud_name=cloudname, force=True)
            if cloud:
                registered[cloudname] = True
                # pprint(cloud.user_token)
                if cloudname not in user['defaults']['registered_clouds']:
                    user['defaults']['registered_clouds'].append(cloudname)
                    user_obj.set_defaults(cm_user_id, user['defaults'])
            else:
                registered[cloudname] = False

        if registered[cloudname]:
            checkmark = 'field-cloud-activated-{0}'.format(cloudname)
            if checkmark in request.form:
                try:
                    if cloudname not in user['defaults']['activeclouds']:
                        (user['defaults']['activeclouds']).append(cloudname)
                except:
                    # create_dict(user, "defaults", "activeclouds")
                    log.info("ERROR user defaults activecloud does not exist")
            else:
                try:
                    if cloudname in user['defaults']['activeclouds']:
                        active = user['defaults']['activeclouds']
                        active.remove(cloudname)
                        user['defaults']['activeclouds'] = active
                except:
                    # create_dict(user, "defaults", "activeclouds")
                    log.info("ERROR user defaults activecloud does not exist")
        else:
            error[cloudname] = error[cloudname] + "Credential Verification Failed!"
            if cloudname in user['defaults']['registered_clouds']:
                (user['defaults']['registered_clouds']).remove(cloudname)
            if cloudname in user['defaults']['activeclouds']:
                (user['defaults']['activeclouds']).remove(cloudname)

        user_obj.set_defaults(cm_user_id, user['defaults'])
    credentials = user_obj.get_credentials(cm_user_id)


    return render_template('mesh/cloud/mesh_register_clouds.html',
                           user=user,
                           credentials=credentials,
                           cm_user_id=cm_user_id,
                           cloudnames=config.cloudnames(),
                           cloudtypes=cloudtypes,
                           error=error,
                           verified=registered)

@mesh_module.route('/mesh/images/', methods=['GET', 'POST'])
@login_required
def mongo_images():
    if not with_active_clouds():
        error = "No Active Clouds set!"
        msg = "Please <a href='/mesh/register/clouds'>Register and Activate</a> a Cloud First"
        return render_template('error.html',
                               type="Refreshing Clouds",
                               error=error,
                               msg=msg)
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    # filter()

    config = cm_config()

    # getting user info
    userdata = g.user
    username = userdata.id
    user_obj = cm_user()
    user = user_obj.info(username)



    c = cm_mongo()
    c.activate(cm_user_id=username)
    # c.refresh(types=["images"])
    clouds = c.images(cm_user_id=username)



    """

    status ACTIVE
    updated 2013-05-26T19:29:09Z
    name menghan/custom-utuntu-01
    links [{u'href': u'http://198.202.120.83:8774/v1.1/1ae6813a3a6d4cebbeb1912f6d139ad0/images/502a5967-18ff-448b-830f-d6150b650d6b', u'rel': u'self'}, {u'href': u'http://198.202.120.83:8774/1ae6813a3a6d4cebbeb1912f6d139ad0/images/502a5967-18ff-448b-830f-d6150b650d6b', u'rel': u'bookmark'}, {u'href': u'http://198.202.120.83:9292/1ae6813a3a6d4cebbeb1912f6d139ad0/images/502a5967-18ff-448b-830f-d6150b650d6b', u'type': u'application/vnd.openstack.image', u'rel': u'alternate'}]
    created 2013-05-26T19:28:09Z
    minDisk 0
    metadata {u'instance_uuid': u'16a5f5ac-7f39-4b01-a2c3-b2003beffb9d',
              u'image_location': u'snapshot',
              u'image_state': u'available',
              u'instance_type_memory_mb': u'2048',
              u'instance_type_swap': u'0',
              u'instance_type_vcpu_weight': u'None',
              u'image_type': u'snapshot',
              u'instance_type_id': u'5',
              u'ramdisk_id': None,
              u'instance_type_name': u'm1.small',
              u'instance_type_ephemeral_gb': u'0',
              u'instance_type_rxtx_factor': u'1',
              u'kernel_id': None,
              u'instance_type_flavorid': u'2',
              u'instance_type_vcpus': u'1',
              u'user_id': u'f603818711324203970ed1e3bb4b90ed',
              u'instance_type_root_gb': u'20',
              u'base_image_ref': u'1a5fd55e-79b9-4dd5-ae9b-ea10ef3156e9',
              u'owner_id': u'1ae6813a3a6d4cebbeb1912f6d139ad0'}
    server {u'id': u'16a5f5ac-7f39-4b01-a2c3-b2003beffb9d', u'links': [{u'href': u'http://198.202.120.83:8774/v1.1/1ae6813a3a6d4cebbeb1912f6d139ad0/servers/16a5f5ac-7f39-4b01-a2c3-b2003beffb9d', u'rel': u'self'}, {u'href': u'http://198.202.120.83:8774/1ae6813a3a6d4cebbeb1912f6d139ad0/servers/16a5f5ac-7f39-4b01-a2c3-b2003beffb9d', u'rel': u'bookmark'}]}
    cm_id sierra_openstack_grizzly-images-menghan/custom-utuntu-01
    cm_refresh 2013-08-06T21-44-13Z
    cm_cloud sierra_openstack_grizzly
    minRam 0
    progress 100
    cm_kind images
    _id 5201a66d7df38caf0fe160b5
    cm_type openstack
    id 502a5967-18ff-448b-830f-d6150b650d6b
    OS-EXT-IMG-SIZE:size 876216320
    b99fa4c8-6b92-49e6-b53f-37e56f9383b6
    """
    """
    2 essex A {u'image_location': u'futuregrid/ubuntu1204-ramdisk.manifest.xml',
               u'image_state':    u'available',
               u'architecture':   u'x86_64'}
    """
    attributes = {"openstack":
                    [
                        # [ "Metadata", "metadata"],
                        [ "status" , "status"],
                        [ "name" , "name"],
                        [ "type_id" , "metadata", "instance_type_id"],
                        [ "iname" , "metadata", "instance_type_name"],
                        [ "location" , "metadata", "image_location"],
                        [ "state" , "metadata", "image_state"],
                        [ "updated" , "updated"],
                        [ "minDisk" , "minDisk"],
                        [ "memory_mb" , "metadata", 'instance_type_memory_mb'],
                        [ "fid" , "metadata", "instance_type_flavorid"],
                        [ "vcpus" , "metadata", "instance_type_vcpus"],
                        [ "user_id" , "metadata", "user_id"],
                        [ "owner_id" , "metadata", "owner_id"],
                        [ "gb" , "metadata", "instance_type_root_gb"],
                        [ "arch", ""]
                    ],
                  "ec2":
                    [
                        # [ "Metadata", "metadata"],
                        [ "state" , "extra", "state"],
                        [ "name" , "name"],
                        [ "id" , "id"],
                        [ "public" , "extra", "is_public"],
                        [ "ownerid" , "extra", "owner_id"],
                        [ "imagetype" , "extra", "image_type"]
                    ],
                  "azure":
                    [
                        [ "name", "label"],
                        [ "category", "category"],
                        [ "id", "id"],
                        [ "size", "logical_size_in_gb" ],
                        [ "os", "os" ]
                    ],
                  "aws":
                    [
                        [ "state", "extra", "state"],
                        [ "name" , "name"],
                        [ "id" , "id"],
                        [ "public" , "extra", "ispublic"],
                        [ "ownerid" , "extra", "ownerid"],
                        [ "imagetype" , "extra", "imagetype"]
                    ]
                  }
    """
    for cloud in clouds:
        pprint (clouds[cloud])
        for image in clouds[cloud]:
            print image
            for attribute in clouds[cloud][image]:
                print attribute, clouds[cloud][image][attribute]
    """
    # commented by HC on Nov. 8, 2013
    # The following check is repetive because these attributes are added
    #    by 'cm_user.init_defaults(username)'
    #    this method will be called when page is loaded
    """
    if 'defaults' not in user:
        user['defaults'] = {}
        user.set_defaults(username, {})
    if 'images' not in user['defaults']:
        user['defaults']['images'] = {}
    """
    # ONLY for debug, if the Accordion does not work, please uncomment it
    #log.debug("mesh_images, before render, user defaults: {0}".format(user['defaults']))
    return render_template('mesh/cloud/mesh_images.html',
                           address_string=address_string,
                           cloud_attributes=attributes,
                           updated=time_now,
                           clouds=clouds,
                           user=user,
                           config=config)

# ============================================================
# ROUTE: mongo
# ============================================================

@mesh_module.route('/mesh/flavors/', methods=['GET', 'POST'])
@login_required
def mongo_flavors():
    if not with_active_clouds():
        error = "No Active Clouds set!"
        msg = "Please <a href='/mesh/register/clouds'>Register and Activate</a> a Cloud First"
        return render_template('error.html',
                               type="Refreshing Clouds",
                               error=error,
                               msg=msg)
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    # filter()
    config = cm_config()

    # getting user info
    userdata = g.user
    username = userdata.id
    user_obj = cm_user()
    user = user_obj.info(username)

    c = cm_mongo()
    c.activate(cm_user_id=username)
    # c.refresh(types=["flavors"])
    clouds = c.flavors(cm_user_id=username)

    os_attributes = [
                     'id',
                     'name',
                     'vcpus',
                     'ram',
                     'disk',
                     'cm_refresh',
                     ]

    # fake entry

    # user['defaults']['pagestatus'] = {'sierra': {"open": "false", "flavor": "3"}}

    # commented by HC on Nov. 8, 2013
    # The following check is repetive because these attributes are added
    #    by 'cm_user.init_defaults(username)'
    #    this method will be called when page is loaded
    """
    if 'pagestatus' not in user['defaults']:
        user['defaults']['pagestatus'] = init_user_pagestatus([cloud_name for cloud_name in clouds])
    """
    # ONLY for debug, if the Accordion does not work, please uncomment it
    #log.debug("mesh_flavors, before render, user defaults: {0}".format(user['defaults']))
    return render_template('mesh/cloud/mesh_flavors.html',
                           address_string=address_string,
                           attributes=os_attributes,
                           updated=time_now,
                           clouds=clouds,
                           user=user,
                           config=config)

# ============================================================
# ROUTE: mongo
# ============================================================

@mesh_module.route('/mesh/users/')
@login_required
@admin_permission.require(http_exception=403)
def mongo_users():
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    # filter()
    config = cm_config_server()
    adminclouds = config.get("cloudmesh.server.keystone").keys()

    username = g.user.id
    userinfo = getCurrentUserinfo()
    activeclouds = []
    if 'activeclouds' in userinfo['defaults']:
        activeclouds = userinfo['defaults']['activeclouds']
    usersinclouds = []
    for cloud in adminclouds:
        if cloud in activeclouds:
            usersinclouds.append(cloud)

    c = cm_mongo()
    c.activate(cm_user_id=username)

    clouds = {}
    clouds = c.users(usersinclouds)
    # print "TYTYTYT", len(clouds), type(clouds), clouds.keys()
    # print len(clouds['sierra'])


    """
    for cloud in clouds:
        print cloud
        for server in clouds[cloud]:
            print server
            for attribute in clouds[cloud][server]:
                print attribute, clouds[cloud][server][attribute]
    """

    attributes = {"grizzly":
                    [
                        [ "Name", "name"],
                        [ "Firstname", "firstname"],
                        [ "Lastname", "lastname"],
                        [ "Id" , "id"],
                        # [ "TenentId" , "tenantId"],
                        [ "E-mail" , "email"],
                        [ "Enabled" , "enabled"],
                        [ "Refresh", "cm_refresh"]
                    ]
                  }

    return render_template('mesh/mesh_users.html',
                           address_string=address_string,
                           cloud_attributes=attributes,
                           updated=time_now,
                           clouds=clouds,
                           config=config)

# ============================================================
# ROUTE: mongo/servers
# ============================================================

@mesh_module.route('/mesh/servers/', methods=['GET', 'POST'])
@login_required
def mongo_table(filters=None):
    if not with_active_clouds():
        error = "No Active Clouds set!"
        msg = "Please <a href='/mesh/register/clouds'>Register and Activate</a> a Cloud First"
        return render_template('error.html',
                               type="Refreshing Clouds",
                               error=error,
                               msg=msg)

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")

    config = cm_config()

    userdata = g.user
    username = userdata.id
    user_obj = cm_user()
    user = user_obj.info(username)

    c = cm_mongo()
    c.activate(cm_user_id=username)
    # c.refresh(types=["servers"])
    clouds = c.servers(cm_user_id=username)
    images = c.images(cm_user_id=username)
    flavors = c.flavors(cm_user_id=username)


    #
    # TODDO HACK for hp cloud to work as it has integer
    #

    """
    for cloud in clouds:
        print cloud
        for server in clouds[cloud]:
            print server
            for attribute in clouds[cloud][server]:
                print attribute, clouds[cloud][server][attribute]
    """
    os_attributes = ['name',
                     'status',
                     'addresses',
                     'flavor',
                     'id',
                     'image',
                     'user_id',
                     'metadata',
                     'key_name',
                     'created']

    attributes = {"openstack":
                  [
                      ['name','name'],
                      ['status','status'],
                      ['addresses','addresses'],
                      ['flavor', 'flavor','id'],
                      ['id','id'],
                      ['image','image','id'],
                      ['user_id', 'user_id'],
                      ['metadata','metadata'],
                      ['key_name','key_name'],
                      ['created','created'],
                  ],
                  "ec2":
                  [
                      ["name", "id"],
                      ["status", "extra", "status"],
                      ["addresses", "public_ips"],
                      ["flavor", "extra", "instance_type"],
                      ['id','id'],
                      ['image','extra', 'imageId'],
                      ["user_id", 'user_id'],
                      ["metadata", "metadata"],
                      ["key_name", "extra", "key_name"],
                      ["created", "extra", "launch_time"]
                  ],
                  "aws":
                  [
                      ["name", "name"],
                      ["status", "extra", "status"],
                      ["addresses", "public_ips"],
                      ["flavor", "extra", "instance_type"],
                      ['id','id'],
                      ['image','extra', 'image_id'],
                      ["user_id","user_id"],
                      ["metadata", "metadata"],
                      ["key_name", "extra", "key_name"],
                      ["created", "extra", "launch_time"]
                  ],
                  "azure":
                  [
                      ['name','name'],
                      ['status','status'],
                      ['addresses','vip'],
                      ['flavor', 'flavor','id'],
                      ['id','id'],
                      ['image','image','id'],
                      ['user_id', 'user_id'],
                      ['metadata','metadata'],
                      ['key_name','key_name'],
                      ['created','created'],
                  ]
                 }
                  
    # c.aggregate needs to be defined
    # def count_status(cloudname):
    #    result = c.aggregate( [ {$match: {"cm_kind":"servers","cm_cloud":cloudname}},
    #                                     {$group: { _id: "$status", count: { $sum: 1}}}
    #                          ])

    cloud_filters = None
    filtered_clouds = clouds
    # pprint(clouds)
    # pprint(flavors)
    # for cloud in clouds:
    #    print cloud
    #    for server in clouds[cloud]:
    #        print server
    #        print clouds[cloud][server]['flavor']

    # ONLY for debug, if the Accordion does not work, please uncomment it
    #log.debug("mesh_servers, before render, user defaults: {0}".format(user['defaults']))
    
    # added by HC on Nov. 15, 2013
    # control the display of 'run' button on a VM
    config_server = cm_config_server()
    flag_production = config_server.get("cloudmesh.server.production");
    return render_template('mesh/cloud/mesh_servers.html',
                           address_string=address_string,
                           attributes=os_attributes,
                           cloud_attributes=attributes,
                           updated=time_now,
                           clouds=filtered_clouds,
                           config=config,
                           images=images,
                           flavors=flavors,
                           user=user,
                           filters=cloud_filters,
                           flag_production=flag_production,
                           )


# ============================================================
# ROUTE: mongo/servers/<filters>
# ============================================================
'''
@mesh_module.route('/mesh/servers/<filters>')
@login_required
@admin_permission.require(http_exception=403)
def mongo_server_table_filter(filters=None):
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    # filter()
    config = cm_config()

    c = cm_mongo()
    c.activate(cm_user_id=username)
    # c.refresh(types=["servers"], cm_user_id=username)
    clouds = c.servers(cm_user_id=username)

    """
    for cloud in clouds:
        print cloud
        for server in clouds[cloud]:
            print server
            for attribute in clouds[cloud][server]:
                print attribute, clouds[cloud][server][attribute]
    """
    os_attributes = ['name',
                     'status',
                     'addresses',
                     'flavor',
                     'id',
                     'user_id',
                     'metadata',
                     'key_name',
                     'created']

    # c.aggregate needs to be defined
    # def count_status(cloudname):
    #    result = c.aggregate( [ {$match: {"cm_kind":"servers","cm_cloud":cloudname}},
    #                                     {$group: { _id: "$status", count: { $sum: 1}}}
    #                          ])

    def test_server_filters(server_attrs, server_filters):
        """ Note there are special cases handled when the direct value of a server attribute
        is itself not a simple value... can we handle this better? """
        if len(server_filters) == 0:
            return True
        check_attr, check_value = server_filters[0]
        if check_attr == 'flavor':
            test_value = server_attrs[check_attr]['id']
        else:
            test_value = server_attrs[check_attr]
        return test_value == check_value and test_server_filters(server_attrs, server_filters[1:])


    def server_filter_maker(cloud_filters):
        """ Condtions should be passed as a dict keyed by cloud name,
        with a list of (attr, value) filters, e.g.:
            { cloud_name: [(attribute, value), ... ]) } """
        return lambda((c, s)): { sk: sa for sk, sa in s.iteritems()
                                 if not cloud_filters.has_key(c) or test_server_filters(sa, cloud_filters[c]) }

    if filters:
        cloud_filters = literal_eval(filters)
        server_filter = server_filter_maker(cloud_filters)
        filtered_clouds = { c: server_filter((c, s)) for c, s in clouds.iteritems() }
    else:
        cloud_filters = None
        filtered_clouds = clouds

    return render_template('mesh/cloud/mesh_servers.html',
                           address_string=address_string,
                           attributes=os_attributes,
                           updated=time_now,
                           clouds=filtered_clouds,
                           config=config,
                           filters=cloud_filters)

'''


# ============================================================
# ROUTE: mongo
# ============================================================

# NOT USED
# since Nov. 8, 2013
# init page status of users, open or close
def init_user_pagestatus(cloud_list):
    page_status_dict = {}
    for name in cloud_list:
        page_status_dict[name] = "false"

    return page_status_dict


@mesh_module.route('/mesh/savepagestatus/', methods=['POST'])
@login_required
def mongo_save_pagestatus():
    username = g.user.id
    user_obj = cm_user()
    user = user_obj.info(username)
    cmongo = cm_mongo()
    user_cloud_list = cmongo.active_clouds(username)
    # commented/modified by HC on Nov. 8, 2013
    # The following check is repetive because these attributes are added
    #    by 'cm_user.init_defaults(username)'
    #    this method will be called when page is loaded
    """
    previous_page_status = {}
    if 'pagestatus' in user['defaults']:
        previous_page_status = user['defaults']['pagestatus']

    for user_cloud in user_cloud_list:
        if user_cloud not in previous_page_status:
            previous_page_status[user_cloud] = "false"
    user['defaults']['pagestatus'] = previous_page_status
    """
    # ONLY for debug, if the Accordion does not work, please uncomment it
    #log.debug("request.json page status: {0}".format(request.json))
    current_page_status = request.json
    status_options = {
                        "open":   "pagestatus",
                        "flavor": "flavors",
                        "image":  "images",
                      }
    for cloud_name in current_page_status:
        if cloud_name in user_cloud_list:
            for item in current_page_status[cloud_name]:
                user["defaults"][status_options[item]][cloud_name] = current_page_status[cloud_name][item]

    # ONLY for debug, if the Accordion does not work, please uncomment it
    #log.debug("mesh_save_status, before save, user defaults: {0}".format(user['defaults']))
    user_obj.set_defaults(username, user['defaults'])
    # ONLY for debug, if the Accordion does not work, please uncomment it
    # BEGIN debug
    #user_obj = cm_user()
    #user = user_obj.info(username)
    #log.debug("mesh_save_status, after save, user defaults: {0}".format(user['defaults']))
    # END debug
    return "ok"

def prepJqTreeObj(data):
        jsonList = []

        if(type(data) is list):
            for item in data:
                jsonObject = {}
                jsonObject['label'] = item
                jsonList.append(jsonObject)
        else:
            for key, value in data.items():
                jsonObject = {}
                jsonObject['label'] = key
                if type(value) is dict or type(value) is list:
                    jsonChildObj = prepJqTreeObj(value)
                    jsonObject['children'] = jsonChildObj
                else:
                    jsonObject['label'] += ": " + value
                jsonList.append(jsonObject)
        return jsonList

@mesh_module.route('/mesh/test/', methods=['GET', 'POST'])
@login_required
def test_experiment():

    experiment = cm_experiment_db()
    exptData = experiment.getUserData()
    jsonObj = prepJqTreeObj(exptData)
    return render_template('mesh/test.html',
                           user=json.dumps(jsonObj))

