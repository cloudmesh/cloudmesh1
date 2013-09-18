# ! /usr/local/bin
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import libcloud.security

EC2_ACCESS_KEY = "???"
EC2_SECRET_KEY = "???"
OS_AUTH_URL = "http://149.165.146.50:5000/v2.0"

OS_USERNAME = "???"
OS_PASSWORD = "???"

libcloud.security.VERIFY_SSL_CERT = False

if __name__ == "__main__":
    Driver = get_driver(Provider.OPENSTACK)

    con = Driver(OS_USERNAME,
                 OS_PASSWORD,
                 ex_force_auth_url=OS_AUTH_URL,
                 ex_force_auth_version='2.0_password')

    print con.list_nodes()
test1.py(END)
