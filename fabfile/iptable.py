from fabric.api import task, local
"""
These tasks are for managing iptables rules for cloudmesh.  Currently
we assume there exist two custom rule chains, named:

  cm_production
  cm_ports

By managing rules in these chains we don't interfere with any other
administrative iptables rules on the server.  The initial creation of
these chains is done like this:

  iptables -N cm_production
  iptables -N cm_ports

These then need to be added to the default INPUT chain, after any
other rules that should take precidence, like this:

  iptables -I n INPUT -j cm_ports
  iptables -I n INPUT -j cm_production

Where 'n' is the rule number appropriate for the INPUT chain.

Currently ports defined in the cm_port chain, using the port task,
will take precidence over rules in the cm_production chain.
"""

PRODUCTION_CHAIN = "cm_production"
PORTS_CHAIN = "cm_ports"
PORT_RULE = "%s -p tcp -m state --state NEW -m tcp --dport %s -j ACCEPT"


@task
def info():
    """                                                                                                                             
    provides some info about the iptable rules set on this machine                                                                  
    """
    results1 = local("sudo iptables --line-numbers -L %s" %
                     PORTS_CHAIN, capture=True)
    results2 = local("sudo iptables --line-numbers -L %s" %
                     PRODUCTION_CHAIN, capture=True)
    print "%s\n\n%s" % (results1, results2)


@task
def production(status="on"):
    """                                                                                                                             
    sets the ip table rules for production" vlues are 'on', 'off'. This defines                                                     
    most likely just a small number of ports                                                                                        
    """
    usage = "Usage: production:[on|off]"
    production_ports = [80]
    if status == "on":
        local("sudo iptables -F %s" % PRODUCTION_CHAIN)
        for port in production_ports:
            local("sudo iptables -A " + PORT_RULE % (PRODUCTION_CHAIN, port))
    elif status == "off":
        local("sudo iptables -F %s" % PRODUCTION_CHAIN)
    else:
        print usage


@task
def port(number, status="on"):
    """                                                                                                                             
    sets the ip table rule for a particular port. accepted values are 'on' and 'off'                                                
    """
    usage = "Usage: port:number,[on|off]"

    if not number or not number.isdigit():
        print usage
        return

    if status == "on":
        local("sudo iptables -A " + PORT_RULE % (PORTS_CHAIN, number))
    elif status == "off":
        local("sudo iptables -D " + PORT_RULE % (PORTS_CHAIN, number))
    else:
        print usage
