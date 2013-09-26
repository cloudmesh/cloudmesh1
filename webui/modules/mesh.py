from flask import Blueprint
from flask import render_template, request, redirect
from cloudmesh.config.cm_config import cm_config
from cloudmesh.cm_mongo import cm_mongo
from datetime import datetime
from cloudmesh.util.util import address_string
from pprint import pprint
from ast import literal_eval
from cloudmesh.pbs.pbs_mongo import pbs_mongo
from cloudmesh.util.util import cond_decorator
from flask.ext.login import login_required
import cloudmesh

from cloudmesh.util.logger import LOGGER

log = LOGGER(__file__)

mesh_module = Blueprint('mesh_module', __name__)

# ============================================================
# ROUTE: /mesh/images
# ============================================================

@mesh_module.route('/mesh/images/')
@cond_decorator(cloudmesh.with_login, login_required)
def mongo_images():
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    # filter()
    config = cm_config()

    c = cm_mongo()
    c.activate()
    clouds = c.images()

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
    2 essex A {u'image_location': u'ktanaka/ubuntu1204-ramdisk.manifest.xml', 
               u'image_state':    u'available', 
               u'architecture':   u'x86_64'} 
    """
    attributes = {"grizzly":
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

    return render_template('mesh_images.html',
                           address_string=address_string,
                           cloud_attributes=attributes,
                           updated=time_now,
                           clouds=clouds,
                           config=config)

# ============================================================
# ROUTE: mongo
# ============================================================

@mesh_module.route('/mesh/flavors/')
@cond_decorator(cloudmesh.with_login, login_required)
def mongo_flavors():
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    # filter()
    config = cm_config()

    c = cm_mongo()
    c.activate()
    clouds = c.flavors()

    """    
    2
    disk 20
    name m1.small
    links [{u'href': u'http://198.202.120.83:8774/v1.1/1ae6813a3a6d4cebbeb1912f6d139ad0/flavors/2', u'rel': u'self'}, {u'href': u'http://198.202.120.83:8774/1ae6813a3a6d4cebbeb1912f6d139ad0/flavors/2', u'rel': u'bookmark'}]
    OS-FLV-EXT-DATA:ephemeral 0
    ram 2048
    cm_refresh 2013-08-06T21-44-13Z
    OS-FLV-DISABLED:disabled False
    cm_id sierra_openstack_grizzly-flavors-m1-small
    vcpus 1
    cm_cloud sierra_openstack_grizzly
    swap 
    os-flavor-access:is_public True
    rxtx_factor 1.0
    cm_kind flavors
    _id 5201a66d7df38caf0fe160bc
    cm_type openstack
    id 2
    """

    """
    for cloud in clouds:
        print cloud
        for flavor in clouds[cloud]:
            print flavor
            for attribute in clouds[cloud][flavor]:
                print attribute, clouds[cloud][flavor][attribute]
    """

    os_attributes = [
                     'id',
                     'name',
                     'vcpus',
                     'ram',
                     'disk',
                     'cm_refresh',
                     ]

    return render_template('mesh_flavors.html',
                           address_string=address_string,
                           attributes=os_attributes,
                           updated=time_now,
                           clouds=clouds,
                           config=config)

# ============================================================
# ROUTE: mongo
# ============================================================

@mesh_module.route('/mesh/users/')
@cond_decorator(cloudmesh.with_login, login_required)
def mongo_users():
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    # filter()
    config = cm_config()

    c = cm_mongo()
    c.activate()
    clouds = {}
    clouds = c.users()
    print "TYTYTYT", len(clouds), type(clouds), clouds.keys()
    print len(clouds['sierra_openstack_grizzly'])


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
                        [ "Id" , "id"],
                        [ "TenentId" , "tenantId"],
                        [ "e-mail" , "e_mail"],
                        [ "enabled" , "enabled"],
                        [ "Cloud" , "cloud"],
                        ['cm_cloud', "cm_cloud"],
                        ['cm_id', "cm_id"],
                        ['cm_type', "cm_type"],
                        [ "Refresh", "cm_refresh"]
                    ]
                  }

    return render_template('mesh_users.html',
                           address_string=address_string,
                           cloud_attributes=attributes,
                           updated=time_now,
                           clouds=clouds,
                           config=config)

# ============================================================
# ROUTE: mongo/servers
# ============================================================

@mesh_module.route('/mesh/servers/')
@mesh_module.route('/mesh/servers/<filters>')
@cond_decorator(cloudmesh.with_login, login_required)
def mongo_table(filters=None):
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    # filter()
    config = cm_config()

    c = cm_mongo()
    c.activate()
    clouds = c.servers()

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

    return render_template('mesh_servers.html',
                           address_string=address_string,
                           attributes=os_attributes,
                           updated=time_now,
                           clouds=filtered_clouds,
                           config=config,
                           filters=cloud_filters)
