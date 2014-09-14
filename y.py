import cloudmesh
from cloudmesh_install import config_file

config = cloudmesh.load("user")

def yaml_attribute_replace(filename='abc.yaml',
                           replacements={}):
    """ example

    filename = config_file("/cloudmesh.yaml")
    replacements = {
        "cloudmesh.profile.phone": "hallo",
        }

    yaml_attribute_replace(filename,replacements)

    """
    result = ""
    
    max_indent = 10
    
    with open(filename, 'r') as f:
        content = f.read()

        
    for replacement in replacements:
        attributes = replacement.split('.')
        found = [''] * max_indent # just a high number
        
        for line in content.split('\n'):
            # find the indentation level
            indent = (len(line) - len(line.lstrip(' '))) / 2
            # set all previously higher found indent to '' 
            for x in range(indent,max_indent):
                found[x] = ''
            # get the attribute name    
            attribute = line.split(":")[0].strip()
            # set the attribute name for the indentation level
            found[indent] = attribute
            # create the attribute name from teh indentation levels and remove the traiing .
            name = '.'.join(found).split('..')[0]
            if name == replacement:
                result += "{0}{1}: {2}".format(' ' * indent * 2, attribute, replacements[replacement])
            else:
                result += line
            
    #for _old, _new in replacements.iteritems():
    #    content = content.replace(_old, _new)

    outfile = open(filename, 'w')
    outfile.write(content)
    outfile.close()

