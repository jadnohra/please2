import please2.reg_cmd as reg_cmd
from please2.util.tree import TreeNode
from ..cmd_base import Command, Match
from .cmd_docker_util import run_docker_get_lines, get_all_containers

class CommandDockerKillAllContainers(Command):

    def help(self):
        return self.key()

    def opt_keys(self):
        return set()

    def key(self):
        return 'docker kill all containers'


    def run_match(self, args, params):
        containers = get_all_containers(args, params)
        if len(containers):
            run_docker_get_lines(args, params, ['rm'] + containers)
        return Match({'success': f"Removed {len(containers)} containers"})


reg_cmd.register_command(CommandDockerKillAllContainers())
