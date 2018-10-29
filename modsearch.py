from os import walk, stat, getcwd, access, R_OK
from time import ctime
import re
from os.path import join, splitext, isdir, exists, expanduser, normpath
from bg.ansi import trucolor, resetbg, color256

def modsearch(path=None, links=True, modified=True, classes=True, functions=True, docs=True, saveas=None, colormode='trucolor', scheme='deepblue', skipdir=''):
    """modsearch(path=None, links=True, modified=True, classes=True, functions=True, 
    docs=True, saveas=None, colormode='trucolor', scheme='deepblue', skipdir='')
    a simple, terminal based python module search, returns a list
    of python files, with classes, functions, methods and heredocs
    with syntax highlighting and optional output to file.
    
    Highlighting includes multiple color schemes as well as support for
    256 colors and trucolor.
    
    It can be used with no arguments and will search the current
    working directory with all display options enabled.
    
    Use the following options to set a search directory and save path,
    disable details and change the formatting of the display.
    path       string, directory path to search
    links      boolean, show clickable links to files
    modified   boolean, show file modified time
    classes    boolean, show classes
    functions  boolean, show functions
    docs       boolean, show heredocs
    saveas     string, file path to a copy of output
    colors     string, set display color mode: none, 256, trucolor
    scheme     string, choose color scheme: 'deepblue', 'chocolate' or 'bright'
    skipdir    directory name to skip in search
    NOTES:
    * if colors=True, output saved to file will include
    ansi codes, which will display normally in a terminal,
    but will not be interpretted correctly by most editors.
    set colors to False to save plain text output.
    * scheme setting has no effect if colors=False
    """

    if path == None:
        path = getcwd()
    else:
        path = expanduser(normpath(path))
    if exists(path):
        if not isdir(path):
            return 'The specified search path is not a directory.'
        if not access(path, R_OK):
            return 'Insufficient privilege to read the specified path.'
    else:
        return 'The specified path does not exist.'

    colorschemes = {
        'deepblue': {
            'pathcolor': {'trucolor': '#0086d2', '256': 'DeepSkyBlue3'},
            'filecolor': {'trucolor': '#fb660a', '256': 'OrangeRed1'},
            'keywordcolor': {'trucolor': '#fb660a', '256': 'OrangeRed1'},
            'functioncolor': {'trucolor': '#cdcaa9', '256': 'LightYellow3'},
            'arglistcolor': {'trucolor': '#0086d2', '256': 'DeepSkyBlue3'},
            'linkcolor': {'trucolor': '#ffffff', '256': 'White'},
            'timestampcolor': {'trucolor': '#0086f7', '256': 'DodgerBlue1'},
            'commentcolor': {'trucolor': '#5bc4bf', '256': 'Aquamarine3'},
            'setbackgroundcolor': '\033[48;2;0;0;11m'
        },
        'chocolate': {
            'pathcolor': {'trucolor': '#ffafd7', '256': 'Pink1'},
            'filecolor': {'trucolor': '#ffd7af', '256': 'NavajoWhite1'},
            'keywordcolor': {'trucolor': '#ffff00', '256': 'Yellow'},
            'functioncolor': {'trucolor': '#ff0000', '256': 'Red'},
            'arglistcolor': {'trucolor': '#ffffd7', '256': 'Cornsilk1'},
            'linkcolor': {'trucolor': '#ff87af', '256': 'PaleVioletRed1'},
            'timestampcolor': {'trucolor': '#ffaf00', '256': 'Orange1'},
            'commentcolor': {'trucolor': '#ffffff', '256': 'Grey100'},
            'setbackgroundcolor': '\033[48;5;234m'
        },
        'bright': {
            'pathcolor': {'trucolor': '#af0087', '256': 'MediumVioletRed'},
            'filecolor': {'trucolor': '#870000', '256': 'DarkRed'},
            'keywordcolor': {'trucolor': '#0000ff', '256': 'Blue1'},
            'functioncolor': {'trucolor': '#005fff', '256': 'DodgerBlue2'},
            'arglistcolor': {'trucolor': '#262626', '256': 'Grey15'},
            'linkcolor': {'trucolor': '#5f00af', '256': 'Purple4'},
            'timestampcolor': {'trucolor': '#00875f', '256': 'SpringGreen4'},
            'commentcolor': {'trucolor': '#000000', '256': 'Black'},
            'setbackgroundcolor': '\033[48;5;15m'
        }
    }
    # output colors
    if not scheme in colorschemes:
        scheme = 'deepblue'
    if colormode == 'trucolor':
        pathcolor = lambda s: trucolor(s, colorschemes[scheme]['pathcolor']['trucolor'])
        filecolor = lambda s: trucolor(s, colorschemes[scheme]['filecolor']['trucolor'])
        keywordcolor = lambda s: trucolor(s, colorschemes[scheme]['keywordcolor']['trucolor'])
        functioncolor = lambda s: trucolor(s, colorschemes[scheme]['functioncolor']['trucolor'])
        arglistcolor = lambda s: trucolor(s, colorschemes[scheme]['arglistcolor']['trucolor'])
        linkcolor = lambda s: trucolor(s, colorschemes[scheme]['linkcolor']['trucolor'])
        timestampcolor = lambda s: trucolor(s, colorschemes[scheme]['timestampcolor']['trucolor'])
        commentcolor = lambda s: trucolor(s, colorschemes[scheme]['commentcolor']['trucolor'])
        setbackground = colorschemes[scheme]['setbackgroundcolor']
        clearbackground = resetbg
    elif colormode == '256':
        pathcolor = lambda s: color256(s, colorschemes[scheme]['pathcolor']['256'])
        filecolor = lambda s: color256(s, colorschemes[scheme]['filecolor']['256'])
        keywordcolor = lambda s: color256(s, colorschemes[scheme]['keywordcolor']['256'])
        functioncolor = lambda s: color256(s, colorschemes[scheme]['functioncolor']['256'])
        arglistcolor = lambda s: color256(s, colorschemes[scheme]['arglistcolor']['256'])
        linkcolor = lambda s: color256(s, colorschemes[scheme]['linkcolor']['256'])
        timestampcolor = lambda s: color256(s, colorschemes[scheme]['timestampcolor']['256'])
        commentcolor = lambda s: color256(s, colorschemes[scheme]['commentcolor']['256'])
        setbackground = colorschemes[scheme]['setbackgroundcolor']
        clearbackground = resetbg
    else:
        pathcolor = lambda s: unjob(s)
        filecolor = lambda s: unjob(s)
        keywordcolor = lambda s: unjob(s)
        functioncolor = lambda s: unjob(s)
        arglistcolor = lambda s: unjob(s)
        linkcolor = lambda s: unjob(s)
        timestampcolor = lambda s: unjob(s)
        commentcolor = lambda s: unjob(s)
        setbackground = ''
        clearbackground = ''

    def unjob(s):
        """unjob(string)
        fake function for lambda
        returns the string it receives, unchanged.
        """
        return s

    tab = '    '
    docIndent = '\n' + tab*3
    rx = re.compile('^\s*((def|class)\s*([a-zA-Z0-9_]+)\s*(\([a-zA-Z0-9_\,\ \=\'\"\*\.]*\))*):[\s]*(\"\"\"([\S\s]*?)\"\"\")*', re.MULTILINE)
    #rx = re.compile('^\s*((def|class)\s*(([^ (:]+)[\s]*([(][^:]+[\)])*)):[\s]*(\"\"\"([\S\s]*?)\"\"\")*', re.MULTILINE)
    out = ''
    lines = []
    for root, dirs, files in walk(path):
        pyfiles = []
        for f in files:
            if splitext(join(root, f))[1] == '.py' and not f == '__init__.py':
                pyfiles.append(f)
        if len(pyfiles)>0:
            lines.append(pathcolor(root))
            for f in pyfiles:
                lines.append(tab + filecolor(f))
                if links == True:
                    lines.append(tab*2 + linkcolor('file://' + re.sub(' ', r'\ ', join(root, f))))
                if modified == True:
                    lines.append(tab*2 + timestampcolor('Modified: ' + str(ctime(stat(join(root, f)).st_mtime))))
                if classes == True or functioncolors == True:
                    with open(join(root, f), "rt") as file:
                        t = file.read()
                    for d in rx.findall(t):
                        if d[1] == 'class' and classes == True:
                            lines.append(tab*2 + keywordcolor(d[1].strip()) + ' ' + \
                            functioncolor(d[2].strip()) + arglistcolor(d[3].strip()))
                            if docs == True and not d[5] == '':
                                [lines.append(tab*3 + commentcolor(s.strip())) for s in d[5].split('\n')]
                        if d[1] == 'def' and functions == True:
                            lines.append(tab*2 + functioncolor(d[2].strip()) + arglistcolor(d[3].strip()))
                            if docs == True and not d[5] == '':
                                [lines.append(tab*3 + commentcolor(s.strip())) for s in d[5].split('\n')]
        if skipdir in dirs:
            dirs.remove(skipdir)

    print(setbackground + '\n' + '\n'.join(lines) + clearbackground)

    if not saveas == None:
        with open(saveas, 'wt') as f:
            f.write(setbackground + '\n' + '\n'.join(lines) + clearbackground)
        print('output saved to:', saveas)
