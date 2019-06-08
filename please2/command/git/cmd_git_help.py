import please2.reg_cmd as reg_cmd
from ..cmd_base import Command, Match

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

# TODO: git log --graph --full-history --all --color         --pretty=format:"%x1b[31m%h%x09%x1b[32m%d%x1b[0m%x20%s"
# https://stackoverflow.com/questions/1057564/pretty-git-branch-graphs

reg_cmd.register_command(CommandGitHelp())
