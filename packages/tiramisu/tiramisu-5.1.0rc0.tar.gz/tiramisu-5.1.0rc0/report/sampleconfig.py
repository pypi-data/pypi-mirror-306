# coding: utf-8
from tiramisu.config import *
from tiramisu.option import *

gcoption = ChoiceOption('name', 'GC name', ('ref', 'framework'), 'ref')
gcdummy = BoolOption('dummy', 'dummy', default=False)
objspaceoption = ChoiceOption('objspace', 'Object space',
                            ('std', 'thunk'), 'std')
booloption = BoolOption('bool', 'Test boolean option', default=True)
intoption = IntOption('int', 'Test int option', default=0)
floatoption = FloatOption('float', 'Test float option', default=2.3)
stroption = StrOption('str', 'Test string option', default="abc")
boolop = BoolOption('boolop', 'Test boolean option op', default=True)
wantref_option = BoolOption('wantref', 'Test requires', default=False)
wantframework_option = BoolOption('wantframework', 'Test requires',
                                  default=False)

gcgroup = OptionDescription('gc', 'doc pour gc', [gcoption, gcdummy, floatoption])
descr = OptionDescription('essai', 'une éééééé doc pour essai', [gcgroup, booloption, objspaceoption,
                                       wantref_option, stroption,
                                       wantframework_option,
                                       intoption, boolop])

def get_example_config():
    return Config(descr)
