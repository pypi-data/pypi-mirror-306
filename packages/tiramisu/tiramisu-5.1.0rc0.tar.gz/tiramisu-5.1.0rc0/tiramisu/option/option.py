# -*- coding: utf-8 -*-
"option types and option description"
# Copyright (C) 2012-2024 Team tiramisu (see AUTHORS for all contributors)
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
import warnings
from typing import Any, List, Optional, Dict
from itertools import chain

from .baseoption import BaseOption, submulti
from ..i18n import _
from ..setting import undefined
from ..autolib import Calculation
from ..error import ValueWarning, ValueErrorWarning, ValueOptionError


class Option(BaseOption):
    # pylint: disable=too-many-statements,too-many-branches,too-many-arguments,too-many-locals
    """
    Abstract base class for configuration option's.

    Reminder: an Option object is **not** a container for the value.
    """
    __slots__ = (
        "_extra",
        "_warnings_only",
        # multi
        "_multi",
        # value
        "_default",
        "_default_multi",
        #
        "_validators",
        #
        "_leadership",
        "_choice_values",
        "_choice_values_params",
    )
    _type = None

    def __init__(
        self,
        name: str,
        doc: str,
        default: Any = undefined,
        default_multi: Any = None,
        multi: bool = False,
        validators: Optional[List[Calculation]] = None,
        properties: Optional[List[str]] = None,
        warnings_only: bool = False,
        extra: Optional[Dict] = None,
        informations: Optional[Dict] = None,
    ):
        _setattr = object.__setattr__
        if not multi and default_multi is not None:
            raise ValueError(
                _(
                    "default_multi is set whereas multi is False" " in option: {0}"
                ).format(name)
            )
        if default is undefined:
            if multi is False:
                default = None
            else:
                default = []
        if multi is True:
            is_multi = True
            _multi = 0
        elif multi is False:
            is_multi = False
            _multi = 1
        elif multi is submulti:
            is_multi = True
            _multi = submulti
        else:
            raise ValueError(
                _('invalid multi type "{}" for "{}"').format(
                    multi,
                    name,
                )
            )
        if _multi != 1:
            _setattr(self, "_multi", _multi)
        if multi is not False and default is None:
            default = []
        super().__init__(
            name,
            doc,
            informations,
            properties=properties,
            is_multi=is_multi,
        )
        if validators is not None:
            if __debug__ and not isinstance(validators, list):
                raise ValueError(
                    _('validators must be a list of Calculation for "{0}"').format(name)
                )
            for validator in validators:
                if __debug__ and not isinstance(validator, Calculation):
                    raise ValueError(
                        _('validators must be a Calculation for "{0}"').format(name)
                    )
                self.value_dependency(validator)
                self._validators = tuple(validators)
        if extra is not None and extra != {}:
            _setattr(self, "_extra", extra)
        if warnings_only is True:
            _setattr(self, "_warnings_only", warnings_only)
        if is_multi and default_multi is not None:

            def test_multi_value(value):
                if isinstance(value, Calculation):
                    return
                #                option_bag = OptionBag(self,
                #                                       None,
                #                                       undefined,
                #                                       properties=None,
                #                                       )
                try:
                    self.validate(value)
                    self.validate_with_option(
                        value,
                        None,
                        loaded=True,
                    )
                except ValueError as err:
                    str_err = str(err)
                    if not str_err:
                        raise ValueError(
                            _(
                                'invalid default_multi value "{0}" ' "for option {1}"
                            ).format(
                                str(value),
                                self.impl_get_display_name(None, with_quote=True),
                            )
                        ) from err
                    raise ValueError(
                        _(
                            'invalid default_multi value "{0}" for option {1}, {2}'
                        ).format(
                            value,
                            self.impl_get_display_name(None, with_quote=True),
                            str_err,
                        )
                    ) from err

            if _multi is submulti:
                if not isinstance(default_multi, Calculation):
                    if not isinstance(default_multi, list):
                        raise ValueError(
                            _(
                                'invalid default_multi value "{0}" '
                                "for option {1}, must be a list for a submulti"
                                ""
                            ).format(
                                str(default_multi),
                                self.impl_get_display_name(None, with_quote=True),
                            )
                        )
                    for value in default_multi:
                        test_multi_value(value)
            else:
                test_multi_value(default_multi)
            _setattr(self, "_default_multi", default_multi)
        #        option_bag = OptionBag(self,
        #                               None,
        #                               undefined,
        #                               properties=None,
        #                               )
        self.impl_validate(
            None,
            default,
            loaded=True,
        )
        self.impl_validate(
            None,
            default,
            check_error=False,
            loaded=True,
        )
        self.value_dependencies(default)
        if (is_multi and default != []) or (not is_multi and default is not None):
            if is_multi and isinstance(default, list):
                default = tuple(default)
            _setattr(self, "_default", default)

    # __________________________________________________________________________
    # option's information

    def impl_is_multi(self) -> bool:
        """is it a multi option"""
        return getattr(self, "_multi", 1) != 1

    def impl_is_submulti(self) -> bool:
        """is it a submulti option"""
        return getattr(self, "_multi", 1) == 2

    def impl_is_dynsymlinkoption(self) -> bool:
        """is a dynsymlinkoption?"""
        return False

    def get_type(self) -> str:
        """get the type of option"""
        return self._type

    def impl_getdefault(self) -> Any:
        """accessing the default value"""
        is_multi = self.impl_is_multi()
        default = getattr(self, "_default", undefined)
        if default is undefined:
            if is_multi:
                default = []
            else:
                default = None
        elif is_multi and isinstance(default, tuple):
            default = list(default)
        return default

    def impl_getdefault_multi(self) -> Any:
        """accessing the default value for a multi"""
        if self.impl_is_submulti():
            default_value = []
        else:
            default_value = None
        return getattr(self, "_default_multi", default_value)

    def impl_get_extra(
        self,
        key: str,
    ) -> Any:
        """if extra parameters are store get it"""
        extra = getattr(self, "_extra", {})
        if isinstance(extra, tuple):
            if key in extra[0]:
                return extra[1][extra[0].index(key)]
            return None
        return extra.get(key)

    # __________________________________________________________________________
    # validator
    def impl_validate(
        self,
        subconfig: Optional["SubConfig"],
        value: Any,
        *,
        check_error: bool = True,
        loaded: bool = False,
    ) -> bool:
        """Return True if value is really valid
        If not validate or invalid return it returns False
        """
        if (
            check_error
            and subconfig
            and not "validator" in subconfig.config_bag.properties
        ):
            return False
        if subconfig:
            force_index = subconfig.index
        else:
            force_index = None
        is_warnings_only = getattr(self, "_warnings_only", False)

        def _is_not_unique(value):
            # if set(value) has not same length than value
            if not subconfig or not check_error or "unique" not in subconfig.properties:
                return
            lvalue = [val for val in value if val is not None]
            if len(set(lvalue)) == len(lvalue):
                return
            for idx, val in enumerate(value):
                if val not in value[idx + 1 :]:
                    continue
                raise ValueError(_('the value "{}" is not unique' "").format(val))

        def calculation_validator(
            val,
            _index,
        ):
            for validator in getattr(self, "_validators", []):
                calc_is_warnings_only = (
                    hasattr(validator, "warnings_only") and validator.warnings_only
                )
                if (check_error and not calc_is_warnings_only) or (
                    not check_error and calc_is_warnings_only
                ):
                    try:
                        kwargs = {
                            "allow_value_error": True,
                            "force_value_warning": calc_is_warnings_only,
                        }
                        if _index is not None and subconfig.index == _index:
                            lsubconfig = subconfig
                        else:
                            identifier = subconfig.identifiers
                            if identifier is not None:
                                identifier = identifier[-1]
                            lsubconfig = subconfig.parent.get_child(
                                subconfig.option,
                                _index,
                                False,
                                properties=subconfig.properties,
                                identifier=identifier,
                                name=subconfig.path.rsplit(".", 1)[-1],
                                check_index=False,
                            )
                        kwargs["orig_value"] = value

                        validator.execute(
                            lsubconfig,
                            **kwargs,
                        )
                    except ValueWarning as warn:
                        warnings.warn_explicit(
                            ValueWarning(
                                subconfig,
                                val,
                                _(self.get_type()),
                                self,
                                str(warn),
                                _index,
                            ),
                            ValueWarning,
                            self.__class__.__name__,
                            319,
                        )

        def do_validation(
            _value,
            _index,
        ):
            #
            if _value is None:
                return
            if isinstance(_value, list):
                raise ValueError(_("which must not be a list"))
            if isinstance(_value, Calculation) and not subconfig:
                return
            # option validation
            if check_error:
                self.validate(_value)
                self.validate_with_option(
                    _value,
                    subconfig,
                    loaded=loaded,
                )
            # second level validation
            if (check_error and not is_warnings_only) or (
                not check_error and is_warnings_only
            ):
                try:
                    self.second_level_validation(_value, is_warnings_only)
                except ValueError as err:
                    if is_warnings_only:
                        warnings.warn_explicit(
                            ValueWarning(
                                subconfig,
                                _value,
                                _(self.get_type()),
                                self,
                                str(err),
                                _index,
                            ),
                            ValueWarning,
                            self.__class__.__name__,
                            0,
                        )
                    else:
                        raise err from err
            # ?
            if not loaded:
                calculation_validator(
                    _value,
                    _index,
                )

        val = value
        err_index = force_index
        try:
            if not self.impl_is_multi():
                do_validation(
                    val,
                    None,
                )
            elif force_index is not None:
                if self.impl_is_submulti():
                    if not isinstance(value, list):
                        raise ValueError(_("which must be a list"))
                    for val in value:
                        do_validation(
                            val,
                            force_index,
                        )
                    _is_not_unique(value)
                else:
                    do_validation(
                        val,
                        force_index,
                    )
            elif isinstance(value, Calculation) and not subconfig:
                pass
            elif self.impl_is_submulti():
                for err_index, lval in enumerate(value):
                    if isinstance(lval, Calculation):
                        continue
                    if not isinstance(lval, list):
                        raise ValueError(
                            _('which "{}" must be a list of list' "").format(lval)
                        )
                    for val in lval:
                        do_validation(val, err_index)
                    _is_not_unique(lval)
            elif not isinstance(value, list):
                raise ValueError(_("which must be a list"))
            else:
                # FIXME suboptimal, not several time for whole=True!
                for err_index, val in enumerate(value):
                    do_validation(
                        val,
                        err_index,
                    )
                _is_not_unique(value)
        except ValueError as err:
            if (
                not subconfig
                or "demoting_error_warning" not in subconfig.config_bag.properties
            ):
                raise ValueOptionError(
                    subconfig, val, _(self.get_type()), self, str(err), err_index
                ) from err
            warnings.warn_explicit(
                ValueErrorWarning(
                    subconfig, val, _(self.get_type()), self, str(err), err_index
                ),
                ValueErrorWarning,
                self.__class__.__name__,
                0,
            )
            return False
        return True

    def validate_with_option(
        self,
        value: Any,
        subconfig: "SubConfig",
        *,
        loaded: bool,
    ) -> None:
        """validation function with option"""

    def second_level_validation(
        self,
        value: Any,
        warnings_only: bool,
    ) -> None:
        """less import validation function"""

    def impl_is_leader(self):
        """check if option is a leader in a leadership"""
        leadership = self.impl_get_leadership()
        if leadership is None:
            return False
        return leadership.is_leader(self)

    def impl_is_follower(self):
        """check if option is a leader in a follower"""
        leadership = self.impl_get_leadership()
        if leadership is None:
            return False
        return not leadership.is_leader(self)

    def impl_get_leadership(self):
        """get leadership"""
        leadership = getattr(self, "_leadership", None)
        if leadership is None:
            return leadership
        # pylint: disable=not-callable
        return leadership()

    def validate(self, value: Any):
        """option needs a validate function"""
        raise NotImplementedError()
