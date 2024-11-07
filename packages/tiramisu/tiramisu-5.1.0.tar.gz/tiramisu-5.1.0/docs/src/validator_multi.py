from tiramisu import IntOption, OptionDescription, Config, \
                     Calculation, Params, ParamSelfOption
from tiramisu.error import ValueWarning
import warnings


def valid_pourcent(option):
    total = sum(option)
    if total > 100:
        raise ValueError(f'the total {total}% is bigger than 100%')
    if total < 100:
        raise ValueWarning(f'the total {total}% is lower than 100%')


percent = IntOption('percent',
                    'Percent',
                    multi=True,
                    validators=[Calculation(valid_pourcent, Params(ParamSelfOption()))])
config = Config(OptionDescription('root', 'root', [percent]))


# too big
try:
    config.option('percent').value.set([20, 90])
except ValueError as err:
    err.prefix = ''
    print(f'Error: {err}')
percent_value = config.option('percent').value.get()
print(f'The value is "{percent_value}"')

# too short
warnings.simplefilter('always', ValueWarning)
with warnings.catch_warnings(record=True) as warn:
    config.option('percent').value.set([20, 70])
    if warn:
        warn[0].message.prefix = ''
        print(f'Warning: {warn[0].message}')
    percent_value = config.option('percent').value.get()
print(f'The value is "{percent_value}"')

# correct
config.option('percent').value.set([20, 80])
percent_value = config.option('percent').value.get()
print(f'The value is "{percent_value}"')
