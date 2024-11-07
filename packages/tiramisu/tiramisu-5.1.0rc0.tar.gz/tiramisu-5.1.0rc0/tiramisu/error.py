# -*- coding: utf-8 -*-
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
# ____________________________________________________________
"user defined exceptions"
import weakref
from .i18n import _


def display_list(
    lst,
    *,
    separator="and",
    add_quote=False,
) -> str():
    if not lst:
        return '""'
    if separator == "and":
        separator = _("and")
    elif separator == "or":
        separator = _("or")
    if isinstance(lst, tuple) or isinstance(lst, frozenset):
        lst = list(lst)
    if len(lst) == 1:
        ret = lst[0]
        if not isinstance(ret, str):
            ret = str(ret)
        if add_quote and not ret.startswith('"'):
            ret = '"{}"'.format(ret)
        return ret
    lst_ = []
    for l in lst:
        if not isinstance(l, str):
            l = str(l)
        lst_.append(_(l))
    lst__ = []
    for l in lst_:
        if add_quote and not l.startswith('"'):
            l = '"{}"'.format(l)
        lst__.append(l)
    lst__.sort()
    last = lst__[-1]
    return ", ".join(lst__[:-1]) + _(" {} ").format(separator) + "{}".format(last)


# Exceptions for an Option
class PropertiesOptionError(AttributeError):
    "attempt to access to an option with a property that is not allowed"

    def __init__(
        self,
        subconfig,
        proptype,
        settings,
        opt_type=None,
        name=None,
        orig_opt=None,
        help_properties=None,
    ):
        if opt_type:
            self._opt_type = opt_type
            self._name = name
            self._orig_opt = orig_opt
        else:
            if subconfig.option.impl_is_optiondescription():
                self._opt_type = "optiondescription"
            else:
                self._opt_type = "option"
            self._name = subconfig.option.impl_get_display_name(
                subconfig, with_quote=True
            )
            self._orig_opt = None
        self._subconfig = subconfig
        self.proptype = proptype
        self.help_properties = help_properties
        self._settings = settings
        self.msg = None
        super().__init__(None)

    def set_orig_opt(self, opt):
        self._orig_opt = opt

    def __str__(self):
        # this part is a bit slow, so only execute when display
        if self.msg is not None:
            return self.msg
        if self._settings is None:
            return "error"
        if self.help_properties:
            properties = list(self.help_properties)
        else:
            properties = list(self.proptype)
        only_one = len(properties) == 1
        properties_msg = display_list(properties, add_quote=True)
        if only_one:
            prop_msg = _("property")
        else:
            prop_msg = _("properties")
        if properties == ["frozen"]:
            if self._orig_opt:
                msg = _('cannot modify the {0} {1} because "{2}" has {3} {4}')
            else:
                msg = _("cannot modify the {0} {1} because has {2} {3}")
        else:
            if self._orig_opt:
                msg = _('cannot access to {0} {1} because "{2}" has {3} {4}')
            else:
                msg = _("cannot access to {0} {1} because has {2} {3}")
        if self._orig_opt:
            # FIXME _orig_opt ?
            self.msg = msg.format(
                self._opt_type,
                self._orig_opt.impl_get_display_name(subconfig, with_quote=True),
                self._name,
                prop_msg,
                properties_msg,
            )
        else:
            self.msg = msg.format(self._opt_type, self._name, prop_msg, properties_msg)
        del self._opt_type, self._name
        del self._settings, self._orig_opt
        return self.msg


# ____________________________________________________________
# Exceptions for a Config
class ConfigError(Exception):
    """attempt to change an option's owner without a value
    or in case of `_descr` is None
    or if a calculation cannot be carried out"""

    def __init__(
        self,
        exp,
        ori_err=None,
    ):
        super().__init__(exp)
        self.ori_err = ori_err


class ConflictError(Exception):
    "duplicate options are present in a single config"
    pass


# ____________________________________________________________
# miscellaneous exceptions
class LeadershipError(Exception):
    "problem with a leadership's value length"
    pass


class ConstError(TypeError):
    "no uniq value in _NameSpace"
    pass


class _CommonError:
    def __init__(self, subconfig, val, display_type, opt, err_msg, index):
        self.val = val
        self.display_type = display_type
        self.opt = weakref.ref(opt)
        self.name = opt.impl_get_display_name(subconfig)
        self.err_msg = err_msg
        self.index = index
        super().__init__(self.err_msg)

    def __str__(self):
        try:
            msg = self.prefix
        except AttributeError:
            self.prefix = self.tmpl.format(self.val, _(self.display_type), self.name)
            msg = self.prefix
        if self.err_msg:
            if msg:
                msg += ", {}".format(self.err_msg)
            else:
                msg = self.err_msg
        if not msg:
            msg = _("invalid value")
        return msg


class ValueWarning(_CommonError, UserWarning):
    tmpl = None

    def __init__(self, *args, **kwargs):
        if ValueWarning.tmpl is None:
            ValueWarning.tmpl = _('attention, "{0}" could be an invalid {1} for "{2}"')
        if len(args) == 1 and not kwargs:
            self.msg = args[0]
        else:
            super().__init__(*args, **kwargs)
            self.msg = None

    def __str__(self):
        if self.msg is None:
            return super().__str__()
        return self.msg


class ValueOptionError(_CommonError, ValueError):
    tmpl = None

    def __init__(self, *args, **kwargs):
        if ValueOptionError.tmpl is None:
            ValueOptionError.tmpl = _('"{0}" is an invalid {1} for "{2}"')
        super().__init__(*args, **kwargs)


class ValueErrorWarning(ValueWarning):
    tmpl = None

    def __init__(self, *args, **kwargs):
        if ValueErrorWarning.tmpl is None:
            ValueErrorWarning.tmpl = _('"{0}" is an invalid {1} for "{2}"')
        super().__init__(*args, **kwargs)
