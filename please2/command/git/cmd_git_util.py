from os import getcwd
from please2.util.run import run_get_stdout, run_get_lines

def run_git_get_stdout(args, params, git_args):
    run_args = ['git']+git_args
    return run_get_stdout(args, params, run_args)

def is_in_git_repo(args, params):
    result_stdout = run_git_get_stdout(args, params, ['rev-parse', '--is-inside-work-tree'])
    return result_stdout.strip().lower() == 'true'

def run_git_get_lines(args, params, git_args):
    run_args = ['git']+git_args
    return run_get_lines(args, params, run_args)

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

def checkout_branch(args, params, branch):
    result_stdout = run_git_get_stdout(args, params, ['checkout', branch])
    return result_stdout.strip().lower() == 'your branch is up to date'

def find_branch_diff_files(args, params, target_branch):
    lines = run_git_get_lines(args, params, ['diff', '-R', '--name-only', target_branch])
    return lines

def merge_branch(args, params, target_branch):
    result_stdout = run_git_get_stdout(args, params, ['merge', target_branch])
    return result_stdout.strip().lower() == 'your branch is up to date'

def git_reset(args, params, key, soft):
    git_args = ['reset']
    if key is not None:
        git_args.append(key)
    git_args.append('--soft' if soft else '--hard')
    result_stdout = run_git_get_stdout(args, params, git_args)
    return result_stdout.strip().lower() == ''
