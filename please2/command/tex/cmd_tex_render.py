import tempfile
import os
import subprocess
import pkg_resources
import please2.reg_cmd as reg_cmd
from ..cmd_base import Command, Match
from please2.util.run import run
from please2.util.tree import TreeNode
from please2.util.os import display_image
from please2.util.run import run_get_lines
from please2.util.args import get_positional_after

class CommandTexRender(Command):

    def help(self):
        return self.key() + ' <tex-code> [visualize] [debug]'

    def opt_keys(self):
        return set(['visualize', 'debug'])

    def key(self):
        return 'tex render'

    def references(self):
        return ['https://tex.stackexchange.com/questions/11866',
                'https://tex.stackexchange.com/questions/110273']

    def run_match(self, args, params):
        def make_tex_doc(content):
            host_tex_code = pkg_resources.resource_string(__name__, "host.tex")\
                            .decode('utf-8')
            return host_tex_code.replace('BODY', content)
        latex_code = get_positional_after(args.args, self.key().split()[-1])
        result_tree = TreeNode('')
        with tempfile.NamedTemporaryFile(delete=False, suffix='.tex', mode='w') as tex_dot:
            tex_dot.write(make_tex_doc(latex_code))
            tex_dot.flush()
            target_node = result_tree.add_child(TreeNode(tex_dot.name))
            temp_path = os.path.split(tex_dot.name)[0]
            tex_args = ['pdflatex', '-interaction=nonstopmode',
                        '-output-format=dvi', tex_dot.name]
            run_kwargs = {'cwd':temp_path}
            if 'debug' not in args.args:
                run_kwargs['stdout'] = subprocess.DEVNULL
            run(args, params, tex_args, run_kwargs=run_kwargs)
            dvi_path = tex_dot.name.replace('.tex', '.dvi')
            target_node = result_tree.add_child(TreeNode(dvi_path))
            '''
            pdf_path = tex_dot.name.replace('.tex', '.pdf')
            crop_args = ['pdfcrop', pdf_path]
            run(args, params, crop_args, run_kwargs=run_kwargs)
            '''
            png_path = tex_dot.name.replace('.tex', '.png')
            dvipng_args = ['dvipng', '-T', 'tight',
                            '-o', os.path.split(png_path)[1], dvi_path]
            run(args, params, dvipng_args, run_kwargs=run_kwargs)
            target_node = result_tree.add_child(TreeNode(png_path))
            if 'visualize' in args.args:
                display_image(args, params, png_path)
        return Match(result = {
            'temp_files': result_tree
        })


reg_cmd.register_command(CommandTexRender())
