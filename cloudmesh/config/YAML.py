from __future__ import print_function
import re
import cloudmesh
from cloudmesh_base.locations import config_file


class YAML(object):
    """
    Examples::

    test = "   jjj"            
    print YAML.leading_spaces(test)

    filename = config_file("/cloudmesh.yaml")

            
    print YAML.first_indent(filename)

    print YAML.check_indent(filename)

    print YAML.check_indent(filename, indent=2)

    """
    
    @staticmethod
    def leading_spaces(line):
        return re.search('[^ ]', line).start()

    @staticmethod        
    def first_indent(filename):
        no = 1    
        with open(filename, 'r') as f:
            content = f.read()
        for line in content.split("\n"):
            if line != '':
                try:
                    spaces = YAML.leading_spaces(line)
                    if spaces > 0:
                        return spaces
                except Exception, e:
                    print("ERROR(", no, ")", e)
            no = no + 1
        return 0

    @staticmethod        
    def check_indent(filename, indent=4):

        success = True
        _indent = YAML.first_indent(filename)

        try:
            if indent != _indent:
                raise ValueError("the indenetation is wrong. "
                                 "Specified {0}, found {1}"
                                 .format(indent, _indent))
        except Exception, e:
            print("ERROR(indent)", e)
            return False
                
        with open(filename, 'r') as f:
            content = f.read()

        no = 1
        for line in content.split("\n"):
            if line != '':
                try:
                    spaces = YAML.leading_spaces(line)
                    if spaces % indent != 0:
                        success = False
                        raise ValueError("Line {0}. The indenetation is not a "
                                         "multiple of {1}. Indent found: {2}\n"
                                         "{0}: {3}".format(no, indent, spaces, line))
                except Exception, e:
                    success = False
                    print("ERROR(indent)", e)
            no = no + 1
        return success
    

