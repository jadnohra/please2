import please2.reg_cmd as reg_cmd
from ..cmd_base import Command, Match
from please2.util.tree import TreeNode
from please2.util.run import run_get_lines

class CommandNetworkDevicesLs(Command):

    def help(self):
        return self.key()

    def key(self):
        return 'network devices ls'

    def layer_name(self):
        return 'devices'

    def run_match(self, args, params):
        def create_device_node(name):
            node = TreeNode()
            node.set_name(name)
            return node
        out_lines = run_get_lines(args, params, ['ip', 'addr'])
        out_lines = [x.strip() for x in out_lines]
        found_devices = []
        next_device_index = 1
        curr_device_index = -1
        for line in out_lines:
            if line.startswith('{}: '.format(next_device_index)):
                curr_device_index = next_device_index
                next_device_index = next_device_index+1
                device_info = {'index':curr_device_index}
                device_info['name'] = line.split(':')[1]
                found_devices.append(device_info)
        if len(found_devices):
            root_node = create_device_node('.')
            for i,device in enumerate(found_devices):
                node = create_device_node(device['name'])
                root_node.add_child(node)
            result = {
                self.layer_name(): root_node,
            }
        else:
            result = make_error_result(args, params)
        return Match(result)


reg_cmd.register_command(CommandNetworkDevicesLs())
