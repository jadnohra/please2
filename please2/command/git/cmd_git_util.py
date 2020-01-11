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

def get_ws_modifs(args, params, *, ws_cache=True, cache_local=True):
    git_args = ['status', '--porcelain']
    #_extend_list_cond(git_args, cached, ['--cached'])
    lines = run_git_get_lines(args, params, git_args, strip=False)
    modifs = [(line[:2], line[3:]) for line in lines if len(line.strip())]
    filtered_modifs = []
    for key, filename in modifs:
        ws_cache_key = key[1] if ws_cache else ''
        ws_cache_key = '' if ws_cache_key in [' '] else ws_cache_key
        cache_local_key = key[0] if cache_local else ''
        cache_local_key = '' if cache_local_key in [' ', '?'] else cache_local_key
        combined_key = ws_cache_key + cache_local_key
        if len(combined_key):
            filtered_modifs.append( (combined_key, filename) )
    return filtered_modifs

def get_ws_modifs_tree(args, params, *, ws_cache=True, cache_local=True):
    git_args = ['status', '--porcelain']
    lines = run_git_get_lines(args, params, git_args, strip=False)
    modifs = [(line[:2], line[3:]) for line in lines if len(line.strip())]
    root = create_git_diff_root_node(params)
    for key, filename in modifs:
        ws_cache_key = key[1] if ws_cache else None
        ws_cache_key = '_' if ws_cache_key in [' '] else ws_cache_key
        cache_local_key = key[0] if cache_local else None
        cache_local_key = '_' if cache_local_key in [' ', '?'] else cache_local_key
        if ws_cache_key or cache_local_key:
            keys = []
            _extend_list_cond(keys, ws_cache_key, [ws_cache_key])
            _extend_list_cond(keys, cache_local_key, [cache_local_key])
            node = create_git_diff_node(filename, ''.join(keys))
            '''
            if ws_cache and cache_local:
                if ws_cache_key != '_':
                    node.label_layer(git_diff_layer_name()+'-stage').set_label('ws-cache')
                if cache_local_key != '_':
                    node.label_layer(git_diff_layer_name()+'-stage').set_label('cache-local')
            '''
            root.add_child(node)
    return root

def include_filter_ws_modifs(modifs, include_untracked=True, include_tracked=True):
    def include_modif(modif):
        return include_untracked if modif[0][1] == '?' else include_tracked
    return [x for x in modifs if include_modif(x)]

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
