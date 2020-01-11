from os import getcwd
from please2.util.run import run, run_get_stdout, run_get_lines

# git commands that can cause data loss: https://stackoverflow.com/questions/21048765/what-can-cause-data-loss-in-git
# git process for safe pull
#   - https://stackoverflow.com/questions/17222440/is-there-a-git-pull-dry-run-option-in-git
#   - https://stackoverflow.com/questions/35591887/how-to-undo-git-fetch
#       - https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes
#        - https://stackoverflow.com/questions/18137175/in-git-what-is-the-difference-between-origin-master-vs-origin-master

def _extend_cond_args(args, condition, extensions):
    if condition:
        args.extend(extensions)

def run_git_get_exitcode(args, params, git_args):
    run_args = ['git']+git_args
    return run(args, params, run_args)

def run_git_get_stdout(args, params, git_args):
    run_args = ['git']+git_args
    return run_get_stdout(args, params, run_args)

def is_in_git_repo(args, params):
    result_stdout = run_git_get_stdout(args, params, ['rev-parse', '--is-inside-work-tree'])
    return result_stdout.strip().lower() == 'true'

def run_git_get_lines(args, params, git_args, strip=True):
    run_args = ['git']+git_args
    return run_get_lines(args, params, run_args, strip=strip)

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

def git_clone(args, params, upsteam_url, *, no_checkout, branch_name, single_branch):
    # https://stackoverflow.com/questions/1911109/how-do-i-clone-a-specific-git-branch
    git_args = ['clone']
    _extend_cond_args(git_args, single_branch, ['--single_branch'])
    _extend_cond_args(git_args, branch_name, ['--branch', branch_name])
    git_args.append(upsteam_url)
    return run_git_get_exitcode(args, params, git_args)

def get_ws_modifs(args, params, *, ws_cache=True, cache_local=True):
    git_args = ['status', '--porcelain']
    #_extend_cond_args(git_args, cached, ['--cached'])
    lines = run_git_get_lines(args, params, git_args, strip=False)
    print(lines)
    modifs = [(line[:2], line[2:]) for line in lines if len(line.strip())]
    filtered_modifs = []
    print(modifs)
    if not ws_cache or not cache_local:
        for modif in modifs:
            key, info = modif
            print('[{}]'.format(key))
            if not((ws_cache == False and key[0] in [' ', '?'])
                or (cache_local == False and key[1] == ' ')):
                    filtered_modifs.append(modif)
        return filtered_modifs
    else:
        return modifs


def pprint_ws_modifs(modifs, ws_cache=True, cache_local=True, header="\nModifications", footer="\n"):
    # TODO clip if too large
    if header:
        print(header)
    if ws_cache and cache_local:
        print('\n'.join([f' {x[0]} {x[1]}' for x in modifs]))
    elif ws_cache:
        print('\n'.join([f' {x[0][1]} {x[1]}' for x in modifs]))
    elif cache_local:
        print('\n'.join([f' {x[0][0]} {x[1]}' for x in modifs]))
    else:
        print('\n'.join([f' {x[0]} {x[1]}' for x in modifs]))
    if footer:
        print(footer)

def git_add(args, params):
    return run_git_get_exitcode(args, params, ['add', '--all'])

def git_commit(args, params, *, commit_msg):
    return run_git_get_exitcode(args, params, ['commit', '-m', commit_msg])

def git_push(args, params):
    return run_git_get_exitcode(args, params, ['push'])
