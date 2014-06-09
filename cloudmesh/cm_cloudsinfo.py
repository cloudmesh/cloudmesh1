from cloudmesh.config.cm_config import get_mongo_db, cm_config
from cloudmesh.config.ConfigDict import ConfigDict
from cloudmesh_install import config_file
import sys
from pprint import pprint


class cm_cloudsinfo:

    def _load(self, collection="cloudmesh"):
        self.clouds = None
        self.cloud_names = []
        try:
            self.db_clouds = get_mongo_db(collection)
        except:
            print "ERROR: could not access mongodb."
            sys.exit()
        try:
            self.clouds = self.db_clouds.find({'cm_kind': 'cloud'})
            for cloud in self.clouds:
                if cloud['cm_cloud'].encode('ascii') in self.cloud_names:
                    print "ERROR: cloud name duplicate found, please check your database."
                else:
                    self.cloud_names.append(cloud['cm_cloud'].encode('ascii'))
        except:
            print "ERROR: error when read clouds information."
            sys.exit()

    def add(self, cloudname, d, cm_active=True):
        self._load()
        if cloudname in self.cloud_names:
            print "ERROR: cloud '{0}' exists in database.".format(cloudname)
        else:
            d['cm_kind'] = "cloud"
            d['cm_cloud'] = cloudname
            d['cm_active'] = cm_active
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
            self.db_clouds.insert(d)
            print "cloud '{0}' added.".format(cloudname)
            # pprint(d)

    def add_from_yaml(self, file_name):
        file_name = "/{0}".format(file_name)
        filename = config_file(file_name)
        config = ConfigDict(filename=filename)

        try:
            clouds = config.get("cloudmesh", "clouds")
        except:
            print "Clouds information not in form 'cloudmesh' -> 'clouds' -> clouds."
            print "Cloud information must follow 'cloudmesh' -> 'clouds' in the yaml file."
            sys.exit()

        for key in clouds:
            self.add(key, clouds[key])

    def remove(self, cloudname):
        self.db_clouds.remove({'cm_kind': 'cloud', 'cm_cloud': cloudname})
        print "cloud '{0}' removed.".format(cloudname)

    def _list(self):
        self._load()
        return self.cloud_names

    def get_cloud_info(self, cloudname):
        return self.db_clouds.find_one({'cm_kind': 'cloud', 'cm_cloud': cloudname})

    def get_cloud_info_all(self):
        return self.db_clouds.find({'cm_kind': 'cloud'})

    def activate(self, cloudname):
        self.db_clouds.update({'cm_kind': 'cloud', 'cm_cloud': cloudname}, {'$set': {'cm_active': True}})

    def deactivate(self, cloudname):
        self.db_clouds.update({'cm_kind': 'cloud', 'cm_cloud': cloudname}, {'$set': {'cm_active': False}})

    def set_name(self, cloudname, newname):
        self.db_clouds.update({'cm_kind': 'cloud', 'cm_cloud': cloudname}, {'$set': {'cm_cloud': newname}})
