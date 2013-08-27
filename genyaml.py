from cloudmesh.config.cm_config import cm_config_server
from jinja2 import Template
from jinja2 import Environment, PackageLoader, meta
from sh import fgrep

#config = cm_config_server("etc/cloudmesh.yaml")

#rint config


d = {}


filename = "etc/cloudmesh.yaml"


file_content = open(filename, 'r').read()

print file_content





template = Template(file_content)

env = Environment()

parsed_content = env.parse(file_content)
print meta.find_undeclared_variables(parsed_content)

"""
r = fgrep ("{{")
for line in r:
    print line
"""

#content = template.render(d)
        
    
#print content