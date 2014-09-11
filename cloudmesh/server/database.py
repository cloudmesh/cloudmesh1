from cloudmesh.cm_mongo import cm_mongo
from cloudmesh_install import config_file
from cloudmesh.user.cm_user import cm_user
from cloudmesh.config.cm_config import cm_config
from pprint import pprint
from cloudmesh.user.cm_userLDAP import cm_userLDAP
from cloudmesh.config.cm_keys import keytype, get_key_from_file

class Database(object):

    def __init__(self):
        self.filename = config_file("/cloudmesh.yaml")
        self.config = cm_config(filename=self.filename)
        self.cm_user_id = self.config.get("cloudmesh.hpc.username")
        self.clouds = self.config.get("cloudmesh.clouds")
        self.user_obj = cm_user()
        self.profile = self.config.profile()
        self.mongo = cm_mongo()
        
    def set_credentials(self):
        for cloudname in self.config.cloudnames():
            self.user_obj.set_credential(
                self.cm_user_id,
                cloudname,
                self.clouds[cloudname]['credentials'])

    def initialize_user(self):
        self.set_credentials()
        element = {
            "firstname": self.profile["firstname"],
            "lastname": self.profile["lastname"],
            "uidNumber": self.profile["uid"],
            "phone": self.profile["phone"],
            "gidNumber": self.profile["gid"],
            "address": self.profile["address"][0],
            "cm_user_id": self.config.get("cloudmesh.hpc.username"),
            "email": self.profile["email"],
            "activeclouds": self.config.get("cloudmesh.active")
        }

        projects = {}

        active = self.config.get("cloudmesh.projects.active")

        if active != ['None']:
            projects["active"] = active

        completed = self.config.get("cloudmesh.projects.completed")
        if completed != ['None']:
            projects["completed"] = completed

        if projects != {}:
            element["projects"] = projects

        # get keys and clean the key titles (replace '.' with '_' due
        # to mongo restriction)
        keys = self.config.get("cloudmesh.keys.keylist")
        for keytitle in keys.keys():
            keycontent = keys[keytitle]
            if keytype(keycontent) == "file":
                keycontent = get_key_from_file(keycontent).strip()
                keys[keytitle] = keycontent
            if "." in keytitle:
                newkeytitle = keytitle.replace(".", "_")
                del keys[keytitle]
                keys[newkeytitle] = keycontent
        element['keys'] = keys

        pprint(element)

        # hpc username as key
        username = element["cm_user_id"]
        # populate the local userinfo into the same mongo as though it
        # were from LDAP.
        userstore = cm_userLDAP()
        userstore.updates(username, element)

        self.user_obj = cm_user()
        self.user_obj.init_defaults(username)

        #
        # info disabled due to NameError: global name 'info' is not
        # defined info(username)
        # ------------------------------------------------------------------------------
        # added by Mark X. on Aug.25 2014 add clouds information to
        # mongo when initialize user iformation in mongo

        self.mongo.db_clouds.remove({
            'cm_kind': 'cloud',
            'cm_user_id': username
            })

        cloudsdict = self.config.get("cloudmesh", "clouds")

        for key in cloudsdict:
            Database.import_cloud_to_mongo(cloudsdict[key], key, username)
            print "cloud '{0}' added.".format(key)

    @staticmethod
    def import_cloud_to_mongo(d, cloudname, username):
        '''
        insert a cloud to db_clouds
        additionally, add values cm_cloud, cm_kind=cloud, cm_user_id
        before use this function, check whether cloud exists in db_clouds
        cloud name duplicate is not allowed
        '''
        if d['cm_type'] in ['openstack']:
            if d['credentials']['OS_USERNAME']:
                del d['credentials']['OS_USERNAME']
            if d['credentials']['OS_PASSWORD']:
                del d['credentials']['OS_PASSWORD']
            if d['credentials']['OS_TENANT_NAME']:
                del d['credentials']['OS_TENANT_NAME']
        elif d['cm_type'] in ['ec2', 'aws']:
            if d['credentials']['EC2_ACCESS_KEY']:
                del d['credentials']['EC2_ACCESS_KEY']
            if d['credentials']['EC2_SECRET_KEY']:
                del d['credentials']['EC2_SECRET_KEY']
        elif d['cm_type'] in ['azure']:
            if d['credentials']['subscriptionid']:
                del d['credentials']['subscriptionid']

        d['cm_cloud'] = cloudname
        d['cm_kind'] = 'cloud'
        d['cm_user_id'] = username

        # remove default part from yaml
        if d['default']:
            del d['default']

        mongo = cm_mongo()
        mongo.db_clouds.insert(d)
