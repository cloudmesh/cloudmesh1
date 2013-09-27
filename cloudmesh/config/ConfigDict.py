from cloudmesh.util.util import path_expand
from cloudmesh.util.logger import LOGGER
from cloudmesh.util.config import read_yaml_config
from collections import OrderedDict
import simplejson
from pprint import pprint
import json
import os
import stat
import sys
import copy
from cloudmesh.user.cm_template import cm_template

log = LOGGER(__file__)
package_dir = os.path.dirname(os.path.abspath(__file__))

class OrderedJsonEncoder(simplejson.JSONEncoder):
    indent = 4
    def encode(self, o, depth=0):
        if isinstance(o, OrderedDict):
            return "{" + (",\n ").join([ self.encode(k) + ":" + self.encode(v, depth + 1) for (k, v) in o.iteritems() ]) + "}\n"
        else:
            return simplejson.JSONEncoder.encode(self, o)

def custom_print(data_structure, indent):
    for key, value in data_structure.items():
        print "\n%s%s:" % ('    ' * indent, str(key)),
        if isinstance(value, OrderedDict):
            custom_print(value, indent + 1)
        elif isinstance(value, dict):
            custom_print(value, indent + 1)
        else:
            print "%s" % (str(value)),

class ConfigDict (OrderedDict):

    def _set_filename(self, filename):
        self['filename'] = kwargs['filename']
        self['location'] = path_expand(self.filename)

    def __init__(self, *args, **kwargs) :
        OrderedDict.__init__(self, *args, **kwargs)
        if 'filename' in kwargs:
            self._set_filename(kwargs['filename'])
        else:
            log.error("filename not specified")
        self.load(self['location'])

    def read(self, filename):
        """does the same as load"""
        self.load(filename)

    def load(self, filename):
        self._set_filename(filename)
        d = OrderedDict(read_yaml_config (self['location'], check=True))
        self.update(d)

    def write(self, filename=None):
        """write the dict"""

        fpath = filename or self.filename
        f = os.open(fpath, os.O_CREAT | os.O_TRUNC |
                    os.O_WRONLY, stat.S_IRUSR | stat.S_IWUSR)
        os.write(f, self)
        os.close(f)

    def error_keys_not_found(self, keys):
        log.error("Filename: {0}".format(self['location']))
        log.error("Key '{0}' does not exist".format('.'.join(keys)))
        indent = ""
        last_index = len(keys) - 1
        for i, k in enumerate(keys):
            if i == last_index:
                log.error(indent + k + ": <- this value is missing")
            else:
                log.error(indent + k + ":")
            indent = indent + "    "

    def __str__(self):
        return self.json()


    def json(self):
        return json.dumps(self, indent=4)

    def dump(self):
        orderedPrinter = OrderedJsonEncoder()
        return orderedPrinter.encode(self)

    def pprint(self):
        print custom_print(self, 4)

    """
    def __getitem__(self, *mykeys):        
        try:
            item = self.get(mykeys[0])
        except:
            self._notify_of_error(mykeys)
            sys.exit()
        return item
    """

    def get(self, *keys):
        """
        returns the dict of the information as read from the yaml file. To
        access the file safely, you can use the keys in the order of the access.
        Example: get("provisiner","policy") will return the value of
        config["provisiner"]["policy"] from the yaml file if it does not exists
        an error will be printing that the value does not exists and we exit.
        Alternatively you can use the . notation e.g. get("provisiner.policy")
        """
        if keys is None:
            return self

        if "." in keys[0]:
            keys = keys[0].split('.')
        element = self
        for v in keys:
            try:
               element = element[v]
            except:
                self.error_keys_not_found(keys)
                sys.exit()
        return element

if __name__ == "__main__":
    config = ConfigDict({"a":"1", "b" : {"c": 3}}, filename="~/.futuregrid/cloudmesh_server.yaml")

    print "PPRINT"
    print 70 * "="
    pprint(config)

    print "PRINT"
    print 70 * "="
    print config.pprint()
    print config.json()

    print 70 * "="
    print "A =", config["a"]
    print "mongo.path =", config["mongo"]["path"]
    print "mongo.path GET =", config.get("mongo.path")
    print "mongo.path GET =", config.get("mongo.path.wrong")


    print "get A =", config.get("a")

    print "mongo.path.wrong =", config["mongo"]["path"]["wrong"]
    # print config["dummy"]
    # config["x"] = "2"
    # print config["x"]
    # print config.x



