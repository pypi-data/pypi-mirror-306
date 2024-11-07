"""Rougail method

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

from tiramisu import Config, undefined
from tiramisu.error import PropertiesOptionError, LeadershipError, ConfigError
from warnings import warn
from typing import List
from re import compile, findall

from .convert import RougailConvert
from .config import RougailConfig
from .update import RougailUpgrade
from .object_model import CONVERT_OPTION
from .utils import normalize_family


def tiramisu_display_name(
    kls,
    subconfig,
    with_quote: bool = False,
) -> str:
    """Replace the Tiramisu display_name function to display path + description"""
    doc = kls._get_information(subconfig, "doc", None)
    comment = f" ({doc})" if doc and doc != kls.impl_getname() else ""
    if "{{ identifier }}" in comment:
        comment = comment.replace("{{ identifier }}", str(subconfig.identifiers[-1]))
    path = kls.impl_getpath()
    if "{{ identifier }}" in path and subconfig.identifiers:
        path = path.replace(
            "{{ identifier }}", normalize_family(str(subconfig.identifiers[-1]))
        )
    if with_quote:
        return f'"{path}"{comment}'
    return f"{path}{comment}"


class Rougail:
    """Main Rougail object"""

    def __init__(
        self,
        rougailconfig=None,
    ) -> None:
        if rougailconfig is None:
            rougailconfig = RougailConfig
        self.rougailconfig = rougailconfig
        self.converted = RougailConvert(self.rougailconfig)
        self.config = None

    def add_path_prefix(
        self,
        path_prefix: str,
    ) -> None:
        """Add a prefix"""
        self.converted.load_config()
        self.converted.parse_directories(path_prefix)

    def run(self):
        """Get Tiramisu Config"""
        if not self.config:
            tiram_obj = self.converted.save(self.rougailconfig["tiramisu_cache"])
            optiondescription = {}
            custom_types = {
                custom.__name__: custom
                for custom in self.rougailconfig["custom_types"].values()
            }
            exec(tiram_obj, custom_types, optiondescription)  # pylint: disable=W0122
            self.config = Config(
                optiondescription["option_0"],
                display_name=tiramisu_display_name,
            )
            self.config.property.read_write()
        return self.config

    def get_config(self):
        warn(
            "get_config is deprecated, use run instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.run()

    def user_datas(self, user_datas: List[dict]):
        values = {}
        errors = []
        warnings = []
        for datas in user_datas:
            options = datas.get("options", {})
            for name, data in datas.get("values", {}).items():
                values[name] = {
                    "values": data,
                    "options": options.copy(),
                }
            errors.extend(datas.get("errors", []))
            warnings.extend(datas.get("warnings", []))
        self._auto_configure_dynamics(values)
        while values:
            value_is_set = False
            for option in self._get_variable(self.config):
                path = option.path()
                if path not in values:
                    path = path.upper()
                    options = values.get(path, {}).get("options", {})
                    if path not in values or options.get("upper") is not True:
                        continue
                else:
                    options = values[path].get("options", {})
                value = values[path]["values"]
                if option.ismulti():
                    if options.get("multi_separator") and not isinstance(value, list):
                        value = value.split(options["multi_separator"])
                        values[path]["values"] = value
                    if options.get("needs_convert"):
                        value = [convert_value(option, val) for val in value]
                        values[path]["values"] = value
                        values[path]["options"]["needs_convert"] = False
                elif options.get("needs_convert"):
                    value = convert_value(option, value)
                index = option.index()
                if index is not None:
                    if not isinstance(value, list) or index >= len(value):
                        continue
                    value = value[index]
                try:
                    option.value.set(value)
                    value_is_set = True
                    if index is not None:
                        values[path]["values"][index] = undefined
                        if set(values[path]["values"]) == {undefined}:
                            values.pop(path)
                    else:
                        values.pop(path)
                except Exception as err:
                    if path != option.path():
                        values[option.path()] = values.pop(path)
            if not value_is_set:
                break
        for path, data in values.items():
            try:
                option = self.config.option(path)
                value = data["values"]
                if option.isfollower():
                    for index, val in enumerate(value):
                        if val is undefined:
                            continue
                        self.config.option(path, index).value.set(val)
                else:
                    option.value.set(value)
            except AttributeError as err:
                errors.append(str(err))
            except (ValueError, LeadershipError) as err:
                # errors.append(str(err).replace('"', "'"))
                errors.append(str(err))
            except PropertiesOptionError as err:
                #                warnings.append(f'"{err}" but is defined in "{self.filename}"')
                warnings.append(str(err))
        return {
            "errors": errors,
            "warnings": warnings,
        }

    def _get_variable(self, config):
        for subconfig in config:
            if subconfig.isoptiondescription():
                yield from self._get_variable(subconfig)
            else:
                yield subconfig

    def _auto_configure_dynamics(
        self,
        values,
    ):
        cache = {}
        added = []
        for path, data in list(values.items()):
            value = data["values"]
            #            for value in data['values'].items():
            try:
                option = self.config.option(path)
                option.name()
            except (ConfigError, PropertiesOptionError):
                pass
            except AttributeError:
                config = self.config
                current_path = ""
                identifiers = []
                for name in path.split(".")[:-1]:
                    if current_path:
                        current_path += "."
                    current_path += name
                    if current_path in cache:
                        config, identifier = cache[current_path]
                        identifiers.append(identifier)
                    else:
                        tconfig = config.option(name)
                        try:
                            tconfig.group_type()
                            config = tconfig
                        except AttributeError:
                            for tconfig in config.list(uncalculated=True):
                                if tconfig.isdynamic(only_self=True):
                                    identifier = self._get_identifier(
                                        tconfig.name(), name
                                    )
                                    if identifier is None:
                                        continue
                                    dynamic_variable = tconfig.information.get(
                                        "dynamic_variable",
                                        None,
                                    )
                                    if not dynamic_variable:
                                        continue
                                    option_type = self.config.option(
                                        dynamic_variable
                                    ).information.get("type")
                                    if identifiers:
                                        for s in identifiers:
                                            dynamic_variable = dynamic_variable.replace(
                                                "{{ identifier }}", str(s), 1
                                            )
                                    if dynamic_variable not in values:
                                        values[dynamic_variable] = {"values": []}
                                        added.append(dynamic_variable)
                                    elif dynamic_variable not in added:
                                        continue
                                    config = tconfig
                                    #                                        option_type = option.information.get('type')
                                    typ = CONVERT_OPTION.get(option_type, {}).get(
                                        "func"
                                    )
                                    if typ:
                                        identifier = typ(identifier)
                                    if (
                                        identifier
                                        not in values[dynamic_variable]["values"]
                                    ):
                                        values[dynamic_variable]["values"].append(
                                            identifier
                                        )
                                    identifiers.append(identifier)
                                    cache[current_path] = config, identifier
                                    break
            else:
                if option.isdynamic():
                    parent_option = self.config.option(path.rsplit(".", 1)[0])
                    identifiers = self._get_identifier(
                        parent_option.name(uncalculated=True),
                        parent_option.name(),
                    )
                    dynamic_variable = None
                    while True:
                        dynamic_variable = parent_option.information.get(
                            "dynamic_variable",
                            None,
                        )
                        if dynamic_variable:
                            break
                        parent_option = self.config.option(
                            parent_option.path().rsplit(".", 1)[0]
                        )
                        if "." not in parent_option.path():
                            parent_option = None
                            break
                    if not parent_option:
                        continue
                    identifiers = parent_option.identifiers()
                    for identifier in identifiers:
                        dynamic_variable = dynamic_variable.replace(
                            "{{ identifier }}", str(identifier), 1
                        )
                    if dynamic_variable not in values:
                        values[dynamic_variable] = {"values": []}
                        added.append(dynamic_variable)
                    elif dynamic_variable not in added:
                        continue
                    option_type = option.information.get("type")
                    typ = CONVERT_OPTION.get(option_type, {}).get("func")
                    if typ:
                        identifier = typ(identifier)
                    if identifier not in values[dynamic_variable]["values"]:
                        values[dynamic_variable]["values"].append(identifier)
                    cache[option.path()] = option, identifier

    def _get_identifier(self, true_name, name) -> str:
        regexp = true_name.replace("{{ identifier }}", "(.*)")
        finded = findall(regexp, name)
        if len(finded) != 1 or not finded[0]:
            return
        return finded[0]


def convert_value(option, value):
    if value == "":
        return None
    option_type = option.information.get("type")
    func = CONVERT_OPTION.get(option_type, {}).get("func")
    if func:
        return func(value)
    return value


__all__ = ("Rougail", "RougailConfig", "RougailUpgrade")
