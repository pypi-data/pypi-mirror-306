from tiramisu import IntOption, OptionDescription, MetaConfig
from tiramisu.error import ConfigError
import pytest


def make_metaconfig():
    i1 = IntOption('i1', '')
    i2 = IntOption('i2', '', default=1)
    i3 = IntOption('i3', '')
    i4 = IntOption('i4', '', default=2)
    i5 = IntOption('i5', '', default=[2], multi=True)
    i6 = IntOption('i6', '', properties=('disabled',))
    od1 = OptionDescription('od1', '', [i1, i2, i3, i4, i5, i6])
    od2 = OptionDescription('od2', '', [od1])
    return MetaConfig([], optiondescription=od2, name='metacfg1')


#def test_multi_parents_path():
#    """
#    metacfg1 (1) ---
#                   | -- cfg1
#    metacfg2 (2) ---
#    """
#    metacfg1 = make_metaconfig()
#    cfg1 = metacfg1.config.new(type='config', name="cfg1")
#    metacfg2 = MetaConfig([cfg1], name='metacfg2')
#    #
#    assert metacfg1.config.path() == 'metacfg1'
#    assert metacfg2.config.path() == 'metacfg2'
#    assert cfg1.config.path() == 'metacfg2.metacfg1.cfg1'
#
#
#def test_multi_parents_path_same():
#    """
#               --- metacfg2 (1) ---
#    metacfg1 --|                  | -- cfg1
#               --- metacfg3 (2) ---
#    """
#    metacfg1 = make_metaconfig()
#    metacfg2 = metacfg1.config.new(type='metaconfig', name="metacfg2")
#    metacfg3 = metacfg1.config.new(type='metaconfig', name="metacfg3")
#    cfg1 = metacfg2.config.new(type='config', name="cfg1")
#    metacfg3.config.add(cfg1)
#    #
#    assert metacfg2.config.path() == 'metacfg1.metacfg2'
#    assert metacfg3.config.path() == 'metacfg1.metacfg3'
#    assert cfg1.config.path() == 'metacfg1.metacfg3.metacfg1.metacfg2.cfg1'
#    metacfg1.option('od1.i1').value.set(1)
#    metacfg3.option('od1.i1').value.set(2)
#    assert cfg1.option('od1.i1').value.get() == 1
#    orideep = cfg1.config.deepcopy(metaconfig_prefix="test_", name='test_cfg1')
#    deep = orideep
#    while True:
#        try:
#            children = list(deep.config.list())
#        except:
#            break
#        assert len(children) < 2
#        deep = children[0]
#    assert deep.config.path() == 'test_metacfg3.test_metacfg1.test_metacfg2.test_cfg1'
#    assert cfg1.option('od1.i1').value.get() == 1
#
#
#
#def test_multi_parents_value():
#    metacfg1 = make_metaconfig()
#    cfg1 = metacfg1.config.new(type='config', name="cfg1")
#    metacfg2 = MetaConfig([cfg1], name='metacfg2')
#    #
#    assert cfg1.option('od1.i1').value.get() == None
#    assert cfg1.option('od1.i2').value.get() == 1
#    assert cfg1.option('od1.i3').value.get() == None
#    #
#    assert metacfg1.option('od1.i1').value.get() == None
#    assert metacfg1.option('od1.i2').value.get() == 1
#    assert metacfg1.option('od1.i3').value.get() == None
#    #
#    assert metacfg2.option('od1.i1').value.get() == None
#    assert metacfg2.option('od1.i2').value.get() == 1
#    assert metacfg2.option('od1.i3').value.get() == None
#    #
#    metacfg1.option('od1.i3').value.set(3)
#    assert metacfg1.option('od1.i3').value.get() == 3
#    assert cfg1.option('od1.i3').value.get() == 3
#    assert metacfg2.option('od1.i2').value.get() == 1
#    #
#    metacfg2.option('od1.i2').value.set(4)
#    assert metacfg2.option('od1.i2').value.get() == 4
#    assert metacfg1.option('od1.i2').value.get() == 1
#    assert cfg1.option('od1.i2').value.get() == 4
