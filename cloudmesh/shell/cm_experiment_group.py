from __future__ import print_function
# from cloudmesh.experiment.model_group import ExperimentGroup
from cloudmesh.experiment.group import *
from cloudmesh_common.logger import LOGGER
from cloudmesh.user.cm_user import cm_user
from cloudmesh.config.cm_config import cm_config
from cloudmesh.cm_mongo import cm_mongo

log = LOGGER(__file__)

def shell_command_experiment_group(arguments):
    """
    Usage:
        group list
        group create NAME
        group remove NAME
        group add NAME TYPE VALUE
        group delete NAME TYPE VALUE
        group show NAME

    Arguments:

        NAME    name of the group
        TYPE    type of the value
        VALUE   value

    Options:

        -v         verbose mode

    Description:

       group list       lists in formation about the group
       group create     creates a new group
       group remove     removes a group
       group add        addes an item in a group
       group delete     deletes an item in a group
       group show       views a group

    """

    name = arguments["NAME"]
    type = arguments["TYPE"]
    value = arguments["VALUE"]

    config = cm_config()
    username = config.username()
    # print username
    user = cm_user()

    '''
    if arguments["info"]:

        print("Default experiment group:", user.get_defaults(username)["group"])

    '''
    if arguments["list"]:

        for group in ExperimentGroup.objects(userid__exact=username):
            print (group.name)

    elif arguments["create"]:
        # "sets the group to the given name, the group must exists"
        test = ExperimentGroup(name=name, userid=username).save()
        print (test)

    elif arguments["add"]:
        # "adds the group to the given name, the group must not exist."

        # __exact is the string field exactly matches value
        # ref: http://docs.mongoengine.org/en/latest/guide/querying.html#query-operators
        groups = ExperimentGroup.objects(name__exact=name)
        if len(groups) == 0:
            print ("{0} group does not exist".format(name))
            return

        # select the first value in the list
        group = groups[0]

        if type == "vm":
            post = VM(group_name=group)
            post.vm_name = value
        elif type == "ip":
            post = IP(group_name=group)
            post.ip = value
            post.ip_public = value
            post.ip_private = value
        else:
            print ("invalid type")
            return

        post.tags = ['experiment', 'group', type]
        post.save()

    elif arguments['show']:
        groups = ExperimentGroup.objects(name__exact=name)
        if len(groups) == 0:
            print ("{0} group does not exist".format(name))
            return
        group = groups[0]

        for item in GroupItem.objects(group_name__exact=group):
            print (item.group_name.name)
            print ("=" * len(item.group_name.name))

            if isinstance(item, VM):
                print ("vm_name:", item.vm_name)

            if isinstance(item, IP):
                print ('ip:', item.ip)

            print ("")

    elif arguments["delete"]:
        pass


def get_group_names_list(username, cloudname, refresh=False):
    '''
    loops through all VMs of a cloud of a user, returns a list of all unique group 
    names accorrding to the metadata
    '''
    mongo = cm_mongo()
    if refresh:
        mongo.activate(cm_user_id=username, names=[cloudname])
        mongo.refresh(cm_user_id=username,
                      names=[cloudname],
                      types=['servers'])
    servers_dict = mongo.servers(
                clouds=[cloudname], cm_user_id=username)[cloudname]
                
    res = []
    for k, v in servers_dict.iteritems():
        if 'cm_group' in v['metadata']:
            temp = v['metadata']['cm_group']
            if temp not in res:
                res.append(temp)
    
    return res
        
    


def main():
    # cmd3_call(shell_command_experiment_group)
    pass

if __name__ == '__main__':
    main()
