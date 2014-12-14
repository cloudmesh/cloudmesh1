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

        Description:
            admin password reset
                reset portal password
        """

        if arguments['password'] and arguments['reset']:
            db = Database()
            db.set_password_local()
