from shutil import disk_usage
from os.path import isdir
from tiramisu import FilenameOption, FloatOption, ChoiceOption, OptionDescription, Leadership, \
                     Config, \
                     Calculation, Params, ParamValue, ParamOption, ParamSelfOption

def valid_is_dir(path):
    # verify if path is a directory
    if not isdir(path):
        raise ValueError('this directory does not exist')

def calc_disk_usage(path, size):
    if size == 'bytes':
        div = 1
    else:
        # bytes to gigabytes
        div = 1024 * 1024 * 1024
    return disk_usage(path).free / div


filename = FilenameOption('path', 'Path', validators=[Calculation(valid_is_dir,
                                                      Params(ParamSelfOption(whole=False)))],
                          multi=True)
size_type = ChoiceOption('size_type', 'Size type', ('bytes', 'giga bytes'),
                          default_multi='bytes', multi=True)
usage = FloatOption('usage', 'Disk usage', Calculation(calc_disk_usage,
                                                       Params((ParamOption(filename),
                                                               ParamOption(size_type)))),
                    multi=True)
disk = Leadership('disk', 'Verify disk usage', [filename, size_type, usage])
root = OptionDescription('root', 'root', [disk])
config = Config(root)
config.property.read_write()

