import please2.reg_cmd as reg_cmd
from ..cmd_base import Command, Match
from .cmd_git_util import make_error_result, git_clone
from please2.util.args import get_positional_after


class CommandGitMoveUpstreamWs(Command):

    def help(self):
        return self.key() + ' <url> [branch <name>] [only] [@ <dir>]'

    def opt_keys(self):
        return set(['@', 'branch', 'only'])


    def key(self):
        return 'git move upstream-ws'

    def run_match(self, args, params):
        url = get_positional_after(args.args, self.key().split()[-1])
        single_branch = 'only' in args.args
        branch = params.get('branch', None)
        exitcode = git_clone(args, params, url, no_checkout=False,
                    branch_name=branch, single_branch=single_branch)
        if exitcode == 0:
            return Match('')
        else:
            return Match(result = {'error': 'Panic >:('})

reg_cmd.register_command(CommandGitMoveUpstreamWs())
