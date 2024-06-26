"""Openflow examples."""

import argparse

from pyfpga.openflow import Openflow


parser = argparse.ArgumentParser()
parser.add_argument(
    '--board', choices=['icestick', 'edu-ciaa', 'orangecrab', 'ecp5evn'],
    default='icestick'
)
parser.add_argument(
    '--source', choices=['vlog', 'vhdl', 'slog'], default='vlog'
)
parser.add_argument(
    '--action', choices=['make', 'prog', 'all'], default='make'
)
args = parser.parse_args()

prj = Openflow(odir='../build/openflow')

prj.add_param('FREQ', '100000000')
prj.add_param('SECS', '1')

if args.source == 'vlog':
    prj.add_include('../sources/vlog/include1')
    prj.add_include('../sources/vlog/include2')
    prj.add_vlog('../sources/vlog/*.v')
if args.source in ['vlog', 'slog']:
    prj.add_define('DEFINE1', '1')
    prj.add_define('DEFINE2', '1')

prj.set_top('Top')

if args.action in ['make', 'all']:
    prj.make()

if args.action in ['prog', 'all']:
    prj.prog()
