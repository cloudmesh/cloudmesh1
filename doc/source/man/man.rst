
Commands
======================================================================
EOF
----------------------------------------------------------------------

Commnad - EOF::

    Usage:
        EOF
    
    Action to be performed at the` end of a file. If true it terminates reating the file.
    

clear
----------------------------------------------------------------------

Commnad - clear::

    Usage:
        clear
    
    Clears the screen.

cloud
----------------------------------------------------------------------

Commnad - cloud::

    Usage:
           cloud
           cloud set
           cloud NAME
           cloud info [NAME]
           cloud on NAME
           cloud off NAME
    
    
    Manages the cloud
    
    Arguments:
    
      NAME           The name of a service or server
    
    
    Options:
    
       -v       verbose mode
    
    

count
----------------------------------------------------------------------

Commnad - count::

    Usage:
           count flavors [CLOUD...]
           count servers [CLOUD...]
           count images [CLOUD...]
           count [CLOUD...]
    
    Arguments:
    
            CLOUD    the name of the cloud
    
    Options:
    
       -v       verbose mode
    
    

defaults
----------------------------------------------------------------------

Commnad - defaults::

    Usage:
           defaults [-v] clean
           defaults [-v] load [CLOUD]
           defaults [options] info
           defaults list [options] [CLOUD]
    
    Manages the defaults
    
    Arguments:
    
      NAME           The name of a service or server
      N              The number of defaultss to be started
      CLOUD          The name of Cloud
    
    Options:
    
       -v             verbose mode
       -j --json      json output
    
    

dot2
----------------------------------------------------------------------

Commnad - dot2::

    Usage:
           dot2 FILENAME FORMAT
    
    Export the data in cvs format to a file. Former cvs command
    
    Arguments:
        FILENAME   The filename
        FORMAT     the export format, pdf, png, ...
    
    

edit
----------------------------------------------------------------------

Commnad - edit::
Usage:
                 edit FILENAME
    
            Arguments:
                FILENAME  the file to edit
    
            Edits a file.

exec
----------------------------------------------------------------------

Commnad - exec::
Execute script file

exp
----------------------------------------------------------------------

Commnad - exp::

    Usage:
           exp clean
           exp delete NAME
           exp create [NAME]
           exp info [NAME]
           exp cloud NAME
           exp image NAME
           exp flavour NAME
           exp index NAME
           exp count N
    
    Manages the vm
    
    Arguments:
    
      NAME           The name of a service or server
      N              The number of VMs to be started          
    
    
    Options:
    
       -v       verbose mode
    
    

graphviz
----------------------------------------------------------------------

Commnad - graphviz::

    Usage:
           graphviz FILENAME
    
    Export the data in cvs format to a file. Former cvs command
    
    Arguments:
        FILENAME   The filename
    
    

help
----------------------------------------------------------------------

Commnad - help::
List available commands with "help" or detailed help with "help cmd".

info
----------------------------------------------------------------------

Commnad - info::

    Usage:
           info
    
    Prints some internal information about the shell
    
    

init
----------------------------------------------------------------------

Commnad - init::

    Usage:
           init [force] generate yaml
           init [force] generate me
           init [force] generate none
           init [force] generate FILENAME
    
    Initializes cloudmesh from a yaml file
    
    Arguments:
    
      generate   generates a yaml file 
    
      yaml       specifies if a yaml file is used for generation
                 the file is located at ~/.futuregrid/me.yaml
    
      me         same as yaml
    
      none       specifies if a yaml file is used for generation
                 the file is located at ~/.futuregrid/etc/none.yaml
    
      force      force mode does not ask. This may be dangerous as it
                 overwrites the ~/.futuregrid/cloudmesh.yaml file
    
    Options:
    
       -v       verbose mode
    
    

keys
----------------------------------------------------------------------

Commnad - keys::

    Usage:
           keys info [NAME] 
           keys default 
           keys json info [NAME] 
    
    Manages the keys
    
    Arguments:
    
      NAME           The name of a service or server
    
    
    Options:
    
       -v       verbose mode
    
    

list
----------------------------------------------------------------------

Commnad - list::

    Usage:
           list flavors [CLOUD...]
           list servers [CLOUD...]
           list images [CLOUD...]
           list [CLOUD...]
    
    Arguments:
    
            CLOUD    the name of the cloud
    
    Options:
    
       -v       verbose mode
    
    

man
----------------------------------------------------------------------

Commnad - man::

    Usage:
           man [--noheader]
    
    Options:
           --norule   no rst header
    
    Prints out the help pages
    

open
----------------------------------------------------------------------

Commnad - open::
Usage:
                    open FILENAME
    
            ARGUMENTS:
                FILNAME  the file to open in the cwd if . is
                         specified. If file in in cwd
                         you must specify it with ./FILENAME
    
            Opens the given URL in a browser window.
    

pause
----------------------------------------------------------------------

Commnad - pause::

    Usage:
        pause [MESSAGE]
    
    Displays the specified text then waits for the user to press RETURN.
    
    Arguments:
       MESSAGE  message to be displayed
    

plugins
----------------------------------------------------------------------

Commnad - plugins::

    Ussage:
        plugins
    
    activates the plugins.

project
----------------------------------------------------------------------

Commnad - project::

    Usage:
           project json info [NAME] 
           project info [NAME] 
           project members
           project default NAME
    
    Manages the project
    
    Arguments:
    
      NAME           The name of a service or server
    
    
    Options:
    
       -v       verbose mode
    
    

py
----------------------------------------------------------------------

Commnad - py::

    Usage:
        py
        py COMMAND
    
    Arguments:
        COMMAND   the command to be executed
    
    The command without a parameter will be extecuted and the
    interactive python mode is entered. The python mode can be
    ended with ``Ctrl-D`` (Unix) / ``Ctrl-Z`` (Windows),
    ``quit()``,'`exit()``. Non-python commands can be issued with
    ``cmd("your command")``.  If the python code is located in an
    external file it can be run with ``run("filename.py")``.
    
    In case a COMMAND is provided it will be executed and the
    python interpreter will return to the commandshell.
    
    This code is copied from Cmd2.
    

