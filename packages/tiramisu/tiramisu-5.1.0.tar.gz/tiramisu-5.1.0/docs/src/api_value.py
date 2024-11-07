from shutil import disk_usage
from os.path import isdir
from tiramisu import FilenameOption, FloatOption, OptionDescription, Config, \
                     Calculation, Params, ParamValue, ParamOption, ParamSelfOption

def valid_is_dir(path):
    # verify if path is a directory
    if not isdir(path):
        raise ValueError('this directory does not exist')

def calc_disk_usage(path, size='bytes'):
    # do not calc if path is None
    if path is None:
        return None

    if size == 'bytes':
        div = 1
    else:
        # bytes to gigabytes
        div = 1024 * 1024 * 1024
    return disk_usage(path).free / div


filename = FilenameOption('path', 'Path', validators=[Calculation(valid_is_dir,
                                                      Params(ParamSelfOption()))])
usage = FloatOption('usage', 'Disk usage', Calculation(calc_disk_usage,
                                                       Params(ParamOption(filename))))
disk = OptionDescription('disk', 'Verify disk usage', [filename, usage])
root = OptionDescription('root', 'root', [disk])
config = Config(root)
config.property.read_write()
