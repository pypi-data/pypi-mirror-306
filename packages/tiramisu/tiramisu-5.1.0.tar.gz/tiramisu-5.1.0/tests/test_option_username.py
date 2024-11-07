"configuration objects global API"
from .autopath import do_autopath
do_autopath()

import pytest

from tiramisu import UsernameOption


def test_username():
    UsernameOption('a', '', 'string')
    UsernameOption('a', '', '_string')
    UsernameOption('a', '', 's_tring')
    UsernameOption('a', '', 'string_')
    UsernameOption('a', '', 'string$')
    UsernameOption('a', '', '_string$')
    with pytest.raises(ValueError):
        UsernameOption('a', '', 'strin$g')
    UsernameOption('a', '', 's-tring')
    with pytest.raises(ValueError):
        UsernameOption('a', '', '-string')
    UsernameOption('a', '', 's9tring')
    with pytest.raises(ValueError):
        UsernameOption('a', '', '9string')
    with pytest.raises(ValueError):
        UsernameOption('a', '', '')
    UsernameOption('a', '', 's')
    UsernameOption('a', '', 's2345678901234567890123456789012')
    with pytest.raises(ValueError):
        UsernameOption('a', '', 's23456789012345678901234567890123')
    UsernameOption('a', '', 's234567890123456789012345678901$')
    with pytest.raises(ValueError):
        UsernameOption('a', '', 's2345678901234567890123456789012$')
