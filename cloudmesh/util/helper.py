def vm_name(username, index, n=10000):
    length = len (str(n))
    name = "{0}-{1:0" + str(length) + "d}"
    return name.format(username, index)
