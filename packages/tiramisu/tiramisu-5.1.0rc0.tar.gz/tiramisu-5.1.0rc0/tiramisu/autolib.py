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
# the rough gus of pypy: pypy: http://codespeak.net/svn/pypy/dist/pypy/config/
# the whole pypy projet is under MIT licence
# ____________________________________________________________
"enables us to carry out a calculation and return an option's value"
from typing import Any, Optional, Union, Callable, Dict, List
from itertools import chain
import weakref

from .error import PropertiesOptionError, ConfigError, LeadershipError, ValueWarning
from .i18n import _
from .setting import undefined, ConfigBag
from .function import FUNCTION_WAITING_FOR_DICT, FUNCTION_WAITING_FOR_ERROR

# ____________________________________________________________


def get_calculated_value(
    subconfig: "SubConfig",
    value: Any,
    *,
    reset_cache: bool = True,
    validate_properties: bool = True,
) -> Any:
    """value could be a calculation, in this case do calculation"""
    has_calculation = False
    if isinstance(value, Calculation):
        if subconfig is None:
            return undefined, False
        value = value.execute(
            subconfig,
            validate_properties=validate_properties,
        )
        has_calculation = True
    elif isinstance(value, list):
        # if value is a list, do subcalculation
        for idx, val in enumerate(value):
            value[idx], _has_calculation = get_calculated_value(
                subconfig,
                val,
                reset_cache=False,
                validate_properties=validate_properties,
            )
            if value[idx] is undefined:
                return undefined, False
            if _has_calculation:
                has_calculation = True
    return value, has_calculation


class Params:
    __slots__ = ("args", "kwargs")

    def __init__(self, args=None, kwargs=None, **kwgs):
        if args is None:
            args = tuple()
        if kwargs is None:
            kwargs = {}
        if kwgs:
            kwargs.update(kwgs)
        if isinstance(args, Param):
            args = (args,)
        else:
            if not isinstance(args, tuple):
                raise ValueError(_("args in params must be a tuple"))
            for arg in args:
                if not isinstance(arg, Param):
                    raise ValueError(_("arg in params must be a Param"))
        if not isinstance(kwargs, dict):
            raise ValueError(_("kwargs in params must be a dict"))
        for arg in kwargs.values():
            if not isinstance(arg, Param):
                raise ValueError(_("arg in params must be a Param"))
        self.args = args
        self.kwargs = kwargs


class Param:
    __slots__ = tuple()
    pass


class ParamOption(Param):
    __slots__ = (
        "option",
        "notraisepropertyerror",
        "raisepropertyerror",
    )

    def __init__(
        self,
        option: "Option",
        notraisepropertyerror: bool = False,
        raisepropertyerror: bool = False,
    ) -> None:
        if __debug__ and not hasattr(option, "impl_is_symlinkoption"):
            raise ValueError(
                _("paramoption needs an option not {}").format(type(option))
            )
        if option.impl_is_symlinkoption():
            cur_opt = option.impl_getopt()
        else:
            cur_opt = option
        assert isinstance(notraisepropertyerror, bool), _(
            "param must have a boolean not a {} for notraisepropertyerror"
        ).format(type(notraisepropertyerror))
        assert isinstance(raisepropertyerror, bool), _(
            "param must have a boolean not a {} for raisepropertyerror"
        ).format(type(raisepropertyerror))
        self.option = cur_opt
        self.notraisepropertyerror = notraisepropertyerror
        self.raisepropertyerror = raisepropertyerror


class ParamDynOption(ParamOption):
    __slots__ = (
        "identifiers",
        "optional",
    )

    def __init__(
        self,
        option: "Option",
        identifiers: list[str],
        notraisepropertyerror: bool = False,
        raisepropertyerror: bool = False,
        optional: bool = False,
    ) -> None:
        super().__init__(
            option,
            notraisepropertyerror,
            raisepropertyerror,
        )
        if not isinstance(identifiers, list):
            raise Exception(
                f"identifiers in ParamDynOption must be a list, not {identifiers}"
            )
        if not isinstance(optional, bool):
            raise Exception(
                f"optional in ParamDynOption must be a boolean, not {optional}"
            )
        self.identifiers = identifiers
        self.optional = optional


