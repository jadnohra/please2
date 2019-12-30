import subprocess
import please2.reg_cmd as reg_cmd
from ...cmd_base import Command, Match
from please2.util.tree import TreeNode
from please2.util.run import run_get_stdout
from please2.util.args import get_positional_after

class CommandBazelDepGraph(Command):

    def help(self):
        return self.key() + ' <target> [@ <dir>]'

    def opt_keys(self):
        return set(['@'])

    def key(self):
        return 'bazel dependency graph'

    def run_match(self, args, params):
        target = get_positional_after(args.args, self.key().split()[-1])
        #cwd=path
        run_kwargs = {'stderr':subprocess.DEVNULL, 'shell':True}
        dot_data = run_get_stdout(args, params, "bazel query --nohost_deps --noimplicit_deps 'deps({})' --output graph".format(target), run_kwargs=run_kwargs)
        print('-----')
        print(dot_data)
        print('++++')
        #encoding='ascii'
        #subprocess.run(['xdot'], input=dot_data.encode(), shell=True)

        # xdot <(bazel query --nohost_deps --noimplicit_deps 'deps(//main:hello-world)' --output graph)
        if False:
            pass
        else:
            return Match(result = {
                'error': "Apologies, I don't know how to extract this file type",
            })


reg_cmd.register_command(CommandBazelDepGraph())
