Commands
======================================================================
EOF
----------------------------------------------------------------------

Command - EOF::

    Usage:
        EOF
    
    Action to be performed at the` end of a file. If true it terminates reating the file.
    

banner
----------------------------------------------------------------------

Command - banner::

    Usage:
        banner [-c CHAR] [-n WIDTH] [-i INDENT] TEXT
    
    Arguments:
        TEXT   The text message from which to create the banner
        CHAR   The character for the frame. 
        WIDTH  Width of the banner
        INDENT indentation of the banner
    
    Options:
        -c CHAR   The character for the frame. [default: #]
        -n WIDTH  The width of the banner. [default: 70]
        -i INDENT  The width of the banner. [default: 0]            
    
    Prints a banner form a one line text message.
    

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
        cloud NOTIMPLEMENTED list
        cloud NOTIMPLEMENTED info [NAME|all]
        cloud NOTIMPLEMENTED NAME
        cloud NOTIMPLEMENTED select
        cloud NOTIMPLEMENTED --on | --off NAME
        cloud NOTIMPLEMENTED on NAME
        cloud NOTIMPLEMENTED off NAME
        cloud NOTIMPLEMENTED add [--format=FORMAT] CLOUD
    
    Manages the clouds
    
    Arguments:
    
      NAME           The name of a service or server
      JSON           A JSON
      CLOUD          The cloud to be added
    
    Options:
    
       -v       verbose mode
       --on     Activate the cloud
       --off    Deactivate the cloud
       --format=FORMAT  The format of the activation description.
                        [default: yaml]
    Description:
    
        cloud list
            Lists the cloud names
    
        cloud info [NAME]
            Provides the available information about the clouds
            and their status. A cloud can be activated or deactivated.
            If no name is specified the default cloud is used.
            If the name all is used, all clouds are displayed
    
        cloud NAME
            setst the cloud with the name to the default
    
        cloud select
            selects a cloud from the name of clouds
    
        cloud --on | --off NAME
        cloud on NAME
        cloud off NAME
            activates or deactivates a cloud with a given name
    
        cloud add [--format=FORMAT] CLOUD
            adds a cloud to the list of clouds.
            The format can either be `json` or `yaml`.
    

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
           defaults [list] [--json]
           defaults set variable value NOTIMPLEMENTED
           defaults variable  NOTIMPLEMENTED
           defaults format (json|table)  NOTIMPLEMENTED
    
    This manages the defaults associated with the user.
    You can load, list and clean defaults associated with
    a user and a cloud. The default parameters include
    index, prefix, flavor and image.
    
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
    
         sets the default format how returns are printed.
         if set to json json is returned,
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
    
    executes the commands in the file. See also the script command.
    
    Arguments:
      FILENAME   The name of the file
    
    

exp
----------------------------------------------------------------------

Command - exp::

    Usage:
           exp NOTIMPLEMENTED clean
           exp NOTIMPLEMENTED delete NAME
           exp NOTIMPLEMENTED create [NAME]
           exp NOTIMPLEMENTED info [NAME]
           exp NOTIMPLEMENTED cloud NAME
           exp NOTIMPLEMENTED image NAME
           exp NOTIMPLEMENTED flavour NAME
           exp NOTIMPLEMENTED index NAME
           exp NOTIMPLEMENTED count N
    
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
           info [--all]
    
    Options:
           --all  -a   more extensive information 
    
    Prints some internal information about the shell
    
    

init
----------------------------------------------------------------------

Command - init::

    Usage:
           init [--force] generate yaml
           init [--force] generate me
           init [--force] generate none
           init [--force] generate FILENAME
           init list [KIND] [--json]           
           init list clouds [--file=FILENAME] [--json]
           init inspect --file=FILENAME
           init fill --file=FILENAME [VALUES]
    
    Initializes cloudmesh from a yaml file
    
    Arguments:
       generate   generates a yaml file
       yaml       specifies if a yaml file is used for generation
                  the file is located at ~/.futuregrid/me.yaml
       me         same as yaml
    
       none       specifies if a yaml file is used for generation
                  the file is located at ~/.futuregrid/etc/none.yaml
       FILENAME   The filename to be generated or from which to read
                  information. 
       VALUES     yaml file with the velues to be sed in the FILENAME
       KIND       The kind of the yaml file.
    
    Options:
       --force  force mode does not ask. This may be dangerous as it
                overwrites the ~/.futuregrid/cloudmesh.yaml file
       --file=FILENAME  The file
       --json   make the output format json
       -v       verbose mode
    
    
    Description:
    
      init list [KIND] [--json]
         list the versions and types of the yaml files in the
         ~/.futuregrid and ~/.futuregrid/etc directories.
    
      init list clouds [--file=FILENAME]
         Lists the available clouds in the configuration yaml file.
    
      init inspect --file=FILENAME
         print the variables in the yaml template
    

inventory
----------------------------------------------------------------------

Command - inventory::

    Usage:
           inventory NOTIMPLEMENTED clean
           inventory NOTIMPLEMENTED create image DESCRIPTION
           inventory NOTIMPLEMENTED create server [dynamic] DESCRIPTION
           inventory NOTIMPLEMENTED create service [dynamic] DESCRIPTION
           inventory NOTIMPLEMENTED exists server NAME
           inventory NOTIMPLEMENTED exists service NAME
           inventory NOTIMPLEMENTED
           inventory NOTIMPLEMENTED print
           inventory NOTIMPLEMENTED info [CLUSTER] [SERVER] [v]
           inventory NOTIMPLEMENTED server NAME
           inventory NOTIMPLEMENTED service NAME
    
    Manages the inventory
    
        clean       cleans the inventory
        server      define servers
    
    Arguments:
    
      DESCRIPTION    The hostlist"i[009-011],i[001-002]"
    
      NAME           The name of a service or server
    
    
    Options:
    
       v       verbose mode
    
    

keys
----------------------------------------------------------------------

Command - keys::

    Usage:
           keys
           keys info [--json] [NAME]
           keys default NAME
    
    Manages the keys
    
    Arguments:
    
      NAME           The name of a key
    
    
    Options:
    
       -v --verbose     verbose mode
       -j --json        json output
    
    

label
----------------------------------------------------------------------

Command - label::

    Usage:
           label [--prefix=PREFIX] [--id=ID] [--width=WIDTH]
    
    A command to set the prefix and id for creating an automatic lable for VMs.
    Without paremeter it prints the currect label.
    
    Arguments:
    
      PREFIX     The prefix for the label
      ID         The start ID which is an integer
      WIDTH      The width of the ID in teh label, padded with 0
    
    Options:
    
       -v       verbose mode
    
    

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
    
       This should be similar to the count command,
       e.g. multiple clouds could be specified.
    
    

login
----------------------------------------------------------------------

Command - login::

    Usage:
       login
    

man
----------------------------------------------------------------------

Command - man::

    Usage:
           man COMMAND
           man [--noheader]
    
    Options:
           --norule   no rst header
    
    Arguments:
           COMMAND   the command to be printed 
    
    Description:
    
      man 
            Prints out the help pages
    
      man COMMAND
            Prints out the help page for a specific command
    
    
    

metric
----------------------------------------------------------------------

Command - metric::

        Usage:
    	cm-metric -h | --help
            cm-metric --version
            cm-metric [CLOUD]
                      [-s START|--start=START] 
                      [-e END|--end=END] 
                      [-u USER|--user=USER] 
                      [-m METRIC|--metric=METRIC]
                      [-p PERIOD|--period=PERIOD] 
                      [-c CLUSTER]
    
       Options:
           -h                   help message
           -m, --metric METRIC  use either user|vm|runtime in METRIC
           -u, --user USER      use username in USER
           -s, --start_date START    use YYYYMMDD datetime in START
           -e, --end_date END        use YYYYMMDD datetime in END
           -c, --host HOST      use host name e.g. india, sierra, etc
           -p, --period PERIOD  use either month|day|week (TBD)
    
        Arguments:
            CLOUD               Name of the IaaS cloud e.g. openstack, nimbus, Eucalyptus
            HOST                Name of host e.g. india, sierra, foxtrot,
                                hotel, alamo, lima
    
        Description:
           metric command provides usage data with filter options.
    
        Result:
          The result of the method is a datastructure specified in a given format.
          If no format is specified, we return a JSON string of the following format:
    
             {
                "start_date"    :   start date of search    (datetime),
                "end_date"      :   end date of search      (datetime),
                "ownerid"       :   portal user id          (str),
                "metric"        :   selected metric name    (str),
                "period"        :   monthly, weekly, daily  (str),
                "clouds"        :   set of clouds           (list)
                [
                   {"service"     :   cloud service name  (str),
                    "hostname"     :   hostname (str),
                    "stats"        :   value (int) }
                    ...
                ]
             }
    
        Examples:
            $ cm-metric openstack -c india -u hrlee        
            - Get user statistics
    
    

open
----------------------------------------------------------------------

Command - open::

    Usage:
            open FILENAME
    
    ARGUMENTS:
        FILENAME  the file to open in the cwd if . is
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
           project NOTIMPLEMENTED json info [NAME]
           project NOTIMPLEMENTED info [NAME]
           project NOTIMPLEMENTED members
           project NOTIMPLEMENTED default NAME
    
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
        rain -h | --help
        rain --version
        rain admin add [LABEL] --file=FILE
        rain admin baremetals
        rain admin on HOSTS
        rain admin off HOSTS
        rain admin [-i] delete HOSTS
        rain admin [-i] rm HOSTS
        rain admin list users [--merge]
        rain admin list projects [--merge]
        rain admin list roles
        rain admin list hosts [--user=USERS|--project=PROJECTS|--role=ROLE]
                              [--start=TIME_START]
                              [--end=TIME_END]
                              [--format=FORMAT]
        rain admin policy [--user=USERS|--project=PROJECTS|--role=ROLE]
                          (-l HOSTS|-n COUNT)
                          [--start=TIME_START]
                          [--end=TIME_END]
        rain list [--project=PROJECTS] [HOSTS]    
        rain list hosts [--start=TIME_START]
                        [--end=TIME_END]
                        [--format=FORMAT]
        rain status [--short|--summary][--kind=KIND] [HOSTS]
        rain provision --profile=PROFILE HOSTS
        rain provision list (--distro=DISTRO|--kickstart=KICKSTART)
        rain provision --distro=DITRO --kickstart=KICKSTART HOSTS
        rain provision add (--distro=URL|--kickstart=KICk_CONTENT) NAME
        rain provision power [--off] HOSTS
        rain provision monitor HOSTS
    
    Arguments:
        HOSTS     the list of hosts passed
        LABEL     the label of a host
        COUNT     the count of the bare metal provisioned hosts
        KIND      the kind
    
    Options:
        -n COUNT     count of teh bare metal hosts to be provisined
        -p PROJECTS  --projects=PROJECTS  
        -u USERS     --user=USERS        Specify users
        -f FILE, --file=FILE  file to be specified
        -i           interactive mode adds a yes/no 
                     question for each host specified
        --role=ROLE            Specify predefined role
        --start=TIME_START     Start time of the reservation, in 
                               YYYY/MM/DD HH:MM:SS format. [default: current_time]
        --end=TIME_END         End time of the reservation, in 
                               YYYY/MM/DD HH:MM:SS format. In addition a duration
                               can be specified if the + sign is the first sign.
                               The duration will than be added to
                               the start time. [default: +1d]
        --kind=KIND            Format of the output -png, jpg, pdf. [default:png]
        --format=FORMAT        Format of the output json, cfg. [default:json]
    
    
    

reg
----------------------------------------------------------------------

Command - reg::

    Usage:
      reg NOTIMPLEMENTED [options] NAME
    
    Arguments:
      NAME      Name of the cloud to be registered
    
    Options:
      -a --act      Activate the cloud to be registered
      -d --deact    Deactivate the cloud
    

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
    
    

storm
----------------------------------------------------------------------

Command - storm::

    Usage:
      storm list
      storm ID
      storm register ID [--kind=KIND] [ARGUMENTS...]
    
    Arguments:
    
      list       list the available high level services to be provisioned.
      ID         list the user with the given ID
      ARGUMENTS  The name of the arguments that need to be passed
    
    Options:
      --kind=KIND  the kind of the storm. It can be chef, puppet, or other
                   frameworks. At this time we will focus on chef [default: chef].
    
       -v          verbose mode
    
    Description:
    
      Command to invoce a provisioning of high level services such as
      provided with chef, puppet, or other high level DevOps Tools. If
      needed the machines can be provisioned prior to a storm with
      rain. Together this forms a rain storm.
    
    

timer
----------------------------------------------------------------------

Command - timer::

    Usage:
        timer on
        timer off            
        timer list
        timer start NAME
        timer stop NAME
        timer resume NAME
        timer reset [NAME]
    
    Description (NOT IMPLEMENTED YET):
    
         timer on | off
             switches timers on and off not yet implemented.
             If the timer is on each command will be timed and its
             time is printed after the command. Please note that
             background command times are not added.
    
        timer list
            list all timers
    
        timer start NAME
            starts the timer with the name. A start resets the timer to 0.
    
        timer stop NAME
            stops the timer
    
        timer resume NAME
            resumes the timer
    
        timer reset NAME
            resets the named timer to 0. If no name is specified all
            timers are reset
    
        Implementation note: we have a stopwatch in cloudmesh,
                             that we could copy into cmd3
    

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
           user info [ID]
    
    Administrative command to lists the users from LDAP
    
    Arguments:
    
      list       list the users
      ID         list the user with the given ID
    
    Options:
    
       -v       verbose mode
    
    

var
----------------------------------------------------------------------

Command - var::

    Usage:
        var list 
        var delete NAMES
        var NAME=VALUE
        var NAME
    
    Arguments:
        NAME    Name of the variable
        NAMES   Names of the variable seperated by spaces
        VALUE   VALUE to be assigned
    
    special vars date and time are defined
    

verbose
----------------------------------------------------------------------

Command - verbose::

    Usage:
        verbose (True | False)
        verbose
    
    If set to True prints the command befor execution.
    In interactive mode you may want to set it to False.
    When using scripts we recommend to set it to True.
    
    The default is set to False
    
    If verbose is specified without parameter the flag is
    toggled.
    
    

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
      vm create [--count=<count>]
                [--image=<imgName>]
                [--flavor=<FlavorId>]
                [--cloud=<CloudName>]
      vm delete [[--count=<count>] | [--name=<NAME>]]
                [--cloud=<CloudName>]
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
    
