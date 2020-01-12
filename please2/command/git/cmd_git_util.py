from os import getcwd
from please2.util.run import run, run_get_stdout, run_get_lines
from please2.util.tree import TreeNode

# git commands that can cause data loss: https://stackoverflow.com/questions/21048765/what-can-cause-data-loss-in-git
# git process for safe pull
#   - https://stackoverflow.com/questions/17222440/is-there-a-git-pull-dry-run-option-in-git
#   - https://stackoverflow.com/questions/35591887/how-to-undo-git-fetch
#       - https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes
#        - https://stackoverflow.com/questions/18137175/in-git-what-is-the-difference-between-origin-master-vs-origin-master

def _extend_list_cond(list, condition, extensions):
    if condition:
        list.extend(extensions)

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
    _extend_list_cond(git_args, single_branch, ['--single_branch'])
    _extend_list_cond(git_args, branch_name, ['--branch', branch_name])
    git_args.append(upsteam_url)
    return run_git_get_exitcode(args, params, git_args)

def git_diff_layer_name():
    return 'git-diff'

def create_git_diff_root_node(params, name='.'):
    root = TreeNode('')
    root.label_layer('root').set_value(params.get('@', ''))
    return root

def create_git_diff_node(name, label, layer_name=git_diff_layer_name()):
    node = TreeNode(name)
    node.label_layer(layer_name).set_value(label)
    return node

def get_ws_modifs_tree(args, params, *, ws_cache=True, cache_local=True):
    git_args = ['status', '--porcelain']
    lines = run_git_get_lines(args, params, git_args, strip=False)
    modifs = [(line[:2], line[3:]) for line in lines if len(line.strip())]
    root = create_git_diff_root_node(params)
    for key, filename in modifs:
        active_keys = []
        both_keys = ws_cache and cache_local
        ws_cache_key = key[1]
        cache_local_key = key[0]
        has_ws_cache = (ws_cache_key != ' ')
        has_cache_local = (cache_local_key not in [' ', '?'])
        _extend_list_cond(active_keys, both_keys or (ws_cache and has_ws_cache),
                            ws_cache_key.replace(' ', '_'))
        _extend_list_cond(active_keys, both_keys or (cache_local and has_cache_local),
                            cache_local_key.replace(' ', '_').replace('?', '_'))
        if len(active_keys):
            node = create_git_diff_node(filename, ''.join(active_keys))
            root.add_child(node)
    return root

def modifs_to_files(modifs):
    files = set()
    for modif in modifs:
        arrow_key = ' -> '
        if arrow_key in modif:
            for file in modif.split(arrow_key):
                files.add(file)
        else:
            files.add(modif)
    return list(files)

def git_add(args, params):
    return run_git_get_exitcode(args, params, ['add', '--all'])

def git_add_modifs(args, params, modifs):
    files = modifs_to_files(modifs)
    return run_git_get_exitcode(args, params, ['add']+files)

def git_commit(args, params, *, commit_msg):
    return run_git_get_exitcode(args, params, ['commit', '-m', commit_msg])

def git_commit_modifs(args, params, modifs, *, commit_msg):
    files = modifs_to_files(modifs)
    return run_git_get_exitcode(args, params, ['commit'] + files + ['-m', commit_msg])

def git_push(args, params):
    return run_git_get_exitcode(args, params, ['push'])
