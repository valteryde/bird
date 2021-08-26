
"""
2021 12. AUGUST
A wrapper for the webview module with inspiration from flask.

This project is diveded into areas that takes care of specefic things.

-- GUI
    pywebview.flowrl.com
    BDS License
    2014-2019 Roman Sirokov and contributors


-- HTML template
    github.com/valteryde
    MIT License
    valtert


-- Wrapper for a wrapper
    github.com/valteryde
    MIT License
    valtert

"""


import webview
import sys
import time
import random
import os
import system


# *** const ***
PID = os.getpid()
TEMPLATE_OPEN = '{python}'
TEMPLATE_CLOSE = '{end}'
CHARS = 'abcdefghijklmnopqrstuvwxyzæøåABCDEFGHIJKLMNOPQRSTUVWXYZLÆØÅ_.,123456789()=?$-@^'
JS_SCRIPT = '<script type="text/javascript">const change = page => {pywebview.api.change(page)}</script>'
CSS = 'html,body {overflow: hidden;} \n *::-webkit-scrollbar {display: none;}'

LANDING = '''
<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">

    <style>
      @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap');
    </style>


  </head>
  <body>

    <img style="position:absolute;top:35%;left:50%;transform:translateX(-50%);height:80px;opacity:.4" src="https://icons.iconarchive.com/icons/iconsmind/outline/128/Bird-icon.png" alt="">
    <h1 style="color:rgb(50,50,50);text-align: center;font-family: 'Roboto', sans-serif;position:absolute;left:50%;top:35%;transform:translateX(-50%)">

    {python}

    l = ['This dosent seem right...', 'Maybe something should have happended?', 'Nobody expects the spanish inquisition!', 'Have you made an "index" view?']
    echo(l[random.randint(0,len(l)-1)])

    {end}

    </h1>

  </body>
</html>
'''


# *** styles(zzzz) ***
def get_style(path):
    return CSS + open(path, 'r', encoding='utf-8').read()



# *** template function
html_msg_holder = []
def echo(msg):
    html_msg_holder.append(msg)

def init():
    html_msg_holder.append(JS_SCRIPT)


# *** htmlpage loader and opener ***
def render_html(path=None, html=None, **kwargs):
    global html_msg_holder

    if path:
        html = open(path, 'r', encoding='utf-8').read()
    elif not html:
        return
    #res = '' #empty string to attatch "good" and correct html

    for key in kwargs:
        if type(kwargs[key]) is str:
            exec(key + '= "' + str(kwargs[key]) + '"')
        else:
            exec(key + '=' + str(kwargs[key]))


    while TEMPLATE_OPEN in html:
        open_index = html.index(TEMPLATE_OPEN)
        close_index = html.index(TEMPLATE_CLOSE)
        code = html[open_index+len(TEMPLATE_OPEN):close_index]
        fcode = '' #formated code
        first_line_found = False #fix identation error
        indentation = 0

        for line in code.split('\n'):
            if len(line) > 0:
                #line = line.replace('echo(','echo(html, ')

                if not first_line_found:
                    for charNum in range(len(line)):
                        if line[charNum] in CHARS:
                            indentation = charNum
                            break
                    first_line_found = True

                fcode += line[indentation:]+'\n'

        exec(fcode)
        html = html[:open_index] + '\n'.join(html_msg_holder) + html[close_index+len(TEMPLATE_CLOSE):]
        html_msg_holder = []

    return html


# *** baseapi class ***
class Api:
    def __init__(self):
        #self._open_() = app._open_
        #instead of only giving the function the
        #whole bird class is given.

        pass


    #method to change page to
    def change(self, page):
        time.sleep(0.1)

        # self._open_ will be given when the api is created.
        try:
            self.bird._open_(page)
        except Exception as e:
            print(e)

        #return 'Skifter til -> {}'.format(page)


