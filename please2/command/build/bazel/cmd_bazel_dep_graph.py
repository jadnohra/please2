import subprocess
import os
import tempfile
import please2.reg_cmd as reg_cmd
from ...cmd_base import Command, Match
from please2.util.tree import TreeNode
from please2.util.run import run, run_get_stdout
from please2.util.args import get_positional_after
from please2.util.chain import find_tree_as_list

class CommandBazelDepGraph(Command):

    def help(self):
        return self.key() + ' <target> [@ <dir>] [auxiliary] [debug-bazel]'

    def opt_keys(self):
        return set(['@', 'auxiliary', 'debug-bazel'])

    def key(self):
        return 'bazel dep graph'

    def run_match(self, args, params):
        bzl_use_paths = True
        targets = find_tree_as_list(params)
        if targets is None:
            bzl_use_paths = False
            targets = [get_positional_after(args.args, self.key().split()[-1])]
        result_tree = TreeNode('')
        for target in targets:
            #target_node = result_tree.add_child(TreeNode(target))
            run_kwargs = {'shell':True}
            if bzl_use_paths:
                pkg_path, target = os.path.split(target)
                working_dir, pkg = os.path.split(pkg_path)
                bzl_target = f'{pkg}/{target}'
                run_kwargs['cwd'] = working_dir
            else:
                bzl_target = target
            if 'debug-bazel' not in args.args:
                run_kwargs['stderr'] = subprocess.DEVNULL
            bzl_query = "bazel query --nohost_deps --noimplicit_deps 'deps({})' \
                        --output graph".format(bzl_target)
            dot_data = run_get_stdout(args, params, [bzl_query], run_kwargs=run_kwargs)
            with tempfile.NamedTemporaryFile(delete=False, suffix='.dot', mode='w') as temp_dot:
                temp_dot.write(dot_data)
                temp_dot.flush()
                with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_png:
                    dot_args = ['dot', temp_dot.name, '-Tpng', '-o', temp_png.name]
                    run(args, params, dot_args)
                    result_tree.add_child(TreeNode(temp_png.name))
                if 'auxiliary' in args.args:
                    result_tree.add_child(TreeNode(temp_dot.name))
        return Match(result = {
            'out': result_tree
        })


reg_cmd.register_command(CommandBazelDepGraph())
