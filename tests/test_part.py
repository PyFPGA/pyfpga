from pyfpga.ise import get_info as get_info_ise
from pyfpga.libero import get_info as get_info_libero
from pyfpga.openflow import get_info as get_info_openflow


def test_ise():
    info = {
        'family': 'kintex7',
        'device': 'xc7k160t',
        'speed': '3',
        'package': 'fbg484'
    }
    assert get_info_ise('xc7k160t-3-fbg484') == info
    assert get_info_ise('xc7k160t-fbg484-3') == info


def test_libero():
    info = {
        'family': 'SmartFusion2',
        'device': 'm2s010',
        'speed': '-1',
        'package': 'tq144'
    }
    assert get_info_libero('m2s010-1-tq144') == info
    assert get_info_libero('m2s010-tq144-1') == info
    info['speed'] = 'STD'
    assert get_info_libero('m2s010-tq144') == info


def test_openflow():
    info = {'family': 'xc7', 'device': 'xc7k160t-3', 'package': 'fbg484'}
    assert get_info_openflow('xc7k160t-3-fbg484') == info
    info = {'family': 'ice40', 'device': 'hx1k', 'package': 'tq144'}
    assert get_info_openflow('hx1k-tq144') == info
    info = {'family': 'ecp5', 'device': '25k', 'package': 'CSFBGA285'}
    assert get_info_openflow('25k-CSFBGA285') == info
    info = {'family': 'ecp5', 'device': 'um5g-85k', 'package': 'CABGA381'}
    assert get_info_openflow('um5g-85k-CABGA381') == info
