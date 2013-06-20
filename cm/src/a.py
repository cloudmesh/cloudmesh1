import os
import sys
from sh import curl
import httplib
import json
import pprint
pp = pprint.PrettyPrinter(indent=4)

user = {

"tenant"   : os.environ['OS_TENANT_NAME'],
"username" :os.environ['OS_USERNAME'],
"password" : os.environ['OS_PASSWORD'],
"ip"      : "149.165.146.50",
}


def get_token():
    global user
    params = '{"auth":{"passwordCredentials":{"username": "%(username)s", "password":"%(password)s"}}}' % user
    headers = {"Content-Type": "application/json"}
    conn = httplib.HTTPConnection("%(ip)s:5000" % user)
    conn.request("POST", "/v2.0/tokens", params, headers)
    response = conn.getresponse()
    data = response.read()
    dd = json.loads(data)
    conn.close()
    apitoken = dd['access']['token']['id']
    #    pp.pprint (dd)
    print json.dumps (dd, indent=4)
    user['token'] = apitoken
    return apitoken

token = get_token()

print token

cmd = "curl -H \"X-Auth-Token:%(token)s\" http://%(ip)s:35357/v2.0/tenants" % user

print cmd
os.system(cmd)


sys.exit()

print data







cmd = "curl -d '{\"auth\":{\"passwordCredentials\":{\"username\": \"%(username)s\", \"password\": \"%(password)s\"}}}' -H \"Content-type: application/json\" http://%(ip)s:35357/v2.0/tokens" % data




def get_token():
#    curl("-d", "'{\"auth\":{\"passwordCredentials\":{\"username\": \"%(username)s\", \"password\": \"%(password)s\"}}}' -H \"Content-type: application/json\" http://%(ip)s:35357/v2.0/tokens" % data
    result = curl("-d",
		  "'{\"auth\":{\"passwordCredentials\":{\"username\": \"gvonlasz\", \"password\": \"OTg5NmVkZTdkMzEwOThmMDMxZDJmNmY1\"}}}'",
	"-H",
	"\"Content-type: application/json\"",
	"http://149.165.146.50:35357/v2.0/tokens")
    print result


print 70 * "-"

print cmd
print 70 * "-"
result = os.system(cmd)
print 70 * "-"
print result
print 70 * "-"



get_token()
