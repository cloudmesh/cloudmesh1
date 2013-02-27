from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver

import os
import libcloud.security

#libcloud.security.VERIFY_SSL_CERT = False
#make sure you set export NOVAKEYDIR= ............
libcloud.security.CA_CERTS_PATH = os.environ['NOVA_KEY_DIR']

username=os.environ['OS_USERNAME']
password=os.environ['OS_PASSWORD']
auth_url=os.environ['OS_AUTH_URL']

OpenStack = get_driver(Provider.OPENSTACK)

# I tried in the next call 
#                    ex_force_auth_url=auth_url,
# but did not work

# I tried 
driver = OpenStack(username, password,
                   ex_force_auth_url='http://149.165.146.50:5443/v2.0',
                   ex_force_auth_version='2.0_password')

images = driver.list_images()
sizes = driver.list_sizes()

#but this did not work either, what am i doing wrong

#nodes = driver.list_nodes()
#size = [s for s in sizes if s.ram == 512][0]
#image = [i for i in images if i.name == 'natty-server-cloudimg-amd64'][0]

#node = driver.create_node(name='test node', image=image, size=size)
