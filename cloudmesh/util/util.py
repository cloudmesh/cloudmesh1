from string import Template
import os

"""Some simple utility functions"""

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
    return result


def HEADING(txt):
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
                result = result +\
                    '<tr><td>{0}</td><td>{1}</td></tr>'.format(name.title(),
                                                               str(table_printer(value)))
        result = '<table>' + result + '</table>'
        return result
    else:
        return the_dict
