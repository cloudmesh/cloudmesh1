from cloudmesh_base.Shell import Shell
from sh import rsync

# TODO bake not implemented

def vm_up(*args):
    a = ['up'] + args
    return Shell.execute('vagrant', a)

def vm_ssh(*args):
    a = ['ssh'] + args
    return Shell.execute('vagrant', a)

def vm_init(*args):
    a = ['init'] + args
    return Shell.execute('vagrant', a)

def vm_suspend(*args):
    a = ['suspend'] + args
    return Shell.execute('vagrant', a)

def vm_halt(*args):
    a = ['halt'] + args
    return Shell.execute('vagrant', a)

def vm_destroy(*args):
    a = ['destroy'] + args
    return Shell.execute('vagrant', a)



class vagrant:

    _provider = None

    def __init__(self, label, dir=None):
        """creates dir/label"""
        if dir is None:
            raise NotImplementedError()
            # use cwd
        else:
            self.dir = dir
        self.label = label
        # create dir/label

    def bootstrap(self, script):
        """creates a bootsrap.sh file with the script contents"""
        raise NotImplementedError()

    def folder(self, name, source):
        """creates a foler with the name and rsyncs the condents from a source"""
        raise NotImplementedError()

    def forward(self, host_guest_array):
        """(host portid, guest_portid)*"""
        raise NotImplementedError()

    def add_forward(self, host_port, guest_port):
        """adds a singgle host giest port forward"""
        raise NotImplementedError()

    @property
    def provider(self):
        self._provider = provider
        if provider is None:
            def vm_up(*args):
                a = ['up',"--provider", provider] + args
                return Shell.execute('vagrant', a)

        else:
            def vm_up(*args):
                a = ['up'] + args
                return Shell.execute('vagrant', a)

        self.vm_up = vm_up

    def image_list(self):
        images = {}
        lines = Shell.vagrant("box", "list")
        for line in lines:
            (name, kind) = line.split("(")
            name = name.strip()
            kind = kind.split(")")[0].strip()
            images[name] = {"name": name, "kind": kind}
        return images
