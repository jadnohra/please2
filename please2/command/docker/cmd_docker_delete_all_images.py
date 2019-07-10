import please2.reg_cmd as reg_cmd
from please2.util.tree import TreeNode
from ..cmd_base import Command, Match
from .cmd_docker_util import run_docker_get_lines, get_all_images

class CommandDockerDeleteAllImages(Command):

    def help(self):
        return self.key()

    def opt_keys(self):
        return set()

    def key(self):
        return 'docker delete all images'


    def run_match(self, args, params):
        images = get_all_images(args, params)
        if len(images):
            run_docker_get_lines(args, params, ['rmi'] + images)
        return Match({'success': f"Removed {len(images)} images"})


reg_cmd.register_command(CommandDockerDeleteAllImages())
