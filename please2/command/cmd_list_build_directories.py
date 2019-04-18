import os
import platform
import please2.reg_cmd as reg_cmd
from .cmd_base import generic_match, generic_key_args, generic_parametrize, Match
import please2.util.fs_tree as fs_tree

class CommandListBuildDirectories:

    def key(self):
        return 'list build directories'

    def match(self, str_args, str_args_low):
        return generic_match(self, str_args, str_args_low)

    def parametrize(self, str_args, str_args_low):
        return generic_parametrize(generic_key_args(self),
                                    str_args, str_args_low)

    def get_excludes(self):
        return set(['.git', '.circleci', '__pycache__'])

    def run_match(self, params):
        def recurse(dir_tree, build_dirs):
            pass
        dir_tree = fs_tree.run(os.getcwd(), dirs_only=True,
                                excludes=self.get_excludes())
        build_dirs = []
        recurse(dir_tree, build_dirs)
        result = {
            'dirs': build_dirs
            }
        return Match(result)


reg_cmd.register_command(CommandListBuildDirectories())
