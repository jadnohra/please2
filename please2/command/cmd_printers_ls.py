import please2.reg_cmd as reg_cmd
from .cmd_base import Command, Match
from please2.util.tree import TreeNode
from please2.util.run import run_get_lines

class CommandPrintersLs(Command):

    def help(self):
        return self.key()


    def key(self):
        return 'printers ls'

    def layer_name(self):
        return 'printers'


    def run_match(self, args, params):
        def create_branch_node(name):
            node = TreeNode()
            node.set_name(name)
            return node
        result_lines = run_get_lines(args, params, ['lpstat', '-a'])
        found_printers = [x.split()[0] for x in result_lines]
        if len(found_printers):
            root_node = create_branch_node('.')
            for branch in found_printers:
                root_node.add_child(create_branch_node(branch))
            result = {
                self.layer_name(): root_node,
            }
        else:
            result = make_error_result(args, params)
        return Match(result)


reg_cmd.register_command(CommandPrintersLs())
