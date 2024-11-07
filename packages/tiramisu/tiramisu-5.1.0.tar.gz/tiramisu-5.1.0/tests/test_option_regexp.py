""" RegexpOption
"""
from .autopath import do_autopath
do_autopath()

import pytest
from tiramisu import RegexpOption, OptionDescription, Config
import re


class ColorOption(RegexpOption):
    __slots__ = tuple()
    _type = 'Color'
    _regexp = re.compile(r"^#(?:[0-9a-f]{3}){1,2}$")


def test_regexp_option():
    r = ColorOption('test', 'test')
    od = OptionDescription('od', 'od', [r])
    cfg = Config(od)
    cfg.option('test').value.set('#ff0000')
    with pytest.raises(ValueError):
        cfg.option('test').value.set('not a color')
