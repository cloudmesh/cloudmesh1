'''some useful functions while working with shell'''
from __future__ import print_function
from cloudmesh.config.cm_config import cm_config
from cloudmesh.user.cm_user import cm_user
import json
from cloudmesh_common.tables import array_dict_table_printer
from cloudmesh import banner
import csv
from cmd3.console import Console
import hostlist
from cloudmesh.cm_mongo import cm_mongo
from cloudmesh.util.naming import server_name_analyzer


def shell_commands_dict_output(d,
                               print_format=None,
                               firstheader=None,
                               header=None,
                               oneitem=False,
                               vertical_table=False,
                               title=None,
                               count=False):
    '''
    some shell commands output a dict or table, this function should be
    called when commands are printing in such way.
    if none of parameters json and table is given, the funtion will try
    to find the default printing form from db_defaults
    if db_defaults has no item 'shell_print_format', the function will
    set 'shell_print_format' = table

    param d:: data to print
    param print_format:: print format: table, json, csv
    param firstheader:: designed for table, provide a attribute name for the
                        first item of each row, since the dict doesn't provide
                        it
    param header:: designed for table(and used to filter input dict), a list of lists, 
                   provides column order, e.g.
                   [[a,b], [c, d], ...
                   where 'a' is the printing column name and 'b' is the attribute name
                   in the dict
                   if you don't want to change the header name but want to keep the
                   header order or filter the items to list, for each item in the list
                   you may provide a string or a list with one item instead of a list of 
                   two items
    param oneitem:: designed for table, normally the input dict should be in such
                    form:
                    {a: {...}, b:{...}}, where each subitem is a row
                    if there is only one item, input dict is the {...} of the subitem
                    above
    param title: provide a title for the table
    param count: provide count info at the end of the table
    '''
    format_type = None
    if print_format:
        format_type = print_format
    else:
        try:
            config = cm_config()
        except:
            Console.error(
                "There is a problem with the configuration yaml files")
        username = config['cloudmesh']['profile']['username']
        user_obj = cm_user()
        userdata = user_obj.info(username)
        try:
            format_type = userdata['defaults']['shell_print_format']
        except:
            pass
        if format_type in [None, 'none']:
            userdata['defaults']['shell_print_format'] = "table"
            user_obj.set_defaults(username, userdata['defaults'])
            userdata = user_obj.info(username)
            format_type = userdata['defaults']['shell_print_format']

    if format_type not in ['table', 'json', 'csv']:
        print("ERROR: something wrong while reading print format infomation")
        return False
    
    headers = None
    order = None
    if header:
        headers = []
        order = []
        for i in header:
            if isinstance(i, basestring):
                headers.append(i)
                order.append(i)
            elif isinstance(i, list):
                if len(i) == 1:
                    headers.append(i[0])
                    order.append(i[0])
                else:
                    headers.append(i[0])
                    order.append(i[1])
            else:
                print("ERROR: header info is not correct")
                return False
    
    # --------------------------------------------------------------------------       
    # filter the input dict
    # -------------------------------------------------------------------------- 
    if order:
        new_d = {}
        if oneitem:
            for item in order:
                if item in d:
                    new_d[item] = d[item]
        else:
            for i in d:
                new_d[i] = {}
                for item in order:
                    if item in d[i]:
                        new_d[i][item] = d[i][item]
        d = new_d
    # -------------------------------------------------------------------------- 
 
    if format_type == "json":
        if title:
            banner(title)
        print(json.dumps(d, indent=4))
        
    elif format_type == "csv":
        with open(".temp.csv", "wb") as f:
            w = csv.DictWriter(f, d.keys())
            w.writeheader()
            w.writerow(d)
        
    elif format_type == "table":
        if title:
            print("+" + "-" * (len(title) - 2) + "+")
            print(title)

        print_data = []
        if oneitem:
            print_data = [d]
        else:
            for k in sorted(d):
                d[k][' '] = k
                print_data.append(d[k])
            if header:
                if firstheader:
                    headers = [firstheader] + headers
                order = [' '] + order
        
        if vertical_table:
            print(array_dict_table_printer(print_data, 
                                           order=order, 
                                           header=headers,
                                           vertical=True))
        else:
            print(array_dict_table_printer(print_data, order=order, header=headers))

        if count:
            c = len(print_data)
            sentence = "count: {0}".format(c)
            print(sentence)
            print("+" + "-" * (len(sentence) - 2) + "+")




