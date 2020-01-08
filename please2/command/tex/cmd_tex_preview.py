import tempfile
import os
import subprocess
import pkg_resources
import please2.reg_cmd as reg_cmd
from ..cmd_base import Command, Match
from please2.util.run import run
from please2.util.tree import TreeNode
from please2.util.input import resolve_smart_input
from please2.util.platform import display_image
from please2.util.run import run_get_lines
from please2.util.args import get_positional_after

class CommandTexPreview(Command):

    def help(self):
        return self.key() + ' <tex-code> [packages <packages>] [visualize] [debug]'

    def opt_keys(self):
        return set(['packages','visualize', 'debug'])

    def key(self):
        return 'tex preview'

    def references(self):
        return ['https://tex.stackexchange.com/questions/11866',
                'https://tex.stackexchange.com/questions/110273']

    def run_match(self, args, params):
        def make_tex_doc(content, packages=[]):
            packages_str = '\n'.join(['\\usepackage{{ {} }}'.format(pkg) for pkg in packages])
            host_tex_code = pkg_resources.resource_string(__name__, "host.tex")\
                            .decode('utf-8')
            return host_tex_code.replace('BODY', content).replace('PACKAGES', packages_str)
        latex_code = get_positional_after(args.args, self.key().split()[-1])
        latex_code = resolve_smart_input(latex_code)

        packages = []
        if 'packages' in params:
            packages = params.get('packages', '').split(',')

        result_tree = TreeNode('')
        with tempfile.NamedTemporaryFile(delete=False, suffix='.tex', mode='w') as tex_dot:
            tex_dot.write(make_tex_doc(latex_code, packages))
            tex_dot.flush()
            result_tree.add_child(TreeNode(tex_dot.name))
            temp_path = os.path.split(tex_dot.name)[0]

            run_kwargs = {'cwd':temp_path}
            if 'debug' not in args.args:
                run_kwargs['stdout'] = subprocess.DEVNULL

            if True:
                tex_args = ['pdflatex', '-interaction=nonstopmode',
                            '-output-format=dvi', tex_dot.name]

                run(args, params, tex_args, run_kwargs=run_kwargs)
                dvi_path = tex_dot.name.replace('.tex', '.dvi')
                result_tree.add_child(TreeNode(dvi_path))

            if False:
                tex_args = ['pdflatex', '-interaction=nonstopmode',
                            '-output-format=pdf', tex_dot.name]
                run(args, params, tex_args, run_kwargs=run_kwargs)
                pdf_path = tex_dot.name.replace('.tex', '.pdf')
                crop_args = ['pdfcrop', pdf_path]
                run(args, params, crop_args, run_kwargs=run_kwargs)
                result_tree.add_child(TreeNode(pdf_path))

            png_path = tex_dot.name.replace('.tex', '.png')
            dvipng_args = ['dvipng', '-T', 'tight',
                            '-o', os.path.split(png_path)[1], dvi_path]
            run(args, params, dvipng_args, run_kwargs=run_kwargs)
            result_tree.add_child(TreeNode(png_path))
            if 'visualize' in args.args:
                display_image(args, params, png_path)
        return Match(result = {
            'temp_files': result_tree
        })


reg_cmd.register_command(CommandTexPreview())
