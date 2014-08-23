cloudmesh command
=====================
Command to generate rc files from our cloudmesh configuration files.

Usage::

  cm config [-f FILE] [-o OUT] NAME [-]
  cm config list
  cm --version
  cm --help

This program generates form a YAML file containing the login
information for a cloud an rc file that can be used to later source
it. 

Example:
  we assume the yaml file has an entry india-openstack::

    cm config -o novarc india-openstack
    source novarc

  This will create a novarc file and than you can source it.::


     cm config ? -

   Presents a selction of cloud choices and writes the choice into a
   file called ~/.cloudmesh/novarc

Arguments::

  NAME name of the cloud

Options::

  -h --help            show this help message and exit
  -v --version         show version and exit
  -f NAME --file=NAME  the Name of the cloud to be specified, if ? a selection is presented
  -o OUT --out=OUT     writes the result in the specifide file
  -                    if data is written to a file it is also put out to stdout
    
