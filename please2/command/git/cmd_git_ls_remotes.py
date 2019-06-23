import please2.reg_cmd as reg_cmd
from please2.util.tree import TreeNode
from ..cmd_base import Command, Match
from .cmd_git_util import run_git_get_lines, run_git_get_stdout

class CommandGitLsRemotes(Command):

    def help(self):
        return self.key() + ' [@ <dir>]'

    def opt_keys(self):
        return set(['@')


    def key(self):
        return 'git ls remotes'

    def layer_name(self):
        return 'git_remotes'


    def run_match(self, args, params):
        def create_branch_node(name):
            node = TreeNode()
            node.set_name(name)
            return node
        found_remotes = run_git_get_lines(args, params, ['remote'])
        root_node = create_branch_node('.')
        if len(found_remotes):
            for remote in found_remotes:
                remote_node = create_branch_node(remote)
                root_node.add_child(remote_node)
                remote_url = run_git_get_stdout(args, params, ['remote', 'get-url', remote])
                remote_url_node = create_branch_node(remote_url)
                remote_node.add_child(remote_url_node)
            result = { self.layer_name(): root_node}
        else:
            result = { 'info' : 'It seems the repo has no remotes' }
        return Match(result)


reg_cmd.register_command(CommandGitLsRemotes())
