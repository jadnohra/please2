import please2.reg_cmd as reg_cmd
from please2.util.tree import TreeNode
from ..cmd_base import Command, Match
from .ssh_util import ssh_keygen_new

class CommandSshNew(Command):

    def help(self):
        return self.key() + ' [for <name>] [with purpose <purpose>]'

    def opt_keys(self):
        return set(['for', 'with purpose'])

    def key(self):
        return 'ssh new keypair'

    def run_match(self, args, params):
        name = params.get('for', None)
        if name is None:
            name = str(input("username: "))
        purpose = params.get('with purpose', None)
        if purpose is None:
            purpose = str(input("purpose: "))
        ssh_filename = ssh_keygen_new(args, params, purpose, name)
        if ssh_filename is not None:
            with open('{}.pub'.format(ssh_filename),'r') as f:
                key = f.read()
            result = {'pub-key':key}
        else:
            result = make_error_result(args, params)
        return Match(result)

reg_cmd.register_command(CommandSshNew())
