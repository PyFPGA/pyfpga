"""Vivado examples."""

import sys

from pyfpga.ise import Ise
from pyfpga.libero import Libero
from pyfpga.openflow import Openflow
from pyfpga.quartus import Quartus
from pyfpga.vivado import Vivado


classes = {
    'ise': Ise,
    'libero': Libero,
    'openflow': Openflow,
    'quartus': Quartus,
    'vivado': Vivado
}

tool = sys.argv[1] if len(sys.argv) > 1 else 'openflow'

Class = classes.get(tool)

if Class is None:
    sys.exit('Unsupported tool')

print(f'* Class Under Test: {Class.__name__}')

try:
    print('* Verilog Includes')
    prj = Class()
    prj.add_vlog('../../examples/sources/vlog/*.v')
    prj.set_top('Top')
    prj.add_define('DEFINE1', '1')
    prj.add_define('DEFINE2', '1')
    prj.add_param('FREQ', '1')
    prj.add_param('SECS', '1')
    prj.make()
    sys.exit('* FAIL')
except SystemExit:
    raise
except:
    print('* PASS')

try:
    print('* Verilog Defines')
    prj = Class()
    prj.add_vlog('../../examples/sources/vlog/*.v')
    prj.set_top('Top')
    prj.add_include('../../examples/sources/vlog/include1')
    prj.add_include('../../examples/sources/vlog/include2')
    prj.add_param('FREQ', '1')
    prj.add_param('SECS', '1')
    prj.make()
    sys.exit('* FAIL')
except SystemExit:
    raise
except:
    print('* PASS')

try:
    print('* Verilog Parameters')
    prj = Class()
    prj.add_vlog('../../examples/sources/vlog/*.v')
    prj.set_top('Top')
    prj.add_include('../../examples/sources/vlog/include1')
    prj.add_include('../../examples/sources/vlog/include2')
    prj.add_define('DEFINE1', '1')
    prj.add_define('DEFINE2', '1')
    prj.make()
    sys.exit('* FAIL')
except SystemExit:
    raise
except:
    print('* PASS')

print('* Verilog Support')
prj = Class()
prj.add_vlog('../../examples/sources/vlog/*.v')
prj.set_top('Top')
prj.add_include('../../examples/sources/vlog/include1')
prj.add_include('../../examples/sources/vlog/include2')
prj.add_define('DEFINE1', '1')
prj.add_define('DEFINE2', '1')
prj.add_param('FREQ', '1')
prj.add_param('SECS', '1')
prj.make()
print('* PASS')

if tool not in ['ise', 'openflow']:
    print('* System Verilog Support')
    prj = Class()
    prj.add_vlog('../../examples/sources/slog/*.sv')
    prj.set_top('Top')
    prj.add_include('../../examples/sources/slog/include1')
    prj.add_include('../../examples/sources/slog/include2')
    prj.add_define('DEFINE1', '1')
    prj.add_define('DEFINE2', '1')
    prj.add_param('FREQ', '1')
    prj.add_param('SECS', '1')
    prj.make()
    print('* PASS')

if tool not in ['openflow']:
    try:
        print('* VHDL Generics')
        prj = Class()
        prj.add_vhdl('../../examples/sources/vhdl/*.vhdl', 'blink_lib')
        prj.set_top('Top')
        prj.make()
        sys.exit('* FAIL')
    except SystemExit:
        raise
    except:
        print('* PASS')

    print('* VHDL Support')
    prj = Class()
    prj.add_vhdl('../../examples/sources/vhdl/*.vhdl', 'blink_lib')
    prj.set_top('Top')
    prj.add_param('FREQ', '1')
    prj.add_param('SECS', '1')
    prj.make()
    print('* PASS')

print(f'* Class Under Test works as expected')
