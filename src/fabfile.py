import sys
import os
try:
    from sh import nova
except:
    print "========================================="
    print "Please add the folloing in your shell,"
    print "then restart your command"
    print "========================================="
    print "source ~/ENV/bin/activate; source ~/openstack/novarc"
    print "========================================="
    sys.exit()
from fabric.api import *
from sh import ssh
from sh import fgrep
from sh import sleep
from multiprocessing import Pool
from progress.bar import Bar
#import re,datetime
from datetime import datetime

prefix = "gregor"
maxparallel=10

#env.user=["gvonlasz"]
#env.hosts=["localhost"]
#env.hosts=["india.futuregrid.org",
#           "sierra.futuregrid.org",
#           "alamos.futuregrid.org",
#           "hotel.futuregrid.org",
#           "delta.futuregrid.org",
#           "bravo.futuregrid.org"]

def key():
    """adds your public ~/.ssh/id_rsa.pub to the keypairs"""
    keyadd("gvonlasz")

def test(index):
    name = generate_name(index)
    result = fgrep(nova.show(name),"network")

    (start,label,ips,rest) = result.replace(" ","").split("|")
    print ips
    try:
        (private_ip, public_ip) = ips.split(",")
    except:
        print "public IP is not yet assigned"
        sys.exit()
    print public_ip
    rsh = ssh.bake("%s@%s" % ("ubuntu",str(public_ip)))
    remote = rsh.bake("-o StrictHostKeyChecking no")
    test1 = remote("uname").replace("\n","")
    print "<%s>" % test1
    print remote("uname -a")
    print remote("hostname")
    print remote("pwd")
    
def keyadd(name):
    bar = Bar('Processing', max=5)
    try:
        bar.next()
        nova("keypair-add", "--pub-key", "~/.ssh/id_rsa.pub", "%s" % name)
    except:
        #print "Key add error on %s" % name
        bar.next()
        try:
            bar.next()
            #print "Tryig to delete key"
            result = nova("keypair-delete", "%s" % name)
            #print result
            #print "Tryig to add key"
            bar.next()
            results = nova ("keypair-add", "--pub-key", "~/.ssh/id_rsa.pub", "%s" % name)
            #print result
        except:
            print "\nKey deletion error on %s\n" % name
    bar.next()
    bar.finish()
    result =  nova("keypair-list")
    print result
    
def keylist():
    """list my key"""
    nova("keypair-list")

def keydelete(name):
    """delets the named key"""
    nova("keypair-delete", "%s" % name)
    
def activate():
    local("source ~/ENV/bin/activate")

def bwait(index):
    """create a vm with the label prefix-index"""
    try:
        name = generate_name(index)
        tmp = nova("show", name)
        print tmp
    except:
        print "Failure to launch %s" % name

def generate_name(index):
    number = str(index).zfill(3);
    name = "%s-%s" % (prefix, number)
    return (name)

def boot(index):
    """create a vm with the label prefix-index"""
    #nova boot --flavor 1 --image 9bab7ce7-7523-4d37-831f-c18fbc5cb543 --key_name mykey myinstance

    try:
        number = str(index).zfill(3);
        name = "%s-%s" % (prefix, number)
        print name
        print "Launching VM %s" % name
        tmp = nova("boot",
             "--flavor=1",
             "--image=common/precise-server-cloudimg-amd64.img.manifest.xml",
             "--key_name","%s" % "gvonlasz",
             "%s" % name)
        print tmp
    except:
        print "Failure to launch %s" % name

def cluster(number):
    """creates number of virtual machines in sequential order"""
    vm(number)

    
def vm(number):
    """Creates a number of vms with the labels prefix-0 to prefix-<number-1>""" 
    for index in range(0,int(number)):
        boot(index)


def pcluster(number):
    """Creates a number of vms with the labels prefix-0 to prefix-<number-1>""" 
        
    pool = Pool(processes=maxparallel)
    list = range(0,int(number))
    result = pool.map(boot, list)
    status()

def created():
    """show all the instances with prefix-*"""

    t_now = datetime.now()
    try:
        instances = fgrep(nova("list"),"|")
        print instances
        for line in instances:
            columns = line.split("|")
            id = columns[1].strip()
            name = columns[2].strip()
            if id != "ID":
                line = fgrep(nova("show", id),"created")
                line = line.replace ("\n", "")
                line = line.replace (" ", "")
                fields = line.split("|")
                value = fields[2]
                value = value.replace("T"," ")
                value = value.replace("Z","")
                t_a = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                delta = t_now - t_a
                print name, "=", delta
    except:
        print "Found 0 instances to show"

