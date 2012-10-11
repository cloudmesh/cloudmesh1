
import os
import cmd2
from cmd2 import options, make_option



from myInventory import Server, Services, myInventory


inventory = myInventory()
serverobj = Server()
serviceobj = Services()
class Console(cmd2.Cmd):

    '''instantiate myInventory class'''
   
    def __init__(self):
        cmd2.Cmd.__init__(self)
    prompt = "fg_inventory>"
    ## defaults to None
    
    ## Command definitions ##
    def do_hist(self, args):
        """Print a list of commands that have been entered"""
        print self._hist

    def do_exit(self, args):
        """Exits from the console"""
        return -1

    ## Command definitions to support Cmd object functionality ##
    def do_EOF(self, args):
        """Exit on system end of file character"""
        return self.do_exit(args)

    def do_help(self, args):
        """Get all the command line arguments        """
        ## The only reason to define this method is for the help text in the doc string
        cmd2.Cmd.do_help(self, args)

    ## Override methods in Cmd object ##
    def preloop(self):
        """Initialization before prompting user for commands.
        """
        cmd2.Cmd.preloop(self)   ## sets up command completion
        self._hist    = []      ## No history yet
        self._locals  = {}      ## Initialize execution namespace for user
        self._globals = {}

    def postloop(self):
        """Take care of any unfinished business.
           Despite the claims in the Cmd documentaion, Cmd.postloop() is not a stub.
        """
        cmd2.Cmd.postloop(self)   ## Clean up command completion
        print "Exiting..."

    def precmd(self, line):
        """ This method is called after the line has been input but before
            it has been interpreted. If you want to modidy the input line
            before execution (for example, variable substitution) do it here.
        """
        self._hist += [ line.strip() ]
        return line

    def postcmd(self, stop, line):
        """If you want to stop the console, return something that evaluates to true.
           If you want to do some post command processing, do it here.
        """
        return stop

    def default(self, line):       
        """Called on an input line when the command prefix is not recognized.
           In that case we execute the line as Python code.
        """
        try:
            exec(line) in self._locals, self._globals
        except Exception, e:
            print e.__class__, ":", e
            
    @options([
    make_option('-p', '--prefix',action="store_const",help="Server name"),
    make_option('-r', '--range', action="store_const",
                help="Give the range of servers to create"),
    ])
    def do_list(self, arg, opts):# = None):
        #print arg.parse_args()
        if(opts.prefix):
            arg = ''.join(arg)
            print arg
            
        if(opts.range):
            print "in here"
            print arg
        '''List the data '''
        
    @options([
    make_option('-p', '--prefix',action="store_true",help=" server name"),\
    #, dest = "kall"),
    make_option('-r', '--range', type="int",action = "store",
                help=" give the range of servers to create"),
    ])
    def do_add_server(self, args, opts ):
        '''Add a server with given name in the inventory.'''
        
        if (opts.range):
            print args
            if(args > 0):
                for i in range(args):
                    myInventory.add(inventory,serverobj)
                    
        args = ''.join(args)
        if(opts.prefix):
            print args
            #print options.kall
            myInventory.add(inventory,serverobj, name = args)
        return
    
    @options([
    make_option('-p', '--prefix',action="store_true",help="Service name"),
    make_option('-r', '--range', type="string",
                help="Give the range of servers to create"),
    make_option('-s', '--server', type = "string", help="Server name for binding the service" )
    ])
    def do_add_services(self, args, opts=None ):
        '''Add a server with given name in the inventory.'''
        #print 'Adds a server with given arguments'
        
        args = ''.join(args)
        if(opts.prefix):
            myInventory.add(inventory,serviceobj, name = args)
            #inventory.test()
            
        if(opts.range):
            print "process range print inventory"
        if(opts.server):
            print "the servers name is"
        return
   
    def do_summary(self,args):
        '''Print the summary of available services'''
        inventory.dump()

if __name__ == '__main__':
        console = Console()
        console.cmdloop() 