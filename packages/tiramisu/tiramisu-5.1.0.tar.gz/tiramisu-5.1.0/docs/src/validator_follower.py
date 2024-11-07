from tiramisu import StrOption, IntOption, Leadership, OptionDescription, Config, \
                     Calculation, Params, ParamSelfOption, ParamIndex
from tiramisu.error import ValueWarning
import warnings


def valid_pourcent(option, current_option, index):
    if None in option:
        return
    total = sum(option)
    if total > 100:
        raise ValueError(f'the value {current_option} (at index {index}) is too big, the total is {total}%')


calculation = Calculation(valid_pourcent, Params((ParamSelfOption(whole=True),
                                                  ParamSelfOption(),
												  ParamIndex())))


user = StrOption('user', 'User', multi=True)
percent = IntOption('percent',
                    'Distribution',
                    multi=True,
                    validators=[calculation])
od = Leadership('percent', 'Percent', [user, percent])
config = Config(OptionDescription('root', 'root', [od]))


config.option('percent.user').value.set(['user1', 'user2'])
config.option('percent.percent', 0).value.set(20)


# too big
try:
    config.option('percent.percent', 1).value.set(90)
except ValueError as err:
    err.prefix = ''
    print(f'Error: {err}')

# correct
config.option('percent.percent', 1).value.set(80)
