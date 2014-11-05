from __future__ import print_function
from sh import VBoxManage
from collections import OrderedDict
from pprint import pprint

vbox_list = VBoxManage.bake("list", "vms", "-l")
vbox_vminfo = VBoxManage.bake("showvminfo")
#
# LIST
#


def convert_to_dict(lines):
    m = {}
    for line in lines:
        try:
            attribute, value = line.split(':', 1)
            if attribute == "State":
                value = value.split("(")[0]
            m.update({attribute: value.strip()})
        except:
            pass
    return m


def filter_attributes(d, filterkeys=["Name", "UUID", "State"]):
    f = {}
    for name in d:
        m = d[name]

        f[m["Name"]] = dict(zip(filterkeys, [m[k] for k in filterkeys]))
    return f


def get_vms(filter=None):
    result = vbox_list()
    d = {}
    for info in result.split("\n\n\n"):
        lines = info.split("\n\n")[0].split("\n")
        m = convert_to_dict(lines)
        try:
            d[m["Name"]] = m
        except:
            pass

    if filter is None:
        return d

    if filter == "simple":
        filterkeys = ["Name", "UUID", "State"]
    else:
        filterkeys = filter

    f = filter_attributes(d, filterkeys)
    return f

print("ALL INFO")
print(70 * "-")
vms = get_vms()

pprint(vms)

print("SMALL INFO")
print(70 * "-")

vms = get_vms("simple")

pprint(vms)


def get_vminfo(name, filter=None):
    data = vbox_vminfo(name).split("\n\n")[0].split("\n")
    m = convert_to_dict(data)
    if filter is None:
        return m

    if filter == "simple":
        filterkeys = ["Name", "UUID", "State"]
    else:
        filterkeys = filter

    f = dict(zip(filterkeys, [m[k] for k in filterkeys]))
    return f


def get_state(name):
    info = get_vminfo(name, filter=["State"])
    return info["State"]


print("OOOO")
name = "compute1.puppetlabs.lan"
pprint(get_vminfo(name))

print("YYYYY")
pprint(get_vminfo(name, "simple"))

print("STATE")
print(get_state(name))
