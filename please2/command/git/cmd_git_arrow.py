import subprocess
import please2.reg_cmd as reg_cmd
from ..cmd_base import Command, Match
from .cmd_git_util import which_branch, checkout_branch
from .cmd_git_util import make_error_result, run_git_get_lines
from .cmd_git_util import find_branch_diff_files


class CommandGitArrow(Command):

    def help(self):
        return self.key() + ' (index|remote)/<source-branch> (index|remote)/<target-branch>'

    def opt_keys(self):
        return set(['@', 'trace'])

    def key(self):
        return 'git ='
        
    def run_match(self, args, params):
        def resolve_branch_special(branch, curr_branch):
            if branch in ['current', '']:
                return curr_branch
            return branch
        key_staging = 'index/'
        key_remote = 'remote/'
        def find_src_target(args, params):
            cands = [x for x in args.args if any(x.startswith(y) for y in [key_staging, key_remote])]
            if len(cands) != 2:
                return None
            return cands
        curr_branch = which_branch(args, params)
        if curr_branch is not None:
            src_target = find_src_target(args, params)
            if src_target is not None:
                src, target = src_target
                src_staging = src.startswith(key_staging)
                target_staging = target.startswith(key_staging)
                if src_staging and target_staging:
                    src_branch = resolve_branch_special(src[len(key_staging):], curr_branch)
                    target_branch = resolve_branch_special(target[len(key_staging):], curr_branch)
                    # checkout target
                    if curr_branch != target_branch:
                        diffs_curr_target = find_branch_diff_files(args, params, target_branch)
                        if len(diffs_curr_target):
                            return Match({ 'error': f"There are differences between your current branch'{curr_branch}' and the target branch '{target_branch}', this prevents checking it out to perform the merge, please fix this first (stash or commit)."})
                        
                        if not checkout_branch(args, params, target_branch):
                            return Match({ 'error': f"Sorry, could not checkout the target branch'{target_branch}'" })
                    # do the merge
                    if OK:
                        print('OK')
                    # checkout initial branch
                    if OK:
                        if curr_branch != target_branch:
                            if not checkout_branch(args, params, curr_branch):
                                return Match({ 'error': f"Sorry, could not checkout your initial branch '{curr_branch}'" })
                else:
                    return Match({ 'error': 'Sorry, supporting this is WIP' })
            else:
                return Match({ 'error': 'I could not extract the source and target paramters' })
        else:
            return Match(make_error_result(args, params))
        return Match(result)


reg_cmd.register_command(CommandGitArrow())
