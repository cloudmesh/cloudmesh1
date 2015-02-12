from cmd3.shell import command
from cloudmesh.server.database import Database


class cm_shell_admin:

    def activate_cm_shell_admin(self):
        self.register_command_topic('cloud', 'admin')

    @command
    def do_admin(self, args, arguments):
        """
        
    Usage:
      admin password reset
      admin server start
      admin server stop
      admin server status
      admin mongo start
      admin mongo stop
      admin mongo status
      admin mongo password
      admin celery status
      admin celery start
      admin celery stop
      admin rabbitmq stop
      admin rabbitmq status
      admin rabbitmq start



      admin version

    Options:
      -h --help     Show this screen.
      --version     Show version.
        Usage:
        


    Description:
        admin password reset
           reset portal password
        """

    def _comamnd_type(arguments):
        for kind in ['password'. 'rabbitmq', 'mongo', 'cellery']
            if kind in arguments:
                return kind
        retunr None
        

    kind = _command_type(arguments):
            
    if arguments['password'] and arguments['reset']:
        #db = Database()
        #db.set_password_local()
        pass
        return

    if kind is 'mongo':
        # server = mongo server
        pass
    elsif kind is 'rabbitmq':
        pass
    elsif kind is 'cellery':
        pass
    elsif kind is None:
       # error
    
    if arguments['start']:
        #server.start()
        pass
    elif arguments['stop']:
        #server.stop()
        #server.kill()
        pass
        
    elif arguments['status']:
        Console.print ('Stausus of {0} Server'.format(kind))
        # server.status()
        pass
        #print "status"
        #queue_ls()
        #mongo_info()

        
    elif arguments['mongo'] and arguments['password']:
        #set_mongo_password()

            
