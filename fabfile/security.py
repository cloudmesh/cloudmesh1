from fabric.api import task, local
import sys
import os

@task
def check(search=""):
    if not search:
        search = "OS_PASSWORD': '[a-zA-Z0-9]+'"
    cmd = "egrep -ri \"{0}\" * | cut -d\":\" -f1".format(search)
    print(cmd)
    res = local(cmd, capture=True)
    if res:
        print ("ERROR: OS_PASSWORD DETECTED, SEE FILES BELOW")
        print ("")
        print (res)
    else:
        print ("NO PASSWORD DETECTED")
