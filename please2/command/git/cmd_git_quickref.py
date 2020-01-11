import please2.reg_cmd as reg_cmd
from ..cmd_base import Command, Match

help_ascii = '''
              Staging is .git/index and .git/objects.
              Single binary file .git/index,
              lists all files in the curr branch,
              their sha1 checksums, time stamps
                       ~~~~~~~~~
                           |
      +                    |            +              +
      | +------add-------> | +-commit-> | +--push----> |
      +                    +            +              +
   workspace         cache/index   local/downstream  remote/upstream
    (files)             (branch)      (repo)          (repo)
      +                    +            +              +
      | <-checkout-index-+ |            | <--fetch---+ |
      |                    |            |              |
      +-----diff-index-----+            |              |
      |                    |            |              |
      | <-----------checkout----------+ |              |
      | <-------------merge-----------+ |              |
      |                    |            |              |
      +-------------diff----------------+              |
      |                    |            |              |
      | <--------------------pull/rebase-------------+ +
      |                    |            |
      |                    +            |
  ~~~~~~~~~                         ~~~~~~~~~
Directory of files           Directory .git including
you see and edit             an objects directory containing
                             all versions of all files
                             (local branches and
                             copies of remote branches)
                             as a compressed "blob" file
'''

class CommandGitQuickref(Command):

    def help(self):
        return self.key()

    def references(self):
        return ['http://www.ndpsoftware.com/git-cheatsheet.html#loc=index;',
                'https://stackoverflow.com/questions/57547095/where-does-git-merge-fit-in-this-diagrams']

    def key(self):
        return 'git quickref'

    def run_match(self, args, params):
        return Match({'info': help_ascii})
        return Match(result)

# TODO: git log --graph --full-history --all --color         --pretty=format:"%x1b[31m%h%x09%x1b[32m%d%x1b[0m%x20%s"
# https://stackoverflow.com/questions/1057564/pretty-git-branch-graphs
# https://stackoverflow.com/questions/40978921/how-to-add-chmod-permissions-to-file-in-git/40979016
# http://justinhileman.info/article/git-pretty/git-pretty.png

reg_cmd.register_command(CommandGitQuickref())
