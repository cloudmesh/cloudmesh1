import sys
import yaml
from jinja2 import Template
from cloudmesh.util.util import path_expand
from cloudmesh.util.util import banner

class cm_template():

    def __init__(self, filename):

        self.filename = path_expand(filename)
        self.content = open(self.filename, 'r').read()

    def variables(self):
        vars = list()
        lines = self.content.splitlines()
        for line in lines:
            if "{{" in line:
                words = line.split("{{")
                for word in words:
                    if "}}" in word:
                        name = word.split("}}")[0].strip()
                        vars.append(name)
        return vars

    def _variables(self):
        env = Environment()
        parsed_content = env.parse(self.content)
        print meta.find_undeclared_variables(parsed_content)

    def replace(self, kind='text', values=None):

        try:
            template = Template(self.content)
            if kind == "text":
                self.result = template.render(**values)
            elif kind == "dict":
                self.result = yaml.safe_load(template.render(**values))
            else:
                log.error("kind='dict' or 'text' parameter missing in template replace")
                raise RuntimeError
            return self.result
        except:
            banner ("ERROR")
            print sys.exc_info()
            # return self.content
            return None

if __name__ == "__main__":
    d = {
      "portalname": "gvonlasz"
    }
    filename = "etc/cloudmesh.yaml"

    t = cm_template(filename)
    print t.variables()

    print t.replace(values=d, format="dict")

#    if not t.complete():
#       print "ERROR: undefined variables"
#       print t.variables()



