# -*- coding: utf-8 -*-
"Leadership support"
# Copyright (C) 2014-2024 Team tiramisu (see AUTHORS for all contributors)
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
import weakref
from typing import List, Iterator, Optional


from ..i18n import _
from ..setting import groups, undefined, ALLOWED_LEADER_PROPERTIES
from .optiondescription import OptionDescription

# from .syndynoption import SynDynLeadership
from .baseoption import BaseOption
from .option import Option
from ..error import LeadershipError
from ..autolib import Calculation


class Leadership(OptionDescription):
    """Leadership"""

    # pylint: disable=too-many-arguments
    __slots__ = (
        "leader",
        "followers",
    )

    def __init__(
        self,
        name: str,
        doc,
        children: List[BaseOption],
        **kwargs,
    ) -> None:
        if "group_type" in kwargs:
            raise LeadershipError(
                _('cannot set "group_type" attribute for a Leadership')
            )
        super().__init__(
            name,
            doc,
            children,
            **kwargs,
        )
        self._group_type = groups.leadership
        followers = []
        if len(children) < 2:
            raise ValueError(
                _(
                    'a leader and a follower are mandatories in leadership "{}"' ""
                ).format(name)
            )
        for idx, child in enumerate(children):
            if __debug__:
                self._check_child_is_valid(child, idx, children)
            if idx != 0:
                if __debug__:
                    self._check_default_value(child)
                # remove empty property for follower
                child._properties = frozenset(child._properties - {"empty", "unique"})
                followers.append(child)
            child._add_dependency(self)
            child._leadership = weakref.ref(self)
        if __debug__:
            leader = children[0]
            for prop in leader.impl_getproperties():
                if prop not in ALLOWED_LEADER_PROPERTIES and not isinstance(
                    prop, Calculation
                ):
                    raise LeadershipError(
                        _('leader cannot have "{}" property').format(prop)
                    )

    def _check_child_is_valid(
        self,
        child: BaseOption,
        index: int,
        children: [BaseOption],
    ) -> None:
        if child.impl_is_symlinkoption():
            if not index:
                raise ValueError(
                    _("leadership {0} shall not have " "a symlinkoption").format(
                        self.impl_get_display_name(None, with_quote=True)
                    )
                )
            return
        if not isinstance(child, Option):
            raise ValueError(
                _("leadership {0} shall not have " "a subgroup").format(
                    self.impl_get_display_name(None, with_quote=True)
                )
            )
        if not child.impl_is_multi():
            raise ValueError(
                _(
                    "only multi option allowed in leadership {0} but option "
                    "{1} is not a multi"
                    ""
                ).format(
                    self.impl_get_display_name(None, with_quote=True),
                    child.impl_get_display_name(None, with_quote=True),
                )
            )

    def _check_default_value(self, child: BaseOption):
        if child.impl_is_symlinkoption():
            return
        default = child.impl_getdefault()
        if default != []:
            if child.impl_is_submulti() and isinstance(default, (list, tuple)):
                for val in default:
                    if not isinstance(val, Calculation):
                        calculation = False
                        break
                else:
                    # empty default is valid
                    calculation = True
            else:
                calculation = isinstance(default, Calculation)
            if not calculation:
                raise ValueError(
                    _(
                        "not allowed default value for follower option {0} in leadership {1}"
                    ).format(
                        child.impl_get_display_name(None, with_quote=True),
                        self.impl_get_display_name(None, with_quote=True),
                    )
                )

    def _setsubdyn(
        self,
        subdyn,
    ) -> None:
        for chld in self._children[1]:
            chld._setsubdyn(subdyn)
        super()._setsubdyn(subdyn)

    def is_leader(
        self,
        opt: Option,
    ) -> bool:
        """the option is the leader"""
        leader = self.get_leader()
        if opt.impl_is_dynsymlinkoption():
            opt = opt.opt
        return opt == leader

    def get_leader(self) -> Option:
        """get leader"""
        return self._children[1][0]

    def get_followers(self) -> Iterator[Option]:
        """get all followers"""
        for follower in self._children[1][1:]:
            yield follower

    def in_same_leadership(
        self,
        opt: Option,
    ) -> bool:
        """check if followers are in same leadership"""
        if opt.impl_is_dynsymlinkoption():
            opt = opt.opt
        return opt in self._children[1]

    def reset(self, parent: "SubConfig") -> None:
        """reset follower value"""
        values = parent.config_bag.context.get_values()
        for follower in self.get_followers():
            subconfig_follower = parent.get_child(
                follower,
                None,
                False,
            )
            values.reset(
                subconfig_follower,
                validate=False,
            )

    def follower_force_store_value(
        self,
        value,
        subconfig: "SubConfig",
        owner,
    ) -> None:
        """apply force_store_value to follower"""
        if not value:
            return
        config_bag = subconfig.config_bag
        values = config_bag.context.get_values()
        for idx, follower in enumerate(self.get_children()):
            sub_subconfig = subconfig.get_child(
                follower,
                None,
                False,
                config_bag=config_bag,
            )
            if "force_store_value" not in sub_subconfig.properties:
                continue
            self_path = sub_subconfig.path
            if not idx:
                # it's a master
                apply_requires = True
                indexes = [None]
            else:
                apply_requires = False
                indexes = range(len(value))
            for index in indexes:
                i_sub_subconfig = subconfig.get_child(
                    follower,
                    index,
                    False,
                    config_bag=config_bag,
                )
                values.set_storage_value(
                    self_path,
                    index,
                    values.get_value(i_sub_subconfig)[0],
                    owner,
                )

    def pop(
        self,
        subconfig: "SubConfig",
        index: int,
        *,
        followers: Optional[List[Option]] = undefined,
    ) -> None:
        """pop leader value and follower's one"""
        if followers is undefined:
            # followers are not undefined only in SynDynLeadership
            followers = self.get_followers()
        config_bag = subconfig.config_bag.copy()
        config_bag.remove_validation()
        values = config_bag.context.get_values()
        for follower in followers:
            sub_subconfig = subconfig.parent.get_child(
                follower,
                index,
                True,
                properties=set(),  # do not check force_default_on_freeze
                # or force_metaconfig_on_freeze
                config_bag=config_bag,
            )
            values.reduce_index(sub_subconfig)

    def reset_cache(
        self,
        path: str,
        config_bag: "ConfigBag",
        resetted_opts: List[Option],
    ) -> None:
        self._reset_cache(
            path,
            self.get_leader(),
            self.get_followers(),
            config_bag,
            resetted_opts,
        )

    def _reset_cache(
        self,
        path: str,
        leader: Option,
        followers: List[Option],
        config_bag: "ConfigBag",
        resetted_opts: List[Option],
    ) -> None:
        super().reset_cache(
            path,
            config_bag,
            resetted_opts,
        )
        leader_path = leader.impl_getpath()
        if leader_path not in resetted_opts:
            leader.reset_cache(
                leader_path,
                config_bag,
                resetted_opts,
            )
        for follower in followers:
            follower_path = follower.impl_getpath()
            if follower_path not in resetted_opts:
                follower.reset_cache(
                    follower_path,
                    config_bag,
                    resetted_opts,
                )

    def impl_is_leadership(self) -> None:
        return True
