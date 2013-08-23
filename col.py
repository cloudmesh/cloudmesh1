
# value between 0 and 1 (percent)   
def color(value) :
    # y = mx + b
    # m = 4
    # x = value
    # y = RGB__
    if (0 <= value and value <= 1/8) :
        RGB_R = 0
        RGB_G = 0
        RGB_B = 4*value + .5 # .5 - 1 # b = 1/2
    elif (1/8 < value and value <= 3/8) :
        RGB_R = 0
        RGB_G = 4*value - .5 # 0 - 1 # b = - 1/2
        RGB_B = 0
    elif (3/8 < value and value <= 5/8) :
        RGB_R = 4*value - 1.5 # 0 - 1 # b = - 3/2
        RGB_G = 1
        RGB_B = -4*value + 2.5 # 1 - 0 # b = 5/2
    elif (5/8 < value and value <= 7/8) :
        RGB_R = 1
        RGB_G = -4*value + 3.5 # 1 - 0 # b = 7/2
        RGB_B = 0
    elif (7/8 < value and value <= 1) :
        RGB_R = -4*value + 4.5 # 1 - .5 # b = 9/2
        RGB_G = 0
        RGB_B = 0
    else :    # should never happen - value > 1
        RGB_R = .5
        RGB_G = 0
        RGB_B = 0
    

    # scale for hex conversion
    RGB_R *= 15
    RGB_G *= 15
    RGB_B *= 15

    return "{0:02X}-{1:02X}-{2:02X}".format(int(round(RGB_R)),int(round(RGB_G)),int(round(RGB_B)))

for i in [0,0.1,0.2,0.3,0.4,0.5]:
     print color(i)
