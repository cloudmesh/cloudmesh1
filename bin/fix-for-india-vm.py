#! /usr/bin/env python

#
# fix-for-india-vm -f
#
#    changes the ~/.cloudmesh/cloudmesh_server.yaml
import sys
from cloudmesh.config.cm_config import cm_config
from cloudmesh_install import config_file

filename = config_file("/cloudmesh_server.yaml")

with open(filename, 'r') as f:
    content = f.read()

replacements = {'browser: True': 'browser: False',
                'host: 127.0.0.1': 'host: 0.0.0.0'}

for _old, _new in replacements.iteritems():
    content = content.replace(_old, _new)

if sys.argv[1] == "-f":
    outfile = open(filename, 'w')
    outfile.write(content)
    outfile.close()
elif sys.argv[1] == "-v":
    print content


