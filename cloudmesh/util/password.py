import getpass
import platform

input = raw_input

def ask_for_input(label,init_function,echo=False):
    result = input("{0} [{1}]: ".format(label,init_function()))
    if not result:
        result = init_function()
    if echo:
        print "{0}: {1}".format(label,result)
    return result
    
def get_host():
    return ask_for_input("Hostname", platform.node)

def get_user():
    return ask_for_input("Username", getpass.getuser)

def password_valid(password, repeat_password):
    return password == repeat_password and password != "" and password != None 
    
def get_password():
    # inspired by
    # http://stackoverflow.com/questions/1761744/python-read-password-from-stdin

    pprompt = lambda: (getpass.getpass(), getpass.getpass('Retype password: '))
    
    password, repeat_password = pprompt()
    while not password_valid(password, repeat_password):
        print('Passwords do not match or is empty. Try again')
        password, repeat_password = pprompt()

    return password