class ParamSelfOption(Param):
    __slots__ = "whole"

    def __init__(
        self,
        whole: bool = undefined,
    ) -> None:
        """whole: send all value for a multi, not only indexed value"""
        if whole is not undefined:
            self.whole = whole


class ParamValue(Param):
    __slots__ = ("value",)

    def __init__(self, value):
        self.value = value


class ParamInformation(Param):
    __slots__ = (
        "information_name",
        "default_value",
        "option",
        "self_option",
    )

    def __init__(
        self,
        information_name: str,
        default_value: Any = undefined,
        option: "Option" = None,
    ) -> None:
        self.information_name = information_name
        self.default_value = default_value
        self.self_option = None
        self.option = None
        if option:
            self.set_option(option)

    def set_self_option(self, option):
        self.self_option = option

    def set_option(self, option: "Option" = None) -> None:
        if not hasattr(self, "self_option"):
            raise ConfigError("cannot add option in information after creating config")
        if self.option:
            raise ConfigError("cannot redefine option in information")
        if not option.impl_is_optiondescription():
            if option.impl_is_symlinkoption():
                raise ValueError(
                    _("option in ParamInformation cannot be a symlinkoption")
                )
            if option.impl_is_follower():
                raise ValueError(_("option in ParamInformation cannot be a follower"))
            if option.impl_is_dynsymlinkoption():
                raise ValueError(
                    _("option in ParamInformation cannot be a dynamic option")
                )
        self.option = option
        if self.self_option:
            informations = self.self_option._dependencies_information
            if set(informations) == {None, self.information_name}:
                del self.self_option._dependencies_information
            else:
                informations.remove(None)
            if not getattr(option, "_dependencies_information", {}):
                option._dependencies_information = {None: []}
            option._dependencies_information[None].append(self)
            option._dependencies_information.setdefault(
                self.information_name, []
            ).append(weakref.ref(self.self_option))


class ParamSelfInformation(ParamInformation):
    __slots__ = tuple()

    def __init__(
        self,
        information_name: str,
        default_value: Any = undefined,
    ) -> None:
        return super().__init__(
            information_name,
            default_value,
        )


class ParamIndex(Param):
    __slots__ = tuple()


class ParamIdentifier(Param):
    __slots__ = ("identifier_index",)

    def __init__(
        self,
        identifier_index: int = -1,
    ) -> None:
        self.identifier_index = identifier_index


class Calculation:
    __slots__ = (
        "function",
        "params",
        "help_function",
        "_has_index",
        "warnings_only",
    )

    def __init__(
        self,
        function: Callable,
        params: Params = Params(),
        help_function: Optional[Callable] = None,
        warnings_only: bool = False,
    ):
        assert isinstance(function, Callable), _(
            "first argument ({0}) must be a function"
        ).format(function)
        if help_function:
            assert isinstance(help_function, Callable), _(
                "help_function ({0}) must be a function"
            ).format(help_function)
            self.help_function = help_function
        else:
            self.help_function = None
        self.function = function
        self.params = params
        for arg in chain(self.params.args, self.params.kwargs.values()):
            if isinstance(arg, ParamIndex):
                self._has_index = True
                break
        if warnings_only is True:
            self.warnings_only = warnings_only

    def execute(
        self,
        subconfig: "SubConfig",
        *,
        orig_value: Any = undefined,
        allow_value_error: bool = False,
        force_value_warning: bool = False,
        for_settings: bool = False,
        validate_properties: bool = True,
    ) -> Any:
        return carry_out_calculation(
            subconfig,
            callback=self.function,
            callback_params=self.params,
            index=subconfig.index,
            config_bag=subconfig.config_bag,
            orig_value=orig_value,
            allow_value_error=allow_value_error,
            force_value_warning=force_value_warning,
            for_settings=for_settings,
            validate_properties=validate_properties,
        )

    def help(
        self,
        subconfig: "SubConfig",
        for_settings: bool = False,
    ) -> str:
        if not self.help_function:
            return self.execute(
                subconfig,
                for_settings=for_settings,
            )
        return carry_out_calculation(
            subconfig,
            callback=self.help_function,
            callback_params=self.params,
            index=subconfig.index,
            config_bag=subconfig.config_bag,
            for_settings=for_settings,
        )

    def __deepcopy__(x, memo):
        return x


