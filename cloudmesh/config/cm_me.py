#! /usr/bin/env python
from __future__ import print_function
from jinja2 import Template
import sys


def command_me(arguments):

    t = Template("Hello {{ something }}!")
    result = t.render(something="World")
    print(result)

if __name__ == "__main__":
    command_me(sys.argv)
