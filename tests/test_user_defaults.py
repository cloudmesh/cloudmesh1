from cloudmesh.user.cm_user import cm_user
import sys
from pprint import pprint

# print "sys len is: ", len(sys.argv)
# print "para: ", sys.argv[1]
if (len(sys.argv) < 2):
    print "usage: "
    print "    {0} your_user_name".format(sys.argv[0])
    sys.exit()

print "Your username is: {0}".format(sys.argv[1])
cuser = cm_user()
user = cuser.info(sys.argv[1])
print "-*=" * 20
print "images:"
pprint(user["defaults"]["images"])

print "flavors:"
pprint(user["defaults"]["flavors"])

print "pagestatus:"
pprint(user["defaults"]["pagestatus"])
