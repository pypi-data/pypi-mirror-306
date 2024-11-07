"""Takes a bunch of Rougail YAML dispatched in differents folders
as an input and outputs a Tiramisu's file.

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

import logging
from itertools import chain
from pathlib import Path
from re import compile, findall
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Literal,
    Optional,
    Tuple,
    Union,
    get_type_hints,
)

from pydantic import ValidationError
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap
from pydantic import ValidationError

from warnings import warn

from tiramisu.error import display_list

from .annotator import SpaceAnnotator
from .i18n import _
from .object_model import CONVERT_OPTION  # Choice,
from .object_model import (
    PROPERTY_ATTRIBUTE,
    CALCULATION_TYPES,
    CALCULATION_PROPERTY_TYPES,
    PARAM_TYPES,
    AnyParam,
    Calculation,
    Dynamic,
    Family,
    SymLink,
    Variable,
    VariableCalculation,
)
from .tiramisureflector import TiramisuReflector
from .utils import get_realpath, normalize_family, load_modules
from .error import DictConsistencyError

property_types = Union[Literal[True], Calculation]
properties_types = Dict[str, property_types]


class Property:
    def __init__(self) -> None:
        self._properties: Dict[str, properties_types] = {}

    def add(
        self,
        path: str,
        property_: str,
        value: property_types,
    ) -> None:
        self._properties.setdefault(path, {})[property_] = value

    def __getitem__(
        self,
        path: str,
    ) -> properties_types:
        return self._properties.get(path, {})

    def __contains__(
        self,
        path: str,
    ) -> bool:
        return path in self._properties


class Paths:
    regexp_relative = compile(r"^_*\.(.*)$")

    def __init__(
        self,
        default_namespace: str,
    ) -> None:
        self._data: Dict[str, Union[Variable, Family]] = {}
        self._dynamics: Dict[str:str] = {}
        if default_namespace is not None:
            default_namespace = normalize_family(default_namespace)
        self.default_namespace = default_namespace
        self.path_prefix = None

    def has_value(self) -> bool:
        return self._data != {}

    def add(
        self,
        path: str,
        data: Any,
        is_dynamic: bool,
        dynamic: str,
        *,
        force: bool = False,
    ) -> None:
        self._data[path] = data
        if not force and is_dynamic:
            self._dynamics[path] = dynamic

    def get_full_path(
        self,
        path: str,
        current_path: str,
    ):
        relative, subpath = path.split(".", 1)
        relative_len = len(relative)
        path_len = current_path.count(".")
        if path_len + 1 == relative_len:
            return subpath
        parent_path = current_path.rsplit(".", relative_len)[0]
        return parent_path + "." + subpath

    def get_with_dynamic(
        self,
        path: str,
        identifier_path: str,
        current_path: str,
        version: str,
        namespace: str,
        xmlfiles: List[str],
    ) -> Any:
        identifier = None
        if version != "1.0" and self.regexp_relative.search(path):
            path = self.get_full_path(
                path,
                current_path,
            )
        else:
            path = get_realpath(path, identifier_path)
        dynamic = None
        # version 1.0
        if version == "1.0":
            if not path in self._data and "{{ suffix }}" not in path:
                new_path = None
                current_path = None
                identifiers = []
                for name in path.split("."):
                    parent_path = current_path
                    if current_path:
                        current_path += "." + name
                    else:
                        current_path = name
                    if current_path in self._data:
                        if new_path:
                            new_path += "." + name
                        else:
                            new_path = name
                        continue
                    for dynamic_path in self._dynamics:
                        if "." in dynamic_path:
                            parent_dynamic, name_dynamic = dynamic_path.rsplit(".", 1)
                        else:
                            parent_dynamic = None
                            name_dynamic = dynamic_path
                        if (
                            parent_dynamic == parent_path
                            and name_dynamic.endswith("{{ identifier }}")
                            and name == name_dynamic.replace("{{ identifier }}", "")
                        ):
                            new_path += "." + name_dynamic
                            break
                        regexp = "^" + name_dynamic.replace("{{ identifier }}", "(.*)")
                        finded = findall(regexp, name)
                        if len(finded) != 1 or not finded[0]:
                            continue
                        if finded[0] == "{{ identifier }}":
                            identifiers.append(None)
                        else:
                            identifiers.append(finded[0])
                        if new_path is None:
                            new_path = name_dynamic
                        else:
                            new_path += "." + name_dynamic
                        parent_path = dynamic_path
                        break
                    else:
                        if new_path:
                            new_path += "." + name
                        else:
                            new_path = name
                path = new_path
            else:
                identifiers = None
                if "{{ suffix }}" in path:
                    path = path.replace("{{ suffix }}", "{{ identifier }}")
        elif not path in self._data:
            current_path = None
            parent_path = None
            new_path = current_path
            identifiers = []
            for name in path.split("."):
                if current_path:
                    current_path += "." + name
                else:
                    current_path = name
                # parent_path, name_path = path.rsplit('.', 1)
                if current_path in self._data:
                    if new_path:
                        new_path += "." + name
                    else:
                        new_path = name
                    parent_path = current_path
                    continue
                for dynamic_path in self._dynamics:
                    if "." in dynamic_path:
                        parent_dynamic, name_dynamic = dynamic_path.rsplit(".", 1)
                    else:
                        parent_dynamic = None
                        name_dynamic = dynamic_path
                    if (
                        "{{ identifier }}" not in name_dynamic
                        or parent_path != parent_dynamic
                    ):
                        continue
                    regexp = "^" + name_dynamic.replace("{{ identifier }}", "(.*)")
                    finded = findall(regexp, name)
                    if len(finded) != 1 or not finded[0]:
                        continue
                    if finded[0] == "{{ identifier }}":
                        identifiers.append(None)
                    else:
                        identifiers.append(finded[0])
                    if new_path is None:
                        new_path = name_dynamic
                    else:
                        new_path += "." + name_dynamic
                    parent_path = dynamic_path
                    break
                else:
                    if new_path:
                        new_path += "." + name
                    else:
                        new_path = name
                    if "{{ identifier }}" in name:
                        identifiers.append(None)
                    parent_path = current_path
            path = new_path
        else:
            identifiers = None
        if path not in self._data:
            return None, None
        option = self._data[path]
        option_namespace = option.namespace
        if (
            self.default_namespace not in [namespace, option_namespace]
            and namespace != option_namespace
        ):
            msg = _(
                'A variable or a family located in the "{0}" namespace shall not be used in the "{1}" namespace'
            ).format(option_namespace, namespace)
            raise DictConsistencyError(msg, 38, xmlfiles)
        return option, identifiers

    def __getitem__(
        self,
        path: str,
    ) -> Union[Family, Variable]:
        if not path in self._data:
            raise AttributeError(f"cannot find variable or family {path}")
        return self._data[path]

    def __contains__(
        self,
        path: str,
    ) -> bool:
        return path in self._data

    def __delitem__(
        self,
        path: str,
    ) -> None:
        logging.info("remove empty family %s", path)
        del self._data[path]

    def is_dynamic(self, path: str) -> bool:
        return path in self._dynamics

    def get(self):
        return self._data.values()


information_types = Dict[str, Union[str, int, float, bool]]


class Informations:
    def __init__(self) -> None:
        self._data: Dict[str, information_types] = {}

    def add(
        self,
        path: str,
        key: str,
        data: Any,
    ) -> None:
        if path not in self._data:
            self._data[path] = {}
        if key in self._data[path]:
            raise Exception(f'an information "{key}" is already present in "{path}"')
        self._data[path][key] = data

    def get(
        self,
        path: str,
    ) -> information_types:
        return self._data.get(path, {})


class ParserVariable:
    def __init__(self, rougailconfig):
        self.rougailconfig = rougailconfig
        self.load_config()
        self.paths = Paths(self.main_namespace)
        self.families = []
        self.variables = []
        self.parents = {".": []}
        self.index = 0
        self.reflector_names = {}
        self.leaders = []
        self.followers = []
        self.multis = {}
        self.default_multi = {}
        self.jinja = {}
        #
        self.convert_options = list(CONVERT_OPTION)
        self.convert_options.extend(self.custom_types)
        #
        self.exclude_imports = []
        self.informations = Informations()
        self.properties = Property()
        # self.choices = Appendable()
        self.has_dyn_option = False
        self.path_prefix = None
        self.is_init = False
        super().__init__()

    def load_config(self) -> None:
        rougailconfig = self.rougailconfig
        self.sort_dictionaries_all = rougailconfig["sort_dictionaries_all"]
        try:
            self.main_dictionaries = rougailconfig["main_dictionaries"]
        except:
            self.main_dictionaries = []
        self.main_namespace = rougailconfig["main_namespace"]
        if self.main_namespace:
            self.extra_dictionaries = rougailconfig["extra_dictionaries"]
        self.suffix = rougailconfig["suffix"]
        self.default_dictionary_format_version = rougailconfig[
            "default_dictionary_format_version"
        ]
        self.custom_types = rougailconfig["custom_types"]
        self.functions_files = rougailconfig["functions_files"]
        self.modes_level = rougailconfig["modes_level"]
        if self.modes_level:
            self.default_variable_mode = rougailconfig["default_variable_mode"]
            self.default_family_mode = rougailconfig["default_family_mode"]
        self.extra_annotators = rougailconfig["extra_annotators"]
        self.base_option_name = rougailconfig["base_option_name"]
        self.export_with_import = rougailconfig["export_with_import"]
        self.internal_functions = rougailconfig["internal_functions"]
        self.add_extra_options = rougailconfig[
            "structural_commandline.add_extra_options"
        ]
        self.plugins = rougailconfig["plugins"]

    def _init(self):
        if self.is_init:
            return
        variable = Variable
        family = Family
        if self.plugins:
            root = Path(__file__).parent
            for plugin in self.plugins:
                module_path = root / plugin / "object_model.py"
                if not module_path.is_file():
                    continue
                module = load_modules(
                    f"rougail.{plugin}.object_model", str(module_path)
                )
                if "Variable" in module.__all__:
                    variable = type(
                        variable.__name__ + "_" + plugin,
                        (variable, module.Variable),
                        {},
                    )
                if "Family" in module.__all__:
                    family = type(
                        family.__name__ + "_" + plugin, (family, module.Family), {}
                    )
        self.variable = variable
        self.family = family
        self.dynamic = type(Dynamic.__name__, (Dynamic, family), {})
        hint = get_type_hints(self.dynamic)
        # FIXME: only for format 1.0
        self.family_types = hint["type"].__args__  # pylint: disable=W0201
        self.family_attrs = frozenset(  # pylint: disable=W0201
            set(hint) - {"name", "path", "xmlfiles"} | {"redefine"}
        )
        self.family_calculations = self.search_calculation(  # pylint: disable=W0201
            hint
        )
        #
        hint = get_type_hints(self.variable)
        self.variable_types = (
            self.convert_options
        )  # hint["type"].__args__  # pylint: disable=W0201
        #
        self.variable_attrs = frozenset(  # pylint: disable=W0201
            set(hint) - {"name", "path", "xmlfiles"} | {"redefine", "exists"}
        )
        self.variable_calculations = self.search_calculation(  # pylint: disable=W0201
            hint
        )
        self.is_init = True

    ###############################################################################################
    # determine if the object is a family or a variable
    ###############################################################################################
    def is_family_or_variable(
        self,
        path: str,
        obj: dict,
        family_is_leadership: bool,
        version: str,
        filename: str,
    ) -> Literal["variable", "family"]:
        """Check object to determine if it's a variable or a family"""
        # it's already has a variable or a family
        if path in self.paths:
            if path in self.families:
                return "family"
            return "variable"
        # it's: "my_variable:"
        if not obj:
            return "variable"
        # check type attributes
        obj_type = self.get_family_or_variable_type(obj)
        if obj_type:
            if obj_type in self.family_types:
                return "family"
            if obj_type in self.variable_types:
                return "variable"
            msg = _("unknown type {0} for {1}").format(obj_type, path)
            raise DictConsistencyError(msg, 43, [filename])
        # in a leadership there is only variable
        if family_is_leadership:
            return "variable"
        # all attributes are in variable object
        # and values in attributes are not dict is not Calculation
        if isinstance(obj, dict):
            extra_keys = set(obj) - self.variable_attrs
            if not extra_keys:
                for key, value in obj.items():
                    if (
                        isinstance(value, dict)
                        and key != "params"
                        and not self.is_calculation(
                            key,
                            value,
                            self.variable_calculations,
                            False,
                        )
                    ):
                        break
                else:
                    return "variable"
        else:
            if version == "1.0":
                msg = f'Invalid value for the variable "{path}": "{obj}"'
                raise DictConsistencyError(msg, 102, [filename])
            return "variable"
        return "family"

    def get_family_or_variable_type(
        self,
        obj: dict,
    ) -> Optional[str]:
        """Check 'type' attributes"""
        if not isinstance(obj, dict):
            return None
        if "_type" in obj:
            # only family has _type attributs
            return obj["_type"]
        if "type" in obj and isinstance(obj["type"], str):
            return obj["type"]
        return None

    ###############################################################################################
    # create, update or delete family or variable object
    ###############################################################################################
    def family_or_variable(
        self,
        filename: str,
        name: str,
        subpath: str,
        obj: dict,
        version: str,
        comment: Optional[str],
        *,
        first_variable: bool = False,
        family_is_leadership: bool = False,
        family_is_dynamic: bool = False,
        parent_dynamic: Optional[str] = None,
    ) -> None:
        if name.startswith("_"):
            msg = f'the variable or family name "{name}" is incorrect, it must not starts with "_" character'
            raise DictConsistencyError(msg, 16, [filename])
        if not subpath:
            path = name
        else:
            path = f"{subpath}.{name}"
        if version == "0.1" and not isinstance(obj, dict) and obj is not None:
            msg = f'the variable "{path}" has a wrong type "{type(obj)}"'
            raise DictConsistencyError(msg, 17, [filename])
        typ = self.is_family_or_variable(
            path,
            obj,
            family_is_leadership,
            version,
            filename,
        )
        logging.info("family_or_variable: %s is a %s", path, typ)
        if typ == "family":
            parser = self.parse_family
        else:
            parser = self.parse_variable
        parser(
            filename,
            name,
            path,
            obj,
            version,
            comment=comment,
            first_variable=first_variable,
            family_is_leadership=family_is_leadership,
            family_is_dynamic=family_is_dynamic,
            parent_dynamic=parent_dynamic,
        )

    def parse_family(
        self,
        filename: str,
        name: str,
        path: str,
        obj: Optional[Dict[str, Any]],
        version: str,
        *,
        comment: Optional[str] = None,
        first_variable: bool = False,
        family_is_leadership: bool = False,
        family_is_dynamic: bool = False,
        parent_dynamic: Optional[str] = None,
    ) -> None:
        """Parse a family"""
        if obj is None:
            return
        family_obj = {}
        subfamily_obj = {}
        force_to_attrs = list(self.list_attributes(obj))
        for key, value in obj.items():
            if key in force_to_attrs:
                if key.startswith("_"):
                    key = key[1:]
                family_obj[key] = value
            else:
                subfamily_obj[key] = value
        if path in self.paths:
            # it's just for modify subfamily or subvariable, do not redefine
            if family_obj:
                if not obj.pop("redefine", False):
                    raise DictConsistencyError(
                        f'The family "{path}" already exists and it is not redefined',
                        32,
                        [filename],
                    )
                # convert to Calculation objects
                self.parse_parameters(
                    path,
                    obj,
                    filename,
                    family_is_dynamic,
                    False,
                    version,
                    typ="family",
                )
                self.paths.add(
                    path,
                    self.paths[path].model_copy(update=obj),
                    family_is_dynamic,
                    parent_dynamic,
                    force=True,
                )
            self.paths[path].xmlfiles.append(filename)
            force_not_first = True
            if self.paths[path].type == "dynamic":
                family_is_dynamic = True
                parent_dynamic = path
        else:
            if "redefine" in obj and obj["redefine"]:
                raise Exception(
                    f'cannot redefine the inexisting family "{path}" in {filename}'
                )
            extra_attrs = set(family_obj) - self.family_attrs
            if extra_attrs:
                raise Exception(f"extra attrs ... {extra_attrs}")
            obj_type = self.get_family_or_variable_type(family_obj)
            if obj_type is None:
                # auto set type
                if "_dynamic" in family_obj:
                    dynamic = family_obj["_dynamic"]
                elif "dynamic" in family_obj:
                    dynamic = family_obj["dynamic"]
                else:
                    dynamic = None
                if isinstance(dynamic, (list, dict)):
                    family_obj["type"] = obj_type = "dynamic"
            if obj_type == "dynamic":
                family_is_dynamic = True
                if "{{ identifier }}" not in name:
                    if version == "1.0" and "{{ suffix }}" in name:
                        name = name.replace("{{ suffix }}", "{{ identifier }}")
                        path = path.replace("{{ suffix }}", "{{ identifier }}")
                    elif "variable" in family_obj:
                        name += "{{ identifier }}"
                        path += "{{ identifier }}"
                    else:
                        msg = f'dynamic family name must have "{{{{ identifier }}}}" in his name for "{path}"'
                        raise DictConsistencyError(msg, 13, [filename])
                parent_dynamic = path
            if version != "1.0" and not family_obj and comment:
                family_obj["description"] = comment
            self.add_family(
                path,
                name,
                family_obj,
                filename,
                family_is_dynamic,
                parent_dynamic,
                version,
            )
            force_not_first = False
        if self.paths[path].type == "leadership":
            family_is_leadership = True
        for idx, key in enumerate(subfamily_obj):
            value = subfamily_obj[key]
            first_variable = not force_not_first and idx == 0
            comment = self.get_comment(key, obj)
            self.family_or_variable(
                filename,
                key,
                path,
                value,
                version,
                comment,
                first_variable=first_variable,
                family_is_leadership=family_is_leadership,
                family_is_dynamic=family_is_dynamic,
                parent_dynamic=parent_dynamic,
            )

    def list_attributes(
        self,
        obj: Dict[str, Any],
    ) -> Iterator[str]:
        """List attributes"""
        force_to_variable = []
        for key, value in obj.items():
            if key in force_to_variable:
                continue
            if key.startswith("_"):
                # if key starts with _, it's an attribute
                yield key
                # if same key without _ exists, it's a variable!
                true_key = key[1:]
                if true_key in obj:
                    force_to_variable.append(true_key)
                continue
            if isinstance(value, dict) and not self.is_calculation(
                key,
                value,
                self.family_calculations,
                False,
            ):
                # it's a dict, so a new variables!
                continue
            # 'variable' for compatibility to format 1.0
            if (
                key == "variable"
                and obj.get("type") != "dynamic"
                and obj.get("_type") != "dynamic"
            ):
                continue
            if key in self.family_attrs:
                yield key

    def add_family(
        self,
        path: str,
        name: str,
        family: dict,
        filename: str,
        family_is_dynamic: bool,
        parent_dynamic: str,
        version: str,
    ) -> None:
        """Add a new family"""
        family["path"] = path
        family["namespace"] = self.namespace
        family["version"] = version
        family["xmlfiles"] = [filename]
        obj_type = self.get_family_or_variable_type(family)
        if obj_type == "dynamic":
            family_obj = self.dynamic
            if version == "1.0":
                if "variable" not in family:
                    raise DictConsistencyError(
                        f'dynamic family must have "variable" attribute for "{path}"',
                        101,
                        family["xmlfiles"],
                    )
                if "dynamic" in family:
                    raise DictConsistencyError(
                        'variable and dynamic cannot be set together in the dynamic family "{path}"',
                        100,
                        family["xmlfiles"],
                    )
                family["dynamic"] = {
                    "type": "variable",
                    "variable": family["variable"],
                    "propertyerror": False,
                    "allow_none": True,
                }
                del family["variable"]
            # FIXME only for 1.0
            if "variable" in family:
                family["dynamic"] = {
                    "type": "variable",
                    "variable": family["variable"],
                    "propertyerror": False,
                    "allow_none": True,
                }
                del family["variable"]
                if version != "1.0":
                    warning = f'"variable" attribute in dynamic family "{ path }" is depreciated in {filename}'
                    warn(warning)
            if "variable" in family:
                raise Exception(
                    f'dynamic family must not have "variable" attribute for "{family["path"]}" in {family["xmlfiles"]}'
                )
        else:
            family_obj = self.family
        # convert to Calculation objects
        self.parse_parameters(
            path,
            family,
            filename,
            family_is_dynamic,
            False,
            version,
            typ="family",
        )
        try:
            self.paths.add(
                path,
                family_obj(name=name, **family),
                family_is_dynamic,
                parent_dynamic,
            )
        except ValidationError as err:
            raise Exception(f'invalid family "{path}" in "{filename}": {err}') from err
        self.set_name(
            self.paths[path],
            "optiondescription_",
        )
        if "." not in path:
            parent = "."
        else:
            parent = path.rsplit(".", 1)[0]
        self.parents[parent].append(path)
        self.parents[path] = []
        self.families.append(path)

    def parse_variable(
        self,
        filename: str,
        name: str,
        path: str,
        obj: Optional[Dict[str, Any]],
        version: str,
        *,
        comment: Optional[str] = None,
        first_variable: bool = False,
        family_is_leadership: bool = False,
        family_is_dynamic: bool = False,
        parent_dynamic: Optional[str] = None,
    ) -> None:
        """Parse variable"""
        if version == "1.0" or isinstance(obj, dict):
            if obj is None:
                obj = {}
            extra_attrs = set(obj) - self.variable_attrs
        else:
            extra_attrs = []
            obj = {"default": obj}
            if comment:
                obj["description"] = comment
        if extra_attrs:
            raise Exception(
                f'"{path}" is not a valid variable, there are additional '
                f'attributes: "{", ".join(extra_attrs)}"'
            )
        self.parse_parameters(
            path,
            obj,
            filename,
            family_is_dynamic,
            family_is_leadership is True and first_variable is False,
            version,
        )
        self.parse_params(path, obj)
        if path in self.paths:
            if "exists" in obj and not obj.pop("exists"):
                return
            if not obj.pop("redefine", False):
                msg = f'Variable "{path}" already exists'
                raise DictConsistencyError(msg, 45, [filename])
            self.paths.add(
                path,
                self.paths[path].model_copy(update=obj),
                family_is_dynamic,
                parent_dynamic,
                force=True,
            )
            self.paths[path].xmlfiles.append(filename)
        else:
            if "exists" in obj and obj.pop("exists"):
                # this variable must exist
                # but it's not the case
                # so do nothing
                return
            if "redefine" in obj and obj["redefine"]:
                msg = f'cannot redefine the inexisting variable "{path}"'
                raise DictConsistencyError(msg, 46, [filename])
            obj["path"] = path
            self.add_variable(
                name, obj, filename, family_is_dynamic, parent_dynamic, version
            )
            if family_is_leadership:
                if first_variable:
                    self.leaders.append(path)
                else:
                    self.followers.append(path)

    def parse_parameters(
        self,
        path: str,
        obj: dict,
        filename: str,
        family_is_dynamic: bool,
        is_follower: bool,
        version: str,
        *,
        typ: str = "variable",
    ):
        """Parse variable or family parameters"""
        if typ == "variable":
            calculations = self.variable_calculations
        else:
            calculations = self.family_calculations
        for key, value in obj.items():
            if self.is_calculation(
                key,
                value,
                calculations,
                False,
            ):
                try:
                    self.set_calculation(
                        obj,
                        key,
                        value,
                        path,
                        family_is_dynamic,
                        is_follower,
                        version,
                        [filename],
                    )
                except ValidationError as err:
                    raise Exception(
                        f'the {typ} "{path}" in "{filename}" has an invalid "{key}": {err}'
                    ) from err
                continue
            if not isinstance(value, list):
                continue
            for idx, val in enumerate(value):
                if not self.is_calculation(
                    key,
                    val,
                    calculations,
                    True,
                ):
                    continue
                try:
                    self.set_calculation(
                        obj,
                        key,
                        val,
                        path,
                        family_is_dynamic,
                        is_follower,
                        version,
                        [filename],
                        inside_list=True,
                        index=idx,
                    )
                except ValidationError as err:
                    raise Exception(
                        f'the {typ} "{path}" in "{filename}" has an invalid "{key}" '
                        f"at index {idx}: {err}"
                    ) from err

    def parse_params(self, path, obj):
        """Parse variable params"""
        if "params" not in obj:
            return
        if not isinstance(obj["params"], dict):
            raise Exception(f"params must be a dict for {path}")
        params = []
        for key, val in obj["params"].items():
            try:
                params.append(
                    AnyParam(
                        key=key,
                        value=val,
                        type="any",
                        path=None,
                        is_follower=None,
                        attribute=None,
                        family_is_dynamic=None,
                        xmlfiles=None,
                    )
                )
            except ValidationError as err:
                raise Exception(
                    f'"{key}" has an invalid "params" for {path}: {err}'
                ) from err
        obj["params"] = params

    def add_variable(
        self,
        name: str,
        variable: dict,
        filename: str,
        family_is_dynamic: bool,
        parent_dynamic: Optional[str],
        version: str,
    ) -> None:
        """Add a new variable"""
        if not isinstance(filename, list):
            filename = [filename]

        variable["namespace"] = self.namespace
        variable["version"] = version
        variable["path_prefix"] = self.path_prefix
        variable["xmlfiles"] = filename
        variable_type = self.get_family_or_variable_type(variable)
        obj = {
            "symlink": SymLink,
            "choice": self.variable,
        }.get(variable_type, self.variable)
        try:
            variable_obj = obj(name=name, **variable)
        except ValidationError as err:
            raise Exception(
                f'invalid variable "{variable["path"]}" in "{filename}": {err}'
            ) from err
        self.paths.add(
            variable["path"],
            variable_obj,
            family_is_dynamic,
            parent_dynamic,
        )
        self.variables.append(variable["path"])
        if "." in variable["path"]:
            parent_path = variable["path"].rsplit(".", 1)[0]
        else:
            parent_path = "."
        self.parents[parent_path].append(variable["path"])
        self.set_name(
            variable_obj,
            "option_",
        )

    def del_family(
        self,
        path: str,
    ) -> None:
        """The family is empty, so delete it"""
        del self.paths[path]
        self.families.remove(path)
        del self.parents[path]
        if "." in path:
            parent = path.rsplit(".", 1)[0]
        else:
            parent = "."
        self.parents[parent].remove(path)

    ###############################################################################################
    # set tiramisu file name
    ###############################################################################################
    def set_name(
        self,
        obj: Union[Variable, Family],
        option_prefix: str,
    ):
        """Set Tiramisu object name"""
        self.index += 1
        self.reflector_names[obj.path] = f"{option_prefix}{self.index}{self.suffix}"

    ###############################################################################################
    # calculations
    ###############################################################################################
    def is_calculation(
        self,
        attribute: str,
        value: dict,
        calculations: list,
        inside_list: bool,
    ):
        """Check if it's a calculation"""
        if inside_list:
            calculations = calculations[0]
        else:
            calculations = calculations[1]
        if not isinstance(value, dict) or attribute not in calculations:
            return False
        if "type" in value:
            return value["type"] in CALCULATION_TYPES
        # auto set type
        typ = set(CALCULATION_TYPES) & set(value)
        if len(typ) == 1:
            value["type"] = list(typ)[0]
            return True
        return False

    def set_calculation(
        self,
        obj: dict,
        attribute: str,
        value: dict,
        path: str,
        family_is_dynamic: bool,
        is_follower: bool,
        version: str,
        xmlfiles: List[str],
        *,
        inside_list: bool = False,
        index: int = None,
    ):
        """This variable is a calculation"""
        calculation_object = value.copy()
        typ = calculation_object.pop("type")

        calculation_object["attribute_name"] = attribute
        calculation_object["path_prefix"] = self.path_prefix
        calculation_object["path"] = path
        calculation_object["inside_list"] = inside_list
        calculation_object["version"] = version
        calculation_object["namespace"] = self.namespace
        calculation_object["xmlfiles"] = xmlfiles
        #
        if "params" in calculation_object:
            if not isinstance(calculation_object["params"], dict):
                raise Exception("params must be a dict")
            params = []
            for key, val in calculation_object["params"].items():
                if isinstance(val, dict) and "type" not in val:
                    # auto set type
                    param_typ = set(CALCULATION_TYPES) & set(val)
                    if len(param_typ) == 1:
                        val["type"] = list(param_typ)[0]
                if not isinstance(val, dict) or "type" not in val:
                    param_typ = "any"
                    val = {
                        "value": val,
                        "type": "any",
                    }
                else:
                    if version == "1.0" and val["type"] == "suffix":
                        val["type"] = "identifier"
                    param_typ = val["type"]
                val["key"] = key
                val["path"] = path
                val["family_is_dynamic"] = family_is_dynamic
                val["is_follower"] = is_follower
                val["attribute"] = attribute
                val["xmlfiles"] = xmlfiles
                try:
                    params.append(PARAM_TYPES[param_typ](**val))
                except ValidationError as err:
                    raise DictConsistencyError(
                        f'"{attribute}" has an invalid "{key}" for {path}: {err}',
                        29,
                        xmlfiles,
                    ) from err
            calculation_object["params"] = params
        #
        return_type = calculation_object.get("return_type")
        if return_type:
            if return_type not in self.variable_types:
                raise Exception(
                    f'unknown "return_type" in {attribute} of variable "{path}"'
                )
        #
        if typ == "identifier" and not family_is_dynamic:
            msg = f'identifier calculation for "{attribute}" in "{path}" cannot be set none dynamic family'
            raise DictConsistencyError(msg, 53, xmlfiles)
        if attribute in PROPERTY_ATTRIBUTE:
            calc = CALCULATION_PROPERTY_TYPES[typ](**calculation_object)
        else:
            calc = CALCULATION_TYPES[typ](**calculation_object)
        if index is None:
            obj[attribute] = calc
        else:
            obj[attribute][index] = calc


