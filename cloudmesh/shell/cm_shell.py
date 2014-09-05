#! /usr/bin/env python
"""cm config
------------
Command to generate rc files from our cloudmesh configuration files.

Usage:
  cm defaults [FILENAME] - stores also alias
  cm defaults clear - clears the defaults

  cm set PREFIX INDEX - automatic index index must be of the form 00001  from which to start naming vms. 0 indicate how many leading 0s in the index.
  cm set project [PROJECT] - set functions will be interactive if no param is given
  cm set cloud [CLOUD]
  cm set image [IMAGE] [CLOUD]
  cm set flavor [FLAVOR] [CLOUD]

  cm list [CLOUD | all]
  cm list servers [CLOUD]
  cm list images [CLOUD]
  cm list flavors [CLOUD]
  cm list config [CLOUD]

  cm find REGEX - finds the fm that match the condition  (cloud="name", ...)

  cm start COUNT [IMAGE] [FLAVOR] [CLOUD]
  cm stop [INDEX]
  cm delete [INDEX]

  cm info [CLOUD]
  cm info [NAME] - info of the vom with name
  cm info [INDEX] - info about the vm with the given index

  cm referesh [all | CLOUD] [images | servers | flavors]

  cm alias ALIAS=STRING

  cm rain IMAGE CLOUD

  cm usage START END [CLOUD] [PROJECT]

  cm --version
  cm --help


  cm config ... take from cm_cli

"""

if __name__ == '__main__':

    print "not yet implemented"
