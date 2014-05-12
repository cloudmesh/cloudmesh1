from cmd3.shell import function_command
from cloudmesh.rain.cobbler.cobbler_rain import rain_command

class cm_shell_rain:

    """The command handler for rain"""

    def activate_cm_shell_rain(self):
        self.register_command_topic('cloud','rain')
        pass

    @function_command(rain_command)
    def do_rain(self, args, arguments):
        rain_command(arguments)
        pass