class RougailConvert(ParserVariable):
    """Main Rougail conversion"""

    supported_version = ["1.0", "1.1"]

    def __init__(self, rougailconfig) -> None:
        self.annotator = False
        self.yaml = YAML()
        super().__init__(rougailconfig)

    def search_calculation(
        self,
        hint: dict,
    ) -> Tuple[List[Any], List[Any]]:
        """attribute is calculated if typing is like: Union[Calculation, xxx]"""
        inside_list = []
        outside_list = []
        for key, value in hint.items():
            if "Union" in value.__class__.__name__ and (
                Calculation in value.__args__ or VariableCalculation in value.__args__
            ):
                outside_list.append(key)
            if (
                "Union" in value.__class__.__name__
                and "_GenericAlias" in value.__args__[0].__class__.__name__
                and Calculation in value.__args__[0].__args__
            ):
                inside_list.append(key)
            if (
                "Union" in value.__class__.__name__
                and value.__args__[0].__class__.__name__ == "_GenericAlias"
                and "Union" in value.__args__[0].__args__[0].__class__.__name__
                and Calculation in value.__args__[0].__args__[0].__args__
            ):
                inside_list.append(key)
        return inside_list, outside_list

    def parse_directories(
        self,
        path_prefix: Optional[str] = None,
    ) -> None:
        """Parse directories content"""
        self._init()
        if path_prefix:
            n_path_prefix = normalize_family(path_prefix)
            if n_path_prefix in self.parents:
                raise Exception("pfffff")
            root_parent = n_path_prefix
            self.path_prefix = n_path_prefix
            self.namespace = None
            self.add_family(
                n_path_prefix,
                n_path_prefix,
                {"description": path_prefix},
                "",
                False,
                None,
                "",
            )
        else:
            root_parent = "."
        if self.main_namespace:
            directory_dict = chain(
                (
                    (
                        self.main_namespace,
                        self.main_dictionaries,
                    ),
                ),
                self.extra_dictionaries.items(),
            )
            for namespace, extra_dirs in directory_dict:
                if namespace is None:
                    self.namespace = namespace
                else:
                    self.namespace = normalize_family(namespace)
                if root_parent == ".":
                    namespace_path = self.namespace
                else:
                    namespace_path = f"{root_parent}.{self.namespace}"
                if namespace_path in self.parents:
                    raise Exception("pfff")
                for idx, filename in enumerate(self.get_sorted_filename(extra_dirs)):
                    if not idx:
                        self.parse_family(
                            "",
                            self.namespace,
                            namespace_path,
                            {
                                "description": namespace,
                            },
                            "",
                        )
                    self.parse_variable_file(
                        filename,
                        namespace_path,
                    )
        else:
            self.namespace = None
            if root_parent == ".":
                namespace_path = ""
            else:
                namespace_path = f"{root_parent}"
            if namespace_path in self.parents:
                raise Exception("pfff")
            for filename in self.get_sorted_filename(self.main_dictionaries):
                self.parse_variable_file(
                    filename,
                    namespace_path,
                )
        if path_prefix:
            self.path_prefix = None

    def get_comment(
        self,
        name: str,
        objects: CommentedMap,
    ) -> Optional[str]:
        if name in objects.ca.items:
            comment = objects.ca.items[name][2]
        else:
            comment = None
        if comment:
            comment = comment.value[1:].strip()
        return comment

    def parse_variable_file(
        self,
        filename: str,
        path: str,
    ) -> None:
        """Parse file"""
        with open(filename, encoding="utf8") as file_fh:
            objects = self.yaml.load(file_fh)
        version = self.validate_file_version(
            objects,
            filename,
        )
        if objects is None:
            return
        self.parse_root_file(
            filename,
            path,
            version,
            objects,
        )

    def parse_root_file(
        self,
        filename: str,
        path: str,
        version: str,
        objects: dict,
    ) -> None:
        for name, obj in objects.items():
            comment = self.get_comment(name, objects)
            self.family_or_variable(
                filename,
                name,
                path,
                obj,
                version,
                comment,
            )

    def get_sorted_filename(
        self,
        directories: Union[str, List[str]],
    ) -> Iterator[str]:
        """Sort filename"""
        if not isinstance(directories, list):
            directories = [directories]
        if self.sort_dictionaries_all:
            filenames = {}
        for directory_name in directories:
            directory = Path(directory_name)
            if not directory.is_dir():
                continue
            if not self.sort_dictionaries_all:
                filenames = {}
            for file_path in directory.iterdir():
                if file_path.suffix not in [".yml", ".yaml"]:
                    continue
                if file_path.name in filenames:
                    raise DictConsistencyError(
                        _("duplicate dictionary file name {0}").format(file_path.name),
                        78,
                        [filenames[file_path.name][1]],
                    )
                filenames[file_path.name] = str(file_path)
            if not self.sort_dictionaries_all:
                for filename in sorted(filenames):
                    yield filenames[filename]
        if self.sort_dictionaries_all:
            for filename in sorted(filenames):
                yield filenames[filename]

    def validate_file_version(
        self,
        obj: dict,
        filename: str,
    ) -> None:
        """version is mandatory in YAML file"""
        if obj is None:
            obj = {}
        for name in ["_version", "version"]:
            if name not in obj:
                continue
            version = str(obj.pop(name))
            break
        else:
            # the `version` attribute is not mandatory
            default_version = self.default_dictionary_format_version
            if default_version is not None:
                version = default_version
            else:
                msg = '"version" attribut is mandatory in YAML file'
                raise DictConsistencyError(msg, 27, [filename])

        if version not in self.supported_version:
            msg = f'version "{version}" is not supported, list of supported versions: {display_list(self.supported_version, separator="or", add_quote=True)}'
            raise DictConsistencyError(msg, 28, [filename])
        return version

    def annotate(
        self,
    ):
        """Apply annotation"""
        if not self.paths.has_value():
            self.parse_directories()
        if self.annotator:
            raise DictConsistencyError(
                _("Cannot execute annotate multiple time"), 85, None
            )
        SpaceAnnotator(self)
        self.annotator = True

    def reflect(self) -> None:
        """Apply TiramisuReflector"""
        functions_files = [
            func for func in self.functions_files if func not in self.exclude_imports
        ]
        self.reflector = TiramisuReflector(
            self,
            functions_files,
        )

    def save(
        self,
        filename: str,
    ):
        """Return tiramisu object declaration as a string"""
        self._init()
        self.annotate()
        self.reflect()
        output = self.reflector.get_text() + "\n"
        if filename:
            with open(filename, "w", encoding="utf-8") as tiramisu:
                tiramisu.write(output)
        # print(output)
        return output
