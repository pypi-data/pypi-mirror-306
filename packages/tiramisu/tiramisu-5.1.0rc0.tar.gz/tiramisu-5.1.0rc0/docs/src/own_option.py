#!/usr/bin/env python3

import re
from tiramisu import RegexpOption


class VowelOption(RegexpOption):
    __slots__ = tuple()
    _type = 'vowel'
    _regexp = re.compile(r"^[aeiouy]*$")
