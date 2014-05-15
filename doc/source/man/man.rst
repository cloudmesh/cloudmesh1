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
    
