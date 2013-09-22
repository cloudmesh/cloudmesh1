from sh import VBoxManage
from collections import OrderedDict
from pprint import pprint

vbox_list = VBoxManage.bake("list","vms","-l")

#
# LIST
#
def get_vms_info():
    result = vbox_list()
    d = {}
    for info in result.split("\n\n\n"):
        lines = info.split("\n\n")[0].split("\n")
        m = {}
        for line in lines:
            try:
                attribute, value =  line.split(':',1)
                if attribute == "State":
                    value = value.split("(")[0]
                m.update ({attribute : value.strip()})
            except:
                print line
                pass
        try: 
            d[m["Name"]] = m
        except:
            pass
    return d

def filter_attributes(d, filterkeys=["Name", "UUID", "State"]):
    f = {}
    for name in d:
        m = d[name]

        f[m["Name"]] = dict(zip(filterkeys, [m[k] for k in filterkeys]))
    return f
        
def get_vms():
    vms = get_vms_info()
    f = filter_attributes(vms)
    return f

print "ALL INFO"
print 70 * "-"
vms = get_vms_info()

pprint (vms)

print "SMALL INFO"
print 70 * "-"

vms = get_vms()

pprint (vms)

