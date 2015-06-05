from __future__ import print_function
from cloudmesh_base.Shell import Shell

def nova_provider(kind):
    sh_nova = None

    def sh_nova(*args):
        if kind is "sh":
            return Shell.nova(args)
        elif kind.startswith("sim"):
            print(args, kwargs)

    return sh_nova


# nova = nova_providor("simulator")

# nova("a", "b", h="k")
