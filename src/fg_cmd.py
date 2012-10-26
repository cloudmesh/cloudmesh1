#! /usr/bin/env python


import os
import cmd2
from cmd2 import options, make_option
import argparse
import re

from myInventory import Server, Services, myInventory

inventory = myInventory()
serverobj = Server()
serviceobj = Services()
class Console(cmd2.Cmd):

    '''instantiate myInventory class'''
    setcommands = {'server':'', 'service':''}
    
    def __init__(self):
        cmd2.Cmd.__init__(self)
        
    prompt = "fg_inventory> "
    
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
            
    def get_prefix(self, string, value ):
        '''Returns the IP prefix in format as e.g. i1.iu.edu'''   
        stri = str(value)
        a = re.sub('#', stri ,string)
        return a
    
    def do_assign(self, args):
        '''Set the required field values in order to ease the pain of \
        not specifying them again right now using a delimiter ':' \
        to separate the two.
        '''
        parser = argparse.ArgumentParser()
        parser.add_argument("position", help='positional parameter can have\
         values server or services e.g assign server:india')
        args = parser.parse_args(args.split())
        temp =  args.position.split(':')
        if temp[0].lower() not in ['server', 'service']:
            print 'invalid operator to assign'
            print 'Can only accept server, service operator'
            return
        self.setcommands[temp[0]] = temp[1]
        #print self.setcommands
        
    def do_unassign(self, args):
        '''Set the required field values in order to ease the pain of \
        not specifying them again right now using a delimiter ':' \
        to separate the two.
        '''
        parser = argparse.ArgumentParser()
        parser.add_argument("position")
        args = parser.parse_args(args.split())
        print args.position
        temp=args.position
        if temp.lower() not in ['server', 'service']:
            print 'invalid operator to unassign'
            print 'Can only accept server, service operator'
            return
        self.setcommands[temp] = ''
        print self.setcommands
    
    def do_printassign(self, args):
        '''Shows which fields are currently assigned'''
        print self.setcommands

    #Helper Method to find all the assigned values to reduce typing
    def isassigned(self, tocheck):
        '''Returns true or false depending on whether the given parameter \
        is set or not'''
        for tocheck,value in self.setcommands.iteritems():
            if value != '':
                return True
            return False
                            
    def do_add_server(self, args):
        '''Add a server with given name in the inventory.'''
        parser = argparse.ArgumentParser()
        
        parser.add_argument('-r','--range', action="store", default=False, type = self.parseNumList, dest = "range")
        parser.add_argument('-p','--prefix', action="store", dest = "prefix")
        parser.add_argument('-s','--set', action = "store", dest = "set")
        args = parser.parse_args(args.split())
        if (args.range):
            print args.range
            for i in args.range:
                if(args.prefix == None):
                    print "Error No prefix specified"
                else:
                    myInventory.add(inventory,serverobj, name = args.prefix, \
                                    ip_address = self.get_prefix(args.prefix, i))
        
        '''           
        if(args.prefix):
            print args.prefix
            myInventory.add(inventory,serverobj, name = args.prefix)
        '''
                    
    def do_add_services(self, args, opts=None ):
        '''Add a service to a given server name in the inventory.'''
        parser = argparse.ArgumentParser()
        
        parser.add_argument('-r','--range', action="store", default=False \
                            ,type = self.parseNumList, dest = "range",  \
                             help="set a range of services to start")
        
        parser.add_argument('-p','--prefix', action="store", \
        default="i#.iu.edu", dest = "prefix", help="Server name for binding the service")
        
        parser.add_argument('-n','--name', action = "store", dest = "servername" ,\
                            help="Set the server name to given option")
        
        parser.add_argument('-s', '--sname',action="store", dest = "servicename",\
                             help="Service name")
        args = parser.parse_args(args.split())
        if (args.range):
            print args.range
            for _ in args.range:    
                if(args.prefix == None) or (args.servicename == None) :
                    print "Error No prefix and/or servicename specified"
                else:
                    myInventory.add(inventory,serviceobj, name = args.prefix, service_name = args.servicename)
                    
        if(args.prefix)  and (args.servicename) and (args.range ==None):
            myInventory.add(inventory,serviceobj, name = args.prefix, service_name = args.servicename)

    def parseNumList(self,string):
        '''Method for enumerating the numbers specified in the range interval'''
        m = re.match(r'(\d+)(?:-(\d+))?$', string)
        # ^ (or use .split('-'). anyway you like.)
        if not m:
            raise argparse.ArgumentTypeError("'" + string + "' is not a range of number. Expected forms like '0-5' or '2'.")
        start = m.group(1)
        end = m.group(2) or start
        return list(range(int(start,10), int(end,10)+1)) 
    
    def do_add(self , args):
        '''Instead of having add_server and add_services, combine them into a single add method'''
        parser = argparse.ArgumentParser()
        #positional argument immediately after add
        parser.add_argument("firstargument")
        parser.add_argument('-n','--name', action="store", dest = "name")
        parser.add_argument('-r','--range', action="store", default=False, \
                            type = self.parseNumList, dest = "range")
        parser.add_argument('-s','--servicename', action="store", dest = "servicename")
        parser.add_argument('-p','--prefix', action="store", default="i#.iu.edu", dest = "prefix")
        args = parser.parse_args(args.split())
        print args.firstargument
        
        if (args.firstargument.lower() == "server"):
            #print 'in server'
            if (args.range):
                for i in args.range:
                    if((args.name == None) and (self.setcommands['server'] != '')):
                        myInventory.add(inventory,serverobj, name = self.setcommands['server'], \
                                        prefix = self.get_prefix(args.prefix, i))
                    else:
                        myInventory.add(inventory,serverobj, name = args.name, \
                                        prefix = self.get_prefix(args.prefix, i))
            elif (self.isassigned('server')):
                myInventory.add(inventory,serverobj, name = self.setcommands['server'], \
                                       prefix = self.get_prefix(args.prefix, 1))
                #setting the prefix to 1 by default
                return
            
        elif (args.firstargument.lower() == "service"):
            #print 'services called'  
            if (args.range):
                #print args.range
                for i in args.range:    
                    if (args.servicename == None) and (args.name == None):
                        if (not self.isassigned('server')) and (not self.isassigned('service')):
                            print "Error No server and/or servicename specified"
                            return
                        else: #assuming that server and servicename are assigned
                            myInventory.add(inventory,serviceobj, name = self.setcommands['server'], \
                                            service_name = self.setcommands['service'],\
                                            prefix = self.get_prefix(args.prefix, i))
                            
                    elif(args.servicename != None) and (args.name != None):
                        myInventory.add(inventory,serviceobj, name = args.name,\
                                         service_name = args.servicename,prefix = self.get_prefix(args.prefix, i))
                    
                    elif((args.name) and self.isassigned('service')):
                        myInventory.add(inventory,serviceobj, name = args.name, \
                                        service_name = self.setcommands['service'],\
                                        prefix = self.get_prefix(args.prefix, i))
                    
                    if((args.servicename) and self.isassigned('server')):
                        myInventory.add(inventory,serviceobj, name = self.setcommands['server'], \
                                        service_name = args.servicename ,prefix = self.get_prefix(args.prefix, i))
                    
                    else:
                        myInventory.add(inventory,serviceobj, name = self.setcommands['server'], \
                                        service_name = self.setcommands['service'],prefix = self.get_prefix(args.prefix, i))
                        
            elif ((args.name)  and (args.servicename)):
                myInventory.add(inventory,serviceobj, name = args.name, service_name = args.servicename,\
                                prefix = self.get_prefix(args.prefix, i))
        
        else:
            print "invalid argument only options are : server, service"
            return
        

    def do_list(self,args):
        '''List the contents of the inventory'''
        parser = argparse.ArgumentParser()
        parser.add_argument('type')
        args = parser.parse_args(args.split())
        if args.type.lower() == 'server':
            myInventory.list(inventory,serverobj)
        if args.type.lower() == 'service':
            myInventory.list(inventory,serviceobj)
            
    def do_summary(self,args):
        '''Print the summary of available services'''
        inventory.dump()

if __name__ == '__main__':
        console = Console()
        console.cmdloop()