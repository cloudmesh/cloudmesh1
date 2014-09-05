#! /usr/bin/env python
import os
import json
from datetime import datetime
import requests
from pprint import pprint

from cloudmesh.config.cm_config import cm_config_server
from cloudmesh.config.cm_config import cm_config
from cloudmesh_common.logger import LOGGER

log = LOGGER(__file__)


class keystone(object):
    users = {}  # global var
    tenants = {}
    roles = {}
    admin_credential = None
    admin_token = None
    # cloud label to identify which keystone this serves
    label = None  # global var
    #
    # initialize
    #
    # possibly make connext seperate

    def __init__(self, label, admin_credential=None):
        """
        initializes the keystone client from a file
        located at cloudmesh_server.yaml.
        """
        self.clear()
        self.label = label
        self.admin_credential = admin_credential

        if admin_credential is None:
            try:
                self.admin_credential = cm_config_server().get(
                    "cloudmesh.server.keystone.{0}".format(label))
            except:
                log.error(
                    "No admin credential found! Please check your cloudmesh_server.yaml file.")
        # connecting within init will lead to long delays
        if self.admin_credential is not None:
            self.connect()
            self.load()

    # clear all data
    def clear(self):
        """
        clears the data
        """
        self.users = {}
        self.tenants = {}
        self.roles = {}
        #self.admin_token = None
        #self.admin_credentials = None

    # obtain admin token
    def connect(self):
        # create admin token for further connection use
        log.info("Loading Admin Credentials")
        if self.admin_credential is None:
            log.error(
                "error connecting to openstack compute, credential is None")
        elif not self.admin_token:
            self.admin_token = self.get_token(self.admin_credential)

    # load users, tenants, roles from keystone
    def load(self, types=None):
        #banner("admin token before loading...")
        # print self.admin_token
        if self.admin_token:
            if types is None or types == ['all']:
                types = ['users', 'tenants', 'roles']
            if 'users' in types:
                self.users = self.load_users()
            if 'tenants' in types:
                self.tenants = self.load_tenants()
            if 'roles' in types:
                self.roles = self.load_roles()

    def refresh(self, types=None):
        self.clear()
        self.load(types)

    def get_token(self, credential=None):
        # print "get_token is being invoked"
        if credential is None:
            credential = self.admin_credential

        param = None
        if 'OS_TENANT_NAME' in credential:
            param = {"auth": {"passwordCredentials": {
                "username": credential['OS_USERNAME'],
                "password": credential['OS_PASSWORD'],
            },
                "tenantName": credential['OS_TENANT_NAME']
            }
            }
        elif 'OS_TENANT_ID' in credential:
            param = {"auth": {"passwordCredentials": {
                "username": credential['OS_USERNAME'],
                "password": credential['OS_PASSWORD'],
            },
                "tenantId": credential['OS_TENANT_ID']
            }
            }
        url = "{0}/tokens".format(credential['OS_AUTH_URL'])

        # print "URL", url

        headers = {'content-type': 'application/json'}
        verify = self._get_cacert(credential)
        # print "PARAM", json.dumps(param)
        # print "HEADER", headers
        # print "VERIFY", verify

        r = requests.post(url,
                          data=json.dumps(param),
                          headers=headers,
                          verify=verify)
        return r.json()

    def _get_service(self, type="identity", token=None):

        if token is None:
            token = self.admin_token

        for service in token['access']['serviceCatalog']:
            if service['type'] == type:
                break
        return service

    def _get_cacert(self, credential=None):
        if credential is None:
            credential = self.admin_credential
        verify = False
        if 'OS_CACERT' in credential:
            if credential['OS_CACERT'] is not None and \
               credential['OS_CACERT'] != "None" and \
               os.path.isfile(credential['OS_CACERT']):
                verify = credential['OS_CACERT']
        return verify

    def _post(self, posturl, params=None, credential=None):
        # print posturl
        # print self.config
        if credential is None:
            credential = self.admin_credential
        conf = self._get_service_endpoint("identity")
        headers = {'content-type': 'application/json',
                   'X-Auth-Token': '%s' % conf['token']}
        # print headers
        # print self._get_cacert(credential)
        r = requests.post(posturl, headers=headers,
                          data=json.dumps(params),
                          verify=self._get_cacert(credential))
        ret = {"msg": "success"}
        if r.text:
            ret = r.json()
        return ret

    def _put(self, posturl, params=None, credential=None):
        # print self.config
        if credential is None:
            credential = self.admin_credential
        conf = self._get_service_endpoint("identity")
        headers = {'content-type': 'application/json',
                   'X-Auth-Token': '%s' % conf['token']}
        # print headers
        r = requests.put(posturl, headers=headers,
                         data=json.dumps(params),
                         verify=self._get_cacert(credential))
        ret = {"msg": "success"}
        if r.text:
            ret = r.json()
        return ret

    def _get(self, msg, service="identity", urltype="publicURL", credential=None, payload=None, json=True):

        # kind = "admin", "user"
        # service = "publicURL, adminURL"
        # service=  "compute", "identity", ....
        # token=None, url=None, kind=None, urltype=None, json=True):
        if credential is None:
            credential = self.admin_credential
            token = self.admin_token

        conf = self._get_service_endpoint(service)
        url = conf[urltype]

        url = "{0}/{1}".format(url, msg)
        # print url

        headers = {'X-Auth-Token': token['access']['token']['id']}
        r = requests.get(
            url, headers=headers, verify=self._get_cacert(credential), params=payload)

        if json:
            return r.json()
        else:
            return r

    def _get_service_endpoint(self, type=None, credential=None):
        # kind is 'admin' or 'user'
        if type is None:
            type = "identity"
        token = self.admin_token
        if credential:
            token = self.get_token(credential)
            #banner("user token")
            # pprint(token)
        conf = {}
        if 'access' in token:
            service = self._get_service(type, token)
            # pprint(identity_service)
            conf['publicURL'] = str(service['endpoints'][0]['publicURL'])
            conf['adminURL'] = None
            if 'adminURL' in service['endpoints'][0]:
                conf['adminURL'] = str(service['endpoints'][0]['adminURL'])
            conf['token'] = str(token['access']['token']['id'])
        return conf

    def _now(self):
        return datetime.now().strftime('%Y-%m-%dT%H-%M-%SZ')

    def load_tenants(self):
        time_stamp = self._now()
        msg = "tenants"
        tenantslist = self._get(msg, urltype='adminURL')['tenants']
        return self._list_to_dict(tenantslist, 'name', 'tenants', time_stamp)

    def load_users(self):
        time_stamp = self._now()
        msg = "users"
        userslist = self._get(msg, urltype='adminURL')['users']
        return self._list_to_dict(userslist, 'name', 'users', time_stamp)

    def load_roles(self):
        time_stamp = self._now()
        msg = "OS-KSADM/roles"
        roleslist = self._get(msg, urltype='adminURL')['roles']
        return self._list_to_dict(roleslist, 'name', 'roles', time_stamp)

    def get(self, type="users"):
        d = {}
        if type == 'users':
            d = self.users
        elif type == 'tenants':
            d = self.tenants
        elif type == 'roles':
            d = self.roles
        return d

    def get_user_by_name(self, name):
        userid = None
        if name in self.users:
            userid = self.users[name]['id']
        return userid

    def get_tenant_by_name(self, name):
        tenantid = None
        if name in self.tenants:
            tenantid = self.tenants[name]['id']
        return tenantid

    def get_role_by_name(self, name):
        roleid = None
        if name in self.roles:
            roleid = self.roles[name]['id']
        return roleid

    def create_new_tenant(self, name, description='', enabled=True):
        conf = self._get_service_endpoint("identity")
        adminURL = conf['adminURL']
        posturl = "%s/tenants" % adminURL
        tenantdata = {
            "tenant": {
                "name": "%s" % name,
                "description": "%s" % description,
                "enabled": enabled
            }
        }
        ret = self._post(posturl, tenantdata)
        self.refresh()
        return ret
    # create a new user
    # or if username exist and password provided, reset the password

    def create_new_user(self, username, password=None, email=None, enabled=True):
        conf = self._get_service_endpoint("identity")
        adminURL = conf['adminURL']
        posturl = "%s/users" % adminURL
        userinfo = {
            "user": {
                "name": "%s" % username,
                "email": "%s" % email,
                "enabled": enabled,
                #"passowrd": "%s" % password
                #"OS-KSADM:password": "%s" % password
            }
        }
        ret = self._post(posturl, userinfo)
        self.refresh()
        if password:
            uid = self.get_user_by_name(username)
            self.set_user_password(uid, password)
        return ret

    def add_role_to_user_tenant(self, tenantid, userid, roleid):
        conf = self._get_service_endpoint("identity")
        adminURL = conf['adminURL']
        url = "%s/tenants/%s/users/%s/roles/OS-KSADM/%s" % (
            adminURL, tenantid, userid, roleid)
        return self._put(url)

    def delete_user(self, userid):
        conf = self._get_service_endpoint("identity")
        adminURL = conf['adminURL']
        url = "%s/users/%s" % (adminURL, userid)

        headers = {'content-type': 'application/json',
                   'X-Auth-Token': '%s' % conf['token']}
        # print headers
        # no return from http delete via rest api
        r = requests.delete(url, headers=headers, verify=self._get_cacert())
        self.refresh()
        ret = {"msg": "success"}
        if r.text:
            ret = r.json()
        return ret

    def delete_tenant(self, tenantid):
        conf = self._get_service_endpoint("identity")
        adminURL = conf['adminURL']
        url = "%s/tenants/%s" % (adminURL, tenantid)

        headers = {'content-type': 'application/json',
                   'X-Auth-Token': '%s' % conf['token']}
        # print headers
        # no return from http delete via rest api
        r = requests.delete(url, headers=headers, verify=self._get_cacert())
        self.refresh()
        ret = {"msg": "success"}
        if r.text:
            ret = r.json()
        return ret

    def set_user_password(self, userid, newpass):
        conf = self._get_service_endpoint("identity")
        adminURL = conf['adminURL']
        posturl = "%s/users/%s/OS-KSADM/password" % (adminURL, userid)
        userinfo = {
            "user": {
                "id": "%s" % userid,
                "password": "%s" % newpass
            }
        }
        return self._put(posturl, userinfo)

    def change_own_password(self, credential, userid, oldpass, newpass):
        conf = self._get_service_endpoint("identity", credential)
        # banner("conf")
        # print conf
        ret = {}
        if 'publicURL' in conf:
            publicURL = conf['publicURL']
            url = "%s/OS-KSCRUD/users/%s" % (publicURL, userid)
            params = {
                "user": {"password": "%s" % newpass,
                         "original_password": "%s" % oldpass
                         }
            }
            headers = {'content-type': 'application/json',
                       'X-Auth-Token': '%s' % conf['token']
                       }
            # banner("headers")
            # print headers
            # banner("url")
            # print url
            # no return from http delete via rest api
            r = requests.patch(url, headers=headers,
                               data=json.dumps(params),
                               verify=self._get_cacert(credential)
                               )
            ret = r.json()
        if "access" in ret:
            ret = {"msg": "success"}
        elif "error" in ret:
            ret = ret['error']
        else:
            ret = {
                "error": "failed to obtain auth_token using the provided credential"}
        return ret

    def test_change_own_password(self, cloudlabel, oldpass, newpass):
        mycredential = cm_config().get(
            "cloudmesh.clouds.{0}.credentials".format(cloudlabel))
        userid = self.get_user_by_name('cmdevtesting')
        #oldpass = 'password02'
        #newpass = 'password03'
        return self.change_own_password(mycredential, userid, oldpass, newpass)

    def _list_to_dict(self, list, id, type, time_stamp):
        d = {}
        for element in list:
            element['cm_type'] = type
            element['cm_cloud'] = self.label
            element['cm_refresh'] = time_stamp
            d[element[id]] = dict(element)
        return d


