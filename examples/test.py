"""Example used to test pyfpga."""

from fpga.project import Project

#

print('* Testing default values')

ISE = Project('ise')
CONFIGS = ISE.get_configs()
assert CONFIGS['tool'] == 'ise'
assert CONFIGS['project'] == 'ise'
assert CONFIGS['extension'] == 'xise'
assert CONFIGS['part'] == 'XC6SLX9-2-CSG324'

LIBERO = Project('libero')
CONFIGS = LIBERO.get_configs()
assert CONFIGS['tool'] == 'libero'
assert CONFIGS['project'] == 'libero'
assert CONFIGS['extension'] == 'prjx'
assert CONFIGS['part'] == 'mpf300ts-1-fcg1152'

QUARTUS = Project('quartus')
CONFIGS = QUARTUS.get_configs()
assert CONFIGS['tool'] == 'quartus'
assert CONFIGS['project'] == 'quartus'
assert CONFIGS['extension'] == 'qpf'
assert CONFIGS['part'] == '10M08SAE144C8G'

VIVADO = Project('vivado')
CONFIGS = VIVADO.get_configs()
assert CONFIGS['tool'] == 'vivado'
assert CONFIGS['project'] == 'vivado'
assert CONFIGS['extension'] == 'xpr'
assert CONFIGS['part'] == 'xc7z010-1-clg400'

assert VIVADO.outdir == 'build'

#

print('* Testing changed values')

PRJ = Project('vivado', 'testPRJ')
PRJ.set_part('testFPGA')
CONFIGS = PRJ.get_configs()
assert CONFIGS['project'] == 'testPRJ'
assert CONFIGS['part'] == 'testFPGA'

PRJ.set_outdir('/tmp')
assert PRJ.outdir == '/tmp'

#

print('* Testing Flow')

PRJ.add_files('hdl/*.vhdl')
assert len(PRJ.tool.files) == 3

PRJ.set_top('Top')
assert PRJ.tool.top == 'Top'

PRJ.add_project_opt('PROJECT OPTIONS 1')
PRJ.add_project_opt('PROJECT OPTIONS 2')
assert PRJ.tool.options['project'][0] == 'PROJECT OPTIONS 1'
assert PRJ.tool.options['project'][1] == 'PROJECT OPTIONS 2'

PRJ.add_preflow_opt('PRE FLOW OPTIONS')
assert PRJ.tool.options['preflow'][0] == 'PRE FLOW OPTIONS'
PRJ.add_postsyn_opt('POST SYN OPTIONS')
assert PRJ.tool.options['postsyn'][0] == 'POST SYN OPTIONS'
PRJ.add_postimp_opt('POST IMP OPTIONS')
assert PRJ.tool.options['postimp'][0] == 'POST IMP OPTIONS'
PRJ.add_postbit_opt('POST BIT OPTIONS')
assert PRJ.tool.options['postbit'][0] == 'POST BIT OPTIONS'

#

PRJ.generate()
