import please2.reg_cmd as reg_cmd
from please2.util.tree import TreeNode
from ..cmd_base import Command, Match
from .cmd_git_util import run_git_get_lines, run_git_get_stdout

class CommandGitLsCommits(Command):

    def help(self):
        return self.key() + ' [@ <dir>] [last <count>] [workspace]'

    def opt_keys(self):
        return set(['@', 'last', 'workspace'])


    def key(self):
        return 'git ls commits'

    def layer_name(self):
        return 'git_commits'


    def run_match(self, args, params):
        def create_branch_node(name):
            node = TreeNode()
            node.set_name(name)
            return node
        workspace = 'workspace' in args.args
        ws_params = ['--single-worktree'] if workspace else []
        n = int(params['last']) if 'last' in params else 25
        found_reflog_lines = run_git_get_lines(args, params, ['reflog', '-n', str(n)] + ws_params)
        root_node = create_branch_node('.')
        i = 0
        if len(found_reflog_lines):
            for reflog_line in found_reflog_lines:
                commit_split = reflog_line.split('commit: ')
                if len(commit_split) > 1:
                    commit_msg = commit_split[1]
                    commit_hash = commit_split[0].split()[0]
                    remote_node = create_branch_node(f"{i}. {commit_hash} : {commit_msg}")
                    root_node.add_child(remote_node)
                    i = i+1
            result = { self.layer_name(): root_node}
        else:
            result = { 'info' : 'It seems the repo has no commits' }
        return Match(result)


reg_cmd.register_command(CommandGitLsCommits())
