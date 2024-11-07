from stat import S_IMODE, S_ISDIR, S_ISSOCK
from os import lstat, getuid, getgid
from os.path import exists
from pwd import getpwuid
from grp import getgrgid
from tiramisu import FilenameOption, UsernameOption, GroupnameOption, IntOption, BoolOption, ChoiceOption, \
                     OptionDescription, Leadership, Config, Calculation, Params, ParamSelfOption, ParamOption, ParamValue, \
                     calc_value
from tiramisu.error import LeadershipError, PropertiesOptionError


def get_username(filename, exists, create=False):
    if exists:
        uid = lstat(filename).st_uid
    elif create:
        # the current uid
        uid = getuid()
    else:
        return

    return getpwuid(uid).pw_name


def get_grpname(filename, exists, create=False):
    if exists:
        gid = lstat(filename).st_gid
    elif create:
        # the current gid
        gid = getgid()
    else:
        return
    return getgrgid(gid).gr_name


def calc_type(filename, is_exists):
    if is_exists:
        mode = lstat(filename).st_mode
        if S_ISSOCK(mode):
            return 'socket'
        elif S_ISDIR(mode):
            return 'directory'
        return 'file'


def calc_mode(filename, is_exists, type):
    if is_exists:
        return int(oct(S_IMODE(lstat(filename).st_mode))[2:])
    if type == 'file':
        return 644
    elif type == 'directory':
        return 755
    elif type == 'socket':
        return 444


filename = FilenameOption('filename',
                          'Filename',
                          multi=True,
                          properties=('mandatory',))
exists_ = BoolOption('exists',
                     'This file exists',
                     Calculation(exists, Params(ParamOption(filename))),
                     multi=True,
                     properties=('mandatory', 'frozen', 'force_default_on_freeze', 'advanced'))
create = BoolOption('create',
                    'Create automaticly the file',
                    multi=True,
                    default_multi=True,
                    properties=(Calculation(calc_value,
                                            Params(ParamValue('disabled'),
                                                   kwargs={'condition': ParamOption(exists_),
                                                           'expected': ParamValue(True)})),))
type_ = ChoiceOption('type',
                     'The file type',
                     ('file', 'directory', 'socket'),
                     Calculation(calc_type, Params((ParamOption(filename),
                                                    ParamOption(exists_)))),
                     multi=True,
                     properties=('force_default_on_freeze', 'mandatory',
                                 Calculation(calc_value,
                                             Params(ParamValue('hidden'),
                                                     kwargs={'condition': ParamOption(exists_),
                                                             'expected': ParamValue(True)})),
                                 Calculation(calc_value,
                                             Params(ParamValue('frozen'),
                                                     kwargs={'condition': ParamOption(exists_),
                                                             'expected': ParamValue(True)}))))
username = UsernameOption('user',
                          'User',
                          default_multi=Calculation(get_username, Params((ParamOption(filename),
                                                                          ParamOption(exists_),
                                                                          ParamOption(create, notraisepropertyerror=True)))),
                          multi=True,
                          properties=('force_store_value',
                                      Calculation(calc_value,
                                                  Params(ParamValue('mandatory'),
                                                          kwargs={'condition': ParamOption(create, notraisepropertyerror=True),
                                                                  'expected': ParamValue(True),
                                                                  'no_condition_is_invalid': ParamValue(True)})),))
grpname = GroupnameOption('group',
                          'Group',
                          default_multi=Calculation(get_grpname, Params((ParamOption(filename),
                                                                          ParamOption(exists_),
                                                                          ParamOption(create, notraisepropertyerror=True)))),
                          multi=True,
                          properties=('force_store_value',
                                      Calculation(calc_value,
                                                  Params(ParamValue('mandatory'),
                                                          kwargs={'condition': ParamOption(create, notraisepropertyerror=True),
                                                                  'expected': ParamValue(True),
                                                                  'no_condition_is_invalid': ParamValue(True)})),))
mode = IntOption('mode',
                 'Mode',
                 default_multi=Calculation(calc_mode, Params((ParamOption(filename), ParamOption(exists_), ParamOption(type_)))),
                 multi=True,
                 properties=('mandatory', 'advanced', 'force_store_value'))

new = Leadership('new',
                 'Add new file',
                 [filename, exists_, create, type_, username, grpname, mode])

root = OptionDescription('root', 'root', [new])

config = Config(root)




#config.option('new.create', 1).value.set(False)
#config.option('new.type', 1).value.set('file')
#config.option('new.type', 2).value.set('file')
#print(config.value.dict())
#config.option('new.type', 2).value.set('directory')
#print(config.value.dict())
#print(config.unrestraint.option('new.mode', 0).owner.isdefault())
#print(config.unrestraint.option('new.mode', 1).owner.isdefault())
#print(config.unrestraint.option('new.mode', 2).owner.isdefault())
#config.property.read_only()
#print(config.option('new.mode', 0).owner.isdefault())
#print(config.option('new.mode', 1).owner.isdefault())
#print(config.option('new.mode', 2).owner.isdefault())
#print(config.value.dict())
#config.property.read_write()
#config.option('new.type', 2).value.set('file')
#print(config.value.dict())
#config.option('new.mode', 2).value.reset()
#print(config.value.dict())
