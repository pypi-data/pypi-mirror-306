from os.path import exists
from tiramisu import FilenameOption, BoolOption, OptionDescription, Leadership, \
                     Config, Calculation, Params, ParamOption, ParamValue, calc_value
from tiramisu.error import PropertiesOptionError, ConfigError


def inverse(exists_):
    return not exists_


filename = FilenameOption('filename',
                          'Filename',
                          multi=True,
                          properties=('mandatory',))
exists_ = BoolOption('exists',
                     'This file exists',
                     Calculation(exists, Params(ParamOption(filename))),
                     multi=True,
                     properties=('frozen', 'force_default_on_freeze', 'advanced'))
create = BoolOption('create',
                    'Create automaticly the file',
                    multi=True,
                    default_multi=Calculation(inverse, Params(ParamOption(exists_))))
new = Leadership('new',
                 'Add new file',
                 [filename, exists_, create])
root = OptionDescription('root', 'root', [new])
config = Config(root)
