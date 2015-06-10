import clean
import server
import build
import git
import pep8
import pypi
import doc
import mq
import test
import nose
import mongo
import iptable
import tunnel
import user
import mooc
import hpc
import qc
import manage
import india
import ipython
import security

try:
    import queue
except Exception, e:
    import sys
    import traceback
    print "ERROR: failed to load queue fabfile"
    print e
    print '-' * 60
    traceback.print_exc(file=sys.stdout)
    print '-' * 60
