#! /usr/bin/env python

from cmd import Cmd


class CommandTwo(Cmd):

    def do_two(self, args):
        """Says hello. If you provide a name, it will greet you with it."""
        if len(args) == 0:
            name = 'Two'
        else:
            name = args
        print "Hello, %s" % name

if __name__ == '__main__':
    prompt = CommandOne()
    prompt.prompt = '> '
    prompt.cmdloop('Starting prompt...')
