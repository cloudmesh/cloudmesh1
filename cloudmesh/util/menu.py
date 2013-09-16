'''Ascii menu class'''

def ascii_menu(title=None, menu_list=None):
    '''
    creates a simple ASCII menu from a list of tuples containing a label and a functions refernec. The function should not use parameters.
    :param title: the title of the menu
    :param menu_list: an array of tuples [('label', f1), ...]
    '''
    if not title:
        title = "Menu"

    n = len(menu_list)

    def display():
        index = 1
        print
        print title
        print len(title) * "="
        print
        for (label, function) in menu_list:
            print "    {0} - {1}".format(index, label)
            index += 1
        print "    q - quit"
        print
        print

    display()
    while True:
        result = input("Select between {0} - {1}: ".format(1, n))
        print "<{0}>".format(result)
        if result == "q":
            break
        else:
            try:
                result = int(result) - 1
                if result > 0 and result < n:
                    (label, f) = menu_list[result]
                    print "EXECUTING:", label, f.__name__
                    f()
                else:
                    print "ERROR: wrong selection"
            except Exception, e:
                print "ERROR: ", e
        display()

