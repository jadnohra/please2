import please2.reg_cmd as reg_cmd
from ..cmd_base import Command, Match
from .cmd_git_util import which_branch, make_error_result

help_ascii = '''
              Single binary file .git/index,
              lists all files in the curr branch,
              their sha1 checksums, time stamps
                           +
                           |
      +                    |            +            +
      | +------add-------> | +-commit-> | +--push--> |
      +                    +            +            +
   workspace            staging       local       remote
      +                 (branch)      (repo)      (repo)
      |                    +            +            +
      | <-checkout-index-+ |            | <--fetch-+ |
      |                    |            |            |
      +----+diff-index+----+            |            |
      |                    |            |            |
      | <-----------checkout----------+ |            |
      |                    |            |            |
      +------------+diff+---------------+            |
      |                    |            |            |
      | <------------------+-pull/rebase+----------+ +
      |                                 |
      +                                 +
Directory of files           Directory .git including
you see and edit             an objects directory containing
                             all versions of all files
                             (local branches and
                             copies of remote branches)
                             as a compressed "blob" file
'''

class CommandGitHelp(Command):

    def help(self):
        return self.key()

    def key(self):
        return 'git help'

    def run_match(self, args, params):
        return Match({'info': help_ascii})
        return Match(result)


reg_cmd.register_command(CommandGitHelp())
