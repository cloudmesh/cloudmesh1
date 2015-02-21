from __future__ import print_function
from cmd3.shell import command
from cloudmesh.server.database import Database
from cmd3.console import Console
from cloudmesh_admin.server_admin import cloudmesh_server



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
        """
        
        '''
        def _comamnd_type(arguments):
            for kind in ['server', 'rabbitmq', 'mongo', 'celery']:
                if arguments[kind] == True:
                    if kind == "server":
                        kind = "cloudmesh"
                    return kind
            return None
                 
        if arguments['password'] and arguments['reset']:
            db = Database()
            db.set_password_local()
            return
            
        elif arguments['mongo'] and arguments['password']:
            set_mongo_password()
            return
            
        kind = _command_type(arguments)
            
        if kind is 'cloudmesh':
            server = cloudmesh_server()
        elif kind is 'mongo':
            server = mongo_server()
        elif kind is 'rabbitmq':
            server = rabbitmq_server()
        elif kind is 'celery':
            server = celery_server()
        elif kind is None:
           raise Exception("wrong command type")
        
        if arguments['start']:
            #server.start()
            pass
        elif arguments['stop']:
            #server.stop()
            #server.kill()
            pass
            
        elif arguments['status']:
            Console.msg('Status of {0} Server'.format(kind))
            # server.status()
            pass
            #print "status"
            #queue_ls()
            #mongo_info()
        '''
        if arguments['password'] and arguments['reset']:
            db = Database()
            db.set_password_local()
            return
            
        elif arguments['mongo'] and arguments['password']:
            set_mongo_password()
            return
            
        server = cloudmesh_server()
        # ######################################################################
        # MONGO SERVER
        # ######################################################################
        if arguments['mongo'] and arguments['status']:
            print(server._info_mongo())
        elif arguments['mongo'] and arguments['start']:
            server._start_mongo()
        elif arguments['mongo'] and arguments['stop']:
            server._stop_mongo()
        
        
        else:
            print("UNDER DEVELOPMENT")

        

            
