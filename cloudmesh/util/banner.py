def banner(txt=None, c="#"):
    """prints a banner of the form with a frame of # arround the txt::

      ############################
      # txt
      ############################

    .
    
    :param txt: a text message to be printed
    :type txt: string
    :param c: thecharacter used instead of c
    :type c: character 
    """
    print
    print "#", 70 * c
    print "#", txt
    print "#", 70 * c

