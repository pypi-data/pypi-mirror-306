# -*- coding: utf-8 -*-
# Copyright (C) 2017-2024 Team tiramisu (see AUTHORS for all contributors)
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# The original `Config` design model is unproudly borrowed from
# the rough pypy's guys: http://codespeak.net/svn/pypy/dist/pypy/config/
# the whole pypy projet is under MIT licence
# ____________________________________________________________
"""SymLinkOption link to an other option
"""
from typing import Any, Optional, Dict
from .baseoption import BaseOption, valid_name
from ..error import ConfigError
from ..i18n import _


class SymLinkOption(BaseOption):
    """SymLinkOption link to an other option"""

    __slots__ = (
        "_opt",
        "_leadership",
    )

    def __init__(
        self,
        name: str,
        opt: BaseOption,
    ) -> None:
        # pylint: disable=super-init-not-called
        if not valid_name(name):
            raise ValueError(_('"{0}" is an invalid name for an option').format(name))
        if (
            not isinstance(opt, BaseOption)
            or opt.impl_is_optiondescription()
            or opt.impl_is_symlinkoption()
        ):
            raise ValueError(
                _(
                    'malformed symlink second parameters must be an option for "{0}", not {1}'
                ).format(name, opt)
            )
        self._name = name
        self._opt = opt
        self._leadership = None
        opt._add_dependency(self)

    def __getattr__(
        self,
        name: str,
    ) -> Any:
        if name == "_subdyns":
            return None
        if name == "_path":
            raise AttributeError()
        return getattr(self._opt, name)

    def impl_is_symlinkoption(self) -> bool:
        """it's a symlinkoption"""
        return True

    def impl_is_leader(self) -> bool:
        return False

    def impl_is_follower(self):
        """check if option is a leader in a follower"""
        leadership = self._leadership
        if leadership is None:
            return False
        return not leadership().is_leader(self)

    def impl_getopt(self) -> BaseOption:
        """get to linked option"""
        return self._opt

    def impl_is_multi(self) -> bool:
        """is it a multi?"""
        if self._opt.impl_is_multi():
            return True
        if self._opt.issubdyn() or self.issubdyn():
            if self.issubdyn() != self._opt.issubdyn():
                return self._opt.issubdyn()
            return self._opt.issubdyn() in self.get_sub_dyns()
        return False

    def impl_is_submulti(self) -> bool:
        """is it a submulti?"""
        return self._opt.impl_is_submulti()
