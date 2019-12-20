import please2.reg_cmd as reg_cmd
from please2.util.tree import TreeNode
from ..cmd_base import Command, Match
from please2.command.ssh.ssh_util import ssh_keygen_new_interactive

class CommandGithubNewSsh(Command):

    def help(self):
        return self.key() + ' [for <email>]'

    def opt_keys(self):
        return set('for')

    def key(self):
        return 'github new ssh'

    def run_match(self, args, params):
        email = params.get('for', None)

        ssh_keygen_new_interactive(args, params, 'github', email=email)
        return Match('')

reg_cmd.register_command(CommandGithubNewSsh())
