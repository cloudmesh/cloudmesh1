from string import Template
import os

def path_expand(text):
    """ returns a string with expanded variavble """
    template = Template(text)
    result = template.substitute(os.environ)
    return result

def HEADING(txt):
    print
    print "#", 70 * '#'
    print "#", txt
    print "#", 70 * '#'

def table_printer(the_dict, header_info=None):
    # header_info ["attribute", "value"]
    if header_info != None or (header_info == "") :
        result = '<tr><th>{0}</th><th>{1}</th></tr>'.format(header_info[0], header_info[1])
    else:
        result = ''
    if isinstance(the_dict, dict):
        for name,value in the_dict.iteritems() :
            result = result + \
                '<tr><td>{0}</td><td>{1}</td></tr>'.format(name.title(),
                                                           str(table_printer(value)))
        result = '<table>' + result + '</table>'
        return result
    elif type(the_dict) is list: 
        for element in the_dict:
            for name,value in element.iteritems() :
                result =result +\
                    '<tr><td>{0}</td><td>{1}</td></tr>'.format(name.title(),
                                                               str(table_printer(value)))
        result = '<table>' + result + '</table>'
        return result 
    else:
        return the_dict
