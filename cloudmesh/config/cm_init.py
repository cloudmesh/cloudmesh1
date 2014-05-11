#! /usr/bin/env python
from jinja2.runtime import Undefined
from jinja2 import Template, FileSystemLoader
from cloudmesh.config.ConfigDict import ConfigDict
from pprint import pprint
import json
import types
import textwrap
from docopt import docopt
import inspect
import sys
import importlib
from cloudmesh.config.cm_config import cm_config
from cloudmesh.util.util import path_expand
from cloudmesh.user.cm_template import cm_template
from cloudmesh.util.util import yn_choice
from cloudmesh.util.banner import banner
from cloudmesh.util.util import column_table
from sh import less
import os
from sets import Set

from jinja2 import Environment, meta
from jinja2 import Undefined
JINJA2_ENVIRONMENT_OPTIONS = { 'undefined' : Undefined }


from cloudmesh.util.logger import LOGGER

log = LOGGER(__file__)

class IgnoreUndefined(Undefined):
    def __int__(self):
        return "None"

    
def init_shell_command(arguments):
    """
    Usage:
           init [force] generate yaml
           init [force] generate me
           init [force] generate none
           init [force] generate FILENAME
           init list [-f FILENAME] [--json]
           init inspect [-f FILENAME]
           init fill [--in=FILENAME] [VALUES]
                      
    Initializes cloudmesh from a yaml file

    Arguments:
       generate   generates a yaml file
       yaml       specifies if a yaml file is used for generation
                  the file is located at ~/.futuregrid/me.yaml
       me         same as yaml

       none       specifies if a yaml file is used for generation
                  the file is located at ~/.futuregrid/etc/none.yaml
       force      force mode does not ask. This may be dangerous as it
                  overwrites the ~/.futuregrid/cloudmesh.yaml file
       FILENAME   The filename to be generated or from which to read
                  information. 
       VALUES     yaml file with the velues to be sed in the FILENAME
       
    Options:
       --json   make the output format json
       -v       verbose mode

    Description:

      init list [-f FILENAME]
         Lists the available clouds in the configuration yaml file.

      init inspect [-f FILENAME] [--json]
         print the variables in the yaml template
    """
    # log.info(arguments)
    # print "<", args, ">"
    if arguments["inspect"]:
        filename = arguments['FILENAME']
        if filename is None:
            filename = path_expand('~/.futuregrid/cloudmesh.yaml')

        content = open(filename, 'r').read()
        
        t = cm_template(filename)
        sorted_vars = sorted(set(t.variables()))
        print "\n".join(sorted_vars)
        # banner("PARSER")
        # env = Environment()
        # ast = env.parse(content)
        # for v in meta.find_undeclared_variables(ast):
        #    print v



    
    if arguments["list"]:
        filename = arguments['FILENAME']
        if filename is None:
            filename = path_expand('~/.futuregrid/cloudmesh.yaml')
        config = cm_config(filename)

        data = {}
        data['Clouds'] = config.cloudnames()
        data['Labels'] = []
        data['Type'] = []
        data['Version'] = []                
        for cloud_key in data['Clouds']:
            data['Labels'].append(config.cloud(cloud_key)['cm_label'])
            data['Type'].append(config.cloud(cloud_key)['cm_type'])
            data['Version'].append(config.cloud(cloud_key)['cm_type_version'])
        if arguments["--json"]:
            print json.dumps(data, sort_keys=True, indent=4)
        else:
            print column_table(data, ['Labels','Clouds','Type','Version'])

    if arguments["fill"]:
            
        print arguments
        filename_template = arguments['--in']
        if filename_template is None:
            filename_template = '~/.futuregrid/etc/a-cloudmesh-template.yaml'
        filename_template = path_expand(filename_template)
        
        filename_values = arguments['VALUES']

        if filename_values is None:
            filename_values = path_expand('~/.futuregrid/me.yaml')

        print "PPPPP", filename_template
        content = open(filename_template, 'r').read()
        
        t = cm_template(filename_template)
        sorted_vars = sorted(set(t.variables()))
        print "\n".join(sorted_vars)

        #print arguments
        try:
            values = ConfigDict(filename=filename_values)
        except Exception, e:
            print "ERROR: There is an error in teh yaml file", e
        #print value_dict



        banner ("set dafault")
        
        for cloud in values['clouds']:
            print cloud
            values['clouds'][cloud]['default'] = {}            
            values['clouds'][cloud]['default']['image'] = None
            values['clouds'][cloud]['default']['flavor'] = None            
        print values
                    
        banner("%s -> %s" % (filename_values, filename_template))
        env = Environment(undefined=IgnoreUndefined)
        template = env.from_string(content)
        result = template.render(values)
        print result
        
        #        JINJA2_ENVIRONMENT_OPTIONS = { 'undefined' : Undefined }
        #env = Environment(JINJA2_ENVIRONMENT_OPTIONS)
        #print content
        #ast = env.parse(content)
        
        #for v in meta.find_undeclared_variables(ast):
        #    print v


        #try:
        #    
        #    print t._generate_from_dict(values)
        #except UndefinedError, e:
        #    print "OOOO", e
        #except Exception, e:
        #    print "EEEE", e
    if arguments["generate"]:
        new_yaml = path_expand('~/.futuregrid/cloudmesh-new.yaml')
        print "1aaaaaa"
        old_yaml = path_expand('~/.futuregrid/cloudmesh.yaml')
        print "2aaaaaa"
        etc_filename = path_expand("~/.futuregrid/etc/cloudmesh.yaml")
        print "3aaaaaa"

        if arguments["generate"] and (arguments["me"] or arguments["yaml"]):
            print "4aaaaaa"
            me_filename = path_expand("~/.futuregrid/me.yaml")
            print "5aaaaaa"

        elif (args.strip() in ["generate none"]):
            me_filename = path_expand("~/.futuregrid/etc/none.yaml")
        elif arguments["FILENAME"] is not None:
            me_filename = path_expand(arguments["FILENAME"])
        # print me_filename
        # print etc_filename
        print "b"
        t = cm_template(etc_filename)
        print "c"
        t.generate(me_filename, new_yaml)
        print "d"

        if not arguments["force"]:
            if yn_choice("Review the new yaml file", default='n'):
                os.system("less -E {0}".format(new_yaml))
        if arguments["force"]:
            os.system("mv {0} {1}".format(new_yaml, old_yaml))
        elif yn_choice("Move the new yaml file to {0}"
                       .format(old_yaml), default='y'):
            os.system("mv {0} {1}".format(new_yaml, old_yaml))
        return

def main():
    arguments = docopt(init_shell_command.__doc__)
    init_shell_command(arguments)

if __name__ == '__main__':
    main()
