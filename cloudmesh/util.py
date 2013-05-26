from string import Template
import os

def path_expand(text):
    """ returns a string with expanded variavble """
    template = Template(text)
    result = template.substitute(os.environ)
    return result

if __name__ == "__main__":

    a = 1
