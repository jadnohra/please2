from os import getcwd
from os.path import join
from copy import copy
import please2.reg_cmd as reg_cmd
from .cmd_base import Command, Match
import please2.util.fs as fs
from please2.util.pprint import pprint_tree_node

# Note, to list make targets: https://gist.github.com/pvdb/777954

class CommandBuildLs(Command):

    def help(self):
        return self.key() + ' [@ dir] [only filter]'

    def opt_keys(self):
        return set(['@', 'only'])

    def key(self):
        return 'build ls'

    def run_match(self, params):
        def dir_filter_func(name):
            return not any(name.startswith(x) for x in ['.', '_'])
        def file_filter_func(name):
            return name in ['WORKSPACE', 'BUILD', 'CMakeLists.txt', 'Makefile']
        def recurse_label(path, node, only_filter):
            def is_cmake_directory(node):
                return any(x.name() == 'CMakeLists.txt' for x in node.children())
            def is_make_directory(node):
                return any(x.name() == 'Makefile' for x in node.children())
            def is_bazel_workspace(node):
                return any(x.name() == 'WORKSPACE' for x in node.children())
            def is_bazel_package(node):
                return any(x.name() == 'BUILD' for x in node.children())
            def allow(type, only_filter):
                return True if only_filter is None else (type in only_filter)
            if allow('cmake', only_filter) and is_cmake_directory(node):
                node.set_label('build')
                node.set_label('cmake-directory')
                node.merge_attr_set('pprint-highlight', 'cmake')
            if allow('make', only_filter) and is_make_directory(node):
                node.set_label('build')
                node.set_label('make-directory')
                node.merge_attr_set('pprint-highlight', 'make')
            if allow('bazel-workspace', only_filter) and is_bazel_workspace(node):
                node.set_label('build')
                node.set_label('bazel-workspace')
                node.merge_attr_set('pprint-highlight', 'bazel-workspace')
            if allow('bazel-package', only_filter) and is_bazel_package(node):
                node.set_label('build')
                node.set_label('bazel-package')
                node.merge_attr_set('pprint-highlight', 'bazel-package')
            for child in node.children():
                if child.has_label('d'):
                    dir_path = join(path, child.name())
                    recurse_label(dir_path, child, only_filter)
        def recurse_clean(node):
            clean_children = [recurse_clean(x) for x in node.children()]
            clean_children = [x for x in clean_children if x is not None]
            keep_self = node.has_label('build')
            if keep_self or clean_children:
                clean_node = copy(node)
                clean_node.set_children(clean_children)
                return clean_node
            else:
                return None
        working_dir = params.get('@', getcwd())
        dir_tree = fs.dir_tree(working_dir, dirs_only=True,
                                dir_filter_func=dir_filter_func,
                                file_filter_func=file_filter_func)
        only_filter = None
        if 'only' in params:
            only_filter = set([x.strip() for x in params['only'].split(',')])
        recurse_label(dir_tree.get_attr('root', None), dir_tree, only_filter)
        clean_dir_tree = recurse_clean(dir_tree)
        #pprint_tree_node(dir_tree)
        result = {
            'build_dir_tree': clean_dir_tree
            }
        return Match(result)


reg_cmd.register_command(CommandBuildLs())