def manager_callback(
    callback: Callable,
    param: Param,
    subconfig: "SubConfig",
    index: Optional[int],
    orig_value,
    config_bag: ConfigBag,
    for_settings: bool,
    validate_properties: bool,
) -> Any:
    """replace Param by true value"""
    option = subconfig.option

    def calc_apply_index(
        param,
        same_leadership,
    ):
        return index is not None and not getattr(param, "whole", not same_leadership)

    def calc_self(
        param,
        index,
        value,
        config_bag,
    ):
        # index must be apply only if follower
        is_follower = subconfig.option.impl_is_follower()
        # FIXME "same_leadership" or "is_follower"?
        apply_index = calc_apply_index(
            param,
            is_follower,
        )
        if value is undefined or (apply_index is False and is_follower):
            path = subconfig.path
            properties = config_bag.context.get_settings().getproperties(
                subconfig,
                uncalculated=True,
            )
            new_value = get_value(
                config_bag,
                subconfig,
                param,
                True,
                apply_index=apply_index,
                properties=properties,
            )
            if apply_index is False and is_follower:
                new_value[index] = value
            value = new_value
        elif apply_index is not False and not is_follower:
            value = value[index]
        return value

    def get_value(
        config_bag,
        subconfig,
        param,
        self_calc,
        *,
        apply_index=True,
        properties=undefined,
    ):
        option = subconfig.option
        if option.impl_is_follower() and (
            subconfig.index is None or apply_index is False
        ):
            value = []
            for idx in range(subconfig.parent.get_length_leadership()):
                subconfig = get_option_bag(
                    config_bag,
                    option,
                    param,
                    idx,
                    self_calc,
                    properties=properties,
                )
                value.append(
                    _get_value(
                        param,
                        subconfig,
                    )
                )
        else:
            value = _get_value(
                param,
                subconfig,
            )
        return value

    def _get_value(
        param: Params,
        subconfig: "SubConfig",
    ) -> Any:
        try:
            # get value
            value = config_bag.context.get_value(subconfig)
        except PropertiesOptionError as err:
            # raise PropertiesOptionError (which is catched) because must not add value None in carry_out_calculation
            if (
                isinstance(param, ParamSelfOption)
                or param.notraisepropertyerror
                or param.raisepropertyerror
            ):
                raise err from err
            display_name = subconfig.option.impl_get_display_name(
                subconfig, with_quote=True
            )
            raise ConfigError(
                _("unable to carry out a calculation for {}, {}").format(
                    display_name, err
                )
            ) from err
        except ValueError as err:
            display_name = subconfig.option.impl_get_display_name(
                subconfig, with_quote=True
            )
            raise ValueError(
                _(
                    "the option {0} is used in a calculation but is invalid ({1})"
                ).format(display_name, err)
            ) from err
        except AttributeError as err:
            if isinstance(param, ParamDynOption) and param.optional:
                # cannot acces, simulate a propertyerror
                raise PropertiesOptionError(
                    subconfig,
                    ["configerror"],
                    config_bag.context.get_settings(),
                )
            display_name = subconfig.option.impl_get_display_name(
                subconfig, with_quote=True
            )
            raise ConfigError(
                _("unable to get value for calculating {0}, {1}").format(
                    display_name, err
                )
            ) from err
        return value

    def get_option_bag(
        config_bag,
        opt,
        param,
        index_,
        self_calc,
        *,
        properties=undefined,
    ):
        # don't validate if option is option that we tried to validate
        if for_settings:
            config_bag.properties = config_bag.properties - {"warnings"}
        if not for_settings:
            config_bag.properties -= {"warnings"}
        if self_calc:
            config_bag.unrestraint()
            config_bag.remove_validation()
        try:
            subsubconfig = config_bag.context.get_sub_config(
                config_bag,
                opt.impl_getpath(),
                index_,
                validate_properties=not self_calc,
                properties=properties,
            )
        except PropertiesOptionError as err:
            # raise PropertiesOptionError (which is catched) because must not add value None in carry_out_calculation
            if param.notraisepropertyerror or param.raisepropertyerror:
                raise err from err
            display_name = option.impl_get_display_name(subconfig, with_quote=True)
            raise ConfigError(
                _("unable to carry out a calculation for {}, {}").format(
                    display_name, err
                )
            ) from err
        except ValueError as err:
            display_name = option.impl_get_display_name(subconfig, with_quote=True)
            raise ValueError(
                _(
                    "the option {0} is used in a calculation but is invalid ({1})"
                ).format(display_name, err)
            ) from err
        except AttributeError as err:
            if isinstance(param, ParamDynOption) and param.optional:
                # cannot acces, simulate a propertyerror
                raise PropertiesOptionError(
                    param,
                    ["configerror"],
                    config_bag.context.get_settings(),
                )
            display_name = option.impl_get_display_name(subconfig, with_quote=True)
            raise ConfigError(
                _("unable to get value for calculating {0}, {1}").format(
                    display_name, err
                )
            ) from err
        return subsubconfig

    if isinstance(param, ParamValue):
        return param.value

    if isinstance(param, ParamInformation):
        if isinstance(param, ParamSelfInformation):
            isubconfig = subconfig
        elif param.option:
            if param.option.issubdyn():
                search_option = param.option
                isubconfig = subconfig.get_common_child(
                    search_option,
                    true_path=subconfig.path,
                )
                if isinstance(isubconfig, list):
                    display_name = option.impl_get_display_name(
                        subconfig, with_quote=True
                    )
                    search_name = search_option.impl_get_display_name(
                        None, with_quote=True
                    )
                    raise ConfigError(
                        f"cannot find information for {display_name}, {search_name} is a dynamic option"
                    )
            else:
                isubconfig = get_option_bag(
                    config_bag,
                    param.option,
                    param,
                    None,
                    False,
                    # properties=properties,
                )
        else:
            isubconfig = config_bag.context.get_root(config_bag)
        try:
            return config_bag.context.get_values().get_information(
                isubconfig,
                param.information_name,
                param.default_value,
            )
        except ValueError as err:
            display_name = option.impl_get_display_name(subconfig, with_quote=True)
            raise ConfigError(
                _("unable to get value for calculating {0}, {1}").format(
                    display_name, err
                )
            ) from err

    if isinstance(param, ParamIndex):
        return index

    if isinstance(param, ParamIdentifier):
        if not option.issubdyn() and (
            not option.impl_is_optiondescription()
            or not option.impl_is_dynoptiondescription()
        ):
            display_name = subconfig.option.impl_get_display_name(
                subconfig, with_quote=True
            )
            raise ConfigError(
                _(
                    "option {0} is not a dynoptiondescription or in a dynoptiondescription"
                ).format(display_name)
            )
        return subconfig.identifiers[param.identifier_index]

    if isinstance(param, ParamSelfOption):
        value = calc_self(
            param,
            index,
            orig_value,
            config_bag,
        )
        if callback.__name__ not in FUNCTION_WAITING_FOR_DICT:
            return value
        return {
            "name": option.impl_get_display_name(subconfig),
            "value": value,
        }

    if isinstance(param, ParamOption):
        callbk_option = param.option
        if (
            index is not None
            and callbk_option.impl_get_leadership()
            and callbk_option.impl_get_leadership().in_same_leadership(option)
        ):
            if not callbk_option.impl_is_follower():
                # leader
                index_ = None
                with_index = True
            else:
                # follower
                index_ = index
                with_index = False
        else:
            index_ = None
            with_index = False
        if callbk_option.issubdyn():
            if isinstance(param, ParamDynOption):
                identifiers = param.identifiers.copy()
                paths = callbk_option.impl_getpath().split(".")
                parents = [config_bag.context.get_root(config_bag)]
                subconfigs_is_a_list = False
                for name in paths:
                    new_parents = []
                    for parent in parents:
                        doption = parent.option.get_child(
                            name,
                            config_bag,
                            parent,
                            allow_dynoption=True,
                        )
                        if doption.impl_is_dynoptiondescription():
                            if not identifiers:
                                identifier = None
                            else:
                                identifier = identifiers.pop(0)
                            if not identifier:
                                subconfigs_is_a_list = True
                                new_parents.extend(
                                    parent.dyn_to_subconfig(
                                        doption,
                                        True,
                                    )
                                )
                            else:
                                name = doption.impl_getname(identifier)
                                try:
                                    doption = parent.option.get_child(
                                        name,
                                        config_bag,
                                        parent,
                                    )
                                except AttributeError as err:
                                    raise ConfigError(err) from err
                                new_parents.append(
                                    parent.get_child(
                                        doption,
                                        None,
                                        True,
                                        name=name,
                                        identifier=identifier,
                                    )
                                )
                        else:
                            new_parents.append(
                                parent.get_child(
                                    doption,
                                    None,
                                    True,
                                    name=name,
                                )
                            )
                    parents = new_parents

                if subconfigs_is_a_list:
                    subconfigs = parents
                else:
                    subconfigs = parents[0]

            else:
                search_option = param.option
                subconfigs = subconfig.get_common_child(
                    search_option,
                    true_path=subconfig.path,
                    validate_properties=validate_properties,
                )
            if isinstance(subconfigs, list):
                values = []
            else:
                values = None
                subconfigs = [subconfigs]
        else:
            subconfigs = [
                get_option_bag(
                    config_bag,
                    callbk_option,
                    param,
                    index_,
                    False,
                    # properties=properties,
                )
            ]
            values = None
        for subconfig in subconfigs:
            callbk_option = subconfig.option
            value = get_value(
                config_bag,
                subconfig,
                param,
                False,
            )
            if with_index:
                value = value[index]
            if values is not None:
                values.append(value)
        if values is not None:
            value = values
        if callback.__name__ not in FUNCTION_WAITING_FOR_DICT:
            return value
        return {"name": callbk_option.impl_get_display_name(subconfig), "value": value}


