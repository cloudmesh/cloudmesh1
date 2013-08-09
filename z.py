from cloudmesh.config.cm_config import cm_config
import requests
from requests.auth import AuthBase
import os.path

import sys
from pprint import pprint
from sh import curl
import json

'''
def get_token(credential):
    """ the authentikation token from keystone with a curl call"""
    param = {"auth": { "passwordCredentials": {
                            "username": credential['OS_USERNAME'], 
                            "password":credential['OS_PASSWORD'], 
                        }, 
                       "tenantName":credential['OS_TENANT_NAME']
                    }
         }
    param=json.dumps(param)
    
    response = curl(
                    "--cacert", credential['OS_CACERT'],
                    "-k",
                    "-X",
                    "POST", "%s/tokens" % credential['OS_AUTH_URL'],
                    "-d", param,
                    "-H", 'Content-type: application/json'
                    )

    result = json.loads(str(response))
    return result
'''


config = cm_config()
credential = config.credential('sierra-openstack-grizzly')
pprint(credential)


def get_token(credential):
    
    if not os.path.isfile(credential['OS_CACERT']):
        print "Error: certfile", credential['OS_CACERT'], "does not exist"
        sys.exit()
        
    param = {"auth": { "passwordCredentials": {
                            "username": credential['OS_USERNAME'], 
                            "password":credential['OS_PASSWORD'], 
                        }, 
                       "tenantName":credential['OS_TENANT_NAME']
                    }
         }

    print param
    url = "{0}/tokens".format(credential['OS_AUTH_URL'])
    print url
    headers = {'content-type': 'application/json'}

    r = requests.post(url,                
                      data=json.dumps(param), 
                      headers=headers,
                      #cert=credential['OS_CACERT'],
                      verify=False).json() 
    return r
    

    
r = get_token(credential)

pprint(r)

print 70 * "="
pprint (r["access"]["token"]["id"])


"""
r = requests.get('http://google.com')
                 
print r.status_code
print r.text
"""              
"""
class OpenStackAuth(AuthBase):
    def __init__(self, auth_user, auth_key, auth_tenant):
        self.auth_key = auth_key
        self.auth_user = auth_user
        self.auth_tenant = auth_tenant

    def __call__(self, r):
        r.headers['Content-type'] = "application/json"
        r.headers['X-Auth-User'] = self.auth_user
        r.headers['X-Auth-Key'] = self.auth_key
        r.headers['X-Auth-Tenant'] = self.auth_key
        return r

response = requests.get(credential['OS_AUTH_URL'], 
                        auth=OpenStackAuth(credential['OS_USERNAME'], 
                                           credential['OS_PASSWORD'],
                                           credential['OS_TENANT_NAME']),
                        verify=False)
print 70 * "="
pprint (response.text)
"""
sys.exit()

ENDPOINT_URL = 'https://az-1.region-a.geo-1.compute.hpcloudsvc.com/v1.1/'
ACCESS_KEY = 'Your Access Key'
ACCOUNT_ID = 'Your Account ID'
response = requests.get(credential['OS_AUTH_URL'], 
                        auth=OpenStackAuth(credential['OS_USERNAME'], 
                                           credential['OS_PASSWORD']))


"""
class OpenStackAuthToken(AuthBase):
    def __init__(self, request):
        self.auth_token = request.headers['x-auth-token']

def __call__(self, r):
    r.headers['X-Auth-Token'] = self.auth_token
    return r

# Get the management URL from the response header
mgmt_url = response.headers['x-server-management-url']

# Create a new request to the management URL using the /servers path
# and the OpenStackAuthToken scheme we created
r_server = requests.get(mgmt_url + '/servers', auth=OpenStackAuthToken(response))

# Parse the response and show it to the screen
json_parse = json.loads(r_server.text)
print json.dumps(json_parse, indent=4)
"""