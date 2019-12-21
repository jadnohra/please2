from os import getcwd
from os import listdir
from os.path import isfile, join, expanduser
import re
from please2.util.run import run_get_lines

def run_ssh_get_lines(args, params, tool, ssh_args):
    run_args = ['ssh-{}'.format(tool)]+ssh_args
    return run_get_lines(args, params, run_args)

def get_ssh_files():
    files = []
    try:
        path = expanduser('~/.ssh/')
        files = [f for f in listdir(path) if isfile(join(path, f)) and f.startswith('id_rsa')]
    except:
        pass
    return files

def find_ssh_files(ssh_files, purpose_key, username):
    id_file = None
    pub_id_file = None
    purpose_key = make_valid_filename(purpose_key)
    username = make_valid_filename(username)
    for file in ssh_files:
        if purpose_key in file and username in file:
            if file.endswith('.pub'):
                pub_id_file = file
            else:
                id_file = file
    return id_file, pub_id_file

def make_valid_filename(s):
    s = str(s).strip().replace(' ', '_').replace('.', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

def make_ssh_filename(purpose_key, username):
    filename = 'id_rsa_{}_{}'.format(purpose_key, username)
    return expanduser('~/.ssh/{}'.format(make_valid_filename(filename)))

def ssh_keygen_new(args, params, purpose_key, username):
    ssh_files = get_ssh_files()
    id_file, pub_id_file =  find_ssh_files(ssh_files, purpose_key, username)
    if id_file is not None or pub_id_file is not None:
        return None
    ssh_filename = make_ssh_filename(purpose_key, username)
    ssh_args = ['-t', 'rsa', '-C', '"{}"'.format(username),
                '-f', '{}'.format(ssh_filename)]
    run_ssh_get_lines(args, params, 'keygen', ssh_args)
    return ssh_filename
