from subprocess import call

ls = ["cloud", "flavor", "image", "security_group", "vm"]

for item in ls:
    print ("+++++++++++++ {0} ++++++++++++++".format(item))
    call("mv cloudmesh/iaas/cm_{0}.py cloudmesh/shell".format(item), shell=True)
    call("grep -r cloudmesh.iaas.cm_{0}".format(item), shell=True)
    print ("--------------------------------")
    call("grep -r -l cloudmesh.iaas.cm_{0} . | xargs perl -pi -e 's/cloudmesh.iaas.cm_{0}/cloudmesh.shell.cm_{0}/g'".format(item), shell=True)
    call("grep -r cloudmesh.iaas.cm_{0}".format(item), shell=True)

