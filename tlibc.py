from cloudmesh.config.cm_config import cm_config

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
from pprint import pprint
import urlparse

conf = cm_config()
cred = conf.get("india-eucalyptus")
pprint (cred)

euca_id = cred['EC2_ACCESS_KEY']
euca_key = cred['EC2_SECRET_KEY']
ec2_url = cred['EC2_URL']

result = urlparse.urlparse(ec2_url)
is_secure = (result.scheme == 'https')
if ":" in result.netloc:
    host_port_tuple = result.netloc.split(':')
    host = host_port_tuple[0]
    port = int(host_port_tuple[1])
else:
    host = result.netloc
    port = None

path = result.path
# region_name = 'eucalyptus'
# api_version = '2009-11-30'

print 'aws_access_key_id', euca_id,
print 'aws_secret_access_key', euca_key
print 'is_secure', is_secure
# print 'name', region_name
print 'endpoint', host
print 'port', port
print 'path', path
# print 'api_version', api_version


def retrief(f, exclude=[]):

    vms = {}
    nodes = f()
    for node in nodes:
        vm = {}
        for key in node.__dict__:
            value = node.__dict__[key]
            if key == 'extra':
              for e in value:
                   vm[e] = value[e]
            else:
                vm[key] = value
        for d in exclude:
            if d in vm:
                del vm[d]
        vms[node.id] = vm
    return vms


Driver = get_driver(Provider.EUCALYPTUS)
conn = Driver(key=euca_id, secret=euca_key, secure=False, host=host, path=path, port=port)

# images = retrief(conn.list_images,
#                 ['driver','ownerid','owneralias','platform','hypervisor','virtualizationtype','_uuid'])
# pprint (images)


flavors = retrief(conn.list_sizes, ['_uuid'])
pprint (flavors)


vms = retrief(conn.list_nodes, ['private_dns', 'dns_name', 'instanceId', 'driver', '_uuid'])

pprint (vms)

