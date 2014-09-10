import base64
import hashlib
from cloudmesh_install.util import path_expand

def read_key(filename):
    key = {}
    key['filename'] = path_expand(filename)
    key['string'] = open(filename, "r").read()
    key['fingerprint'] = get_fingerprint(key['string'])
    return key
    
        
def get_fingerprint(entirekey):
    """returns the fingerprint of a key.
    :param entireky: the key
    :type entirekey: string
    """
    t, keystring, comment = entirekey.split(" ", 2)
    return key_fingerprint(keystring)


def key_fingerprint(key_string):
    """create the fingerprint form just the key.

    :param key_string: the key
    :type key_string: string
    """
    key = base64.decodestring(key_string)
    fp_plain = hashlib.md5(key).hexdigest()
    return ':'.join(a + b for a, b in zip(fp_plain[::2], fp_plain[1::2]))

#
# TODO: this function seems not to work?
#
def key_validate(keytype, key):
    """reads the key string from a file. THIS FUNCTION HAS A BUG.

    :param key: either the name of  a file that contains the key, or the entire contents of such a file
    :param ketypye: if 'file' the key is read form the file specified in key.
                    if 'string' the key is passed as a string in key
    """
    keystring = "undefined"
    if keytype.lower() == "file":
        try:
            keystring = open(filename, "r").read()
        except:
            return False
    elif keytype.lower() == "string":
        keystring = filename

    try:

        keytype, key_string, comment = keystring.split()
        data = base64.decodestring(key_string)
        int_len = 4
        str_len = struct.unpack('>I', data[:int_len])[0]
        # this should return 7

        if data[int_len:int_len + str_len] == keytype:
            return True
    except Exception, e:
        print e
        return False
