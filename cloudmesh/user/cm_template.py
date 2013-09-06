from jinja2 import Template

class cm_template():

    def __init__(self, filename):
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
        template = Template(self.content)
        self.result = template.render(data=d)
        return self.result

if __name__ == "__main__":
    d = {
      "portalname": "gvonlasz"
    }
    filename = "etc/cloudmesh.yaml"

    t = cm_template(filename)
    print t.variables()
    
    print t.replace(d, format="dict")

#    if not t.complete():
#       print "ERROR: undefined variables"
#       print t.variables()



