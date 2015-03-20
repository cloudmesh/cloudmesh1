'''Ascii menu class'''
from __future__ import print_function


def ascii_menu(title=None, menu_list=None):
    '''
    creates a simple ASCII menu from a list of tuples containing a label
    and a functions refernec. The function should not use parameters.
    :param title: the title of the menu
    :param menu_list: an array of tuples [('label', f1), ...]
    '''
    if not title:
        title = "Menu"

    n = len(menu_list)

    def display():
        index = 1
        print()
        print(title)
        print(len(title) * "=")
        print()
        for (label, function) in menu_list:
            print("    {0} - {1}".format(index, label))
            index += 1
        print("    q - quit")
        print()
        print()

    display()
    running = True
    while running:
        result = raw_input("Select between {0} - {1}: ".format(1, n))
        print("<{0}>".format(result))
        if result.strip() in ["q"]:
            running = False
        else:
            try:
                result = int(result) - 1
                if result >= 0 and result < n:
                    (label, f) = menu_list[result]
                    print("EXECUTING:", label, f.__name__)
                    f()
                else:
                    print("ERROR: wrong selection")
            except Exception, e:
                print("ERROR: ", e)
        display()


def menu_return_num(title=None, menu_list=None, tries=1):
    '''
    creates a simple ASCII menu from a list of labels
    :param title: the title of the menu
    :param menu_list: a list of labels to choose
    :param tries: num of tries till discard
    :return: choice num (head: 0), quit: return 'q'
    '''
    if not title:
        title = "Menu"

    n = len(menu_list)

    def display():
        index = 1
        print()
        print(title)
        print(len(title) * "=")
        print()
        for label in menu_list:
            print("    {0} - {1}".format(index, label))
            index += 1
        print("    q - quit")
        print()
        print()

    display()
    while tries > 0:
        # display()
        result = raw_input("Select between {0} - {1}: ".format(1, n))
        if result == "q":
            return 'q'
        else:
            try:
                result = int(result)
            except:
                print("invalid input...")
                tries = tries - 1
                continue
            if result > 0 and result <= n:
                print("choice {0} selected.".format(result))
                return result - 1
            else:
                print("ERROR: wrong selection")

    return 'q'