def _gt(s):
    d=datetime.datetime(*map(int, re.split('[^\d]', s)[:-1]))
    return d


def show():
    """show all the instances with prefix-*"""
    try:
        instances = fgrep(nova("list"), prefix)
        for line in instances:
            columns = line.split("|")
            id = columns[1].strip()
            name = columns[2].strip()
            print "Found %s to show" % name
            print nova("show", "%s" % id)
    except:
        print "Found 0 instances to show"

    
def kill():
    """kills all the instances with prefix prefix-*"""
    try:
        list = []
        names = []
        instances = fgrep(nova("list"), prefix)
        for line in instances:
            columns = line.split("|")
            id = columns[1].strip()
            name = columns[2].strip()
            print "Found %s to kill" % name
            list.append(id)
            names.append(name)
        print "Starting parallel Delete of: ", names
        pool = Pool(processes=maxparallel)
        result = pool.map(_del, list)

    except:
        print "Found 0 instances to kill"

def killwait():
    kill()
    wait()

def _count(instances):
    total = len(instances.split('\n'))-1 
    return total

def wait():
    try:
        instances = fgrep(nova("list"), prefix)
        total = _count(instances)
        exit
        bar = Bar('Processing', max=total)
        old = total
        while True:
            #_status(instances)
            current = _count(instances)
            if old != current:
                bar.next()
            if current == 0:
                bar.finish()
                break
            sleep(2)
            instances = fgrep(nova("list"), prefix)
    except:
        print "done"

def _del(id):
    nova("delete", "%s" % id)


def reindex():
    """updates the names of all active images"""
    try:
        instances = fgrep(nova("list","--status", "active"), prefix)
        index = 0
        for line in instances:
            line = line.replace(" ","")
            (a, id, name, status, network, rest) = line.split("|")
            newname = generate_name(index)
            
            nova.rename(id, newname)
            index = index + 1
    except:
        print "Found 0 instances with status error to kill"

def limits():
    print nova("absolute-limits")

def clean():
    """kills all the instances with prefix prefix-* and in error state"""
    try:
        instances = fgrep(nova("list"), prefix)
        for line in instances:
            columns = line.split("|")
            id = columns[1].strip()
            name = columns[2].strip()
            status = columns[3].strip()
            if status == "ERROR":
                print "Killing %s" % name
                nova("delete", "%s" % id)
            else:
                print "Keeping %s" % name
    except:
        print "Found 0 instances with status error to kill"

def fix():
    """kills all the instances with prefix-* and in error state"""
    try:
        instances = fgrep(nova("list"), prefix)
        print instances
        for line in instances:
            columns = line.split("|")
            id = columns[1].strip()
            name = columns[2].strip()
            number = name.split('-')[1]
            status = columns[3].strip()
            if status == "ERROR":
                print "Killing %s" % name
                nova("delete", "%s" % id)
                print "Restarting %s" % number
                boot(number)
            else:
                print "Keeping %s" % name
    except:
        print "Found 0 instances with status error to kill"

def images():
    """List the images"""
    local("nova image-list")

def ls():
    """Lists just my own images"""
    try:
        instances = fgrep(nova("list"), prefix)
        print instances
    except:
        print "Found 0 instances"

def list():
    """Lists just my own images"""
    try:
        instances = nova("list")
        print instances
    except:
        print "Found 0 instances"

def status():
    """prints a very small status message of the form
    -A----A--A----A--A---A-----A---A----A--A----------------"""
    try:
        instances = fgrep(nova("list"), prefix)    
        _status(instances)
    except:
        print "Found 0 instances with status error to kill"

def _status(instances):
    """prints a very small status message of the form
    -A----A--A----A--A---A-----A---A----A--A----------------"""
    statuslist = []
    try:
        for line in instances:
            columns = line.split("|")
            status = columns[3].strip()
            statuschar = status.split()[0][0]
            statuslist.append(statuschar)
        result = ''.join(statuslist)
        result = result.replace("E","-")
        print "%d instances:" % len(result), result
    except:
        print "0 instances found"



def flavor():
    """lists the flavors"""
    local("nova flavor-list")

def jtest():
    local("curl http://149.165.146.50:5000 | python -mjson.tool")

def rc():
    local("cat ~/openstack/novarc")

    
    
    
