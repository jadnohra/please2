import please2.reg_cmd as reg_cmd
from .cmd_base import Command, Match
from please2.util.tree import TreeNode
from please2.util.run import run_get_lines

class CommandAudioDevicesLs(Command):

    def help(self):
        return self.key()

    def key(self):
        return 'audio devices ls'

    def layer_name(self):
        return 'devices'

    def run_match(self, args, params):
        def create_device_node(name):
            node = TreeNode()
            node.set_name(name)
            return node
        out_lines = run_get_lines(args, params, ['pacmd', 'list-sinks'])
        out_lines = [x.strip() for x in out_lines]
        out_lines = [x for x in out_lines if any([x.startswith(y) for y in ['* index:', 'index:', 'name:', 'alsa.name = ']])]
        found_devices = []
        found_device_names = []
        default_device_index = -1
        for line in out_lines:
            if line.startswith('*'):
                default_device_index = len(found_devices)
            elif line.startswith('name:'):
                found_devices.append(line.split('name:')[1])
            elif line.startswith('alsa.name = '):
                found_device_names.append(line.split('alsa.name = ')[1])
        if len(found_devices):
            root_node = create_device_node('.')
            for i,device in enumerate(found_devices):
                node = create_device_node(device)
                root_node.add_child(node)
                if i == default_device_index:
                    node.add_label_layer(self.layer_name()).set_label('default')
                node.add_child(create_device_node(found_device_names[i]))
            result = {
                self.layer_name(): root_node,
            }
        else:
            result = make_error_result(args, params)
        return Match(result)


reg_cmd.register_command(CommandAudioDevicesLs())
