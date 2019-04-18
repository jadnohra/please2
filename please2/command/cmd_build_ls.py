from os import getcwd
from os.path import join
import please2.reg_cmd as reg_cmd
from .cmd_base import generic_match, generic_key_args, Match
import please2.util.fs as fs
from please2.util.pprint import pprint_tree_node

class CommandBuildLs:

    def key(self):
        return 'build ls'

    def match(self, args):
        return generic_match(self, args)

    def parametrize(self, args):
        return {} if args.match(generic_key_args(self)) else None

    def run_match(self, params):
        def dir_filter_func(name):
            return not any(name.startswith(x) for x in ['.', '_'])
        def file_filter_func(name):
            return name in ['WORKSPACE', 'BUILD', 'CMakeLists.txt', 'Makefile']
        def recurse(path, node):
            def is_build_workspace(node):
                return any(x.name() == 'WORKSPACE' for x in node.children())
            def is_build_package(node):
                return any(x.name() == 'BUILD' for x in node.children())
            if is_build_workspace(node):
                node.set_label('workspace')
                node.set_label('highlight')
            if is_build_package(node):
                node.set_label('package')
                node.set_label('highlight')
            for child in node.children():
                if child.has_label('d'):
                    dir_path = join(path, child.name())
                    recurse(dir_path, child)

        dir_tree = fs.dir_tree(getcwd(), dirs_only=True,
                                dir_filter_func=dir_filter_func,
                                file_filter_func=file_filter_func)
        recurse(dir_tree.get_attr('root', None), dir_tree)
        #pprint_tree_node(dir_tree)
        result = {
            'build_dir_tree': dir_tree
            }
        return Match(result)


reg_cmd.register_command(CommandBuildLs())
