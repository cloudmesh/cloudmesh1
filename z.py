from cloudmesh.config.cm_config import cm_config
import requests
from requests.auth import AuthBase
import os.path

import sys
from pprint import pprint
from sh import curl
import json

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

    url = "{0}/tokens".format(credential['OS_AUTH_URL'])
    headers = {'content-type': 'application/json'}

    r = requests.post(url,
                      data=json.dumps(param),
                      headers=headers,
                      verify=credential['OS_CACERT'])
                      
    return r.json()


def _get_compute_service(r):
    for service in r['access']['serviceCatalog']:
        if service['type'] == 'compute':
            break
    return service

def get(token, url, msg):
    url = "{0}/{1}".format(url, msg)
    headers = {'X-Auth-Token': token}
    r = requests.get(url, headers=headers, verify=credential['OS_CACERT'])
    return r.json()
    

config = cm_config()
credential = config.credential('sierra_openstack_grizzly')

#pprint(credential)

r = get_token(credential)
token = r["access"]["token"]["id"]
tenant = r["access"]["token"]["tenant"]["id"]

# pprint(r)
# print 70 * "="

url = _get_compute_service(r)['endpoints'][0]['publicURL']
#pprint (url)
pprint (get(token, url, "flavors"))

