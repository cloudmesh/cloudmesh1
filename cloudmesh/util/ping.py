'''Ping a machine'''
from sh import ping as sh_ping

# from pprint import pprint


def ping(host):
    '''ping the specified host.

    :param host: the name or ip of the host
    '''
    try:
        result = sh_ping("-o", "-c", "1", host).strip().split("\n")
    except:
        pass

    try:
        (attributes, values) = result[-1].replace("round-trip", "")\
            .strip().split("=")
        attributes = attributes.strip().split("/")
        values = values.strip().split("/")

        data = dict(zip(attributes, values))
        data['loss'] = result[-2].split(",")[2].split("%")[0].strip() + "%"
    except:
        data = {}

    data['host'] = host
    return data

# host = "india.futuregrid.org"

# print ping(host)
