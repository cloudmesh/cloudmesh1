from fabric.api import task, local

@task
def info():
    """
    provides some info about the iptable rules set on this machine
    """
    print "not yet implemented"

@task
def production(status="on"):
    """
    sets the ip table rules for production" vlues are 'on', 'off'. This defines
    most likely just a small number of ports
    """
    print "not yet implemented"
    
@task 
def port (number,status="on"):
    """
    sets the ip table rule for a particular port. accepted values are 'on' and 'off' 
    """
    print "not yet implemented"    