from pyfpga.vivado import Vivado


def test_vivado():
    prj = Vivado()
    prj.add_hook('precfg', 'HOOK1')
    prj.add_hook('precfg', 'HOOK1')
    prj.add_hook('postcfg', 'HOOK2')
    prj.add_hook('postcfg', 'HOOK2')
    prj.add_hook('presyn', 'HOOK3')
    prj.add_hook('presyn', 'HOOK3')
    prj.add_hook('postsyn', 'HOOK4')
    prj.add_hook('postsyn', 'HOOK4')
    prj.add_hook('prepar', 'HOOK5')
    prj.add_hook('prepar', 'HOOK5')
    prj.add_hook('postpar', 'HOOK6')
    prj.add_hook('postpar', 'HOOK6')
    prj.add_hook('prebit', 'HOOK7')
    prj.add_hook('prebit', 'HOOK7')
    prj.add_hook('postbit', 'HOOK8')
    prj.add_hook('postbit', 'HOOK8')
    prj.make()