q
----------------------------------------------------------------------

Commnad - q::

    Usage:
        quit
    
    Action to be performed whne quit is typed
    

quit
----------------------------------------------------------------------

Commnad - quit::

    Usage:
        quit
    
    Action to be performed whne quit is typed
    

reg
----------------------------------------------------------------------

Commnad - reg::

    Usage:
      reg NAME
    
    Arguments:
      NAME      Name of the cloud to be registered
    

rst
----------------------------------------------------------------------

Commnad - rst::

    Usage:
           rst COMMAND
    
    Prints out the comand for inclusion into rst
    
    Arguments:
      COMMAND    The name of the command
    
    

script
----------------------------------------------------------------------

Commnad - script::

    Usage:
           script
           script load
           script load LABEL FILENAME
           script load REGEXP
           script list
           script LABEL
    
    Arguments:
           load       indicates that we try to do actions toload files.
                      Without parameters, loads scripts from default locations
            NAME      specifies a label for a script
            LABEL     a conveninet LABEL, it must be unique
            FILENAME  the filename in which the script is located
            REGEXP    Not supported yet.
                      If specified looks for files identified by the REGEXP.
    
    NOT SUPPORTED YET
    
       script load LABEL FILENAME
       script load FILENAME
       script load REGEXP
    
    Process FILE and optionally apply some options
    
    

timer
----------------------------------------------------------------------

Commnad - timer::

    Ussage:
        timer (on|off)
    
    switches timers on and off not yet implemented
    

use
----------------------------------------------------------------------

Commnad - use::

    USAGE:
    
        use list           lists the available scopes
    
        use add SCOPE      adds a scope <scope>
    
        use delete SCOPE   removes the <scope>
    
        use                without parameters allows an
                           interactive selection
    
    DESCRIPTION
       often we have to type in a command multiple times. To save
       us typng the name of the commonad, we have defined a simple
       scope thatcan be activated with the use command
    
    ARGUMENTS:
        list         list the available scopes
        add          add a scope with a name
        delete       delete a named scope
        use          activate a scope
    
    

user
----------------------------------------------------------------------

Commnad - user::

    Usage:
           user list
           user ID
           user ID me
           user ID yaml
           user ID ldap
           user ID new FORMAT [dict|yaml]
    
    Administrative command to lists the users from LDAP 
    
    Arguments:
    
      list       list the users
      ID         list the user with the given ID
      me         specifies to generate the me related yaml file
      yaml       specifie to generate the cloudmesh.yaml file
      ldap       get the specifie to generate the cloudmesh.yaml file
      FORMAT     either me or cloudmesh
      OUTPUT     either yaml or dict 
    
    Options:
    
       -v       verbose mode
    
    

var
----------------------------------------------------------------------

Commnad - var::

    Usage:
        var list | var
        var delete NAME
        var NAME=VALUE
    
    Arguments:
        NAME    Name of the variable
        VALUE   VALUE to be assigned
    
    special vars date and time are defined
    

verbose
----------------------------------------------------------------------

Commnad - verbose::

    Usage:
        verbose (True | False)
    
    If set to True prints the command befor execution.
    In interactive mode you may want to set it to False.
    When using scripts we recommend to set it to True.
    
    The default is set to True
    

version
----------------------------------------------------------------------

Commnad - version::

    Usage:
       version
    
    Prints out the version number
    

vm
----------------------------------------------------------------------

Commnad - vm::

    Usage:
      vm create [--count=<count>] [--image=<imgName>] [--flavor=<FlavorId>] [--cloud=<CloudName>]
      vm delete [[--count=<count>] | [--name=<NAME>]] [--cloud=<CloudName>]
      vm cloud [--name=<NAME>]
      vm image [--name=<NAME>]
      vm flavor [--name=<NAME>]
      vm index [--name=<NAME>]
      vm info [--verbose | --json] [--name=<NAME>]
      vm list [--verbose | --json] [--cloud=<CloudName>]
    
    Arguments:
      NAME name of the VM
    
    Options:
       -v --verbose                         verbose mode
       -j --json                            json output
       -x <count> --count=<count>           number of VMs
       -n <NAME> --name=<NAME>              Name of the VM
       -c <CloudName> --cloud=<CloudName>   Name of the Cloud
       -i <index> --index=<index>           Index for default VM Name
       -img <imgName> --image=<imgName>     Name of the image for VM
       -f <FlavorId> --flavor=<FlavorId>    Flavor Id for VM
    

