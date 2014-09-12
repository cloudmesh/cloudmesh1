from cloudmesh.iaas.openstack.cm_compute import openstack
from cloudmesh.iaas.Ec2SecurityGroup import Ec2SecurityGroup
from cloudmesh_install import config_file
'''
utility/helper functions that cannot be properly categorized into the
exsiting fab files
'''


def ec2secgroup_openport(cloudname, port):
    cloud = None
    portnum = 0
    try:
        cloud = openstack(cloudname)
        cloud.get_token()
    except:
        print "Cloud name or credential wrong! Please check your cloudmesh.yaml file"
    try:
        portnum = int(port)
    except:
        print "Invalid port number"

    mygroup = Ec2SecurityGroup("default")
    groupid = cloud.find_security_groupid_by_name(mygroup.name)
        # print groupid
    rule = Ec2SecurityGroup.Rule(portnum, portnum)
    cloud.add_security_group_rules(groupid, [rule])


def yaml_file_replace(filename='/cloudmesh_xxx.yaml', replacements={}):
    filename = config_file(filename)

    with open(filename, 'r') as f:
        content = f.read()

    for _old, _new in replacements.iteritems():
        content = content.replace(_old, _new)

    outfile = open(filename, 'w')
    outfile.write(content)
    outfile.close()
