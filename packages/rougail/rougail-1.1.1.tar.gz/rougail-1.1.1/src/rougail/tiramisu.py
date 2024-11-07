"""Redefine Tiramisu object

Created by:
EOLE (http://eole.orion.education.fr)
Copyright (C) 2005-2018

Forked by:
Cadoles (http://www.cadoles.com)
Copyright (C) 2019-2021

Silique (https://www.silique.fr)
Copyright (C) 2022-2024

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Lesser General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from typing import Any

try:
    from tiramisu5 import DynOptionDescription, calc_value
except ModuleNotFoundError:
    from tiramisu import DynOptionDescription, calc_value
from importlib.machinery import SourceFileLoader as _SourceFileLoader
from importlib.util import (
    spec_from_loader as _spec_from_loader,
    module_from_spec as _module_from_spec,
)
from jinja2 import StrictUndefined, DictLoader
from jinja2.sandbox import SandboxedEnvironment
from rougail.object_model import CONVERT_OPTION
from rougail.error import display_xmlfiles
from tiramisu import function_waiting_for_error
from tiramisu.error import ValueWarning, ConfigError, PropertiesOptionError
from .utils import normalize_family


global func
dict_env = {}
ENV = SandboxedEnvironment(loader=DictLoader(dict_env), undefined=StrictUndefined)
func = ENV.filters
ENV.compile_templates("jinja_caches", zip=None)


class JinjaError:
    __slot__ = ("_err",)

    def __init__(self, err):
        self._err = err

    def __str__(self):
        raise self._err from self._err

    def __repr__(self):
        raise self._err from self._err

    def __eq__(self, *args, **kwargs):
        raise self._err from self._err

    def __ge__(self, *args, **kwargs):
        raise self._err from self._err

    def __gt__(self, *args, **kwargs):
        raise self._err from self._err

    def __le__(self, *args, **kwargs):
        raise self._err from self._err

    def __lt__(self, *args, **kwargs):
        raise self._err from self._err

    def __ne__(self, *args, **kwargs):
        raise self._err from self._err


def test_propertyerror(value: Any) -> bool:
    return isinstance(value, JinjaError)


ENV.tests["propertyerror"] = test_propertyerror


def load_functions(path):
    global _SourceFileLoader, _spec_from_loader, _module_from_spec, func
    loader = _SourceFileLoader("func", path)
    spec = _spec_from_loader(loader.name, loader)
    func_ = _module_from_spec(spec)
    loader.exec_module(func_)
    for function in dir(func_):
        if function.startswith("_"):
            continue
        func[function] = getattr(func_, function)


def rougail_calc_value(*args, __default_value=None, **kwargs):
    values = calc_value(*args, **kwargs)
    if __default_value is not None and values in [None, []]:
        return __default_value
    return values


@function_waiting_for_error
def jinja_to_function(
    __internal_variable,
    __internal_attribute,
    __internal_jinja,
    __internal_type,
    __internal_multi,
    __internal_files,
    __default_value=None,
    **kwargs,
):
    global ENV, CONVERT_OPTION
    kw = {}
    for key, value in kwargs.items():
        if isinstance(value, PropertiesOptionError):
            value = JinjaError(value)
        if "." in key:
            c_kw = kw
            path, var = key.rsplit(".", 1)
            for subkey in path.split("."):
                c_kw = c_kw.setdefault(subkey, {})
            c_kw[var] = value
        else:
            if key in kw:
                raise ConfigError(
                    f'internal error, multi key for "{key}" in jinja_to_function'
                )
            kw[key] = value
    try:
        values = ENV.get_template(__internal_jinja).render(kw, **func).strip()
    except Exception as err:
        raise ConfigError(
            f'cannot calculating "{__internal_attribute}" attribute for variable "{__internal_variable}" in {display_xmlfiles(__internal_files)}: {err}'
        ) from err
    convert = CONVERT_OPTION[__internal_type].get("func", str)
    if __internal_multi:
        values = [convert(val) for val in values.split("\n") if val != ""]
        if not values and __default_value is not None:
            return __default_value
        return values
    try:
        values = convert(values)
    except Exception as err:
        raise ConfigError(
            f'cannot converting "{__internal_attribute}" attribute for variable "{__internal_variable}" in {display_xmlfiles(__internal_files)}: {err}'
        ) from err
    values = values if values != "" and values != "None" else None
    if values is None and __default_value is not None:
        return __default_value
    return values


def variable_to_property(prop, value, when, inverse):
    if isinstance(value, PropertiesOptionError):
        raise value from value
    if inverse:
        is_match = value != when
    else:
        is_match = value == when
    return prop if is_match else None


@function_waiting_for_error
def jinja_to_property(prop, when, inverse, **kwargs):
    value = func["jinja_to_function"](**kwargs)
    return func["variable_to_property"](prop, value is not None, when, inverse)


@function_waiting_for_error
def jinja_to_property_help(prop, **kwargs):
    value = func["jinja_to_function"](**kwargs)
    return (prop, f'"{prop}" ({value})')


@function_waiting_for_error
def valid_with_jinja(warnings_only=False, **kwargs):
    global ValueWarning
    value = func["jinja_to_function"](**kwargs)
    if value:
        if warnings_only:
            raise ValueWarning(value)
        else:
            raise ValueError(value)


func["calc_value"] = rougail_calc_value
func["jinja_to_function"] = jinja_to_function
func["jinja_to_property"] = jinja_to_property
func["jinja_to_property_help"] = jinja_to_property_help
func["variable_to_property"] = variable_to_property
func["valid_with_jinja"] = valid_with_jinja


class ConvertDynOptionDescription(DynOptionDescription):
    """Identifier could be an integer, we should convert it in str
    Identifier could also contain invalid character, so we should "normalize" it
    """

    def convert_identifier_to_path(self, identifier):
        if identifier is None:
            return identifier
        if not isinstance(identifier, str):
            identifier = str(identifier)
        return normalize_family(identifier)

    def impl_getname(
        self,
        identifier=None,
    ) -> str:
        """get name"""
        name = super().impl_getname(None)
        if identifier is None:
            return name
        path_identifier = self.convert_identifier_to_path(identifier)
        if "{{ identifier }}" in name:
            return name.replace("{{ identifier }}", path_identifier)
        return name + path_identifier

    def impl_get_display_name(
        self,
        subconfig,
        with_quote: bool = False,
    ) -> str:
        display = super().impl_get_display_name(subconfig, with_quote=with_quote)
        if "{{ identifier }}" in display:
            return display.replace(
                "{{ identifier }}",
                self.convert_identifier_to_path(self.get_identifiers(subconfig)[-1]),
            )
        return display
