__all__ = []

import pkgutil
import inspect

for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(name).load_module(name)

    for name, value in inspect.getmembers(module):
        if name.startswith('__'):
            continue
        if name in __all__:
            continue
        globals()[name] = value
        __all__.append(name)


def plugins():
    return __all__


def get_class(modname, classname):
    ''' Returns a class of "classname" from module "modname". '''
    module = __import__(modname)
    classobj = getattr(module, classname)
    return classobj


def get_plugins(names=None, verbose=False):
    class_list = []
    if names is None:
        names = plugins()
    for classname in plugins():
        try:
            class_list.append(get_class("plugins", classname))
        except:
            # ignore wrong class load
            if verbose:
                print "WARNING: ignoring class", classname
            pass
    return class_list
