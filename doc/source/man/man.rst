Commands
======================================================================
EOF
----------------------------------------------------------------------

Command - EOF::

    Usage:
        EOF
    
    Action to be performed at the` end of a file. If true it terminates reating the file.
    

clear
----------------------------------------------------------------------

Command - clear::

    Usage:
        clear
    
    Clears the screen.

cloud
----------------------------------------------------------------------

Command - cloud::

    Usage:
           cloud --on | --off <name>
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
       --on     Activate the cloud
       --off    Deactivate the cloud
    
    

count
----------------------------------------------------------------------

Command - count::

    Usage:
           count flavors [CLOUD...] NOTIMPLEMENTED
           count servers [CLOUD...] NOTIMPLEMENTED
           count images [CLOUD...] NOTIMPLEMENTED
           count [CLOUD...] NOTIMPLEMENTED
    
    Arguments:
    
            CLOUD    the name of the cloud
    
    Options:
    
       -v       verbose mode
    
    Description:
    
      missing
    
      Seems this has not been implemented.
    
    

defaults
----------------------------------------------------------------------

Command - defaults::

    Usage:
           defaults clean
           defaults load
           defaults list [--json]
           defaults set variable value NOTIMPLEMENTED
           defaults variable  NOTIMPLEMENTED
           defaults format (json|table)  NOTIMPLEMENTED
    
    This manages the defaults associated with the user.
    You can load, list and clean defaults associated with a user and a cloud.
    The default parameters include index, prefix, flavor and image.
    
    Arguments:
    
      CLOUD          The name of Cloud - this has to be implemented
    
    Options:
    
       -j --json      json output
    
    Description:
    
      defaults set a hallo
    
         sets the variable a to the value hallo
         NOT YET IMPLEMENTED
    
      defaults a
    
         returns the value of the variable
         NOT YET IMPLEMENTED
    
      default format json
      default format table
    
         sets the default format how returns are printed. if set to json json is returned,
         if set to table a pretty table is printed
         NOT YET IMPLEMENTED
    

dot2
----------------------------------------------------------------------

Command - dot2::

    Usage:
           dot2 FILENAME FORMAT
    
    Export the data in cvs format to a file. Former cvs command
    
    Arguments:
        FILENAME   The filename
        FORMAT     the export format, pdf, png, ...
    
    

edit
----------------------------------------------------------------------

Command - edit::

    Usage:
            edit FILENAME
    
    Edits the file with the given name
    
    Arguments:
        FILENAME  the file to edit
    
    

exec
----------------------------------------------------------------------

Command - exec::

    Usage:
       exec FILENAME
    
    executes the command sin the file. See also the script command.
    
    Arguments:
      FILENAME   The name of the file
    
    

exp
----------------------------------------------------------------------

Command - exp::

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

Command - graphviz::

    Usage:
           graphviz FILENAME
    
    Export the data in cvs format to a file. Former cvs command
    
    Arguments:
        FILENAME   The filename
    
    

help
----------------------------------------------------------------------

Command - help::
List available commands with "help" or detailed help with "help cmd".

info
----------------------------------------------------------------------

Command - info::

    Usage:
           info
    
    Prints some internal information about the shell
    
    

init
----------------------------------------------------------------------

Command - init::

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

Command - keys::

    Usage:
           keys info [--json] [NAME]
           keys default NAME
           keys show NAME
    
    Manages the keys
    
    Arguments:
    
      NAME           The name of a key
    
    
    Options:
    
       -v --verbose     verbose mode
       -j --json        json output
    
    

list
----------------------------------------------------------------------

Command - list::

    Usage:
           list flavors [CLOUD]
           list servers [CLOUD]
           list images [CLOUD]
           list
    
           list NOTIMPLEMENTED flavors [CLOUD...]
           list NOTIMPLEMENTED servers [CLOUD...]
           list NOTIMPLEMENTED images [CLOUD...]
           list NOTIMPLEMENTED [CLOUD...]
    
    Arguments:
    
            CLOUD    the name of the cloud
    
    Options:
    
       -v       verbose mode
    
    Description:
    
       missing
    
       This should be similar to the count command, e.g. multiple clouds could be specified.
    
    

man
----------------------------------------------------------------------

Command - man::

    Usage:
           man [--noheader]
    
    Options:
           --norule   no rst header
    
    Prints out the help pages
    

open
----------------------------------------------------------------------

Command - open::

    Usage:
            open FILENAME
    
    ARGUMENTS:
        FILNAME  the file to open in the cwd if . is
                 specified. If file in in cwd
                 you must specify it with ./FILENAME
    
    Opens the given URL in a browser window.
    

pause
----------------------------------------------------------------------

Command - pause::

    Usage:
        pause [MESSAGE]
    
    Displays the specified text then waits for the user to press RETURN.
    
    Arguments:
       MESSAGE  message to be displayed
    

plugins
----------------------------------------------------------------------

Command - plugins::

    Usage:
        plugins
    
    activates the plugins.

project
----------------------------------------------------------------------

Command - project::

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

Command - py::

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

Command - q::

    Usage:
        quit
    
    Action to be performed whne quit is typed
    

quit
----------------------------------------------------------------------

Command - quit::

    Usage:
        quit
    
    Action to be performed whne quit is typed
    

rain
----------------------------------------------------------------------

Command - rain::

    Usage:
           rain info
           rain list NAME [IMAGE list]
           rain add HOSTLIST IMAGE [LABEL]
    
    Provisioning of the images on 
    
    Arguments:
    
      NAME           The name of the server
      IMAGE          The name of the image
      HOSTLIST       The names of hosts
    
    Options:
    
       -v       verbose mode
    
    Description:
    
      rain info
    
           provides information about the images and servers on
           which rain can be applied
    
      rain list india01
    
           list all images that can be provisioned on the server
           with the name india01
    
      rain add [india01-02] precise64.aaa precise64
    
           adding the
    
    

reg
----------------------------------------------------------------------

Command - reg::

    Usage:
      reg [options] NAME
    
    Arguments:
      NAME      Name of the cloud to be registered
    
    Options:
      -a --act      Activate the cloud to be registered
      -d --deact    Deactivate the cloud
    

rst
----------------------------------------------------------------------

Command - rst::

    Usage:
           rst COMMAND
    
    Prints out the comand for inclusion into rst
    
    Arguments:
      COMMAND    The name of the command
    
    

script
----------------------------------------------------------------------

Command - script::

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

Command - timer::

    Usage:
        timer (on|off)
    
    switches timers on and off not yet implemented
    

use
----------------------------------------------------------------------

Command - use::

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

Command - user::

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

Command - var::

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

Command - verbose::

    Usage:
        verbose (True | False)
    
    If set to True prints the command befor execution.
    In interactive mode you may want to set it to False.
    When using scripts we recommend to set it to True.
    
    The default is set to True
    

version
----------------------------------------------------------------------

Command - version::

    Usage:
       version
    
    Prints out the version number
    

vm
----------------------------------------------------------------------

Command - vm::

    Usage:
      vm create [--count=<count>] [--image=<imgName>] [--flavor=<FlavorId>] [--cloud=<CloudName>]
      vm delete [[--count=<count>] | [--name=<NAME>]] [--cloud=<CloudName>]
      vm cloud [--name=<NAME>]
      vm image [--name=<NAME>]
      vm flavor [--name=<NAME>]
      vm index [--index=<index>]
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
       --img=<imgName>                      Name of the image for VM
       -f <FlavorId> --flavor=<FlavorId>    Flavor Id for VM
    
