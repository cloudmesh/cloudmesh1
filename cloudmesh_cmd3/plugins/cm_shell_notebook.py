from __future__ import print_function
# import subprocess
from cmd3.shell import command
from cloudmesh_base.logger import LOGGER
from IPython.lib import passwd
from shutil import copyfile
from cloudmesh_install.util import path_expand
import os
import sh

log = LOGGER(__file__)


class notebook(object):

    def __init__(self):
        self.data = {
            'notebook_dir': path_expand('~/notebook'),
            'profile_nbserver_dir': path_expand('~/.ipython/profile_nbserver'),
            'cert': '~/.ipython/profile_nbserver/mycert.pem',
            'cloudmesh': path_expand('~/.cloudmesh'),
            'pid': None
        }

    def _yaml_file_replace(self, filename, replacements={}):
        with open(filename, 'r') as f:
            content = f.read()

        for _old, _new in replacements.iteritems():
            content = content.replace(_old, _new)

        outfile = open(filename, 'w')
        outfile.write(content)
        outfile.close()

    def _create_dir(self, path=None):
        if path is not None:
            self.data['notebook_dir'] = path_expand(path)
        try:
            os.makedirs("{notebook_dir}".format(**self.data), 0700)
        except:
            pass

    def create(self):
        os.system("ipython profile create nbserver")
        copyfile(
            '{cloudmesh}/etc/ipython_notebook_config.py'.format(**self.data),
            '{profile_nbserver_dir}/ipython_notebook_config.py'.format(**self.data)
        )
        result = passwd()

        self._yaml_file_replace(
            '{profile_nbserver_dir}/ipython_notebook_config.py'.format(**self.data),
            replacements={'SHAPASSWD': result}
        )
        os.system("openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout {cert} -out {cert}".format(**self.data))
        os.system("chmod go-rwx {cert}".format(**self.data))

    def start(self):
        self._create_dir()
        command = "cd {notebook_dir} && ipython notebook --certfile={cert} --profile=nbserver".format(**self.data)
        # self.data['pid'] = subprocess.Popen(command.split(" "))
        print("STARTING:", command)
        os.system(command + " &")

    def kill(self):
        #
        # this is not working, as we do not jet use subprocess
        #
        if self.data['pid'] is not None:
            self.data['pid'].terminate()
            self.data['pid'] = None

        #
        # TODO: this is not a good way to kill, as it apears that we only read 80 chars for each line in ps
        #
        result = sh.ps("-o", "pid,command", _tty_in=False, _tty_out=False)
        for line in result.split("\n"):
            if "notebook" in line and "ipython" in line:
                attributes = line.strip().split(' ')
                pid = attributes[0]
                print("TERMINATING", pid)
                sh.kill("-9", pid)


class cm_shell_notebook:

    """opt_example class"""

    def activate_cm_shell_notebook(self):
        self.register_command_topic('ipython', 'notebook')
        self._notebook = notebook()
        pass

    @command
    def do_notebook(self, args, arguments):
        """
        ::
        
          Usage:
              notebook create
              notebook start
              notebook kill

          Manages the ipython notebook server

          Options:

             -v       verbose mode

        """
        log.info(arguments)

        if arguments["create"]:
            self._notebook.create()
            return

        elif arguments["start"]:
            self._notebook.start()
            return

        if arguments["kill"]:
            self._notebook.kill()
            return
