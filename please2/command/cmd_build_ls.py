from os import getcwd
from os.path import join
import please2.reg_cmd as reg_cmd
from .cmd_base import Command, Match
import please2.util.fs as fs
from please2.util.pprint import pprint_tree_node
from please2.util.tree_algo import recurse_filter_node_copy

# Note, to list make targets: https://gist.github.com/pvdb/777954
# Note, useful bazel commands: https://docs.bazel.build/versions/master/query-how-to.html#what-rules-are-defined-in-the-foo-package

class CommandBuildLs(Command):

    def help(self):
        return self.key() + ' [@ dir] [only filter]'

    def opt_keys(self):
        return set(['@', 'only'])

    def key(self):
        return 'build ls'

    def layer_name(self):
        return 'build_ls'

    def run_match(self, args, params):
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
            labels = []
            if allow('cmake', only_filter) and is_cmake_directory(node):
                labels.append('cmake-dir')
            if allow('make', only_filter) and is_make_directory(node):
                labels.append('make-dir')
            if (allow('bazel', only_filter) or allow('bazel-ws', only_filter)) and is_bazel_workspace(node):
                labels.append('bazel-ws')
            if (allow('bazel', only_filter) or allow('bazel-pkg', only_filter)) and is_bazel_package(node):
                labels.append('bazel-pkg')
            if len(labels):
                layer = node.add_label_layer(self.layer_name())
                for label in labels:
                    layer.set_label(label)
            for child in node.children():
                if child.has_label('d'):
                    dir_path = join(path, child.name())
                    recurse_label(dir_path, child, only_filter)
        def keep_node_clean(node):
            return node.is_label_layer(self.layer_name())
        recurse_clean = recurse_filter_node_copy
        working_dir = params.get('@', getcwd())
        dir_tree = fs.dir_tree(working_dir, dirs_only=True,
                                dir_filter_func=dir_filter_func,
                                file_filter_func=file_filter_func)
        only_filter = None
        if 'only' in params:
            only_filter = set([x.strip() for x in params['only'].split(',')])
        recurse_label(dir_tree.label_layer().get_attr('root', None), dir_tree, only_filter)
        clean_dir_tree = recurse_filter_node_copy(dir_tree, keep_node_clean)
        #pprint_tree_node(dir_tree)
        result = {
            self.layer_name(): clean_dir_tree
            }
        return Match(result)


reg_cmd.register_command(CommandBuildLs())
