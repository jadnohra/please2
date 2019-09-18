import please2.reg_cmd as reg_cmd
from please2.util.tree import TreeNode
from ..cmd_base import Command, Match
from .cmd_docker_util import run_docker_get_lines, make_error_result, inspect_id


class CommandDockerLsContainers(Command):

    def help(self):
        return self.key() + '[detailed]'

    def opt_keys(self):
        return set('detailed')


    def key(self):
        return 'docker ls containers'

    def layer_name(self):
        return 'docker_containers'


    def run_match(self, args, params):
        def create_container_node(container, detailed):
            container_info = inspect_id(container[0], args, params)
            node = TreeNode(name=container_info['Id'])
            node.add_child(TreeNode(('Name', container_info['Name'])))
            img_node = TreeNode(('Image', container_info['Image']))
            if detailed:
                image_info = inspect_id(container_info['Image'], args, params)
                if len(image_info['RepoTags']):
                    img_node.add_child(TreeNode(('RepoTags', ', '.join(image_info['RepoTags']) )))
            node.add_child(img_node)
            node.add_child(TreeNode(('Status', container_info['State']['Status'])))
            return node
        detailed = 'detailed' in args.args
        result_lines = run_docker_get_lines(args, params, ['ps', '-a'])
        found_containers = []
        for line in result_lines[1:]:
            found_containers.append(line.split())
        if len(found_containers):
            root_node = TreeNode(name='.')
            for container in found_containers:
                root_node.add_child(create_container_node(container, detailed))
            result = {
                self.layer_name(): root_node,
            }
        else:
            result = make_error_result(args, params)
        return Match(result)


reg_cmd.register_command(CommandDockerLsContainers())
