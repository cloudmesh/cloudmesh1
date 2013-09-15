from string import Template
import os
import sys
import inspect
# import yaml
# from logger import LOGGER

def cond_decorator(flag, dec):
   def decorate(fn):
      return dec(fn) if flag else fn
   return decorate

def address_string(content, labels=False):
    """content is a dict of the form {u'private': [{u'version':
    4,u'addr': u'10.35.23.30',u'OS-EXT-IPS:type':u'fixed'},
    {u'version': 4, u'addr': u'198.202.120.194',
    u'OS-EXT-IPS:type': u'floating'}]}

    it will return

    "fixed: 10.35.23.30, floating: 198.202.120.194'
    """
    try:
        result = ""
        for address in content['private']:
            if labels:
                result = result + address['OS-EXT-IPS:type'] + "="
            result = result + address['addr']
            result = result + ", "
        result = result[:-2]
    except:
        # THIS SEEMS WRONG
        {u'vlan102': [{u'version': 4, u'addr': u'10.1.2.104'}, {
            u'version': 4, u'addr': u'149.165.158.34'}]}
        try:
            position = 0
            for address in content['vlan102']:
                if position == 0:
                    type = "fixed"
                else:
                    type = "floating"
                if labels:
                    result = result + type
                result = result + address['addr']
                result = result + ", "
                position = +1
            result = result[:-2]
        except:
            result = content
    return result

def status_color(self, status):
    if status == 'ACTIVE':
        return "green"
    if status == 'BUILDING':
        return "blue"
    if status in ['ERROR']:
        return "red"
    return "black"


def check_file_for_tabs(filename, verbose=True):
    """identifies if the file contains tabs and returns True if it
    does. It also prints the location of the lines and columns. If
    verbose is set to False, the location is not printed."""
    file_contains_tabs = False
    with file(filename) as f:
        lines = f.read().split("\n")

    line_no = 1
    for line in lines:
        if "\t" in line:
            file_contains_tabs = True
            location = [i for i in range(len(line)) if line.startswith('\t', i)]
            if verbose:
                print "Tab found in line", line_no, "and column(s)", location
        line_no = line_no + 1
    return file_contains_tabs

def path_expand(text):
    """ returns a string with expanded variavble """
    template = Template(text)
    result = template.substitute(os.environ)
    result = os.path.expanduser(result)
    return result


def HEADING(txt=None):
    if txt is None:
        txt = inspect.getouterframes(inspect.currentframe())[1][3]

    """Prints a message to stdout with #### surrounding it. This is useful for nosetests to better distinguish them."""
    print
    print "#", 70 * '#'
    print "#", txt
    print "#", 70 * '#'


def table_printer(the_dict, header_info=None):
    """prints recurseively a dict as an html. The header info is simpli a list with collun names."""
    # header_info ["attribute", "value"]
    if (header_info is not None) or (header_info == ""):
        result = '<tr><th>{0}</th><th>{1}</th></tr>'.format(
            header_info[0], header_info[1])
    else:
        result = ''
    if isinstance(the_dict, dict):
        for name, value in the_dict.iteritems():
            result = result + \
                '<tr><td>{0}</td><td>{1}</td></tr>'.format(name.title(),
                                                           str(table_printer(value)))
        result = '<table>' + result + '</table>'
        return result
    elif type(the_dict) is list:
        for element in the_dict:
            for name, value in element.iteritems():
                result = result + \
                    '<tr><td>{0}</td><td>{1}</td></tr>'.format(name.title(),
                                                               str(table_printer(value)))
        result = '<table>' + result + '</table>'
        return result
    else:
        return the_dict




