'''a number of useful functions'''
from string import Template
import inspect
import os
import uuid
import functools
import warnings
from datetime import datetime, timedelta
from pytimeparse.timeparse import timeparse
from cloudmesh.util.banner import banner
from prettytable import PrettyTable


def two_column_table(column_dict):
    # header
    header = ['Default','Value']
    x = PrettyTable()
    x.add_column('Default', column_dict.keys())
    x.add_column('Value', column_dict.values())
    x.align = "l"
    return x
        

def not_implemented():
    print "ERROR: not yet implemented"


def parse_time_interval (time_start, time_end):
    """created time values for time_start and time_end, while time_end
    will be replaced with time_start+ a duration if the duration is
    given in time_end. The format of the duration is intuitive through
    the timeparse module. YOu can specify values such as +1d, +1w10s.

    :param time_start: the start time, if the string 'current_time' is passed it will be replaced by the current time
    :param time_end: either a time or a duration
    """ 
    t_end = time_end
    t_start = time_start

    if t_start is not None:
        if t_start in ["current_time","now"]:
            t_start = str(datetime.now())

    if t_end is not None:
        if t_end.startswith("+"):
            duration = t_end[1:]
            delta = timeparse(duration)
            t_start = datetime.strptime(t_start, "%Y-%m-%d %H:%M:%S.%f")
            t_end = t_start + timedelta(seconds=delta)

    return (str(t_start), str(t_end))


def cat(filename):
    """prints the contents of a file with the given name.

    :param filename: name of the file, which can include ~ and $ environment variables 
    :type: string
    """
    banner(filename)
    with open(path_expand(filename), 'r') as f:
        print f.read()

        
def yn_choice(message, default='y'):
    """asks for a yes/no question.
    :param message: the message containing the question
    :param default: the default answer
    """
    # http://stackoverflow.com/questions/3041986/python-command-line-yes-no-input"""
    choices = 'Y/n' if default.lower() in ('y', 'yes') else 'y/N'
    choice = raw_input("%s (%s) " % (message, choices))
    values = ('y', 'yes', '') if default == 'y' else ('y', 'yes')
    return True if choice.strip().lower() in values else False


def deprecated(func):
     '''This is a decorator which can be used to mark functions
     as deprecated. It will result in a warning being emitted
     when the function is used. Just use @deprecated before
     the definition.::

         @deprecated
         def my_func():
           pass

         @other_decorators_must_be_before
         @deprecated
         def my_func():
           pass

     '''
     @functools.wraps(func)
     def new_func(*args, **kwargs):
         '''
         warnings.warn_explicit(
             "Call to deprecated function {}.".format(func.__name__),
             category=DeprecationWarning,
             filename=func.func_code.co_filename,
             lineno=func.func_code.co_firstlineno + 1
         )
         '''
         print
         print 70 * "-"
         print("Warning: Call to deprecated function {}.".format(func.__name__))
         print "         filename=", func.func_code.co_filename
         print "         lineno=", func.func_code.co_firstlineno + 1
         print 70 * "-"

         return func(*args, **kwargs)
     return new_func



def cond_decorator(flag, dec):
    """conditional decorator that is used if the flag is true.

    :param flag: the boolean flag
    :type flag: boolean
    """
    def decorate(fn):
        return dec(fn) if flag else fn
    return decorate

def address_string(content, labels=False):
    """content is a dict of the form::

       {u'private': [{u'version': 4,
                      u'addr': u'10.35.23.30',
                      u'OS-EXT-IPS:kind':u'fixed'},
                     {u'version': 4,
                      u'addr': u'198.202.120.194',
                      u'OS-EXT-IPS:kind': u'floating'}]}

    it will return::

        "fixed: 10.35.23.30, floating: 198.202.120.194'
    """
    try:
        result = ""
        for address in content['private']:
            if labels:
                result = result + address['OS-EXT-IPS:kind'] + "="
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
                    kind = "fixed"
                else:
                    kind = "floating"
                if labels:
                    result = result + kind
                result = result + address['addr']
                result = result + ", "
                position = +1
            result = result[:-2]
        except:
            result = content
    return result

def status_color(status):
    """returns some predefined color values.
    * ACTIVE ::= green
    * BUILDING ::= blue
    * ERROR ::= red
    * default ::= black

    :param status: 'ACTIVE', 'BUILDING', 'ERROR'
    :rtype: string
    """
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
    verbose is set to False, the location is not printed.

    :param filename: the filename
     :rtype: True if there are tabs in the file
    """
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
    """ returns a string with expanded variavble.

    :param text: the path to be expanded, which can include ~ and $ variables
    :param text: string
    
    """
    template = Template(text)
    result = template.substitute(os.environ)
    result = os.path.expanduser(result)
    return result


def HEADING(txt=None):
    """
    Prints a message to stdout with #### surrounding it. This is useful for
    nosetests to better distinguish them.

    :param txt: a text message to be printed
    :type txt: string
    """
    if txt is None:
        txt = inspect.getouterframes(inspect.currentframe())[1][3]

    banner(txt)




def table_printer(the_dict, header_info=None):
    """
    prints recurseively a dict as an html. The header info is simpli a list with
    collun names.

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
                #If the element is not dict
                return str(element)
        result = '<table>' + result + '</table>'
        return result
    else:
        return the_dict

def get_unique_name(prefix=""):
    """Make a UUID without some characters such as '-', '_', ' ', '.'

    :param prefix: a prefix added to the UUID
    """
    change = ['-', '_', ' ', '.']
    id = uuid.uuid1()
    text = str(id).replace("-", "")
    for ch in change:
        if ch in prefix:
            prefix = prefix.replace(ch, "")

    return str(prefix) + text
