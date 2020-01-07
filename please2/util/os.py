import platform
from .run import run

def display_image(args, params, path):
    tool_name = 'eog'
    if platform.system().lower() == 'darwin':
        tool_name = 'open'
    eog_args = [tool_name, path]
    run(args, params, eog_args, asnc=True)
