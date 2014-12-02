"""Convenient methods and classes to print tables"""
from pytimeparse.timeparse import timeparse
from prettytable import PrettyTable
from datetime import datetime
from datetime import timedelta
import json
import yaml
import hostlist

def print_format_dict(d, header=None, kind='table'):
    """kind = json, yaml, table, pprint"""
    if kind == "json":
        return json.dumps(d, indent=4)
    elif kind == "yaml":
        return yaml.dump(d, default_flow_style=False)
    else:
        return two_column_table(d.keys(), header)


def array_dict_table_printer(array, order=None, header=None, vertical=False):
    """prints a pretty table from an array of dicts
    :param array: A an array with dicts of the same type.
                  Each key will be a column
    :param order: The order in which the columns are printed.
                  The order is specified by the key names of the dict.
    :param header: The Header of each of the columns

    """
    # header
    if header is None:
        header = array[0].keys()

    if order is None:
        order = header

    if header is None:
        if vertical:
            
            x = PrettyTable()
            x.add_column("Item", order)
        else:
            x = PrettyTable(order)
    else:
        if vertical:
            x = PrettyTable()
            x.add_column("Item", header)
        else:
            x = PrettyTable(header)

    for element in array:
        values = []
        for key in order:
            try:
                tmp = str(element[key])
            except:
                tmp = ' '
            values.append(tmp)
        if vertical:
            x.add_column(" ", values)
        else:
            x.add_row(values)
    x.align = "l"
    return x


def column_table(column_dict, order=None):
    """prints a pretty table from data in the dict.
    :param column_dict: A dict that has an array for each key in the dict.
                        All arrays are of the same length.
                        The keys are used as headers
    :param order: The order in which the columns are printed.XS
                  The order is specified by the key names of the dict.
    """
    # header
    header = column_dict.keys()
    x = PrettyTable()
    if order is None:
        order = header
    for key in order:
        x.add_column(key, column_dict[key])
    x.align = "l"
    return x

def row_table(d, order=None, labels=None):
    """prints a pretty table from data in the dict.
    :param d: A dict to be printed
    :param order: The order in which the columns are printed.XS
                  The order is specified by the key names of the dict.
    """
    # header
    header = d.keys()
    x = PrettyTable(labels)
    if order is None:
        order = header
    for key in order:
        value = d[key]
        if type(value) == list:
            x.add_row([key, value[0]])            
            for element in value[1:]:
                x.add_row(["", element])
        elif type(value) == dict:
            value_keys = value.keys()
            first_key = value_keys[0]
            rest_keys = value_keys[1:]
            x.add_row([key, "{0} : {1}".format(first_key,value[first_key])])            
            for element in rest_keys:
                x.add_row(["", "{0} : {1}".format(element,value[element])])
        else: 
            x.add_row([key, value])

        
    x.align = "l"
    return x


def two_column_table(column_dict, header=['Default', 'Value']):
    """prints a table with two columns where the first column are the
    attributes, and the second column are the values.

    :param column_dic: the dictionary to be printed
    """
    if not header:
        header = ['Default', 'Value']
    x = PrettyTable()
    x.add_column(header[0], column_dict.keys())
    x.add_column(header[1], column_dict.values())
    x.align = "l"
    return x


def one_column_table(column, header='Value'):
    """prints a table with two columns where the first column are the
    attributes, and the second column are the values.

    :param column_dic: the dictionary to be printed
    """
    x = PrettyTable()
    x.add_column(header, column)
    x.align = "l"
    return x


def table_printer(the_dict, header_info=None):
    """
    prints recurseively a dict as an html. The header info is simpli
    a list with collun names.

    :param the_dict: the dictionary to be printed.
    :param header_info: an array of two values that are used in the header

    """
    # header_info ["attribute", "value"]
    if (header_info is not None) or (header_info == ""):
        result = '<tr><th>{0}</th><th>{1}</th></tr>'\
            .format(header_info[0], header_info[1])
    else:
        result = ''
    if isinstance(the_dict, dict):
        for name, value in the_dict.iteritems():
            result = result + \
                '<tr><td>{0}</td><td>{1}</td></tr>'\
                .format(name.title(), str(table_printer(value)))
        result = '<table>' + result + '</table>'
        return result
    elif isinstance(the_dict, list):
        for element in the_dict:
            try:
                for name, value in element.iteritems():
                    result = result + \
                        '<tr><td>{0}</td><td>{1}</td></tr>'\
                        .format(name.title(), str(table_printer(value)))
            except:
                # If the element is not dict
                return str(element)
        result = '<table>' + result + '</table>'
        return result
    else:
        return the_dict


def parse_time_interval(time_start, time_end):
    """created time values for time_start and time_end, while time_end
    will be replaced with time_start+ a duration if the duration is
    given in time_end. The format of the duration is intuitive through
    the timeparse module. YOu can specify values such as +1d, +1w10s.

    :param time_start: the start time, if the string 'current_time' is
                       passed it will be replaced by the current time

    :param time_end: either a time or a duration
    """
    t_end = time_end
    t_start = time_start

    if t_start is not None:
        if t_start in ["current_time", "now"]:
            t_start = str(datetime.now())

    if t_end is not None:
        if t_end.startswith("+"):
            duration = t_end[1:]
            delta = timeparse(duration)
            t_start = datetime.strptime(t_start, "%Y-%m-%d %H:%M:%S.%f")
            t_end = t_start + timedelta(seconds=delta)

    return (str(t_start), str(t_end))


def dict_key_list_table_printer(d, indexed=False):
    '''
    accept a dict in the form:
    {key1: [list1],
     key2: [list2],
     .......
     =>
     | key1 | key2 |
     | l
     | i
     | s
     | t
    '''
    x = PrettyTable()
    temp = d.values()
    l = 0
    for item in temp:
        l0 = len(item)
        if l0 > l:
            l = l0
            
    if indexed:
        if l == 0:
            index_list = []
        else:
            index_list = hostlist.expand_hostlist("[1-{0}]".format(str(l)))
        x.add_column("index", index_list)
        
    for k,v in d.iteritems():
        v0 = v + [" "]*(l - len(v))
        x.add_column(k, v0)
    x.align = "l"
    return x
