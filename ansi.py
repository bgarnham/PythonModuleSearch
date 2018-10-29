#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ansi:
    A collection of functions and classes for formatting terminal
    output using ANSI escape codes.
    """

import re

resetfg = '\033[38;0;39m'

resetbg = '\033[48;0;49m'

fullreset = '\033[0;0m'

def bold(string):
    """bold(string)
    returns string wrapped in tags for bold text
    a full reset is used which will reset the background as well.
    """
    return '\033[1m{}{}'.format(string, fullreset)

def italic(string):
    """italic(string)
    returns string wrapped in tags for italic text
    a full reset is used which will reset the background as well.
    """
    return '\033[3m{}{}'.format(string, fullreset)

def underline(string):
    """underline(string)
    returns string wrapped in tags for underlined text
    a full reset is used which will reset the background as well.
    """
    return '\033[4m{}{}'.format(string, fullreset)

def reverse(string):
    """reverse(string)
    returns string wrapped in tags for reverse color text
    a full reset is used which will reset the background as well.
    """
    return '\033[7m{}{}'.format(string, fullreset)

def hex256id(hexstring):
    """hex256id(hexstring)
    return the equivalent color id for a hex color
    """
    if _validhex(hexstring):
        r, g, b = _parsehex(hexstring)
        return guess256id(r, g, b)
    else:
        return False

def hex2rgb(string):
    """hex2rgb(string)
    return the integer value of a string, base 16
    """
    return int(string, 16)

def _parsehex(hexstring):
    """_parsehex(hexstring)
    split string and convert hex values to rgb
    """
    r = hex2rgb(hexstring[1:3])
    g = hex2rgb(hexstring[3:5])
    b = hex2rgb(hexstring[5:7])
    return r, g, b

def _validhex(hexstring):
    """_validhex(hexstring)
    validate a string as being a hex color value
    """
    if  len(hexstring) == 7 and hexstring[0] == '#' and \
        re.match('[0-9A-Fa-f]', hexstring[1]) and \
        re.match('[0-9A-Fa-f]', hexstring[2]) and \
        re.match('[0-9A-Fa-f]', hexstring[3]) and \
        re.match('[0-9A-Fa-f]', hexstring[4]) and \
        re.match('[0-9A-Fa-f]', hexstring[5]) and \
        re.match('[0-9A-Fa-f]', hexstring[6]):
        return True
    else:
        return False

def _validrgb(r, g, b):
    """_validrgb(int, int, int)
    validate three ints as valid rgb values
    """
    if  type(r) == int and r > -1 and r < 256 and \
        type(g) == int and g > -1 and g < 256 and \
        type(b) == int and b > -1 and b < 256:
        return True
    else:
        return False

def trucolor(string, *args):
    """trucolor(string, *args)
    Accepts a string and either a hex string: '#adadad' or
    three integers for rgb: 120, 50, 77 and returns
    the string wrapped in the appropriate color tags
    """
    if len(args) == 1 and _validhex(args[0]):
            r, g, b = _parsehex(args[0])
            return '\033[38;2;{};{};{}m{}{}'.format(r,g,b,string,resetfg)
    elif len(args) == 3 and _validrgb(args[0], args[1], args[2]):
            return '\033[38;2;{};{};{}m{}{}'.format(args[0], args[1], args[2], string, resetfg)
    else:
        return False

def color256(string, *args):
    """color256(string, *args)
    Accepts a string and a color. The color can be
    a hex string, three ints for rgb or a 256 color name
    returns the string wrapped in color tags approximating
    the value given if hex or rgb or the exact color if color name
    """
    if len(args) == 1 and _validhex(args[0]):
            r, g, b = _parsehex(args[0])
            return '\033[38;5;{}m{}{}'.format(str(guess256id(r, g, b)), string, resetfg)
    elif len(args) == 3 and _validrgb(args[0], args[1], args[2]):
            return '\033[38;5;{}m{}{}'.format(str(guess256id(args[0], args[1], args[2])), string, resetfg)
    elif len(args) == 1 and args[0] in colornames:
        return '\033[38;5;{}m{}{}'.format(str(colornames.get(args[0])), string, resetfg)

def bg(color):
    """bg(color)
    Accepts a X11 color name and returns a background color opening tag
    """
    return '\033[48;5;' + str(colornames.get(color,0)) + 'm'

def guess256id(r, g, b):
    """guess256id(int, int, int)
    a highly simplistic and questionable method to approximate
    a 24 bit color using the 256 terminal preset colors,
    which is giving better results than anything else,
    so far. I don't know why. I'm guessing it's luck
    """
    id = 'x'
    diff = 765
    for i in rgbvalues:
        this = abs(r - rgbvalues[i]['r'])
        this += abs(g - rgbvalues[i]['g'])
        this += abs(b - rgbvalues[i]['b'])
        if this < diff:
            id = i
            diff = this
    return id

def color16(string,color):
    """color16(string,colorstring)
    returns string wrapped in 16 color tags. Format tags
    can be combined but should be placed inside of the color tags
    as the color tags will override other formatting. Uses
    names from classes normal and normal.intense
    """
    return '\033[0;{}m{}{}'.format(color, string, fullreset)

colornames = {
    'Black': 0, 'Maroon': 1, 'Green': 2, 'Olive': 3, 'Navy': 4,
    'Purple': 129, 'Teal': 6, 'Silver': 7, 'Grey': 8, 'Red': 9,
    'Lime': 10, 'Yellow': 11, 'Blue': 12, 'Fuchsia': 13, 'Aqua': 14,
    'White': 15, 'Grey0': 16, 'NavyBlue': 17, 'DarkBlue': 18,
    'Blue3': 20, 'Blue1': 21, 'DarkGreen': 22, 'DeepSkyBlue4': 25,
    'DodgerBlue3': 26, 'DodgerBlue2': 27, 'Green4': 28,
    'SpringGreen4': 29, 'Turquoise4': 30, 'DeepSkyBlue3': 32,
    'DodgerBlue1': 33, 'Green3': 40, 'SpringGreen3': 41,
    'DarkCyan': 36, 'LightSeaGreen': 37, 'DeepSkyBlue2': 38,
    'DeepSkyBlue1': 39, 'SpringGreen2': 47, 'Cyan3': 43,
    'DarkTurquoise': 44, 'Turquoise2': 45, 'Green1': 46,
    'SpringGreen1': 48, 'MediumSpringGreen': 49, 'Cyan2': 50,
    'Cyan1': 51, 'DarkRed': 88, 'DeepPink4': 125, 'Purple4': 55,
    'Purple3': 56, 'BlueViolet': 57, 'Orange4': 94, 'Grey37': 59,
    'MediumPurple4': 60, 'SlateBlue3': 62, 'RoyalBlue1': 63,
    'Chartreuse4': 64, 'DarkSeaGreen4': 71, 'PaleTurquoise4': 66,
    'SteelBlue': 67, 'SteelBlue3': 68, 'CornflowerBlue': 69,
    'Chartreuse3': 76, 'CadetBlue': 73, 'SkyBlue3': 74,
    'SteelBlue1': 81, 'PaleGreen3': 114, 'SeaGreen3': 78,
    'Aquamarine3': 79, 'MediumTurquoise': 80, 'Chartreuse2': 112,
    'SeaGreen2': 83, 'SeaGreen1': 85, 'Aquamarine1': 122,
    'DarkSlateGray2': 87, 'DarkMagenta': 91, 'DarkViolet': 128,
    'LightPink4': 95, 'Plum4': 96, 'MediumPurple3': 98,
    'SlateBlue1': 99, 'Yellow4': 106, 'Wheat4': 101, 'Grey53': 102,
    'LightSlateGrey': 103, 'MediumPurple': 104, 'LightSlateBlue': 105,
    'DarkOliveGreen3': 149, 'DarkSeaGreen': 108, 'LightSkyBlue3': 110,
    'SkyBlue2': 111, 'DarkSeaGreen3': 150, 'DarkSlateGray3': 116,
    'SkyBlue1': 117, 'Chartreuse1': 118, 'LightGreen': 120,
    'PaleGreen1': 156, 'DarkSlateGray1': 123, 'Red3': 160,
    'MediumVioletRed': 126, 'Magenta3': 164, 'DarkOrange3': 166,
    'IndianRed': 167, 'HotPink3': 168, 'MediumOrchid3': 133,
    'MediumOrchid': 134, 'MediumPurple2': 140, 'DarkGoldenrod': 136,
    'LightSalmon3': 173, 'RosyBrown': 138, 'Grey63': 139,
    'MediumPurple1': 141, 'Gold3': 178, 'DarkKhaki': 143,
    'NavajoWhite3': 144, 'Grey69': 145, 'LightSteelBlue3': 146,
    'LightSteelBlue': 147, 'Yellow3': 184, 'DarkSeaGreen2': 157,
    'LightCyan3': 152, 'LightSkyBlue1': 153, 'GreenYellow': 154,
    'DarkOliveGreen2': 155, 'DarkSeaGreen1': 193, 'PaleTurquoise1': 159,
    'DeepPink3': 162, 'Magenta2': 200, 'HotPink2': 169, 'Orchid': 170,
    'MediumOrchid1': 207, 'Orange3': 172, 'LightPink3': 174, 'Pink3': 175,
    'Plum3': 176, 'Violet': 177, 'LightGoldenrod3': 179, 'Tan': 180,
    'MistyRose3': 181, 'Thistle3': 182, 'Plum2': 183, 'Khaki3': 185,
    'LightGoldenrod2': 222, 'LightYellow3': 187, 'Grey84': 188,
    'LightSteelBlue1': 189, 'Yellow2': 190, 'DarkOliveGreen1': 192,
    'Honeydew2': 194, 'LightCyan1': 195, 'Red1': 196, 'DeepPink2': 197,
    'DeepPink1': 199, 'Magenta1': 201, 'OrangeRed1': 202, 'IndianRed1': 204,
    'HotPink': 206, 'DarkOrange': 208, 'Salmon1': 209, 'LightCoral': 210,
    'PaleVioletRed1': 211, 'Orchid2': 212, 'Orchid1': 213, 'Orange1': 214,
    'SandyBrown': 215, 'LightSalmon1': 216, 'LightPink1': 217, 'Pink1': 218,
    'Plum1': 219, 'Gold1': 220, 'NavajoWhite1': 223, 'MistyRose1': 224,
    'Thistle1': 225, 'Yellow1': 226, 'LightGoldenrod1': 227, 'Khaki1': 228,
    'Wheat1': 229, 'Cornsilk1': 230, 'Grey100': 231, 'Grey3': 232, 'Grey7': 233,
    'Grey11': 234, 'Grey15': 235, 'Grey19': 236, 'Grey23': 237, 'Grey27': 238,
    'Grey30': 239, 'Grey35': 240, 'Grey39': 241, 'Grey42': 242, 'Grey46': 243,
    'Grey50': 244, 'Grey54': 245, 'Grey58': 246, 'Grey62': 247, 'Grey66': 248,
    'Grey70': 249, 'Grey74': 250, 'Grey78': 251, 'Grey82': 252, 'Grey85': 253,
    'Grey89': 254, 'Grey93': 255
}

rgbvalues = {
    0: {'r': 0, 'g': 0, 'b': 0}, 1: {'r': 128, 'g': 0, 'b': 0}, 2: {'r': 0, 'g': 128, 'b': 0},
    3: {'r': 128, 'g': 128, 'b': 0}, 4: {'r': 0, 'g': 0, 'b': 128}, 5: {'r': 128, 'g': 0, 'b': 128},
    6: {'r': 0, 'g': 128, 'b': 128}, 7: {'r': 192, 'g': 192, 'b': 192}, 8: {'r': 128, 'g': 128, 'b': 128},
    9: {'r': 255, 'g': 0, 'b': 0}, 10: {'r': 0, 'g': 255, 'b': 0}, 11: {'r': 255, 'g': 255, 'b': 0},
    12: {'r': 0, 'g': 0, 'b': 255}, 13: {'r': 255, 'g': 0, 'b': 255}, 14: {'r': 0, 'g': 255, 'b': 255},
    15: {'r': 255, 'g': 255, 'b': 255}, 16: {'r': 0, 'g': 0, 'b': 0}, 17: {'r': 0, 'g': 0, 'b': 95},
    18: {'r': 0, 'g': 0, 'b': 135}, 19: {'r': 0, 'g': 0, 'b': 175}, 20: {'r': 0, 'g': 0, 'b': 215},
    21: {'r': 0, 'g': 0, 'b': 255}, 22: {'r': 0, 'g': 95, 'b': 0}, 23: {'r': 0, 'g': 95, 'b': 95},
    24: {'r': 0, 'g': 95, 'b': 135}, 25: {'r': 0, 'g': 95, 'b': 175}, 26: {'r': 0, 'g': 95, 'b': 215},
    27: {'r': 0, 'g': 95, 'b': 255}, 28: {'r': 0, 'g': 135, 'b': 0}, 29: {'r': 0, 'g': 135, 'b': 95},
    30: {'r': 0, 'g': 135, 'b': 135}, 31: {'r': 0, 'g': 135, 'b': 175}, 32: {'r': 0, 'g': 135, 'b': 215},
    33: {'r': 0, 'g': 135, 'b': 255}, 34: {'r': 0, 'g': 175, 'b': 0}, 35: {'r': 0, 'g': 175, 'b': 95},
    36: {'r': 0, 'g': 175, 'b': 135}, 37: {'r': 0, 'g': 175, 'b': 175}, 38: {'r': 0, 'g': 175, 'b': 215},
    39: {'r': 0, 'g': 175, 'b': 255}, 40: {'r': 0, 'g': 215, 'b': 0}, 41: {'r': 0, 'g': 215, 'b': 95},
    42: {'r': 0, 'g': 215, 'b': 135}, 43: {'r': 0, 'g': 215, 'b': 175}, 44: {'r': 0, 'g': 215, 'b': 215},
    45: {'r': 0, 'g': 215, 'b': 255}, 46: {'r': 0, 'g': 255, 'b': 0}, 47: {'r': 0, 'g': 255, 'b': 95},
    48: {'r': 0, 'g': 255, 'b': 135}, 49: {'r': 0, 'g': 255, 'b': 175}, 50: {'r': 0, 'g': 255, 'b': 215},
    51: {'r': 0, 'g': 255, 'b': 255}, 52: {'r': 95, 'g': 0, 'b': 0}, 53: {'r': 95, 'g': 0, 'b': 95},
    54: {'r': 95, 'g': 0, 'b': 135}, 55: {'r': 95, 'g': 0, 'b': 175}, 56: {'r': 95, 'g': 0, 'b': 215},
    57: {'r': 95, 'g': 0, 'b': 255}, 58: {'r': 95, 'g': 95, 'b': 0}, 59: {'r': 95, 'g': 95, 'b': 95},
    60: {'r': 95, 'g': 95, 'b': 135}, 61: {'r': 95, 'g': 95, 'b': 175}, 62: {'r': 95, 'g': 95, 'b': 215},
    63: {'r': 95, 'g': 95, 'b': 255}, 64: {'r': 95, 'g': 135, 'b': 0}, 65: {'r': 95, 'g': 135, 'b': 95},
    66: {'r': 95, 'g': 135, 'b': 135}, 67: {'r': 95, 'g': 135, 'b': 175}, 68: {'r': 95, 'g': 135, 'b': 215},
    69: {'r': 95, 'g': 135, 'b': 255}, 70: {'r': 95, 'g': 175, 'b': 0}, 71: {'r': 95, 'g': 175, 'b': 95},
    72: {'r': 95, 'g': 175, 'b': 135}, 73: {'r': 95, 'g': 175, 'b': 175}, 74: {'r': 95, 'g': 175, 'b': 215},
    75: {'r': 95, 'g': 175, 'b': 255}, 76: {'r': 95, 'g': 215, 'b': 0}, 77: {'r': 95, 'g': 215, 'b': 95},
    78: {'r': 95, 'g': 215, 'b': 135}, 79: {'r': 95, 'g': 215, 'b': 175}, 80: {'r': 95, 'g': 215, 'b': 215},
    81: {'r': 95, 'g': 215, 'b': 255}, 82: {'r': 95, 'g': 255, 'b': 0}, 83: {'r': 95, 'g': 255, 'b': 95},
    84: {'r': 95, 'g': 255, 'b': 135}, 85: {'r': 95, 'g': 255, 'b': 175}, 86: {'r': 95, 'g': 255, 'b': 215},
    87: {'r': 95, 'g': 255, 'b': 255}, 88: {'r': 135, 'g': 0, 'b': 0}, 89: {'r': 135, 'g': 0, 'b': 95},
    90: {'r': 135, 'g': 0, 'b': 135}, 91: {'r': 135, 'g': 0, 'b': 175}, 92: {'r': 135, 'g': 0, 'b': 215},
    93: {'r': 135, 'g': 0, 'b': 255}, 94: {'r': 135, 'g': 95, 'b': 0}, 95: {'r': 135, 'g': 95, 'b': 95},
    96: {'r': 135, 'g': 95, 'b': 135}, 97: {'r': 135, 'g': 95, 'b': 175}, 98: {'r': 135, 'g': 95, 'b': 215},
    99: {'r': 135, 'g': 95, 'b': 255}, 100: {'r': 135, 'g': 135, 'b': 0}, 101: {'r': 135, 'g': 135, 'b': 95},
    102: {'r': 135, 'g': 135, 'b': 135}, 103: {'r': 135, 'g': 135, 'b': 175}, 104: {'r': 135, 'g': 135, 'b': 215},
    105: {'r': 135, 'g': 135, 'b': 255}, 106: {'r': 135, 'g': 175, 'b': 0}, 107: {'r': 135, 'g': 175, 'b': 95},
    108: {'r': 135, 'g': 175, 'b': 135}, 109: {'r': 135, 'g': 175, 'b': 175}, 110: {'r': 135, 'g': 175, 'b': 215},
    111: {'r': 135, 'g': 175, 'b': 255}, 112: {'r': 135, 'g': 215, 'b': 0}, 113: {'r': 135, 'g': 215, 'b': 95},
    114: {'r': 135, 'g': 215, 'b': 135}, 115: {'r': 135, 'g': 215, 'b': 175}, 116: {'r': 135, 'g': 215, 'b': 215},
    117: {'r': 135, 'g': 215, 'b': 255}, 118: {'r': 135, 'g': 255, 'b': 0}, 119: {'r': 135, 'g': 255, 'b': 95},
    120: {'r': 135, 'g': 255, 'b': 135}, 121: {'r': 135, 'g': 255, 'b': 175}, 122: {'r': 135, 'g': 255, 'b': 215},
    123: {'r': 135, 'g': 255, 'b': 255}, 124: {'r': 175, 'g': 0, 'b': 0}, 125: {'r': 175, 'g': 0, 'b': 95},
    126: {'r': 175, 'g': 0, 'b': 135}, 127: {'r': 175, 'g': 0, 'b': 175}, 128: {'r': 175, 'g': 0, 'b': 215},
    129: {'r': 175, 'g': 0, 'b': 255}, 130: {'r': 175, 'g': 95, 'b': 0}, 131: {'r': 175, 'g': 95, 'b': 95},
    132: {'r': 175, 'g': 95, 'b': 135}, 133: {'r': 175, 'g': 95, 'b': 175}, 134: {'r': 175, 'g': 95, 'b': 215},
    135: {'r': 175, 'g': 95, 'b': 255}, 136: {'r': 175, 'g': 135, 'b': 0}, 137: {'r': 175, 'g': 135, 'b': 95},
    138: {'r': 175, 'g': 135, 'b': 135}, 139: {'r': 175, 'g': 135, 'b': 175}, 140: {'r': 175, 'g': 135, 'b': 215},
    141: {'r': 175, 'g': 135, 'b': 255}, 142: {'r': 175, 'g': 175, 'b': 0}, 143: {'r': 175, 'g': 175, 'b': 95},
    144: {'r': 175, 'g': 175, 'b': 135}, 145: {'r': 175, 'g': 175, 'b': 175}, 146: {'r': 175, 'g': 175, 'b': 215},
    147: {'r': 175, 'g': 175, 'b': 255}, 148: {'r': 175, 'g': 215, 'b': 0}, 149: {'r': 175, 'g': 215, 'b': 95},
    150: {'r': 175, 'g': 215, 'b': 135}, 151: {'r': 175, 'g': 215, 'b': 175}, 152: {'r': 175, 'g': 215, 'b': 215},
    153: {'r': 175, 'g': 215, 'b': 255}, 154: {'r': 175, 'g': 255, 'b': 0}, 155: {'r': 175, 'g': 255, 'b': 95},
    156: {'r': 175, 'g': 255, 'b': 135}, 157: {'r': 175, 'g': 255, 'b': 175}, 158: {'r': 175, 'g': 255, 'b': 215},
    159: {'r': 175, 'g': 255, 'b': 255}, 160: {'r': 215, 'g': 0, 'b': 0}, 161: {'r': 215, 'g': 0, 'b': 95},
    162: {'r': 215, 'g': 0, 'b': 135}, 163: {'r': 215, 'g': 0, 'b': 175}, 164: {'r': 215, 'g': 0, 'b': 215},
    165: {'r': 215, 'g': 0, 'b': 255}, 166: {'r': 215, 'g': 95, 'b': 0}, 167: {'r': 215, 'g': 95, 'b': 95},
    168: {'r': 215, 'g': 95, 'b': 135}, 169: {'r': 215, 'g': 95, 'b': 175}, 170: {'r': 215, 'g': 95, 'b': 215},
    171: {'r': 215, 'g': 95, 'b': 255}, 172: {'r': 215, 'g': 135, 'b': 0}, 173: {'r': 215, 'g': 135, 'b': 95},
    174: {'r': 215, 'g': 135, 'b': 135}, 175: {'r': 215, 'g': 135, 'b': 175}, 176: {'r': 215, 'g': 135, 'b': 215},
    177: {'r': 215, 'g': 135, 'b': 255}, 178: {'r': 215, 'g': 175, 'b': 0}, 179: {'r': 215, 'g': 175, 'b': 95},
    180: {'r': 215, 'g': 175, 'b': 135}, 181: {'r': 215, 'g': 175, 'b': 175}, 182: {'r': 215, 'g': 175, 'b': 215},
    183: {'r': 215, 'g': 175, 'b': 255}, 184: {'r': 215, 'g': 215, 'b': 0}, 185: {'r': 215, 'g': 215, 'b': 95},
    186: {'r': 215, 'g': 215, 'b': 135}, 187: {'r': 215, 'g': 215, 'b': 175}, 188: {'r': 215, 'g': 215, 'b': 215},
    189: {'r': 215, 'g': 215, 'b': 255}, 190: {'r': 215, 'g': 255, 'b': 0}, 191: {'r': 215, 'g': 255, 'b': 95},
    192: {'r': 215, 'g': 255, 'b': 135}, 193: {'r': 215, 'g': 255, 'b': 175}, 194: {'r': 215, 'g': 255, 'b': 215},
    195: {'r': 215, 'g': 255, 'b': 255}, 196: {'r': 255, 'g': 0, 'b': 0}, 197: {'r': 255, 'g': 0, 'b': 95},
    198: {'r': 255, 'g': 0, 'b': 135}, 199: {'r': 255, 'g': 0, 'b': 175}, 200: {'r': 255, 'g': 0, 'b': 215},
    201: {'r': 255, 'g': 0, 'b': 255}, 202: {'r': 255, 'g': 95, 'b': 0}, 203: {'r': 255, 'g': 95, 'b': 95},
    204: {'r': 255, 'g': 95, 'b': 135}, 205: {'r': 255, 'g': 95, 'b': 175}, 206: {'r': 255, 'g': 95, 'b': 215},
    207: {'r': 255, 'g': 95, 'b': 255}, 208: {'r': 255, 'g': 135, 'b': 0}, 209: {'r': 255, 'g': 135, 'b': 95},
    210: {'r': 255, 'g': 135, 'b': 135}, 211: {'r': 255, 'g': 135, 'b': 175}, 212: {'r': 255, 'g': 135, 'b': 215},
    213: {'r': 255, 'g': 135, 'b': 255}, 214: {'r': 255, 'g': 175, 'b': 0}, 215: {'r': 255, 'g': 175, 'b': 95},
    216: {'r': 255, 'g': 175, 'b': 135}, 217: {'r': 255, 'g': 175, 'b': 175}, 218: {'r': 255, 'g': 175, 'b': 215},
    219: {'r': 255, 'g': 175, 'b': 255}, 220: {'r': 255, 'g': 215, 'b': 0}, 221: {'r': 255, 'g': 215, 'b': 95},
    222: {'r': 255, 'g': 215, 'b': 135}, 223: {'r': 255, 'g': 215, 'b': 175}, 224: {'r': 255, 'g': 215, 'b': 215},
    225: {'r': 255, 'g': 215, 'b': 255}, 226: {'r': 255, 'g': 255, 'b': 0}, 227: {'r': 255, 'g': 255, 'b': 95},
    228: {'r': 255, 'g': 255, 'b': 135}, 229: {'r': 255, 'g': 255, 'b': 175}, 230: {'r': 255, 'g': 255, 'b': 215},
    231: {'r': 255, 'g': 255, 'b': 255}, 232: {'r': 8, 'g': 8, 'b': 8}, 233: {'r': 18, 'g': 18, 'b': 18},
    234: {'r': 28, 'g': 28, 'b': 28}, 235: {'r': 38, 'g': 38, 'b': 38}, 236: {'r': 48, 'g': 48, 'b': 48},
    237: {'r': 58, 'g': 58, 'b': 58}, 238: {'r': 68, 'g': 68, 'b': 68}, 239: {'r': 78, 'g': 78, 'b': 78},
    240: {'r': 88, 'g': 88, 'b': 88}, 241: {'r': 98, 'g': 98, 'b': 98}, 242: {'r': 108, 'g': 108, 'b': 108},
    243: {'r': 118, 'g': 118, 'b': 118}, 244: {'r': 128, 'g': 128, 'b': 128}, 245: {'r': 138, 'g': 138, 'b': 138},
    246: {'r': 148, 'g': 148, 'b': 148}, 247: {'r': 158, 'g': 158, 'b': 158}, 248: {'r': 168, 'g': 168, 'b': 168},
    249: {'r': 178, 'g': 178, 'b': 178}, 250: {'r': 188, 'g': 188, 'b': 188}, 251: {'r': 198, 'g': 198, 'b': 198},
    252: {'r': 208, 'g': 208, 'b': 208}, 253: {'r': 218, 'g': 218, 'b': 218}, 254: {'r': 228, 'g': 228, 'b': 228},
    255: {'r': 238, 'g': 238, 'b': 238}
}

class normal:
    """normal
    X11 color ids for normal text, nnormal colors
    """
    black = '30'
    red = '31'
    green = '32'
    yellow = '33'
    blue = '34'
    purple = '35'
    cyan = '36'
    white = '37'
    class intense:
        """normal.intense
        X11 color ids for normal text, intense colors
        """
        black = '90'
        red = '91'
        green = '92'
        yellow = '93'
        blue = '94'
        purple = '95'
        cyan = '96'
        white = '97'

class background:
    """background
    X11 color ids for screen or background, normal colors
    """
    black = '40'
    red = '41'
    green = '42'
    yellow = '43'
    blue = '44'
    purple = '45'
    cyan = '46'
    white = '47'
    class intense:
        """background.intense
        X11 color ids for screen or background, intense colors
        """
        black = '100'
        red = '101'
        green = '102'
        yellow = '103'
        blue = '104'
        purple = '105'
        cyan = '106'
        white = '107'
