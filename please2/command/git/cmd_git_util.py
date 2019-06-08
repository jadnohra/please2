from os import getcwd
import subprocess

def run_git_get_stdout(args, params, git_args):
    trace = 'trace' in args.args
    working_dir = params.get('@', getcwd())
    run_args = ['git']+git_args
    if trace:
        print(f' > {working_dir}$ {" ".join(run_args)}')
    result = subprocess.run(run_args, stdout=subprocess.PIPE, cwd=working_dir)
    result_stdout = result.stdout.decode('utf-8')
    return result_stdout

def is_in_git_repo(args, params):
    result_stdout = run_git_get_stdout(args, params, ['rev-parse', '--is-inside-work-tree'])
    return result_stdout.strip().lower() == 'true'
    
def run_git_get_lines(args, params, git_args):
    result_stdout = run_git_get_stdout(args, params, git_args)
    result_lines = [x.strip() for x in result_stdout.split('\n') if len(x.strip())]
    return result_lines
    
def make_error_result(args, params):
    is_repo = is_in_git_repo(args, params)
    result = {
        'error': 'Not a git repo directory' if not is_repo else 'Panic ;(',
    }
    return result

def which_branch(args, params):
    result_lines = run_git_get_lines(args, params, ['branch'])
    found_branch = None
    for line in result_lines:
        if line.startswith('* '):
            found_branch = line.split()[1]
            break
    return found_branch