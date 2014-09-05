""" Basic Clousmesh finctions.

.. role:: strikethrough

This file contains tome veri basic utility functions that must not
need any import from cloudmesh. That is no statement such as

* :strikethrough:`import cloudmesh`

must occur in the list of import. If functions are needed hat need to
be used they must be decleard without dependencies in:: 

  import cloudmesh.util

The reasonong is that during th einitialization where cloudmesh is not
yet installed, the __init__ function for cloudmesh may include some
configuration files that are not yet present at the tome of the first
instalation.
"""

import inspect
import os
import uuid
import functools
#import warnings
import cloudmesh_common.bootstrap_util
import string
import random
try:
    from progress.bar import Bar
except:
    os.system("pip install progress")    
    from progress.bar import Bar    
    
class PROGRESS(object):
    
    def __init__(self,msg=None,limit=10):
        if msg is None:
            msg = "Cloudmesh Services"
        self.msg = msg
        self.bar = Bar(self.msg, max=limit)
        
    def set(self, msg, limit):
        self.bar = Bar(msg, max=limit)

    def next(self):
        self.bar.next()
      
    def finish(self):
        self.bar.finish()        

def path_expand(text):
    """ returns a string with expanded variable.

    :param text: the path to be expanded, which can include ~ and $ variables
    :param text: string

    """
    return cloudmesh_common.bootstrap_util.path_expand(text)


def backup_name(filename):
    """
    :param filename: given a filename creates a backupname of the form
                     filename.back.1. If the filename already exists
                     the number will be increasd as  much as needed so
                     the file does not exist in the given location.
                     The filename can consists a path and is expanded
                     with ~ and environment variables.
    :type filename: string
    :rtype: string
    """
    location = path_expand(filename)
    n = 0
    found = True
    while found:
        n = n + 1
        backup = "{0}.bak.{1}".format(location, n)
        found = os.path.isfile(backup)
    return backup


def banner(txt=None, c="#", debug=True):
    """prints a banner of the form with a frame of # arround the txt::

      ############################
      # txt
      ############################

    .

    :param txt: a text message to be printed
    :type txt: string
    :param c: thecharacter used instead of c
    :type c: character
    """
    if debug:
        cloudmesh_common.bootstrap_util.banner(txt, c, debug=True)


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


def yn_choice(message, default='y'):
    """asks for a yes/no question.
    :param message: the message containing the question
    :param default: the default answer
    """
    return cloudmesh_common.bootstrap_util.yn_choice(message, default)


def cat(filename):
    """prints the contents of a file with the given name.

    :param filename: name of the file, which can include ~ and $
                     environment variables 
    :type: string
    """
    location = path_expand(filename)
    banner(filename)
    with open(location, 'r') as f:
        print f.read()


def not_implemented():
    """prins simply an error that this is not implemented. This can be
    used when you protortype things."""

    print "ERROR: not yet implemented"


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
            location = [
                i for i in range(len(line)) if line.startswith('\t', i)]
            if verbose:
                print "Tab found in line", line_no, "and column(s)", location
        line_no = line_no + 1
    return file_contains_tabs


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
        print "Warning: Call to deprecated function {}.".format(func.__name__)
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
        """the internal decorator"""
        return dec(fn) if flag else fn
    return decorate


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

''' ref:
    http://stackoverflow.com/questions/2257441/python-random-string-generation-with-upper-case-letters-and-digits
'''


def get_rand_string(size=6, chars=string.ascii_uppercase + string.digits):
    """generates a random string.
    :param size: length of the string
    :param chars: string of charaters to chese form, by default a-zA-Z0-9
    """
    return ''.join(random.choice(chars) for _ in range(size))


def get_unique_name(prefix="", **kargs):
    """Make a UUID without some characters such as '-', '_', ' ', '.'

    :param prefix: a prefix added to the UUID
    :param **kargs: keyword arguments for additional options
    """
    change = ['-', '_', ' ', '.']

    id = uuid.uuid1()
    text = str(id).replace("-", "")

    if 'change' in kargs:
        change = kargs['change']

    for character in change:
        if character in prefix:
            prefix = prefix.replace(character, "")

    return str(prefix) + text


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
        
    The 'private' could be any other string indicating the vlan.
    E.g., HP_east cloud might return result which is not 'private'.
    Not necessarilly vlan102 either.
    For now we will assume an arbitry string exists as the name for vlan.
    """
    try:
        result = ""
        vlan = content.keys()[0]
        for address in content[vlan]:
            if labels:
                result = result + address['OS-EXT-IPS:kind'] + "="
            result = result + address['addr']
            result = result + ", "
        result = result[:-2]
    except:
        # THIS SEEMS WRONG
        #{u'vlan102': [{u'version': 4, u'addr': u'10.1.2.104'}, {
        #    u'version': 4, u'addr': u'149.165.158.34'}]}
        #try:
        #    position = 0
        #    for address in content['vlan102']:
        #        if position == 0:
        #            kind = "fixed"
        #        else:
        #            kind = "floating"
        #        if labels:
        #            result = result + kind
        #        result = result + address['addr']
        #        result = result + ", "
        #        position = +1
        #    result = result[:-2]
        #except:
        result = content
    return result


def dict_uni_to_ascii(d):
    '''
    convert mongodb document content from unicode to ascii
    '''
    d1 = {}
    for k, v in d.iteritems():
        k = k.encode("ascii")
        if isinstance(v, dict) or isinstance(v, unicode):
            try:
                v = v.encode("ascii")
            except:
                v = dict_uni_to_ascii(v)
        d1[k] = v
    return d1
        
        
