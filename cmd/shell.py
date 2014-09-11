#! /usr/bin/env python

from cmd import Cmd
from mixin import MixIn, makeWithMixins, makeWithMixinsFromString
from plugins import *
from plugins import get_plugins


class Shell(Cmd):

    def do_hello(self, args):
        """Says hello. If you provide a name, it will greet you with it."""
        if len(args) == 0:
            name = 'stranger'
        else:
            name = args
        print "Hello, %s" % name

    def do_quit(self, args):
        """Quits the program."""

if __name__ == '__main__':

    plugins = get_plugins()
    SuperShell = makeWithMixins(Shell, plugins)
    shell = SuperShell()
    shell.prompt = '> '
    shell.cmdloop('Cloudmesh Shell...')
