#!/usr/bin/env python
from __future__ import print_function
from docopt import docopt
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.config.cm_config import cm_config
from cloudmesh_base.logger import LOGGER
from tabulate import tabulate

log = LOGGER(__file__)


def shell_command_image(arguments):
    """
    ::

      Usage:
          image
          image <cm_cloud>... [--refresh]
      image -h | --help
          image --version

     Options:
         -h                   help message
         --refresh            refresh images of IaaS

      Arguments:
          cm_cloud    Name of the IaaS cloud e.g. india_openstack_grizzly.

      Description:
         image command provides list of available images. Image describes
         pre-configured virtual machine image.


      Result:

      Examples:
          $ image india_openstack_grizzly

    """

    # log.info(arguments)

    cloud_names = arguments['<cm_cloud>']
    # None value means ALL clouds in c.images() function
    if not cloud_names:
        cloud_names = None
    config = cm_config()
    username = config.username()
    c = cm_mongo()
    c.activate(cm_user_id=username)
    if arguments['--refresh']:
        c.refresh(cm_user_id=username, names=cloud_names, types=['images'])
    images_dict = c.images(cm_user_id=username, clouds=cloud_names)
    your_keys = {"openstack":
                 [
                     # ["Metadata", "metadata"],
                     ["status", "status"],
                     ["name", "name"],
                     ["id", "id"],
                     ["type_id", "metadata", "instance_type_id"],
                     ["iname", "metadata", "instance_type_name"],
                     ["location", "metadata", "image_location"],
                     ["state", "metadata", "image_state"],
                     ["updated", "updated"],
                     ["minDisk", "minDisk"],
                     ["memory_mb", "metadata", 'instance_type_memory_mb'],
                     ["fid", "metadata", "instance_type_flavorid"],
                     ["vcpus", "metadata", "instance_type_vcpus"],
                     ["user_id", "metadata", "user_id"],
                     ["owner_id", "metadata", "owner_id"],
                     ["gb", "metadata", "instance_type_root_gb"],
                     ["arch", ""]
                 ],
                 "ec2":
                 [
                     # ["Metadata", "metadata"],
                     ["state", "extra", "state"],
                     ["name", "name"],
                     ["id", "id"],
                     ["public", "extra", "is_public"],
                     ["ownerid", "extra", "owner_id"],
                     ["imagetype", "extra", "image_type"]
                 ],
                 "azure":
                 [
                     ["name", "label"],
                     ["category", "category"],
                     ["id", "id"],
                     ["size", "logical_size_in_gb"],
                     ["os", "os"]
                 ],
                 "aws":
                 [
                     ["state", "extra", "state"],
                     ["name", "name"],
                     ["id", "id"],
                     ["public", "extra", "ispublic"],
                     ["ownerid", "extra", "ownerid"],
                     ["imagetype", "extra", "imagetype"]
                 ]
                 }

    images = _select_images(images_dict, your_keys)

    _display(images)


def _select_images(data, selected_keys, env=[]):
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
    images = []
    keys = []

    def _getFromDict(dataDict, mapList):
        '''Get values of dataDict by mapList
        mapList is a list of keys to find values in dict.
        dataDict is a nested dict and will be searched by the list.

        e.g.  Access to the value 5 in dataDict

        dataDict = { "abc": {
                        "def": 5
                        }
                    }
        mapList = ["abc", "def"]

        _getFromDict(dataDict, mapList) returns 5

        ref: http://stackoverflow.com/questions/14692690/access-python-nested-dictionary-items-via-a-list-of-keys
        '''
        return reduce(lambda d, k: d[k], mapList, dataDict)

    for cm_cloud, _id in data.iteritems():
        for image_name, v in _id.iteritems():
            values = [cm_cloud]
            # cm_type is required to use a selected_keys for the cm_type
            cm_type = v['cm_type']
            keys = []
            for k in selected_keys[cm_type]:
                keys.append(k[0])
                try:
                    values.append(_getFromDict(v, k[1:]))
                except:
                    # print sys.exc_info()
                    values.append(0)
            images.append(values)
    headers = [keys]
    return headers + images


def _display(json_data, headers="firstrow", tablefmt="orgtbl"):
    table = tabulate(json_data, headers, tablefmt)
    try:
        separator = table.split("\n")[1].replace("|", "+")
    except:
        separator = "-" * 50
    print(separator)
    print(table)
    print(separator)


def main():
    arguments = docopt(shell_command_image.__doc__)
    shell_command_image(arguments)

if __name__ == "__main__":
    # print sys.argv
    main()
