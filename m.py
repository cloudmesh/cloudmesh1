import cloudmesh

from pprint import pprint
import sys




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


    cloud = "india"
    
    cloudmesh.banner("LAUNCH VM INSTANCE")
    vm = {}
    for i in range(1,3):
        vm[i] = mesh.start(cloud, username)
    
    
    cloudmesh.banner("TERMINATE VM INSTANCE")
    for i ...:
        server = vm[i]['server']['id']
        mesh.delete(cloud, server, username)
    # hoe do you arrase no the vms????
    
    
    '''
    task :: start a VM on india, before starting, do various default setup actions
    '''
    print "NOT IMPLEMENTED"
    return

    
    flavor=mesh.flavor(cloudname="india", flavorname="m1.small") 
    flavor=mesh.flavor("india", "m1.small") 
    
    # print ???
    
    
    #set image

    image=mesh.image(cloudname="india", imagename="futuregrid/ubuntu-14.04") 
    image=mesh.image("india", "futuregrid/ubuntu-14.04") 
    # 
    
    # print ???
    
    # GET CURRENT VMNAME OR BETTER GET THE NEXT VM NAME????
    
    # vmname = mesh.vmname()
    # vmname = mesh.vmname("next")
    # vmname = mesh.vmname.next() # this is for sure not implemented
    # vmname = mesh.vmname.rest("gregor", "00000000")
    # vmname = mesh.vmname.format("gregor-[00000]") # hopstlist format ;-)
    
    
    
    # cloudmesh.print_label(username) 
    # current name of vm
    
    #start vm1

    # save default image and falvor ????
    
    mesh.default("india", "image", image)
    mesh.deafult("india", "flavor", flavor)
    
    vm = mesh.start("india", userid)


    #start vm2

    # save default image and falvor ????
    
    
    cloud = "india"
    prefix = "gregor"
    index = "10000"
    vm_flavor = "???"
    ...
    
    vm = vm_create(self, cloud, prefix, index, vm_flavor, vm_image, key, meta, cm_user_id):

    # vm where index is NOne ...
    # ....






    
    
    vm = mesh.start("india", image, flavor)
    vm = mesh.assign_public_ip(...)
    
    vmname = vm['lable'/'name'] # prefix-id

    result = mesh.ssh(vmname, "ls", ...)


    mesh.delete(vmname)





