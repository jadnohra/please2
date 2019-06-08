import please2.reg_cmd as reg_cmd
from please2.util.tree import TreeNode
from ..cmd_base import Command, Match
from .cmd_git_util import make_error_result, run_git_get_lines

class CommandGitLsBranches(Command):

    def help(self):
        return self.key() + ' [@ <dir>] [remote] [trace]'

    def opt_keys(self):
        return set(['@', 'remote', 'trace'])


    def key(self):
        return 'git ls branches'

    def layer_name(self):
        return 'git_branches'


    def run_match(self, args, params):
        def create_branch_node(name):
            node = TreeNode()
            node.set_name(name)
            return node
        remote = 'remote' in args.args
        if remote:
            prefix = 'remotes/'
            result_lines = run_git_get_lines(args, params, ['branch', '-a'])
            result_lines = [x[len(prefix):] for x in result_lines if x.startswith(prefix)]
        else:
            result_lines = run_git_get_lines(args, params, ['branch'])
        found_branches = []
        for line in result_lines:
            if line.startswith('* '):
                found_branches.append(line.split()[1])
            else:
                found_branches.append(line)
        if len(found_branches):
            root_node = create_branch_node('.')
            for branch in found_branches:
                root_node.add_child(create_branch_node(branch))
            result = {
                self.layer_name(): root_node,
            }
        else:
            result = make_error_result(args, params)
        return Match(result)


reg_cmd.register_command(CommandGitLsBranches())
