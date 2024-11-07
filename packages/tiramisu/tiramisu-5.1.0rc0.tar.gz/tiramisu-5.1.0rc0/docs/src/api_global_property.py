from os.path import exists
from tiramisu import FilenameOption, BoolOption, OptionDescription, Leadership, \
                     Config, Calculation, Params, ParamOption
from tiramisu.error import PropertiesOptionError


filename = FilenameOption('filename',
                          'Filename',
                          multi=True,
                          properties=('mandatory',))
exists_ = BoolOption('exists',
                     'This file exists',
                     Calculation(exists, Params(ParamOption(filename))),
                     multi=True,
                     properties=('frozen', 'force_default_on_freeze', 'advanced'))
new = Leadership('new',
                 'Add new file',
                 [filename, exists_])
root = OptionDescription('root', 'root', [new])
config = Config(root)
