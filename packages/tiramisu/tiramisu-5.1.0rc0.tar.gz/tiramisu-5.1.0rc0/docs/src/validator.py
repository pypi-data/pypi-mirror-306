#!/usr/bin/env python3

from tiramisu import StrOption, IntOption, OptionDescription, Config, \
                     Calculation, Params, ParamOption, ParamSelfOption, ParamValue
from tiramisu.error import ValueWarning
import warnings
from re import match


# Creation differents function
def is_password_conform(password):
    # password must containe at least a number, a lowercase letter, an uppercase letter and a symbol
    if not match(r'(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W)', password):
        raise ValueError('please choose a stronger password, try a mix of letters, numbers and symbols')


# Password must have at least min_len characters
def password_correct_len(min_len, recommand_len, password):
    if len(password) < min_len:
        raise ValueError(f'use {min_len} characters or more for your password')
    # password should have at least recommand_len characters
    if len(password) < recommand_len:
        raise ValueWarning(f'it would be better to use more than {recommand_len} characters for your password')


def user_not_in_password(login, password):
    if login in password:
        raise ValueError('the login must not be part of the password')


def password_match(password1, password2):
    if password1 != password2:
        raise ValueError("those passwords didn't match, try again")


# Create first option to ask user's login
login = StrOption('login', 'Login', properties=('mandatory',))

# Creation calculatin for first password
calc1 = Calculation(is_password_conform,
                    Params(ParamSelfOption()))

calc2 = Calculation(password_correct_len,
                    Params((ParamValue(8),
                            ParamValue(12),
                            ParamSelfOption())))

calc3 = Calculation(user_not_in_password,
                    Params(kwargs={'login': ParamOption(login),
                                   'password': ParamSelfOption()}),
                    warnings_only=True)


# Create second option to ask user's password
password1 = StrOption('password1',
                      'Password',
                      properties=('mandatory',),
                      validators=[calc1, calc2, calc3])

# Create third option to confirm user's password
password2 = StrOption('password2',
                      'Confirm',
                      properties=('mandatory',),
                      validators=[Calculation(password_match, Params((ParamOption(password1), ParamSelfOption())))])

# Creation optiondescription and config
od = OptionDescription('password', 'Define your password', [password1, password2])
root = OptionDescription('root', '', [login, od])
config = Config(root)
config.property.read_write()

# no number and no symbol (with prefix)
config.option('login').value.set('user')
try:
    config.option('password.password1').value.set('aAbBc')
except ValueError as err:
    print(f'Error: {err}')

# no number and no symbol
config.option('login').value.set('user')
try:
    config.option('password.password1').value.set('aAbBc')
except ValueError as err:
    err.prefix = ''
    print(f'Error: {err}')

# too short password
config.option('login').value.set('user')
try:
    config.option('password.password1').value.set('aZ$1')
except ValueError as err:
    err.prefix = ''
    print(f'Error: {err}')

# warnings too short password
warnings.simplefilter('always', ValueWarning)
config.option('login').value.set('user')
with warnings.catch_warnings(record=True) as warn:
    config.option('password.password1').value.set('aZ$1bN:2')
    if warn:
        warn[0].message.prefix = ''
        print(f'Warning: {warn[0].message}')
    password = config.option('password.password1').value.get()
print(f'The password is "{password}"')

# password with login
warnings.simplefilter('always', ValueWarning)
config.option('login').value.set('user')
with warnings.catch_warnings(record=True) as warn:
    config.option('password.password1').value.set('aZ$1bN:2u@1Bjuser')
    if warn:
        warn[0].message.prefix = ''
        print(f'Warning: {warn[0].message}')
    password = config.option('password.password1').value.get()
print(f'The password is "{password}"')

# password1 not matching password2
config.option('login').value.set('user')
config.option('password.password1').value.set('aZ$1bN:2u@1Bj')
try:
    config.option('password.password2').value.set('aZ$1aaaa')
except ValueError as err:
    err.prefix = ''
    print(f'Error: {err}')

# and finaly passwod match
config.option('login').value.set('user')
config.option('password.password1').value.set('aZ$1bN:2u@1Bj')
config.option('password.password2').value.set('aZ$1bN:2u@1Bj')
config.property.read_only()
user_login = config.option('login').value.get()
password = config.option('password.password2').value.get()
print(f'The password for "{user_login}" is "{password}"')
