import please2.reg_cmd as reg_cmd
from please2.util.tree import TreeNode
from ..cmd_base import Command, Match
from please2.command.ssh.ssh_util import ssh_keygen_new
from .github_util import github_reg_ssh_key

class CommandGithubNewSsh(Command):

    def help(self):
        return self.key() + ' [for <username>]'

    def opt_keys(self):
        return set(['for'])

    def key(self):
        return 'github new ssh'

    def run_match(self, args, params):
        username = params.get('for', None)
        if username is None:
            username = str(input("username: "))
        ssh_filename = ssh_keygen_new(args, params, 'github', username)
        if ssh_filename is not None and \
            github_reg_ssh_key(args, params, username, ssh_filename):
            result = 'Success'
        else:
            result = make_error_result(args, params)
        return Match(result)

# Command borken at the moment, curl succeeds but key does not appear on github
# reg_cmd.register_command(CommandGithubNewSsh())
