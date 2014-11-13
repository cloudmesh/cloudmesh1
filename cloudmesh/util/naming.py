def vm_name(username, index, n=10000):
    length = len(str(n))
    name = "{0}-{1:0" + str(length) + "d}"
    return name.format(username, index)


def server_name_analyzer(name):
    '''
    standard vm name, unless user gives the name, is prefix_index such as abc_11, this
    function returns vm name's prefix and index [prefix, index], if the name is not in
    standard form, returns [input, None]
    '''
    res = [x for x in name.split('_')]
    l = len(res)
    if l == 1:
        return [name, None]

    index = None
    try:
        index = int(res[-1])
    except:
        pass
    if index is None:
        return [name, None]

    prefix = None
    if l > 2:
        del res[-1]
        prefix = "_".join(res)
    else:
        prefix = res[0]
        return [prefix, index]