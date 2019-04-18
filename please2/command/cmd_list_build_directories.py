import os
import platform
import please2.reg_cmd as reg_cmd
from .cmd_base import generic_match, generic_key_args, Match
import please2.util.fs_tree as fs_tree

class CommandListBuildDirectories:

    def key(self):
        return 'list build directories'

    def match(self, args):
        return generic_match(self, args)

    def parametrize(self, args):
        return {} if args.match(generic_key_args(self)) else None

    def filter_func(name):
        return not any(name.startswith(x) for x in ['.', '_'])

    def run_match(self, params):
        def recurse(dir_tree, build_dirs):
            pass
        dir_tree = fs_tree.run(os.getcwd(), dirs_only=True,
                                filter_func=CommandListBuildDirectories.filter_func)
        build_dirs = []
        recurse(dir_tree, build_dirs)
        result = {
            'dirs': build_dirs
            }
        return Match(result)


reg_cmd.register_command(CommandListBuildDirectories())
