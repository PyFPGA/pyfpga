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
PRJ.set_outdir('<OPT_OUTPUT_DIR>')

PRJ.set_part('<FPGA>')
PRJ.add_include('<OPT_VERILOG_INCLUDE_DIRECTORY>')
PRJ.add_files('<PATH_TO_FILE_OR_FILES>', '<OPT_VHDL_PACKAGE_NAME>')
PRJ.set_top('<TOP_LEVEL_COMPONENT_NAME_OR_PATH_TO_FILE>')

PRJ.add_hook('prefile', '<OPT_PRE_FILE_COMMAND_1>')
PRJ.add_hook('postprj', '<OPT_POST_PRJ_COMMAND_1>')
PRJ.add_hook('preflow', '<OPT_PRE_FLOW_COMMAND_1>')
PRJ.add_hook('postsyn', '<OPT_POST_SYN_COMMAND_1>')
PRJ.add_hook('postimp', '<OPT_POST_IMP_COMMAND_1>')
PRJ.add_hook('postbit', '<OPT_POST_BIT_COMMAND_1>')

PRJ.add_hook('prefile', '<OPT_PRE_FILE_COMMAND_2>')
PRJ.add_hook('postprj', '<OPT_POST_PRJ_COMMAND_2>')
PRJ.add_hook('preflow', '<OPT_PRE_FLOW_COMMAND_2>')
PRJ.add_hook('postsyn', '<OPT_POST_SYN_COMMAND_2>')
PRJ.add_hook('postimp', '<OPT_POST_IMP_COMMAND_2>')
PRJ.add_hook('postbit', '<OPT_POST_BIT_COMMAND_2>')

if args.action in ['generate', 'all']:
    try:
        PRJ.generate('<OPT_STRATEGY>', '<OPT_TO_TASK>', '<OPT_FROM_TASK>')
    except Exception as e:
        logging.warning('{} ({})'.format(type(e).__name__, e))

if args.action in ['transfer', 'all']:
    try:
        PRJ.transfer(
            '<OPT_DEVICE>', '<OPT_POSITION>',
            '<OPT_MEM_PART>', '<OPT_MEM_WIDTH>'
        )
    except Exception as e:
        logging.warning('{} ({})'.format(type(e).__name__, e))
