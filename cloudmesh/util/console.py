import textwrap

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = "\033[1m"

class Console(object):

    def __init__(self):
        pass

    def msg(self, message, width=90):
        print textwrap.fill(message, width=width)

    def error(self, message):
        print FAIL + msg(message) + ENDC

    def info(self, message):
        print OKBLUE + msg(message) + ENDC

    def warning(self, message):
        print WARNING + msg(message) + ENDC

