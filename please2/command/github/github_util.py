import socket
from please2.util.run import run_get_lines

def run_curl_get_lines(args, params, curl_args):
    run_args = ['curl']+curl_args
    return run_get_lines(args, params, run_args)

def github_reg_ssh_key(args, params, username, ssh_filename):
    # curl -u "username" --data '{"title":"test-key","key":"ssh-rsa AAA..."}' https://api.github.com/user/keys
    title = '{}-{}'.format(username, socket.gethostname())
    with open('{}.pub'.format(ssh_filename),'r') as f:
        key = f.read()
    curl_args = ['-u', username, '--data',
                '{{"title":"{}", "key":"{}" }}'.format(title, key),
                'https://api.github.com/user/keys']
    run_curl_get_lines(args, params, curl_args)
