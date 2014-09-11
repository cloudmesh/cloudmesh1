def MixIn(pyClass, mixInClass, makeLast=False):
    if mixInClass not in pyClass.__bases__:
        if makeLast:
            pyClass.__bases__ += (mixInClass,)
        else:
            pyClass.__bases__ = (mixInClass,) + pyClass.__bases__

def makeWithMixins(cls, mixins, verbose=False):
    for mixin in mixins:
        if verbose: 
            print "Loading:", mixin
        if mixin not in cls.__bases__:
            cls.__bases__ = (mixin,) + cls.__bases__
        else:
            if verbose:
                print "ERROR: Cannot add %s to %s" % (mixin, cls)
    return cls
#http://alexgaudio.com/2011/10/07/dynamic-inheritance-python.html

def makeWithMixinsFromString(cls, mixins, verbose=False):
    for id in mixins:
        mixin = globals()[id]
        if verbose: 
            print "Loading:", mixin
        if mixin not in cls.__bases__:
            cls.__bases__ = (mixin,) + cls.__bases__
        else:
            if verbose:
                print "ERROR: Cannot add %s to %s" % (mixin, cls)
    return cls

def getclass(modname, classname):
    ''' Returns a class of "classname" from module "modname". '''
    module = __import__(modname)
    classobj = getattr(module, classname)
    return classobj
