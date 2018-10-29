# PythonModuleSearch
Python module search, lists all Python files with classes, function, methods and heredocs with optional syntax highlighting and output to file

modsearch(path=None, links=True, modified=True, classes=True, functions=True, docs=True, saveas=None, colormode='trucolor', scheme='deepblue', skipdir='')
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
    
    NOTE: ansi.py includes some code which isn't necessary for modsearch.py. 
    It's my personal collection of useful ansi stuff and it was easier to 
    upload it in its entirety.
