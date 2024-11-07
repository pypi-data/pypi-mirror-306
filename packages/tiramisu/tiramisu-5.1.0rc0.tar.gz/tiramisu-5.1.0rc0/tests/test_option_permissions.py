"configuration objects global API"
from .autopath import do_autopath
do_autopath()

import pytest

from tiramisu import PermissionsOption


def test_permissions():
    PermissionsOption('a', '', 640)
    PermissionsOption('a', '', 642)
    PermissionsOption('a', '', 751)
    PermissionsOption('a', '', 753)
    PermissionsOption('a', '', 7555)
    PermissionsOption('a', '', 1755)
    with pytest.raises(ValueError):
        PermissionsOption('a', '', 800)
    with pytest.raises(ValueError):
        PermissionsOption('a', '', 75)
    with pytest.raises(ValueError):
        PermissionsOption('a', '', 77775)
    with pytest.raises(ValueError):
        PermissionsOption('a', '', '755')
    with pytest.raises(ValueError):
        PermissionsOption('a', '', 'string')
    with pytest.raises(ValueError):
        PermissionsOption('a', '', 800)
    with pytest.raises(ValueError):
        PermissionsOption('a', '', 1575)
    with pytest.raises(ValueError):
        PermissionsOption('a', '', 1557)
    with pytest.raises(ValueError):
        PermissionsOption('a', '', 777)
    with pytest.raises(ValueError):
        PermissionsOption('a', '', 1777)
