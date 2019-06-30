import please2.reg_cmd as reg_cmd
from .cmd_base import Command, Match
from please2.util.tree import TreeNode
from please2.util.run import run_get_lines

class CommandSetAudioVolume(Command):

    def help(self):
        return self.key() + ' [to X] [card Y]'

    def opt_keys(self):
        return set(['to', 'card'])

    def key(self):
        return 'set audio volume'


    def run_match(self, args, params):
        # Documentation: https://wiki.archlinux.org/index.php/PulseAudio/Examples#Set_the_default_output_source
        if 'card' in params:
            card_number = params.get('card', '1')
        else:
            out_lines = run_get_lines(args, params, ['pacmd', 'list-sinks'])
            out_lines = [x.strip() for x in out_lines if x.strip().startswith('* index:')]
            active_card = out_lines[0].split('index:')[1].strip()
            card_number = active_card
        volume_perc = params.get('to', '100')
        if not volume_perc.endswith('%'):
            volume_perc = volume_perc + '%'
        run_get_lines(args, params, ['pactl', '--', 'set-sink-volume', card_number, volume_perc])
        return Match('')


reg_cmd.register_command(CommandSetAudioVolume())
