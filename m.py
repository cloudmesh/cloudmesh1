import cloudmesh

from pprint import pprint
import sys


def op1():
    cloudmesh.logger(False)
    username = cloudmesh.load().username()
    
    cloudmesh.banner("INIT MONGO")
    mesh = cloudmesh.mesh("mongo")
    
    #
    # authentication as a user - username is requried
    # On webgui side, this is achieved by the framework,
    # and the username is obtined from g.user.id
    #
    # On CLI side, a global user object or username variable
    # should be maintained upon the start of the shell
    # The username could be obtained from yaml file.
    
    cloudmesh.banner("ACTIVATE")
    mesh.activate(username)
    
    cloudmesh.banner("GET FLAVOR")
    mesh.refresh(username,types=['flavors'],names=["india"])
    data = mesh.flavors(cm_user_id=username, clouds=["india"])
    
    pprint (data)
    
    cloudmesh.banner("GET IMAGE")
    mesh.refresh(username,types=['images'],names=["india"])
    data = mesh.images(cm_user_id=username, clouds=["india"])
    
    pprint (data)
    
    cloudmesh.banner("LIST KEYS")
    keyobj = cloudmesh.cm_keys_mongo(username)
    print keyobj.names()
    
    cloudmesh.banner("UPDATE LABELS")
    cloudmesh.print_label(username)
    print "setting labels .... prefix->test index->1"
    cloudmesh.update_label(username, prefix="test", id=1)
    
    #
    # PROPOSAL FOR NEW MESH API
    #
    
    cloud = "india"
    
    cloudmesh.banner("LAUNCH VM INSTANCE")
    result = mesh.start(cloud, username)
    
    cloudmesh.banner("TERMINATE VM INSTANCE")
    server = result['server']['id']
    mesh.delete(cloud, server, username)
    
    
    
def op2():
    '''
    task :: start a VM on india, before starting, do various default setup actions
    '''
    print "NOT IMPLEMENTED"
    return
    
    #set flavor
    
    #set image
    
    #set prefix
    
    #set index
    
    #start vm


def main(argv):
    if len(argv) == 1:
        op1()
    else:
        argv = argv[1]
        if argv == "1":
            cloudmesh.banner("processing operation 1")
            op1()
        elif argv == "2":
            cloudmesh.banner("processing operation 2")
            op2()
        else:
            print "incorrect operation index"
    
    
if __name__ == "__main__":
    main(sys.argv)

