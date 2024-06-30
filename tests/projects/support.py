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

print(f'INFO: the Class Under Test is {Class.__name__}')

try:
    print('INFO: checking Verilog Includes')
    prj = Class()
    prj.add_vlog('../../examples/sources/vlog/*.v')
    prj.set_top('Top')
    prj.add_define('DEFINE1', '1')
    prj.add_define('DEFINE2', '1')
    prj.add_param('FREQ', '1')
    prj.add_param('SECS', '1')
    prj.make(last='syn')
    sys.exit('ERROR: something does not work as expected')
except SystemExit:
    raise
except Exception:
    pass

try:
    print('INFO: checking Verilog Defines')
    prj = Class()
    prj.add_vlog('../../examples/sources/vlog/*.v')
    prj.set_top('Top')
    prj.add_include('../../examples/sources/vlog/include1')
    prj.add_include('../../examples/sources/vlog/include2')
    prj.add_param('FREQ', '1')
    prj.add_param('SECS', '1')
    prj.make(last='syn')
    sys.exit('ERROR: something does not work as expected')
except SystemExit:
    raise
except Exception:
    pass

try:
    print('INFO: checking Verilog Parameters')
    prj = Class()
    prj.add_vlog('../../examples/sources/vlog/*.v')
    prj.set_top('Top')
    prj.add_include('../../examples/sources/vlog/include1')
    prj.add_include('../../examples/sources/vlog/include2')
    prj.add_define('DEFINE1', '1')
    prj.add_define('DEFINE2', '1')
    prj.make(last='syn')
    sys.exit('ERROR: something does not work as expected')
except SystemExit:
    raise
except Exception:
    pass

print('INFO: checking Verilog Support')
prj = Class()
prj.add_vlog('../../examples/sources/vlog/*.v')
prj.set_top('Top')
prj.add_include('../../examples/sources/vlog/include1')
prj.add_include('../../examples/sources/vlog/include2')
prj.add_define('DEFINE1', '1')
prj.add_define('DEFINE2', '1')
prj.add_param('FREQ', '1')
prj.add_param('SECS', '1')
prj.make(last='syn')

if tool not in ['ise', 'openflow']:
    print('INFO: checking System Verilog Support')
    prj = Class()
    prj.add_vlog('../../examples/sources/slog/*.sv')
    prj.set_top('Top')
    prj.add_include('../../examples/sources/slog/include1')
    prj.add_include('../../examples/sources/slog/include2')
    prj.add_define('DEFINE1', '1')
    prj.add_define('DEFINE2', '1')
    prj.add_param('FREQ', '1')
    prj.add_param('SECS', '1')
    prj.make(last='syn')

if tool not in ['openflow']:
    try:
        print('INFO: checking VHDL Generics')
        prj = Class()
        prj.add_vhdl('../../examples/sources/vhdl/*.vhdl', 'blink_lib')
        prj.set_top('Top')
        prj.make(last='syn')
        sys.exit('ERROR: something does not work as expected')
    except SystemExit:
        raise
    except Exception:
        pass

    print('* VHDL Support')
    prj = Class()
    prj.add_vhdl('../../examples/sources/vhdl/*.vhdl', 'blink_lib')
    prj.set_top('Top')
    prj.add_param('FREQ', '1')
    prj.add_param('SECS', '1')
    prj.make(last='syn')

print(f'INFO: Class Under Test works as expected')
