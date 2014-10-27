'''some useful functions while working with shell'''
from __future__ import print_function
from cloudmesh.config.cm_config import cm_config
from cloudmesh.user.cm_user import cm_user
import json
from cloudmesh_common.tables import array_dict_table_printer
from cloudmesh import banner
import csv
from cmd3.console import Console


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
