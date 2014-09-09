#! /usr/bin/env python
from cloudmesh_install import config_file

import cloudmesh_install
import glob
import shutil
from jinja2.runtime import Undefined
from cloudmesh.config.ConfigDict import ConfigDict
import json
from docopt import docopt
from cloudmesh.config.cm_config import cm_config
from cloudmesh_install.util import path_expand
from cloudmesh.user.cm_template import cm_template
from cloudmesh_install.util import yn_choice
from cloudmesh_common.util import backup_name
from cloudmesh_install.util import banner
from cloudmesh_common.tables import column_table
import os


from jinja2 import Environment
from jinja2 import Undefined
JINJA2_ENVIRONMENT_OPTIONS = {'undefined': Undefined}


from cloudmesh_common.logger import LOGGER

config_dir = cloudmesh_install.__config_dir__

log = LOGGER(__file__)


class IgnoreUndefined(Undefined):

    def __int__(self):
        return "None"


def find_meta(filename):
    file = open(filename, 'r')

    found = []
    for line in file:
        if line.startswith("meta:"):
            for i in range(0, 4):
                found.append(file.next())
            return found
    return found


def init_shell_command(arguments):
    """
    ::

      Usage:
             init [--force] generate yaml
             init [--force] generate me
             init [--force] generate none
             init [--force] generate FILENAME
             init list [KIND] [--json]
             init list clouds [--file=FILENAME] [--json]
             init inspect --file=FILENAME
             init fill --file=FILENAME [VALUES]

      Initializes cloudmesh from a yaml file

      Arguments:
         generate   generates a yaml file
         yaml       specifies if a yaml file is used for generation
                    the file is located at me.yaml
         me         same as yaml

         none       specifies if a yaml file is used for generation
                    the file is located at CONFIG/etc/none.yaml
         FILENAME   The filename to be generated or from which to read
                    information.
         VALUES     yaml file with the velues to be sed in the FILENAME
         KIND       The kind of the yaml file.

      Options:
         --force  force mode does not ask. This may be dangerous as it
                  overwrites the CONFIG/cloudmesh.yaml file
         --file=FILENAME  The file
         --json   make the output format json
         -v       verbose mode


      Description:

        init list [KIND] [--json]
           list the versions and types of the yaml files in the
           CONFIG and CONFIG/etc directories.

        init list clouds [--file=FILENAME]
           Lists the available clouds in the configuration yaml file.

        init inspect --file=FILENAME
           print the variables in the yaml template
    """

    if arguments["inspect"]:
        filename = arguments['--file']
        if filename is None:
            filename = config_file('/cloudmesh.yaml')

        content = open(filename, 'r').read()

        t = cm_template(filename)
        sorted_vars = sorted(set(t.variables()))
        print "\n".join(sorted_vars)
        # banner("PARSER")
        # env = Environment()
        # ast = env.parse(content)
        # for v in meta.find_undeclared_variables(ast):
        #    print v
    if arguments["list"] and not arguments["clouds"]:
        dirs = [path_expand(config_dir + '/*.yaml'),
                path_expand(config_dir + '/etc/*.yaml')]
        file_list = []
        for directory in dirs:
            file_list.extend(glob.glob(directory))
        vector = {}
        vector['kind'] = []
        vector['yaml_version'] = []
        vector['meta'] = []
        vector['filename'] = []
        for filename in file_list:
            values = {'kind': "-", 'yaml_version': "-", 'meta': "-"}
            head_of_file = find_meta(filename)
            values = {'kind': "-", 'yaml_version': "-", 'meta': "-"}
            for line in head_of_file:
                if ":" in line:
                    (attribute, value) = line.strip().split(":")
                    if attribute in ["kind", "yaml_version"]:
                        values[attribute] = value.strip()
                    if attribute in ["meta"]:
                        values[attribute] = "+"
            if arguments["KIND"] is None or \
               values['kind'] == arguments['KIND']:
                for attribute in values.keys():
                    vector[attribute].append(values[attribute])
                vector['filename'].append(filename)

        vector['Kind'] = vector.pop('kind')
        vector['Version'] = vector.pop('yaml_version')
        vector['Meta'] = vector.pop('meta')
        vector['Filename'] = vector.pop('filename')

        banner("Configuration Directory: {0}".format(config_dir), c="-")
        print column_table(vector)

        # print filename, values["kind"], values["version"]

    if arguments["list"] and arguments["clouds"]:
        filename = arguments['--file']
        if filename is None:
            filename = config_file('/cloudmesh.yaml')
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
            print column_table(data, ['Labels', 'Clouds', 'Type', 'Version'])

    if arguments["fill"]:

        filename_template = arguments['--file']
        if filename_template is None:
            filename_template = config_file('/etc/cloudmesh.yaml')
        filename_template = path_expand(filename_template)

        filename_values = arguments['VALUES']

        if filename_values is None:
            filename_values = config_file('/me.yaml')

        content = open(filename_template, 'r').read()

        t = cm_template(filename_template)
        sorted_vars = sorted(set(t.variables()))

        try:
            values = ConfigDict(filename=filename_values)
        except Exception, e:
            print "ERROR: There is an error in the yaml file", e

        for cloud in values['clouds']:
            values['clouds'][cloud]['default'] = {}
            values['clouds'][cloud]['default']['image'] = None
            values['clouds'][cloud]['default']['flavor'] = None

        banner("%s -> %s" % (filename_values, filename_template))
        env = Environment(undefined=IgnoreUndefined)
        template = env.from_string(content)
        result = template.render(values)
        print result

    if arguments["generate"]:
        filename_tmp = config_file('/cloudmesh-new.yaml')
        filename_out = config_file('/cloudmesh.yaml')
        filename_bak = backup_name(filename_out)
        filename_template = config_file("/etc/cloudmesh.yaml")
        if arguments["generate"] and (arguments["me"]):
            filename_values = config_file("/me.yaml")
        elif arguments["generate"] and (arguments["yaml"]):
            filename_values = config_file("/me.yaml")
        elif (arguments["generate"] and arguments["none"]):
            filename_values = config_file("/etc/me-none.yaml")
        elif arguments["FILENAME"] is not None:
            filename_values = path_expand(arguments["FILENAME"])
        # print me_filename
        # print etc_filename

        try:
            values = ConfigDict(filename=filename_values)
        except Exception, e:
            print "ERROR: There is an error in the yaml file", e

        for cloud in values['clouds']:
            values['clouds'][cloud]['default'] = {}
            values['clouds'][cloud]['default']['image'] = None
            values['clouds'][cloud]['default']['flavor'] = None

        content = open(filename_template, 'r').read()
        env = Environment(undefined=IgnoreUndefined)
        template = env.from_string(content)
        result = template.render(values)

        out_file = open(filename_tmp, 'w+')
        out_file.write(result)
        out_file.close()

        if not arguments["--force"]:
            if yn_choice("Review the new yaml file", default='n'):
                print filename_tmp
                os.system('less -E {0}'.format(filename_tmp))
        if arguments["--force"]:
            shutil.copy(filename_out, filename_bak)
            os.rename(filename_tmp, filename_out)
            print "# Template: {0}".format(filename_template)
            print "# Values  : {0}".format(filename_values)
            print "# Backup  : {0}".format(filename_bak)
            print "# Created : {0}".format(filename_out)
        elif yn_choice("Move the new yaml file to {0}"
                       .format(filename_out), default='y'):
            shutil.copy(filename_out, filename_bak)
            os.rename(filename_tmp, filename_out)
            print "# Template: {0}".format(filename_template)
            print "# Values  : {0}".format(filename_values)
            print "# Backup : {0}".format(filename_bak)
            print "# Created: {0}".format(filename_out)
        return


def main():
    arguments = docopt(init_shell_command.__doc__)
    init_shell_command(arguments)

if __name__ == '__main__':
    main()
