from cloudmesh.config.cm_config import cm_config_server
from jinja2 import Template
from jinja2 import Environment, PackageLoader, meta
from sh import fgrep
import sys

class cm_template:

    def __init__(self,filename):
        self.filename = filename
        self.content = open(filename, 'r').read()

    def variables(self):
        vars = list()
        lines = self.content.splitlines()
        for line in lines:
            if "{{" in line:
                words = line.split("{{")
                for word in words:
                    if "}}" in word:
                        name = word.split("}}")[0]
                        vars.append(name)
        return vars

    def _variables(self):
        env = Environment()
        parsed_content = env.parse(self.content)
        print meta.find_undeclared_variables(parsed_content)

    
    
    def replace(self, d, format="text"):

        v = self.variables()
        k = d.keys()

        diff = set(v) - set(k)

        self.complete = len(diff) == 0
        if len(diff) > 0:

            print "\nERROR: substitution abborted"
            print "Undefined variables in the file:", self.filename
            if format == "text":
                    print "   ",'\n    '.join(diff)
            elif format == "list":
                    print diff
            else:
                print "d = {"
                for v in d:
                    print '    "{0}" : "{1}",'.format(v, d[v])
                for v in diff:
                    print '    "{0}" : "",'.format(v)
                print '}'
            sys.exit()
        else:
            template = Template(self.content)
            self.result = template.render(d)
            return self.result

if __name__ == "__main__":
    d = {
      "portalname": "gvonlasz"
    }
    filename = "etc/cloudmesh.yaml"

    t = cm_template(filename)
    print t.variables()
    
    print t.replace(d,format="dict")

#    if not t.complete():
#       print "ERROR: undefined variables"
#       print t.variables()



