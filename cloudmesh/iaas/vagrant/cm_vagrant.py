from cloudmesh_base.Shell import Shell
from sh import rsync


vm_up = vagrant.bake("up")
# vagrant up
vm_ssh = vagrant.bake("ssh")
# vargant ssh
# use self.vm_up instead to cover the provider
#
vm_init = vagrant.bake("init")
# vagrant init precise32 http://files.vagrantup.com/precise32.box
vm_suspend = vagrant.bake("suspend")
vm_halt = vagrant.bake("halt")  # ?
vm_destroy = vagrant.bake("destroy")  # ?


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
            self.vm_up = vagrant.bake("up", "--provider", provider)
        else:
            self.vm_up = vagrant.bake("up")

    def image_list(self):
        images = {}
        lines = Shell.vagrant("box", "list")
        for line in lines:
            (name, kind) = line.split("(")
            name = name.strip()
            kind = kind.split(")")[0].strip()
            images[name] = {"name": name, "kind": kind}
        return images
