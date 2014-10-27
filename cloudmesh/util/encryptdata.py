'''simplifing data encryption.

Example::

    password_text = 'super secret'
    plain_text = 'Hello, world'
    encrypted_text = encrypt(plain_text, password_text)
    print plain_text, encrypted_text
    decrypted_text = decrypt(encrypted_text, password_text)
    print decrypted_text

    # Generate some password-like strings and verify encryption/decryption

    import string, random
    chars = string.letters + string.digits
    for i in range(0,100):
        length = random.randint(8,40)
        testdata = ''.join([random.choice(chars) for _ in range(length)])
        if testdata == decrypt(encrypt(testdata, password_text),
                               password_text):
            print i,
        else:
            print testdata, "failed!"
            break


'''
from __future__ import print_function
import os
from hashlib import sha256
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
import uuid
from cloudmesh_install import config_file_prefix


def pad(data, bs):
    """ Pad data to the given blocksize, PKCS-5 style.
    :param data: the data
    :param bs: the blocksize """
    return data + (bs - len(data) % bs) * chr(bs - len(data) % bs)


def unpad(data):
    """ Remove the padding characters.
    :param data: the data
    """
    return data[0:-ord(data[-1])]


def keydigest(key):
    """ Easy way to get a 32-bit key.
    :param key: the key
    """
    return sha256(key).digest()


def encrypt(data, password):
    """
    Encrypts the given data using the password.

    :param data: the data
    :param password: the password
    :rtype: Returns a concatenation of the initialiation vector
            and the encrypted data, base64 encoded so it can be
            qeasily stored as text
    """
    iv = os.urandom(16)
    key = keydigest(password)

    aes = AES.new(key, AES.MODE_CBC, iv)
    cypher = aes.encrypt(pad(data, 16))
    return b64encode(iv + cypher)


def decrypt(data64, password):
    """Decrypts the given data using the password.

    The data64 should be the base64 encoded encrypted value created
    by the encrypt function.

    :param data64: the base64 encoded data
    :param password: the password
    :rtype: Returns decrypted information in data64
    """
    data = b64decode(data64)
    iv = data[:16]
    cypher = data[16:]
    key = keydigest(password)
    aes = AES.new(key, AES.MODE_CBC, iv)
    return unpad(aes.decrypt(cypher))


def encrypt_file(filepath):
    """Encrypt file contents to base64.
    :param filepath: the path of the file.
    """
    try:
        # if it starts with ~
        # os.path.expanduser
        with open(filepath) as inf:
            file_contents = inf.read()
            return file_contents.encode('base64')
    except IOError:
        return filepath


def decrypt_file(content, filename=None):
    """Write a file by descrypting the content and return a filepath.
    :param content: the content to be written
    :param filename: the file name, if non is specified a unique
                     name will be created
    """
    file_contents = content.decode('base64')
    try:
        #
        # to do needs to be replace wit config_file
        #
        uniq_filename = filename or config_file_prefix() + str(uuid.uuid4())
        print(uniq_filename)
        with open(uniq_filename, 'w') as outf:
            outf.write(file_contents)
        outf.close()
        return uniq_filename
    except:
        pass

if __name__ == "__main__":
    print("Easy to use data encryption functions")

    password_text = 'super secret'
    plain_text = 'Hello, world'
    encrypted_text = encrypt(plain_text, password_text)
    print(plain_text, encrypted_text)
    decrypted_text = decrypt(encrypted_text, password_text)
    print(decrypted_text)

    # Generate some password-like strings and verify that
    # encryption/decryption works
    import string
    import random
    chars = string.letters + string.digits
    for i in range(0, 100):
        length = random.randint(8, 40)
        testdata = ''.join([random.choice(chars) for _ in range(length)])
        if testdata == decrypt(encrypt(testdata, password_text),
                               password_text):
            print(i, end=' ')
        else:
            print(testdata, "failed!")
            break
