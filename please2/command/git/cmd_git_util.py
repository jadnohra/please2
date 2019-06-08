from os import getcwd
import subprocess

def is_in_git_repo(params):
    working_dir = params.get('@', getcwd())
    result = subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'], stdout=subprocess.PIPE, cwd=working_dir)
    return result.stdout.decode('utf-8').strip().lower() == 'true'
    
def run_git_get_lines(params, args):
    working_dir = params.get('@', getcwd())
    result = subprocess.run(['git']+args, stdout=subprocess.PIPE, cwd=working_dir)
    result_stdout = result.stdout.decode('utf-8')
    result_lines = [x.strip() for x in result_stdout.split('\n') if len(x.strip())]
    return result_lines
    
def make_error_result(params):
    is_repo = is_in_git_repo(params)
    result = {
        'error': 'Not a git repo directory' if not is_repo else 'Panic ;(',
    }
    return result