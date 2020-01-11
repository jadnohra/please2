import please2.reg_cmd as reg_cmd
from ..cmd_base import Command, Match
from please2.util.args import get_positional_after
from please2.util.run import run

class CommandGitDiffWsRemote(Command):

    def help(self):
        return self.key() + ' [@ <dir>]'

    def references(self):
        return ['https://stackoverflow.com/questions/1800783/how-to-compare-a-local-git-branch-with-its-remote-branch']

    def opt_keys(self):
        return set(['@'])

    def key(self):
        return 'git diff ws-remote'

    def run_match(self, args, params):
        run(args, params, ['git', 'diff', '@{push}', '--compact-summary'])
        # Not perfect, untracked files are missing
        # TODO return trees instead of pprint, analyze results
        return Match('')

reg_cmd.register_command(CommandGitDiffWsRemote())