def banner(header):
    print "#" * 80
    print "#\t%s" % header
    print "#" * 80

#####
# MAIN FOR TESTING
#####
if __name__ == "__main__":
    label = 'sierra'
    idm = keystone(label)
    users = idm.get_users()
    tenants = idm.get_tenants()
    #banner("admin token")
    # pprint(idm.admin_token)
    banner("%s users retrieved" % len(users.keys()))
    print "a sample user is:"
    pprint(users['fuwang'])
    banner("%s tenants retrieved" % len(tenants.keys()))
    print "a sample tenant is:"
    pprint(tenants['fg82'])
    roles = idm.get_roles()
    banner("%s roles found" % len(roles.keys()))
    pprint(roles)
    banner("verify data are loaded...")
    pprint(idm.users['fuwang'])
    pprint(idm.tenants['fg82'])
    pprint(idm.roles['admin'])
    banner("Tesing getting id by names")
    print idm.get_role_by_name('admin')
    rid = idm.get_role_by_name('_member_')
    print rid
    print idm.get_user_by_name('fuwang')
    print idm.get_tenant_by_name('fg82')

    """
    banner("Testing user creation")
    username = "cmdevtesting"
    password1 = "password01"
    password2 = "password02"
    print "before creation, should be None"
    print idm.get_user_by_name(username)
    print "Created, should be something"
    print idm.create_new_user(username, password1)
    #idm.refresh()
    uid = idm.get_user_by_name(username)
    print uid

    banner("Changing password")
    print idm.set_user_password(uid, password2)

    banner("Testing tenant creation")
    tname = "fgcmdev"
    print "before creation, should be None"
    print idm.get_tenant_by_name(tname)
    print "Created, should be something"
    print idm.create_new_tenant(tname)
    tid = idm.get_tenant_by_name(tname)
    print tid

    # general process to add/active a new user
    # 1. create the user
    # 2. for every project, if a tenant for it did not exist yet, create it
    # 3. add role(s) to user-tenant
    banner("assign role to user-tenant")
    print idm.add_role_to_user_tenant(tid, uid, rid)
    """
    """
    banner("Change own password")
    print idm.test_change_own_password(label,"password03","password02")
    #####
    # please be extremely cautious when deleting data
    #####
    """
    """
    username = "cmdevtesting"
    uid = idm.get_user_by_name(username)
    banner("User deletion")
    print "deleted, should be None again"
    idm.delete_user(uid)
    #idm.refresh()
    print idm.get_user_by_name(username)

    tname = "fgcmdev"
    tid = idm.get_tenant_by_name(tname)
    banner("tenant deletion")
    print "deleted, should be None again"
    idm.delete_tenant(tid)
    #idm.refresh()
    print idm.get_tenant_by_name(tname)
    """
