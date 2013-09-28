import sys
import yaml
from jinja2 import Template
from cloudmesh.util.util import path_expand
from cloudmesh.util.util import banner
from cloudmesh.config.ConfigDict import ConfigDict
import yaml
from sh import grep as _grep
from pprint import pprint
from cloudmesh.util.logger import LOGGER


# ----------------------------------------------------------------------
# SETTING UP A LOGGER
# ----------------------------------------------------------------------

log = LOGGER(__file__)

# ----------------------------------------------------------------------
# CM TEMPLATE
# ----------------------------------------------------------------------

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

    def grep(self, strip=True):
        result = []
        s = set(t.variables())
        for attribute in s:
            grep_result = _grep("-n", attribute, cloudmesh_yaml).split("\n")
            for r in grep_result:
                if "{" in r:
                    result.append(str(r).replace("  ", "").replace(":", ": ", 1))
        return result

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

    def generate(self,
                 me_file,
                 out_file):
        cloudmesh_yaml = path_expand(self.filename)
        user_config = ConfigDict(filename=me_file)
        t = cm_template(cloudmesh_yaml)

        result = t.replace(kind="dict", values=user_config)
        location = path_expand(out_file)
        yaml_file = open(location, 'w+')
        print >> yaml_file, yaml.dump(result, default_flow_style=False)
        yaml_file.close()
        log.info("Written new yaml file in " + location)



if __name__ == "__main__":

    cloudmesh_yaml = path_expand("~/.futuregrid/etc/cloudmesh.yaml")
    user_config = ConfigDict(filename="~/.futuregrid/me.yaml")
    t = cm_template(cloudmesh_yaml)

    banner("VARIABLES")
    s = set(t.variables())
    print ("\n".join(s))

    banner("GREP")
    s = t.grep()
    print ("\n".join(s))


    # banner("YAML FILE")
    # result = t.replace(kind="dict", values=user_config)
    # print yaml.dump(result, default_flow_style=False)
    # location = path_expand('~/.futuregrid/cloudmesh-new.yaml')
    # yaml_file = open(location, 'w+')
    # print >> yaml_file, yaml.dump(result, default_flow_style=False)
    # yaml_file.close()
    # print "Written new yaml file in " + location

    t.generate("~/.futuregrid/me.yaml",
               '~/.futuregrid/cloudmesh-new.yaml')

    # print t.replace(values=d)

#    if not t.complete():
#       print "ERROR: undefined variables"
#       print t.variables()



