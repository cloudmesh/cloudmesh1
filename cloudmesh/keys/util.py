from __future__ import print_function
import base64
import hashlib
import struct
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
    t, keystring, comment = key_parse(entirekey)
    if keystring is not None:
        return key_fingerprint(keystring)
    else:
        return ''


def key_fingerprint(key_string):
    """create the fingerprint form just the key.

    :param key_string: the key
    :type key_string: string
    """
    key = base64.decodestring(key_string)
    fp_plain = hashlib.md5(key).hexdigest()
    return ':'.join(a + b for a, b in zip(fp_plain[::2], fp_plain[1::2]))


def key_parse(keystring):
    """
    parse the keystring/keycontent into type,key,comment
    :param keystring: the content of a key in string format
    """
    # comment section could have a space too
    keysegments = keystring.split(" ", 2)
    keystype = keysegments[0]
    key = None
    comment = None
    if len(keysegments) > 1:
        key = keysegments[1]
        if len(keysegments) > 2:
            comment = keysegments[2]
    return (keystype, key, comment)


def key_validate(keytype, key):
    """reads the key string from a file. THIS FUNCTION HAS A BUG.

    :param key: either the name of  a file that contains the key, or the entire contents of such a file
    :param ketypye: if 'file' the key is read form the file specified in key.
                    if 'string' the key is passed as a string in key
    """
    keystring = "undefined"
    if keytype.lower() == "file":
        try:
            keystring = open(key, "r").read()
        except:
            return False
    elif keytype.lower() == "string":
        keystring = key

    try:

        keytype, key_string, comment = key_parse(keystring)
        data = base64.decodestring(key_string)
        int_len = 4
        str_len = struct.unpack('>I', data[:int_len])[0]
        # this should return 7

        if data[int_len:int_len + str_len] == keytype:
            return True
    except Exception, e:
        print(e)
        return False
    
    
def _keyname_sanitation(username, keyname):
    keynamenew = "%s_%s" % (
        username, keyname.replace('.', '_').replace('@', '_'))
    return keynamenew

# unit testing


def main():
    key1 = "ssh-rsa abcdefg comment"
    key2 = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDD+NswLi/zjz7Vf575eo9iWWku5m4nVSPMgP13JbKCTVKtavAXt8UPZTkYVWiUSeXRqlf+EZM11U8Mq6C/P/ECJS868rn2KSwFosNPF0OOz8zmTvBQShtvBBBVd1kmZePxFGviZbKwe3z3iATLKE8h7pwcupqTin9m3FhQRsGSF7YTFcGXv0ZqxFA2j9+Ix7SVbN5IYxxgwc+mxOzYIy1SKEAOPJQFXKkiXxNdLSzGgjkurhPAIns8MNYL9usKMGzhgp656onGkSbQHZR3ZHsSsTXWP3SV5ih4QTTFunwB6C0TMQVsEGw1P49hhFktb3md+RC4DFP7ZOzfkd9nne2B mycomment"
    print(key_validate("string", key1))
    print(key_validate("string", key2))
    print(key_parse(key1))
    print(key_parse("abcdedfg"))
    print(key_parse("ssh-rsa somestringhere")[2])

if __name__ == "__main__":
    main()