def carry_out_calculation(
    subconfig: "SubConfig",
    callback: Callable,
    callback_params: Optional[Params],
    index: Optional[int],
    config_bag: Optional[ConfigBag],
    orig_value=undefined,
    allow_value_error: bool = False,
    force_value_warning: bool = False,
    for_settings: bool = False,
    *,
    validate_properties: bool = True,
):
    """a function that carries out a calculation for an option's value

    :param option: the option
    :param callback: the name of the callback function
    :param callback_params: the callback's parameters
                            (only keyword parameters are allowed)
    :param index: if an option is multi, only calculates the nth value
    :param allow_value_error: to know if carry_out_calculation can return ValueError or ValueWarning (for example if it's a validation)
    :param force_value_warning: transform valueError to ValueWarning object

    The callback_params is a dict. Key is used to build args (if key is '')
    and kwargs (otherwise). Values are tuple of:
    - values
    - tuple with option and boolean's force_permissive (True when don't raise
    if PropertiesOptionError)
    Values could have multiple values only when key is ''."""
    option = subconfig.option
    if (
        not option.impl_is_optiondescription()
        and option.impl_is_follower()
        and index is None
    ):
        raise ConfigError(
            f"the follower {option.impl_get_display_name(subconfig, with_quote=True)} must have index in carry_out_calculation!"
        )

    def fake_items(iterator):
        return ((None, i) for i in iterator)

    args = []
    kwargs = {}
    config_bag = config_bag.copy()
    config_bag.set_permissive()
    if callback_params:
        for key, param in chain(
            fake_items(callback_params.args), callback_params.kwargs.items()
        ):
            try:
                value = manager_callback(
                    callback,
                    param,
                    subconfig,
                    index,
                    orig_value,
                    config_bag,
                    for_settings,
                    validate_properties,
                )
                if key is None:
                    args.append(value)
                else:
                    kwargs[key] = value
            except PropertiesOptionError as err:
                if isinstance(param, ParamSelfOption) or param.raisepropertyerror:
                    raise err
                if callback.__name__ in FUNCTION_WAITING_FOR_DICT:
                    if key is None:
                        args.append(
                            {
                                "propertyerror": str(err),
                                "name": option.impl_get_display_name(subconfig),
                            }
                        )
                    else:
                        kwargs[key] = {
                            "propertyerror": str(err),
                            "name": option.impl_get_display_name(subconfig),
                        }
                if callback.__name__ in FUNCTION_WAITING_FOR_ERROR:
                    if key is None:
                        args.append(err)
                    else:
                        kwargs[key] = err
    ret = calculate(
        subconfig,
        callback,
        allow_value_error,
        force_value_warning,
        args,
        kwargs,
    )
    if (
        isinstance(ret, list)
        and not option.impl_is_dynoptiondescription()
        and not option.impl_is_optiondescription()
        and option.impl_is_follower()
        and not option.impl_is_submulti()
    ):
        if args or kwargs:
            raise LeadershipError(
                _(
                    'the "{}" function with positional arguments "{}" '
                    'and keyword arguments "{}" must not return '
                    'a list ("{}") for the follower option {}'
                    ""
                ).format(
                    callback.__name__,
                    args,
                    kwargs,
                    ret,
                    option.impl_get_display_name(subconfig, with_quote=True),
                )
            )
        else:
            raise LeadershipError(
                _(
                    'the "{}" function must not return a list ("{}") '
                    "for the follower option {}"
                    ""
                ).format(
                    callback.__name__,
                    ret,
                    option.impl_get_display_name(subconfig, with_quote=True),
                )
            )
    return ret


def calculate(
    subconfig,
    callback: Callable,
    allow_value_error: bool,
    force_value_warning: bool,
    args,
    kwargs,
):
    """wrapper that launches the 'callback'

    :param callback: callback function
    :param args: in the callback's arity, the unnamed parameters
    :param kwargs: in the callback's arity, the named parameters

    """
    try:
        return callback(*args, **kwargs)
    except (ValueError, ValueWarning) as err:
        if allow_value_error:
            if force_value_warning:
                raise ValueWarning(str(err))
            raise err from err
        error = err
    except ConfigError as err:
        raise err from err
    except Exception as err:
        error = err
    if args or kwargs:
        msg = _(
            'unexpected error "{0}" in function "{1}" with arguments "{3}" and "{4}" '
            "for option {2}"
        ).format(
            str(error),
            callback.__name__,
            subconfig.option.impl_get_display_name(subconfig, with_quote=True),
            args,
            kwargs,
        )
    else:
        msg = _('unexpected error "{0}" in function "{1}" for option {2}' "").format(
            str(error),
            callback.__name__,
            subconfig.option.impl_get_display_name(subconfig, with_quote=True),
        )
    raise ConfigError(msg) from error
