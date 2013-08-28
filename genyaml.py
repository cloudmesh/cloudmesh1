from cloudmesh.config.cm_config import cm_config_server
from jinja2 import Template
from jinja2 import Environment, PackageLoader, meta
from sh import fgrep

class cm_template:

    def __init__(self,filename):
    	self.filename = filename
	self.content = open(filename, 'r').read()	  

    @property
    def variables(self):
    	vars = []
    	lines = self.content.splitlines()
	for line in lines:
	    if "{{" in line:
	        vars.append(line.split("{{")[1].split("}}")[0])
	return vars

    @property
    def _variables(self):
        env = Environment()
	parsed_content = env.parse(self.content)
	print meta.find_undeclared_variables(parsed_content)

    def replace(self,d):
    	template = Template(self.content)        
	self.reuslt = template.render(d)
	return self.result


if __name__ == "__main__":
    d = {}
    filename = "etc/cloudmesh.yaml"

    t = cm_template(filename)
    print t.content

    #print t.variables



    #print t.replace(d)


