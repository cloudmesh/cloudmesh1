Commands
======================================================================
EOF
----------------------------------------------------------------------

Command - EOF::

    Usage:
        EOF
    
    Command to the shell to terminate reading a script.
    

admin
----------------------------------------------------------------------

Command - admin::

    
    Usage:
      admin password reset
      admin server start
      admin server stop
      admin server status
      admin mongo start
      admin mongo stop
      admin mongo status
      admin mongo password
      admin celery start
      admin celery stop
      admin celery status
      admin rabbitmq status
      admin rabbitmq start
      admin rabbitmq stop
      admin version
    
    Options:
    
    
    Description:
        admin password reset
           reset portal password
    

banner
----------------------------------------------------------------------

Command - banner::

    Usage:
        banner [-c CHAR] [-n WIDTH] [-i INDENT] [-r COLOR] TEXT
    
    Arguments:
        TEXT   The text message from which to create the banner
        CHAR   The character for the frame. 
        WIDTH  Width of the banner
        INDENT indentation of the banner
        COLOR  the color
    
    Options:
        -c CHAR   The character for the frame. [default: #]
        -n WIDTH  The width of the banner. [default: 70]
        -i INDENT  The width of the banner. [default: 0]            
        -r COLOR  The color of the banner. [default: BLACK]
    
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
        cloud [list] [--column=COLUMN] [--format=FORMAT]
        cloud info [CLOUD|--all] [--format=FORMAT]
        cloud alias NAME [CLOUD]
        cloud select [CLOUD]
        cloud on [CLOUD]
        cloud off [CLOUD]
        cloud add <cloudYAMLfile> [--force]
        cloud remove [CLOUD|--all]
        cloud default [CLOUD|--all]
        cloud set flavor [CLOUD] [--name=NAME|--id=ID]
        cloud set image [CLOUD] [--name=NAME|--id=ID]
    
    Arguments:
    
      CLOUD                  the name of a cloud
      <cloudYAMLfile>        a yaml file (with full file path) containing
                             cloud information
      NAME                   name for a cloud (or flavor and image)
    
    Options:
    
       --column=COLUMN       specify what information to display in
                             the columns of the list command. For
                             example, --column=active,label prints the
                             columns active and label. Available
                             columns are active, label, host,
                             type/version, type, heading, user,
                             credentials, defaults (all to display all,
                             semiall to display all except credentials
                             and defaults)
    
       --format=FORMAT       output format: table, json, csv
    
       --all                 display all available columns
    
       --force               if same cloud exists in database, it will be
                             overwritten
    
       --name=NAME           provide flavor or image name
    
       --id=ID               provide flavor or image id
    
    
    Description:
    
        The cloud command allows easy management of clouds in the
        command shell. The following subcommands exist:
    
        cloud [list] [--column=COLUMN] [--json|--table]
            lists the stored clouds, optionally, specify columns for more
            cloud information. For example, --column=active,label
    
        cloud info [CLOUD|--all] [--json|--table]
            provides the available information about the cloud in dict
            format
            options: specify CLOUD to display it, --all to display all,
                     otherwise selected cloud will be used
    
        cloud alias NAME [CLOUD]
            sets a new name for a cloud
            options: CLOUD is the original label of the cloud, if
                     it is not specified the default cloud is used.
    
    
        cloud select [CLOUD]
            selects a cloud to work with from a list of clouds.If the cloud 
            is not specified, it asks for the cloud interactively
    
        cloud on [CLOUD]
        cloud off [CLOUD]
            activates or deactivates a cloud. if CLOUD is not
            given, the default cloud will be used.
    
    
        cloud add <cloudYAMLfile> [--force]
            adds the cloud information to database that is
            specified in the <cloudYAMLfile>. This file is a yaml. You
            need to specify the full path. Inside the yaml, a
            cloud is specified as follows:
    
            cloudmesh:
               clouds:
                 cloud1: ...
                 cloud2: ...
    
            For examples on how to specify the clouds, please see
            cloudmesh.yaml
    
            options: --force. By default, existing cloud in
                     database cannot be overwirtten, the --force
                     allows overwriting the database values.
    
        cloud remove [CLOUD|--all]
            remove a cloud from the database, The default cloud is
            used if CLOUD is not specified.
            This command should be used with caution. It is also
            possible to remove all clouds with the option --all
    
        cloud default [CLOUD|--all]
    
            show default settings of a cloud, --all to show all clouds
    
        cloud set flavor [CLOUD] [--name=NAME|--id=ID]
    
            sets the default flavor for a cloud. If the cloud is
            not specified, it used the default cloud.
    
        cloud set image [CLOUD] [--name=NAME|--id=ID]
    
            sets the default flavor for a cloud. If the cloud is
            not specified, it used the default cloud.
    
    

cluster
----------------------------------------------------------------------

Command - cluster::

    Usage:
        cluster list [--format=FORMAT]
        cluster create <name>
                       [--count=<count>]
                       [--ln=<LoginName>]
                       [--cloud=<CloudName>]
                       [--image=<imgName>|--imageid=<imgId>]
                       [--flavor=<flavorName>|--flavorid=<flavorId>]
                       [--force]
        cluster show <name> 
                     [--format=FORMAT] 
                     [--column=COLUMN]
                     [--detail]
        cluster remove <name> 
                       [--grouponly]
    
    Description:
        Cluster Management
    
        cluster list
            list the clusters
    
        cluster create <name> --count=<count> --ln=<LoginName> [options...]
            Start a cluster of VMs, and each of them can log into all others.
            CAUTION: you sould do some default setting before using this command:
            1. select cloud to work on, e.g. cloud select india
            2. activate the cloud, e.g. cloud on india
            3. set the default key to start VMs, e.g. key default [NAME]
            4. set the start name of VMs, which is prefix and index, e.g. label --prefix=test --id=1
            5. set image of VMs, e.g. default image
            6. set flavor of VMs, e.g. default flavor
            Also, it is better to choose a unused group name
    
        cluster show <name>
            show the detailed information about the cluster VMs
    
        cluster remove <name> [--grouponly]
            remove the cluster and its VMs, if you want to remove the cluster(group name)
            without removing the VMs, use --grouponly flag
    
    Arguments:
        <name>        cluster name or group name
    
    Options:
        --count=<count>            give the number of VMs to add into the cluster
        --ln=<LoginName>           give a login name for the VMs, e.g. ubuntu
        --cloud=<CloudName>        give a cloud to work on
        --flavor=<flavorName>      give the name of the flavor
        --flavorid=<flavorId>      give the id of the flavor
        --image=<imgName>          give the name of the image
        --imageid=<imgId>          give the id of the image
        --force                    if a group exists and there are VMs in it, the program will
                                   ask user to proceed or not, use this flag to respond yes as 
                                   default(if there are VMs in the group before creating this 
                                   cluster, the program will include the exist VMs into the cluster)
        --grouponly                remove the group only without removing the VMs, otherwise 
                                   cluster remove command will remove all the VMs of this cluster
        FORMAT                     output format: table, json, csv
        COLUMN                     customize what information to display, for example:
                                   --column=status,addresses prints the columns status
                                   and addresses
        --detail                   for table print format, a brief version 
                                   is used as default, use this flag to print
                                   detailed table
    
    

color
----------------------------------------------------------------------

Command - color::

    Usage:
        color on
        color off
        color
    
        Turns the shell color printing on or off
    
    Description:
    
        color on   switched the color on
    
        color off  switches the color off
    
        color      without parameters prints a test to display
                   the various colored mesages. It is intended
                   as a test to see if your terminal supports
                   colors.
    
    

debug
----------------------------------------------------------------------

Command - debug::

    Usage:
          debug on
          debug off
    
          Turns the debug log level on and off.
    

default
----------------------------------------------------------------------

Command - default::

    Usage:
        default [--column=COLUMN] [--format=FORMAT]
        default cloud [VALUE]
        default format [VALUE]
        default key [VALUE]
        default flavor [CLOUD] [--name=NAME|--id=ID]
        default image [CLOUD] [--name=NAME|--id=ID]
        default list refresh [--on|--off]
    
    Arguments:
    
        VALUE    provide a value to update default setting
        CLOUD    provide a cloud name to work with, if not
                 specified, the default cloud or a selected
                 cloud will be used
    
    Options:
    
        --column=COLUMN  specify what information to display.
                         The columns are specified as a comma
                         separated list. For example: cloud,format
        --format=FORMAT  output format: table, json, csv
        --name=NAME      provide flavor or image name
        --id=ID          provide flavor or image id
        --on             turn on
        --off            turn off
    
    Description:
    
        default [--column=COLUMN] [--format=FORMAT]
            print user defaults settings
    
        default cloud [VALUE]
            print or change (if VALUE provided) default cloud. To set
            a cloud as default, it must be registered and active (to
            list clouds: cloud [list]; to activate a cloud: cloud on
            [CLOUD])
    
        default format [VALUE]
            print or change(if VALUE provided) default print format,
            available formats are table, json, csv
    
        default key [VALUE]
            print or change (if VALUE provided) default key.
    
        default flavor [CLOUD] [--name=NAME|--id=ID]
            set default flavor for a cloud, same as command:
    
                cloud set flavor [CLOUD] [--name=NAME|--id=ID]
    
            (to check a cloud's default settings:
             cloud default [CLOUD|--all])
    
        default image [CLOUD] [--name=NAME|--id=ID]
            set default image for a cloud, same as command:
    
             cloud set image [CLOUD] [--name=NAME|--id=ID]
    
            (to check a cloud's default settings:
             cloud default [CLOUD|--all])
    
        default list refresh [--on|--off]
            set the default behaviour of the list commands, if the default
            value is on, then the program will always refresh before listing
    
    

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
    
    

flavor
----------------------------------------------------------------------

Command - flavor::

     Usage:
         flavor
         flavor CLOUD... [--refresh]
         flavor -h | --help
         flavor --version
    
    Options:
        -h                   help message
        --refresh            refresh flavors of IaaS
    
     Arguments:
         CLOUD    Name of the IaaS cloud e.g. india_openstack_grizzly.
    
     Description:
        flavor command provides list of available flavors. Flavor describes
        virtual hardware configurations such as size of memory, disk, cpu cores.
    
     Result:
    
     Examples:
         $ flavor india_openstack_grizzly
    
    

graphviz
----------------------------------------------------------------------

Command - graphviz::

    Usage:
           graphviz FILENAME
    
    Export the data in cvs format to a file. Former cvs command
    
    Arguments:
        FILENAME   The filename
    
    

group
----------------------------------------------------------------------

Command - group::

    Usage:
        group list [--format=FORMAT]
        group create NAME
        group remove NAME
        group add item NAME TYPE VALUE
        group remove item NAME TYPE VALUE
        group show NAME [TYPE] [--format=FORMAT]
    
    Arguments:
    
        NAME    name of the group
        TYPE    type of the item in the group, e.g. vm 
        VALUE   value of item to add, e.g. vm name
    
    Options:
    
        -v               verbose mode
        --format=FORMAT  output format: table, json, csv
    
    Description:
    
       group list           lists the groups
       group create         creates a new group
       group remove         removes a group
       group add item       addes an item of a type to a group
       group remove item    removes an item of a type from a group
       group show           lists items of a group
    
    Examples:
        group add item sample vm samplevm
            add vm named samplevm to group sample
    
        group show sample vm --format=json
            list all VMs of group sample in json format
    

help
----------------------------------------------------------------------

Command - help::
List available commands with "help" or detailed help with "help cmd".

image
----------------------------------------------------------------------

Command - image::

     Usage:
         image
         image <cm_cloud>... [--refresh]
     image -h | --help
         image --version
    
    Options:
        -h                   help message
        --refresh            refresh images of IaaS
    
     Arguments:
         cm_cloud    Name of the IaaS cloud e.g. india_openstack_grizzly.
    
     Description:
        image command provides list of available images. Image describes
        pre-configured virtual machine image.
    
    
     Result:
    
     Examples:
         $ image india_openstack_grizzly
    
    

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
                  the file is located at me.yaml
       me         same as yaml
    
       none       specifies if a yaml file is used for generation
                  the file is located at CONFIG/etc/none.yaml
       FILENAME   The filename to be generated or from which to read
                  information.
       VALUES     yaml file with the velues to be sed in the FILENAME
       KIND       The kind of the yaml file.
    
    Options:
       --force  force mode does not ask. This may be dangerous as it
                overwrites the CONFIG/cloudmesh.yaml file
       --file=FILENAME  The file
       --json   make the output format json
       -v       verbose mode
    
    
    Description:
    
      init list [KIND] [--json]
         list the versions and types of the yaml files in the
         CONFIG and CONFIG/etc directories.
    
      init list clouds [--file=FILENAME]
         Lists the available clouds in the configuration yaml file.
    
      init inspect --file=FILENAME
         print the variables in the yaml template
    

inventory
----------------------------------------------------------------------

Command - inventory::

    Usage:
           inventory clean
           inventory create image DESCRIPTION
           inventory create server [dynamic] DESCRIPTION
           inventory create service [dynamic] DESCRIPTION
           inventory exists server NAME
           inventory exists service NAME
           inventory
           inventory print
           inventory info [--cluster=CLUSTER] [--server=SERVER]
           inventory list [--cluster=CLUSTER] [--server=SERVER]
           inventory server NAME
           inventory service NAME
    
    Manages the inventory
    
        clean       cleans the inventory
        server      define servers
    
    Arguments:
    
      DESCRIPTION    The hostlist"i[009-011],i[001-002]"
    
      NAME           The name of a service or server
    
    
    Options:
    
       v       verbose mode
    
    

key
----------------------------------------------------------------------

Command - key::

    Usage:
             key -h|--help
             key list [--source=SOURCE] [--dir=DIR] [--format=FORMAT]
             key add [--keyname=KEYNAME] FILENAME
             key default [KEYNAME]
             key delete KEYNAME
    
      Manages the keys
    
      Arguments:
    
        SOURCE         mongo, yaml, ssh
        KEYNAME        The name of a key
        FORMAT         The format of the output (table, json, yaml)
        FILENAME       The filename with full path in which the key
                       is located
    
      Options:
    
         --dir=DIR            the directory with keys [default: ~/.ssh]
         --format=FORMAT      the format of the output [default: table]
         --source=SOURCE      the source for the keys [default: mongo]
         --keyname=KEYNAME    the name of the keys
    
      Description:
    
    
      key list --source=ssh  [--dir=DIR] [--format=FORMAT]
    
         lists all keys in the directory. If the directory is not
         specified the default will be ~/.ssh
    
      key list --source=yaml  [--dir=DIR] [--format=FORMAT]
    
         lists all keys in cloudmesh.yaml file in the specified directory.
          dir is by default ~/.cloudmesh
    
      key list [--format=FORMAT]
    
          list the keys in mongo
    
      key add [--keyname=keyname] FILENAME
    
          adds the key specifid by the filename to mongodb
    
    
      key list
    
           Prints list of keys. NAME of the key can be specified
    
      key default [NAME]
    
           Used to set a key from the key-list as the default key if NAME
           is given. Otherwise print the current default key
    
      key delete NAME
    
           deletes a key. In yaml mode it can delete only key that
           are not saved in mongo
    
    

label
----------------------------------------------------------------------

Command - label::

    Usage:
           label [--prefix=PREFIX] [--id=ID] [--raw]
    
    Options:
    
      --prefix=PREFIX    provide the prefix for the label
      --id=ID            provide the start ID which is an integer
      --raw              prints label only
    
    Description:
    
        A command to set a prefix and an id for a name of VM. 
        Without a paremeter, it prints a current label.
    
    

launcher
----------------------------------------------------------------------

Command - launcher::

    Usage:
          launcher start MENU
          launcher stop STACK_NAME
          launcher list
          launcher show STACK_NAME
          launcher menu [--column=COLUMN] [--format=FORMAT]
          launcher import [FILEPATH] [--force]
          launcher export FILEPATH
          launcher help | -h
    
      An orchestration tool with Chef Cookbooks
    
      Arguments:
    
        MENU           Name of a cookbook
        STACK_NAME     Name of a launcher
        FILEPATH       Filepath
        COLUMN         column name to display
        FORMAT         display format (json, table)
        help           Prints this message
    
      Options:
    
         -v       verbose mode
    
    

limits
----------------------------------------------------------------------

Command - limits::

    Usage:
        limits [CLOUD] [--format=json]
        limits help | -h
    
    Current usage data with limits on a selected project (tenant)
    
    Arguments:
    
      CLOUD          Cloud name to see the usage
      help           Prints this message
    
    Options:
    
       -v       verbose mode
    
    

list
----------------------------------------------------------------------

Command - list::

    List available flavors, images, vms, projects and clouds
    
    Usage:
        list flavor [CLOUD|--all] 
                    [--refresh] 
                    [--format=FORMAT]
                    [--column=COLUMN]
        list image [CLOUD|--all] 
                   [--refresh] 
                   [--format=FORMAT] 
                   [--column=COLUMN]
        list vm [CLOUD|--all] 
                [--group=<group>]
                [--refresh] 
                [--format=FORMAT] 
                [--column=COLUMN] 
                [--detail]
        list project
        list cloud [--column=COLUMN]
    
    Arguments:
    
        CLOUD    the name of the cloud e.g. india
    
    Options:
    
        --all                  list information of all active clouds
        --refresh              refresh data before list
        --group=<group>        give the group name in list vm
        --detail               for table print format, a brief version 
                               is used as default, use this flag to print
                               detailed table
        --column=COLUMN        specify what information to display in
                               the columns of the list command. For
                               example, --column=active,label prints
                               the columns active and label. Available
                               columns are active, label, host,
                               type/version, type, heading, user,
                               credentials, defaults (all to display
                               all, email to display all except
                               credentials and defaults)
        --format=FORMAT        output format: table, json, csv
    
    Description:
    
        List clouds and projects information, if the CLOUD argument is not specified, the
        selected default cloud will be used. You can interactively set the default cloud with the command
        'cloud select'.
    
        list flavor
        : list the flavors
        list image
        : list the images
        list vm
        : list the vms
        list project
        : list the projects
        list cloud
        : same as cloud list
    
    See Also:
    
        man cloud
    
    

load
----------------------------------------------------------------------

Command - load::

    Usage:
        load MODULE
    
    Loads the plugin given a specific module name. The plugin must be ina plugin directory.
    
    Arguments:
       MODULE  The name of the module.
    

loglevel
----------------------------------------------------------------------

Command - loglevel::

    Usage:
        loglevel
        loglevel critical
        loglevel error
        loglevel warning
        loglevel info
        loglevel debug
    
        Shows current log level or changes it.
    
        loglevel - shows current log level
        critical - shows log message in critical level
        error    - shows log message in error level including critical
        warning  - shows log message in warning level including error
        info     - shows log message in info level including warning
        debug    - shows log message in debug level including info
    
    

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
         $ cm-metric openstack -c india -u albert
         - Get user statistics
    
    

notebook
----------------------------------------------------------------------

Command - notebook::

    Usage:
        notebook create
        notebook start
        notebook kill
    
    Manages the ipython notebook server
    
    Options:
    
       -v       verbose mode
    
    

nova
----------------------------------------------------------------------

Command - nova::

    Usage:
           nova set CLOUD
           nova info [CLOUD]          
           nova help
           nova ARGUMENTS               
    
    A simple wrapper for the openstack nova command
    
    Arguments:
    
      ARGUMENTS      The arguments passed to nova
      help           Prints the nova manual
      set            reads the information from the current cloud
                     and updates the environment variables if
                     the cloud is an openstack cloud
      info           the environment values for OS
    
    Options:
    
       -v       verbose mode
    
    

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
        project
        project info [--format=FORMAT]
        project default NAME
        project active NAME
        project delete NAME
        project completed NAME
    
    Arguments:
    
        NAME           The project id
        FORMAT         The display format. (json, table)
    
    Description:
        Manages the user's projects
    
        project info
            show project information
        project default
            set the default project
        project active
            set/add an active project, 
        project delete
            delete the project
        project completed
            set a completed project, this will remove the project
            from active projects list and defalut project if it is
    
    
    

py
----------------------------------------------------------------------

Command - py::

    Usage:
        py
        py COMMAND
    
    Arguments:
        COMMAND   the command to be executed
    
    Description:
    
        The command without a parameter will be executed and the
        interactive python mode is entered. The python mode can be
        ended with ``Ctrl-D`` (Unix) / ``Ctrl-Z`` (Windows),
        ``quit()``,'`exit()``. Non-python commands can be issued with
        ``cmd("your command")``.  If the python code is located in an
        external file it can be run with ``run("filename.py")``.
    
        In case a COMMAND is provided it will be executed and the
        python interpreter will return to the command shell.
    
        This code is copied from Cmd2.
    

q
----------------------------------------------------------------------

Command - q::

    Usage:
        quit
    
    Action to be performed whne quit is typed
    

qstat
----------------------------------------------------------------------

Command - qstat::

    Usage:
      qstat HOST [-a]  [(--view VIEW | ATTRIBUTES...)] [--output=(dict|table)]
    
    tests via ping if the host ith the give NAME is reacahble
    
    Arguments:
    
      VIEW  the name of the view [default: default].
      HOST      Name of the machine to test
    
    Options:
    
       -v       verbose mode
    
    

quit
----------------------------------------------------------------------

Command - quit::

    Usage:
        quit
    
    Action to be performed whne quit is typed
    

quota
----------------------------------------------------------------------

Command - quota::

    Usage:
        quota [CLOUD] [--format=json]
        quota help | -h
    
    quota limit on a current project (tenant)
    
    Arguments:
    
      CLOUD          Cloud name to see the usage
      help           Prints this message
    
    Options:
    
       -v       verbose mode
    
    

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
        rain user list [--project=PROJECTS] [HOSTS]
        rain user list hosts [--start=TIME_START]
                        [--end=TIME_END]
                        [--format=FORMAT]
        rain status [--short|--summary][--kind=KIND] [HOSTS]
        rain provision --profile=PROFILE HOSTS
        rain provision list [--type=TYPE] (--distro=DISTRO|--kickstart=KICKSTART)
        rain provision --distro=DITRO --kickstart=KICKSTART HOSTS
        rain provision add (--distro=URL|--kickstart=KICk_CONTENT) NAME
        rain provision power [--off] HOSTS
        rain provision monitor HOSTS
    
    Arguments:
        HOSTS     the list of hosts passed
        LABEL     the label of a host
        COUNT     the count of the bare metal provisioned hosts
        KIND      the kind
        TYPE      the type of profile or server
    
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
        --type=TYPE            Format of the output profile, server. [default:server]
    
    
    

register
----------------------------------------------------------------------

Command - register::

    ::
        Usage:
          register [options] NAME
    
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
            LABEL     an identification name, it must be unique
            FILENAME  the filename in which the script is located
            REGEXP    Not supported yet.
                      If specified looks for files identified by the REGEXP.
    
    NOT SUPPORTED YET
    
       script load LABEL FILENAME
       script load FILENAME
       script load REGEXP
    
    Process FILE and optionally apply some options
    
    

security_group
----------------------------------------------------------------------

Command - security_group::

     Usage:
         security_group list <cm_cloud>...
         security_group add <cm_cloud> <label> <parameters>  [NOT IMPLEMENTED]
         security_group delete <cm_cloud> <label>            [NOT IMPLEMENTED]
     security_group -h | --help
         security_group --version
    
    Options:
        -h                   help message
    
     Arguments:
         cm_cloud    Name of the IaaS cloud e.g. india_openstack_grizzly.
    
     Description:
        security_group command provides list of available security_groups.
    
     Result:
    
     Examples:
         $ security_group list india_openstack_grizzly
    
    

setup_yaml
----------------------------------------------------------------------

Command - setup_yaml::

    ::
        Usage:
          setup_yaml  [--force] 
    
        Copies a cmd3.yaml file into ~/.cloudmesh/cmd3.yaml
    

ssh
----------------------------------------------------------------------

Command - ssh::

    Usage:
        ssh list [--format=json|yaml]
        ssh register NAME COMMANDS
        ssh NAME
    
    
    conducts a ssh login into a machine while using a set of
    registered commands under the name of the machine.
    
    Arguments:
    
      NAME      Name of the machine to log in
      list      Lists the machines that are registered and
                the commands to login to them
      register  Register the commands to a name
      COMMANDS  The list of commands executed when issuing a name
    
    Options:
    
       -v       verbose mode
    
    

stack
----------------------------------------------------------------------

Command - stack::

    Usage:
        stack start NAME [--template=TEMPLATE] [--param=PARAM]
        stack stop NAME
        stack show NAME
        stack list [--refresh] [--column=COLUMN] [--format=FORMAT]
        stack help | -h
    
    An orchestration tool (OpenStack Heat)
    
    Arguments:
    
      NAME           stack name
      help           Prints this message
    
    Options:
    
       -v       verbose mode
    
    

status
----------------------------------------------------------------------

Command - status::

    Usage:
        status mongo
        status celery
        status celery ping
        status celery stats
        status rabbitmq
    
      Shows system status
    

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
                   frameworks. At this time we will focus on chef
                   [default: chef].
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
    

usage
----------------------------------------------------------------------

Command - usage::

    Usage:
        usage [CLOUD] [--start=START] [--end=END] [--format=json]
        usage help | -h
    
    Usage data on a current project/tenant
    
    Arguments:
    
      CLOUD          Cloud name to see the usage
      START          start date of usage (YYYY-MM-DD)
      END            end date of usage (YYYY-MM-DD)
      help           Prints this message
    
    Options:
    
       -v       verbose mode
    
    

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
       Often we have to type in a command multiple times. To save
       us typng the name of the command, we have defined a simple
       scope that can be activated with the use command
    
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
           user id
    
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
        NAMES   Names of the variable separated by spaces
        VALUE   VALUE to be assigned
    
    special vars date and time are defined
    

verbose
----------------------------------------------------------------------

Command - verbose::

    Usage:
        verbose (True | False)
        verbose
    
    If it sets to True, a command will be printed before execution.
    In the interactive mode, you may want to set it to False.
    When you use scripts, we recommend to set it to True.
    
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
        vm start [--name=<vmname>]
                 [--count=<count>]
                 [--cloud=<CloudName>]
                 [--image=<imgName>|--imageid=<imgId>]
                 [--flavor=<flavorName>|--flavorid=<flavorId>]
                 [--group=<group>]
        vm delete [NAME|--id=<id>]
                  [--group=<group>]
                  [--cloud=<CloudName>]
                  [--prefix=<prefix>|--names=<hostlist>]
                  [--force]
        vm ip assign (NAME|--id=<id>)
                     [--cloud=<CloudName>]
        vm ip show [NAME|--id=<id>]
                   [--group=<group>]
                   [--cloud=<CloudName>]
                   [--prefix=<prefix>|--names=<hostlist>]
                   [--format=FORMAT]
                   [--refresh]
        vm login (--name=<vmname>|--id=<id>|--addr=<address>) --ln=<LoginName>
                 [--cloud=<CloudName>]
                 [--key=<key>]
                 [--] [<command>...]
        vm login NAME --ln=<LoginName>
                 [--cloud=<CloudName>]
                 [--key=<key>]
                 [--] [<command>...]
        vm list [CLOUD|--all] 
                [--group=<group>]
                [--refresh] 
                [--format=FORMAT] 
                [--column=COLUMN] 
                [--detail]
    
    Arguments:
        <command>              positional arguments, the commands you want to
                               execute on the server(e.g. ls -a), you will get
                               a return of executing result instead of login to
                               the server, note that type in -- is suggested before
                               you input the commands
        NAME                   server name
    
    Options:
        --addr=<address>       give the public ip of the server
        --cloud=<CloudName>    give a cloud to work on, if not given, selected
                               or default cloud will be used
        --count=<count>        give the number of servers to start
        --detail               for table print format, a brief version 
                               is used as default, use this flag to print
                               detailed table
        --flavor=<flavorName>  give the name of the flavor
        --flavorid=<flavorId>  give the id of the flavor
        --group=<group>        give the group name of server
        --id=<id>              give the server id
        --image=<imgName>      give the name of the image
        --imageid=<imgId>      give the id of the image
        --key=<key>            spicfy a private key to use, input a string which
                               is the full path to the key file
        --ln=<LoginName>       give the login name of the server that you want
                               to login
        --name=<vmname>        give the name of the virtual machine
        --names=<hostlist>     give the VM name, but in a hostlist style, which is very
                               convenient when you need a range of VMs e.g. sample[1-3]
                               => ['sample1', 'sample2', 'sample3']
                               sample[1-3,18] => ['sample1', 'sample2', 'sample3', 'sample18']
        --prefix=<prefix>      give the prefix of the server, standand server
                               name is in the form of prefix_index, e.g. abc_9
        --force                delete vms without user's confirmation
    
    Description:
        commands used to start or delete servers of a cloud
    
        vm start [options...]       start servers of a cloud, user may specify
                                    flavor, image .etc, otherwise default values
                                    will be used, see how to set default values
                                    of a cloud: cloud help
        vm delete [options...]      delete servers of a cloud, user may delete
                                    a server by its name or id, delete servers
                                    of a group or servers of a cloud, give prefix
                                    and/or range to find servers by their names.
                                    Or user may specify more options to narrow
                                    the search
        vm ip assign [options...]   assign a public ip to a VM of a cloud
        vm ip show [options...]     show the ips of VMs
        vm login [options...]       login to a server or execute commands on it
        vm list [options...]        same as command "list vm", please refer to it
    
    Examples:
        vm start --count=5 --group=test --cloud=india
                start 5 servers on india and give them group
                name: test
    
        vm delete --group=test --names=sample_[1-9]
                delete servers on selected or default cloud with search conditions:
                group name is test and the VM names are among sample_1 ... sample_9
    
        vm ip show --names=sample_[1-5,9] --format=json
                show the ips of VM names among sample_1 ... sample_5 and sample_9 in
                json format
    
    

volume
----------------------------------------------------------------------

Command - volume::

    Usage:
        volume list
        volume create <size>
                      [--snapshot-id=<snapshot-id>]
                      [--image-id=<image-id>]
                      [--display-name=<display-name>]
                      [--display-description=<display-description>]
                      [--volume-type=<volume-type>]
                      [--availability-zone=<availability-zone>]
        volume delete <volume>
        volume attach <server> <volume> <device>
        volume detach <server> <volume>
        volume show <volume>
        volume snapshot-list
        volume snapshot-create <volume-id>
                               [--force]
                               [--display-name=<display-name>]
                               [--display-description=<display-description>]
        volume snapshot-delete <snapshot>
        volume snapshot-show <snapshot>
        volume help
    
    
    volume management
    
    Arguments:
        <size>            Size of volume in GB
        <volume>          Name or ID of the volume to delete
        <volume-id>       ID of the volume to snapshot
        <server>          Name or ID of server(VM).
        <device>          Name of the device e.g. /dev/vdb. Use "auto" for 
                          autoassign (if supported)
        <snapshot>        Name or ID of the snapshot
    
    Options:
        --snapshot-id <snapshot-id>
                                Optional snapshot id to create the volume from.
                                (Default=None)
        --image-id <image-id>
                                Optional image id to create the volume from.
                                (Default=None)
        --display-name <display-name>
                                Optional volume name. (Default=None)
        --display-description <display-description>
                                Optional volume description. (Default=None)
        --volume-type <volume-type>
                                Optional volume type. (Default=None)
        --availability-zone <availability-zone>
                                Optional Availability Zone for volume. (Default=None)
        --force                 Optional flag to indicate whether to snapshot a volume
                                even if its attached to an instance. (Default=False)
    
    Description:
        volume list
            List all the volumes
        volume create <size> [options...]
            Add a new volume
        volume delete <volume>
            Remove a volume   
        volume attach <server> <volume> <device>
            Attach a volume to a server    
        volume-detach <server> <volume>
            Detach a volume from a server
        volume show <volume>        
            Show details about a volume
        volume snapshot-list
            List all the snapshots
        volume snapshot-create <volume-id> [options...]
            Add a new snapshot
        volume snapshot-delete <snapshot>
            Remove a snapshot
        volume-snapshot-show <snapshot>
            Show details about a snapshot
        volume help 
            Prints the nova manual
    
    

web
----------------------------------------------------------------------

Command - web::

    Usage:
        web [--fg|--cm] [LINK]
    
    Arguments:
    
        LINK    the link on the localhost cm server is opened.
    
    Options:
    
        -v         verbose mode
        --fg       opens a link on the FG portal
        --cm       opens a link on the CM portal
    
    Description:
    
        Opens a web page with the specified link
    
    

yaml
----------------------------------------------------------------------

Command - yaml::

    Usage:
        yaml KIND [KEY] [--filename=FILENAME] [--format=FORMAT]
        yaml KIND KEY VALUE [--filename=FILENAME] 
    
    Provides yaml information or updates yaml on a given replacement
    
    Arguments:
        KIND        The type of the yaml file (server, user) 
        KEY         Key name of the nested dict e.g. cloudmesh.server.loglevel
        VALUE       Value to set on a given KEY
        FILENAME    cloudmesh.yaml or cloudmesh_server.yaml
        FORMAT      The format of the output (table, json, yaml)
    
    Options:
    
        --format=FORMAT      the format of the output [default: print]
    
    Description:
    
       Sets and gets values from a yaml configuration file
    
