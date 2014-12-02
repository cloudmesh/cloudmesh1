import sys
sys.stderr = open('/dev/null')       # Silence silly warnings from paramiko
import paramiko as pm
sys.stderr = sys.__stderr__
# import os
import re
import os
from Crypto.PublicKey import RSA 
from sh import ssh as sh_ssh # import

''' Contains the ssh class. Can be used in casews when you want the output of
an ssh call but need to do steps before and after the call
as part of the ssh session'''


class AllowAllKeys(pm.MissingHostKeyPolicy):

    def missing_host_key(self, client, hostname, key):
        return


class ssh:

    def __init__(self, host, username, password=''):
        self.host = host
        self.username = username
        self.password = password
        self.setup()
        self.client = None

    def setup(self):
        self.client = pm.SSHClient()
        self.client.load_system_host_keys()
        self.client.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
        self.client.set_missing_host_key_policy(AllowAllKeys())
        self.client.connect(
            self.host, username=self.username, password=self.password)

    def ssh_session(self, command, init=None, exit=None):
        channel = self.client.invoke_shell()
        stdin = channel.makefile('wb')
        stdout = channel.makefile('rb')
        query = ""
        if init is not None:
            query += init + "\n"
        query += command
        if exit is not None:
            query += "\n" + exit + "\n"
        # bash\ncm list flavors jedi\nexit\nexit
        # print query
        stdin.write(query)
        output = stdout.read()
        # print output
        if init is not None:
            output = re.split(command, output)
            output = output[1]
        if exit is not None:
            exit = exit.split("\n")
            exit = exit[0]
            output = re.split(".*" + exit, output)
        output = output[0]
        stdout.close()
        stdin.close()
        return output

    def destroy(self):
        self.client.close()

def generate_keypair(type="rsa", bits=2048):
    '''
    Generate a keypair

    param: 
        type (str): the type of key (e.g. rsa, dsa)
        bits (int): the key length in bits
    Return: private key and public key
    '''
    if type == "rsa":
        new_key = RSA.generate(bits, os.urandom)
        public_key = new_key.publickey().exportKey("OpenSSH") 
        private_key = new_key.exportKey("PEM") 
    elif type == "dsa":
        # NOT IMPLEMENTED
        pass

    return private_key, public_key

# -----------------------------------------------------------------------


def ssh_execute(loginuser, addr, cmd, key=None):
    """Execute a command via SSH"""


    # disable SSH host key checking
    option = "-o StrictHostKeyChecking=no "
    host = " {0}@{1} ".format(loginuser, addr)
    cmd = " {0} ".format(cmd)
    if key:
        key = " -i {0} ".format(key)
    else:
        key = ""

    message = (option + key + host + cmd).split()

    return sh_ssh(message)

# -----------------------------------------------------------------------
