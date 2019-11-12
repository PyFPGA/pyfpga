"""PyFPGA Multi Vendor example."""

from fpga.project import Project

tools = {
    'vivado': {
        'project': 'zybo',
        'part': 'xc7z010-1-clg400',
        'constraint': 'zybo/zybo.xdc'
    },
    'ise': {
        'project': 's6micro',
        'part': 'XC6SLX9-2-CSG324',
        'constraint': 's6micro/s6micro.ucf'
    },
    'quartus': {
        'project': 'de10nano',
        'part': '5CSEBA6U23I7',
        'constraint': 'de10nano/de10nano.tcl'
    },
    'libero': {
        'project': 'mpf300',
        'part': 'mpf300ts-1-fcg1152',
        'constraint': 'mpf300/mpf300.pdc'
    }
}

for tool in tools:
    PRJ = Project(tool, tools[tool]['project'])
    PRJ.set_outdir('../build/multi/%s' % tools[tool]['project'])
    PRJ.set_part(tools[tool]['part'])
    PRJ.add_files('hdl/*.vhdl')
    PRJ.add_files(tools[tool]['constraint'])
    PRJ.set_top('Top')
    try:
        PRJ.generate()
    except:
        print('%s is not available' % tool)
