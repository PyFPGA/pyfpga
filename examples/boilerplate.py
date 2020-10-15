"""PyFPGA boilerplate.

References:
* <TAG> must be replaced by a valid value.
* OPT_ means optional.
* What is unused can be deleted.
"""

import argparse
import logging

from fpga.project import Project

logging.basicConfig()
logging.getLogger('fpga.project').level = logging.DEBUG

parser = argparse.ArgumentParser()
parser.add_argument(
    '--action', choices=['generate', 'transfer', 'all'], default='generate',
)
args = parser.parse_args()

PRJ = Project('<TOOL>', '<OPT_PROJECT_NAME>')
PRJ.set_outdir('<OUTPUT_DIR>')  # if needed

PRJ.set_part('<FPGA>')  # default value depends on the used tool
PRJ.add_path('<VERILOG_INCLUDE_DIRECTORY>')  # if needed
PRJ.add_files(
    '<PATH_TO_FILE_OR_FILES>',
    fileset='<OPT_FILESET>',  # automatically discovered if not specified
    library='<OPT_VHDL_PACKAGE_NAME>',
    options='<OPT_OPTIONS>'  # tool specific options for particular cases
)
PRJ.set_top('<TOP_LEVEL_COMPONENT_NAME_OR_PATH_TO_FILE>')

# Following (add_hook) only if needed (uncommon)

PRJ.add_hook('<PRE_FILE_COMMAND_1>', 'prefile')
PRJ.add_hook('<POST_PRJ_COMMAND_1>', 'project')
PRJ.add_hook('<PRE_FLOW_COMMAND_1>', 'preflow')
PRJ.add_hook('<POST_SYN_COMMAND_1>', 'postsyn')
PRJ.add_hook('<POST_IMP_COMMAND_1>', 'postimp')
PRJ.add_hook('<POST_BIT_COMMAND_1>', 'postbit')

PRJ.add_hook('<PRE_FILE_COMMAND_2>', 'prefile')
PRJ.add_hook('<POST_PRJ_COMMAND_2>', 'project')
PRJ.add_hook('<PRE_FLOW_COMMAND_2>', 'preflow')
PRJ.add_hook('<POST_SYN_COMMAND_2>', 'postsyn')
PRJ.add_hook('<POST_IMP_COMMAND_2>', 'postimp')
PRJ.add_hook('<POST_BIT_COMMAND_2>', 'postbit')

if args.action in ['generate', 'all']:
    try:
        PRJ.generate(
            '<OPT_STRATEGY>',            # dafault is 'default'
            to_task='<OPT_TO_TASK>',     # dafault is 'bit'
            from_task='<OPT_FROM_TASK>'  # dafault is 'prj'
        )
    except Exception as e:
        logging.warning('{} ({})'.format(type(e).__name__, e))

if args.action in ['transfer', 'all']:
    try:
        PRJ.transfer(
            '<OPT_DEVICE>',             # default is 'fpga'
            position='<OPT_POSITION>',  # default is 1
            part='<OPT_MEM_PART>',      # default is empty
            width='<OPT_MEM_WIDTH>'     # default is 1
        )
    except Exception as e:
        logging.warning('{} ({})'.format(type(e).__name__, e))
