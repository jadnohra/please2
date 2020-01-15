import platform
import filetype
import shutil
import os
from imgcat import imgcat
from .run import run

def _darwin_is_iterm():
    return 'iterm' in os.environ.get('TERM_PROGRAM', '').lower()

def display_image(args, params, filename):
    run_kwargs = {}
    if platform.system().lower() == 'darwin':
        if _darwin_is_iterm():
            imgcat(open(filename))
            return
        else:
            tool_name = 'open'
            run_kwargs['shell'] = True
    else:
        tool_name = 'eog'
    tool_args = [tool_name, filename]
    run(args, params, tool_args, asnc=True, run_kwargs=run_kwargs)

def display_any_os(args, params, filename):
    tool_name = 'eog'
    if platform.system().lower() == 'darwin':
        tool_name = 'open'
    else:
        tool_name = 'xdg-open'
    eog_args = [tool_name, filename]
    run(args, params, eog_args, asnc=True)

def display_raw(filename):
    # TODO: don't do this for large files
    with open(filename) as fi:
        text = fi.read()
        print(text)

def display_any(args, params, filename):
    kind = filetype.guess(filename)
    if kind is None:
        display_raw(filename)
    elif 'image' in kind.mime:
        display_image(args, params, filename)
    else:
        display_any_os(args, params, filename)
