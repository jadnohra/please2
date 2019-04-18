from os import listdir
from os.path import isfile, join, basename
from functools import reduce

def run(root_dir, dirs_only=False, excludes = set()):
    def recurse(dir, dirname):
        tree = {'dirs':{}, 'files':set()}
        dirs = tree['dirs']
        files = tree['files']
        list_nodes = listdir(dir)
        for node_name in list_nodes:
            if node_name not in excludes:
                node_path = join(dir, node_name)
                if isfile(node_path):
                    if not dirs_only:
                        files.add(node_name)
                else:
                    dirs[node_name] = recurse(node_path, node_name)
        return tree
    return recurse(root_dir, basename(root_dir))
