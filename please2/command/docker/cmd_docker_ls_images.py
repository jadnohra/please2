import please2.reg_cmd as reg_cmd
from please2.util.tree import TreeNode
from ..cmd_base import Command, Match
from .cmd_docker_util import run_docker_get_lines, make_error_result, inspect_id


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
        def create_image_node(image):
            image_info = inspect_id(image[2], args, params)
            node = TreeNode(name=image_info['Id'])
            node.add_child(TreeNode(('Repository', image[0])))
            if len(image_info['RepoTags']):
                node.add_child(TreeNode(('RepoTags', ', '.join(image_info['RepoTags']) )))
            return node
        result_lines = run_docker_get_lines(args, params, ['image', 'ls', '-a'])
        found_images = []
        for line in result_lines[1:]:
            found_images.append(line.split())
        if len(found_images):
            root_node = TreeNode(name='.')
            for image in found_images:
                root_node.add_child(create_image_node(image))
            result = {
                self.layer_name(): root_node,
            }
        else:
            result = make_error_result(args, params)
        return Match(result)


reg_cmd.register_command(CommandDockerLsImages())