# *** main class ***
class Bird:
    """the bird class"""

    def __init__(self, title='My bird app'):
        super(Bird, self).__init__()
        #self.api = Api()
        self.routes = {}
        self.title = title


    def route(self, routingFunction):

        def inner(window):
            args = routingFunction()

            if type(args) is tuple:
                window.load_html(args[0])
                window.load_css(args[1])
            else:
                window.load_html(args)

        self.routes[routingFunction.__name__] = inner


    # function / method to open a page throug a view function
    def _open_(self, nm):
        args = self.routes[nm](webview.windows[0])


    # function / method called when webview spins up.
    def _preload_(self, window):
        self._open_('index')


    def _on_closing_(self):
        os.kill(PID, 9) #bruteforce
        #webview.windows[0].destroy()



    def run(self, api=Api(), debug=False, **kwargs):

        gui = None
        if platform.system().lower() == 'windows':
            gui = 'cef'

        if 'index' not in self.routes.keys():

            @self.route
            def index():
                return render_html(html=LANDING)


        api.bird = self
        window = webview.create_window(self.title, js_api=api, html='', **kwargs)
        window.closing += self._on_closing_
        webview.start(self._preload_, window, debug=debug, gui=gui) #cef


# *** bundle for windows ***
def winbundle(entry='main.py'):
    """
    ::usage::
    Run from terminal in root folder
    You could also zip all the files.

    python3
    > from bird import windowbundle
    > windowbunle() #--> creates a vbs file

    The vbs file along with the root folder
    should not be placed in "application" within windows
    afterwards a shortcut could be made.


    ::bundle architecture::

    .../
        program /
            bird.py
            main.py #entry

            webview (package from github and extracted from pywebview)
            cefpython (package from github)

            launcher.vbs #created


    ::bird settings::

    webview.start(gui="cef") use cef

    extra:
        CSS += '*::-webkit-scrollbar {display: none;}'

    """

    files = []
    for file in os.listdir():
        if file != '.DS_Store' and file != '__pycache__':
            files.append(os.path.join('program',file))


    # create __main__.py
    f = open('launcher.vbs', 'w')

    # oh yes this sucks
    code = '''
Dim objShell
Set objShell = WScript.CreateObject("WScript.Shell")
objShell.Run "python3 {file}"
Set objShell = Nothing
'''.format(file=entry)

    f.write(code)
    return 'succes'

    #return {"build_exe": {'include_files':files}}


# *** bundle for macos ***
def darwinbundle(entry='main.py'):
    """
    ::usage::

    Run from terminal in root folder

    python3
    > from bird import darwinbundle
    > darwinbundle() #--> creates setup.py file with all the files.


    ::bundle architecture::

    .../
        program /
            bird.py
            main.py #entry

            launcher.vbs #created


    ::bird settings::

    webview.start()

    extra:
        CSS -= '*::-webkit-scrollbar {display: none;}'

    """

    files = []
    folders = ''
    for file in os.listdir():
        if file not in ['.DS_Store', '__pycache__', entry, '.git', 'setup.py', 'bird.py']:
            #if file != '.DS_Store' and file != '__pycache__' and file != entry and file != '.git' and file != 'bird.py' and file != 'setup.py':
            if '.' in file:
                files.append(file)
            else:
                folders += 'tree("{}")+'.format(file)

    folders = folders[:-1]


    code = """
#Usage:
#    python setup.py py2app

import os
from setuptools import setup


def tree(src):
    return [(root, map(lambda f: os.path.join(root, f), files))
        for (root, dirs, files) in os.walk(os.path.normpath(src))]


ENTRY_POINT = ['%s']

DATA_FILES = %s + %s
OPTIONS = {
    'argv_emulation': False,
    'strip': True,
    'includes': ['WebKit', 'Foundation', 'webview', 'bird', 'math', 'sys', 'os', 'time', 'random']
}

setup(
    app=ENTRY_POINT,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
    """ % (entry, folders, files)
    #print(code)
    f = open('setup.py', 'w')
    f.write(code)
    f.close()


# pip install automatic ?????? on windows only
