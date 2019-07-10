import please2.reg_cmd as reg_cmd
from please2.util.tree import TreeNode
from ..cmd_base import Command, Match
from .cmd_docker_util import run_docker_get_lines, make_error_result


class CommandDockerLsImages(Command):

    def help(self):
        return self.key()

    def opt_keys(self):
        return set()


    def key(self):
        return 'docker ls images'

    def layer_name(self):
        return 'docker_images'


    def run_match(self, args, params):
        def create_container_node(container):
            node = TreeNode(name=container[0])
            # use docker inspect instead
            # node.add_child(TreeNode(' --- '.join(container)))
            return node
        result_lines = run_docker_get_lines(args, params, ['ps', '-a'])
        found_containers = []
        for line in result_lines[1:]:
            found_containers.append(line.split())
        if len(found_containers):
            root_node = TreeNode(name='.')
            for container in found_containers:
                root_node.add_child(create_container_node(container))
            result = {
                self.layer_name(): root_node,
            }
        else:
            result = make_error_result(args, params)
        return Match(result)


reg_cmd.register_command(CommandDockerLsImages())
