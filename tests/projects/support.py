"""Support examples."""

import argparse
import sys

from pyfpga.ise import Ise
from pyfpga.libero import Libero
from pyfpga.openflow import Openflow
from pyfpga.quartus import Quartus
from pyfpga.vivado import Vivado


tools = {
    'ise': Ise,
    'libero': Libero,
    'openflow': Openflow,
    'quartus': Quartus,
    'vivado': Vivado
}

parser = argparse.ArgumentParser()
parser.add_argument(
    '--tool', default='openflow',
    choices=['ise', 'libero', 'quartus', 'openflow', 'vivado']
)
args = parser.parse_args()

print(f'INFO: the Tool Under Test is {args.tool}')

try:
    print('INFO: checking Verilog Includes')
    prj = tools[args.tool]()
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
    prj = tools[args.tool]()
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
    prj = tools[args.tool]()
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
prj = tools[args.tool]()
prj.add_vlog('../../examples/sources/vlog/*.v')
prj.set_top('Top')
prj.add_include('../../examples/sources/vlog/include1')
prj.add_include('../../examples/sources/vlog/include2')
prj.add_define('DEFINE1', '1')
prj.add_define('DEFINE2', '1')
prj.add_param('FREQ', '1')
prj.add_param('SECS', '1')
prj.make(last='syn')

if args.tool not in ['ise', 'openflow']:
    print('INFO: checking System Verilog Support')
    prj = tools[args.tool]()
    prj.add_slog('../../examples/sources/slog/*.sv')
    prj.set_top('Top')
    prj.add_include('../../examples/sources/slog/include1')
    prj.add_include('../../examples/sources/slog/include2')
    prj.add_define('DEFINE1', '1')
    prj.add_define('DEFINE2', '1')
    prj.add_param('FREQ', '1')
    prj.add_param('SECS', '1')
    prj.make(last='syn')

if args.tool not in ['openflow']:
    try:
        print('INFO: checking VHDL Generics')
        prj = tools[args.tool]()
        prj.add_vhdl('../../examples/sources/vhdl/*.vhdl', 'blink_lib')
        prj.set_top('Top')
        prj.make(last='syn')
        sys.exit('ERROR: something does not work as expected')
    except SystemExit:
        raise
    except Exception:
        pass

    print('* VHDL Support')
    prj = tools[args.tool]()
    prj.add_vhdl('../../examples/sources/vhdl/*.vhdl', 'blink_lib')
    prj.set_top('Top')
    prj.add_param('FREQ', '1')
    prj.add_param('SECS', '1')
    prj.make(last='syn')

print(f'INFO: Class Under Test works as expected')
