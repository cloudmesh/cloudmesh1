'''simplifing password management'''

import getpass
import platform

input = raw_input


def ask_for_input(label, init_function, echo=False):
    ''' A generic input function that asks for a string and returns it after
    typoing it in

    :param label: the label
    :param init_function: a function that is used to initialize the value
    :param echo: if True, the typed in value is echoed. default is False
    '''
    result = input("{0} [{1}]: ".format(label, init_function()))
    if not result:
        result = init_function()
    if echo:
        print "{0}: {1}".format(label, result)
    return result


def get_host():
    '''
    asks for a hostname and uses the platforms hostname as initial value.
    '''
    return ask_for_input("Hostname", platform.node)


def get_user():
    '''
    asks for a username and uses the username of the current system as the
    initial value.
    '''
    return ask_for_input("Username", getpass.getuser)


def _password_valid(password, repeat_password):
    '''
    internal function that checks if two passwords are the same

    :param password: first password
    :param repeat_password: second password
    '''
    return password == repeat_password and password != "" and \
        password is not None


def get_password():
    '''
    gets a new password while asking twice for it and making sure
    we did not mistype.
    '''
    # inspired by
    # http://stackoverflow.com/questions/1761744/python-read-password-from-stdin

    pprompt = lambda: (getpass.getpass(), getpass.getpass('Retype password: '))

    password, repeat_password = pprompt()
    while not _password_valid(password, repeat_password):
        print('Passwords do not match or is empty. Try again')
        password, repeat_password = pprompt()

    return password