def get_command_list_refresh_default_setting(username):
    '''
    value to define the default behaviour of command list, if True, then refresh
    before list as default
    '''
    try:
        user_obj = cm_user()
    except:
        Console.error("There is a problem with "
                              "cm_user object initialization")
        return False
    defaults_data = user_obj.info(username)['defaults']
    if "shell_command_list_refresh_default_setting" not in defaults_data or\
    defaults_data["shell_command_list_refresh_default_setting"] in [None, 'none']:
        defaults_data["shell_command_list_refresh_default_setting"] = True
        user_obj.set_defaults(username, defaults_data)
        return defaults_data["shell_command_list_refresh_default_setting"]
    else:
        return defaults_data["shell_command_list_refresh_default_setting"]
    
    
def get_vms_look_for(username,
                     cloudname,
                     servername=None,
                     serverid=None,
                     groupname=None,
                     prefix=None,
                     hostls=None,
                     getAll=False,
                     refresh=False): 
    '''
    work as a filter to find the VMs you are looking for. Input the seaching conditions,
    and returns a list of server ids that meet the condition
    
    you cannot provide servername and serverid at the same time
    you cannot provide prefix and hostlist at the same time
    param hostls:: e.g. sample[1-3,18] => ['sample1', 'sample2', 'sample3', 'sample18']
    param refresh:: refresh before filtering
    param getAll:: if True, the function consider all VMs are selected before filtering.
                   if False, then none are selected before filtering
    '''
    # input checking 
    if servername and serverid:
        Console.error("you cannot provide servername and serverid at the same time")
        return False
    if prefix and hostls:
        Console.error("you cannot provide prefix and hostlist at the same time")
        return False
    if hostls:
        try:
            hostls_list = hostlist.expand_hostlist(hostls)
        except:
            Console.error("please check your hostlist input, right format e.g. sample[1-9,18]")
            return False
    
    # get server data
    try:
        mongo = cm_mongo()
    except:
        Console.error("There is a problem with the mongo server")
        return False
    
    if refresh:
        mongo.activate(cm_user_id=username, names=[cloudname])
        mongo.refresh(cm_user_id=username,
                      names=[cloudname],
                      types=['servers'])
        
    servers_dict = mongo.servers(
                clouds=[cloudname], cm_user_id=username)[cloudname]
                
    # search for qualified vms for each critera
    ls = [
            [],  # 0 servername
            [],  # 1 serverid
            [],  # 2 groupname
            [],  # 3 prefix
            [],  # 4 hostls
            []   # 5 getAll
         ]
    for k, v in servers_dict.iteritems():
        if servername and servername == v['name']:
            ls[0].append(k)
        if serverid and serverid == k:
            ls[1].append(k)
        if groupname:
            try:
                grouptemp = None
                grouptemp = v['metadata']['cm_group']
            except:
                pass
            if groupname == grouptemp:
                ls[2].append(k)
        if prefix:
            nametemp = server_name_analyzer(v['name'])
        if prefix and prefix == nametemp[0]:
            ls[3].append(k)
        if hostls and v['name'] in hostls_list:
            ls[4].append(k)
        if getAll and v['cm_cloud'] == cloudname:
            ls[5].append(k)
    # -------------------------
    # intersect the results
    ls = [x for x in ls if x != []]
    l = len(ls)
    if l == 0:
        res = []
    elif l == 1:
        res = ls[0]
    else:
        res = ls[0]
        del ls[0]
        for i in ls:
            res = set(res) & set(i)
        res = list(res)
    
    return res
    
