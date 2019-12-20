from os import getcwd
from os import listdir
from os.path import isfile, join
from please2.util.run import run_get_stdout, run_get_lines

def run_ssh_keygen_get_stdout(args, params, ssh_args):
    run_args = ['ssh-keygen']+ssh_args
    return run_get_stdout(args, params, run_args)

def get_ssh_files():
    files = []
    try:
        path = '~/.ssh'
        files = [f for f in listdir(path) if isfile(join(path, f)) and f.startswith('id_rsa')]
    except:
        pass
    return files

def find_purpose_key_files(ssh_files, purpose_key):
    id_file = None
    pub_id_file = None
    for file in ssh_files:
        if file.contains(purpose_key):
            if file.endswith('.pub'):
                pub_id_file = file
            else:
                id_file = file
    return id_file, pub_id_file

def ssh_keygen_new_interactive(args, params, purpose_key, email=None):
    if email is None:
        email = str(input("email: "))
    ssh_files = get_ssh_files()
    id_file, pub_id_file = find_purpose_key_files(ssh_files, purpose_key)
    if id_file is not None or pub_id_file is not None:
        print("Unfortunately, it seems you have some residual files: {}, {}".format(id_file, pub_id_file))
        return
