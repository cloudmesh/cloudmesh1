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
from sh import sed
from sh import tail
from sh import head
from sh import stty
from sh import ssh
from sh import fgrep
from sh import sleep
from multiprocessing import Pool
from progress.bar import Bar
#import re,datetime
from datetime import datetime
import console

prefix = os.environ['OS_USERNAME']
image_name = "common/precise-server-cloudimg-amd64.img.manifest.xml"

with_menu = True

maxparallel=5

#env.user=prefix
#env.hosts=["localhost"]
#env.hosts=["india.futuregrid.org",
#           "sierra.futuregrid.org",
#           "alamos.futuregrid.org",
#           "hotel.futuregrid.org",
#           "delta.futuregrid.org",
#           "bravo.futuregrid.org"]


######################################################################
# Terminal related methods
######################################################################

terminal_height, terminal_width = os.popen('stty size', 'r').read().split()


def _line(name):
    n = len(name)
    print "==", name, (int(terminal_width)-n-4) * "="

def _indent(numSpaces,s):
    return "\n".join((numSpaces * " ") + i for i in s.splitlines())


######################################################################
# Menu related methods
######################################################################

key_cache = []
instances_cache = ""

def _refresh_images():
    global instances_cache
    try: 
        instances_cache = fgrep(nova("list"), prefix)
    except:
        instances_cache = ""

def _get_keynames():
    global key_cache
    key_cache = []
    result = fgrep(tail(nova("keypair-list"), "-n", "+4"),"-v","+")
    for line in result:
        (front, name, signature, back) = line.split("|")
        key_cache.append(name)

def menu():
    global instances_cache
    global key_cache
    if with_menu:
        _line("cm - The FutureGrid Cloud Mesh Platform")
        bar = Bar('Processing', max=3)
        bar.next()
        _refresh_images()
        bar.next()
        _get_keynames()
        bar.next()
        bar.finish()
        os.system('clear')
        _line("cm - The FutureGrid Cloud Mesh Platform")
        _line("Key")
        print ",".join(key_cache)
        #print _indent(8,result_cache)
        _line("VMs")
        print _indent(8,instances_cache)
        _line("Settings")
        print _indent(8,"Theard pool size = %s" % maxparallel)
        print _indent(8,"Image = %s" % image_name)
        _line("Commands")
        print _indent(8,"start:i - reindex - par:n - fix")
        print _indent(8,"delete:i - clean - kill - killwait")
        print _indent(8,"test:i")
        print _indent(8,"status - ls - list - flavor - created - limits - rc")
        _line("")

######################################################################
# Key related methods
######################################################################

def key():
    """adds your public ~/.ssh/id_rsa.pub to the keypairs"""
    keyadd("gvonlasz")
    menu()

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
    

######################################################################
# Test an image by running some commands on it
######################################################################


def test(index):
    name = generate_name(index)
    result = fgrep(nova.show(name),"network")

    (start,label,ips,rest) = result.replace(" ","").split("|")
    print
    ips
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
    
#def activate():
#    local("source ~/ENV/bin/activate")

def bwait(index):
    """create a vm with the label prefix-index"""
    """NOT YET IMPLEMENYTED"""
    try:
        name = generate_name(index)
        tmp = nova("show", name)
        print tmp
    except:
        print "Failure to launch %s" % name

######################################################################
# VM CREATION
######################################################################
        
def generate_name(index):
    '''generates the name of the VM based on the index'''
    number = str(index).zfill(3);
    name = "%s-%s" % (prefix, number)
    return (name)

def start(index):
    '''starts a virtual machine with the given index. Same as boot'''
    boot(index)
    menu()
    
def boot(index):
    '''starts a virtual machine with the given index'''
    try:
        number = str(index).zfill(3);
        name = "%s-%s" % (prefix, number)
        print name
        print "Launching VM %s" % name
        tmp = nova("boot",
             "--flavor=1",
             "--image=%s" % image_name,
             "--key_name","%s" % prefix,
             "%s" % name)
        print tmp
    except Exception, e:
        print e
        print "Failure to launch %s" % name


def seq(number):
    """creates number of virtual machines in sequential order"""
    for index in range(0,int(number)):
        boot(index)
    menu()
    

def par(number):
    """Creates a number of vms with the labels prefix-0 to prefix-<number-1>. It uses a threadpool""" 
        
    pool = Pool(processes=maxparallel)
    list = range(0,int(number))
    result = pool.map(boot, list)
    status()
    menu()

def reindex():
    """updates the names of all active images"""
    try:
        instances = fgrep(nova("list","--status", "active"), prefix)
        index = 0
        for line in instances:
            line = line.replace(" ","")
            (a, id, name, status, network, rest) = line.split("|")
            newname = generate_name(index)
            if (name != newname):
                nova.rename(id, newname)
                print "Renameing %s -> %s" % (name, newname)
            else:
                print "Skipping %s " % name
            index = index + 1
    except:
        print "Found 0 instances with status error to kill"
    menu()

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
    menu()


######################################################################
# STATUS OF VMS
######################################################################    
def created():
    """shows when a VM was created*"""

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

######################################################################
# VM DELETION
######################################################################


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
    menu()
        
def killwait():
    kill()
    wait()
    menu()

def _count(instances):
    total = len(instances.split('\n'))-1 
    return total


def _del(id):
    nova("delete", "%s" % id)

def delete(id):
    _del(id)

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
    menu()


######################################################################
# waiting for public ip assignment
######################################################################    
def wait():
    """not yet implemented"""
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

######################################################################
# INFORMATION SERVICES
######################################################################

def limits():
    print nova("absolute-limits")

def rc():
    local("cat ~/openstack/novarc")

def flavor():
    """lists the flavors"""
    local("nova flavor-list")


def images():
    """List the images"""
    local("nova image-list")

def s(index):
    '''prints the summary status of instance with the index'''
    name = generate_name(index)
    try:
        instances = fgrep(nova("list"), name)
        print instances
    except:
        print "Found 0 instances"
    menu()
    

def ls():
    """Lists just my list - wn images"""
    try:
        instances = fgrep(nova("list"), prefix)
        print instances
    except:
        print "Found 0 instances"
    menu()

def list():
    """Lists just my own images"""
    try:
        instances = nova("list")
        print instances
    except:
        print "Found 0 instances"
    menu()
    
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

######################################################################
# OTHER
######################################################################

def r():
    '''refresh'''
    menu()

def _jtest():
    local("curl http://149.165.146.50:5000 | python -mjson.tool")


#print "... refreshing"
#menu()    

######################################################################
# OTHER
######################################################################

def install():
    os.system("pip install --upgrade -e git+https://github.com/openstack/python-novaclient.git#egg=python-novaclient")
    os.system("cp cm %s" % os.environ['VIRTUAL_ENV'])

