from cloudmesh_base.Shell import Shell


def shell(*args, **kwargs):
    return Shell.cm(args, kwargs)
