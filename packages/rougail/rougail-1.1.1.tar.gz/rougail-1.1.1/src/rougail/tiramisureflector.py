"""loader
flattened XML specific

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

from typing import Optional, Union
from json import dumps
from os.path import isfile, basename

from .i18n import _
from .error import DictConsistencyError, VariableCalculationDependencyError
from .utils import normalize_family
from .object_model import Calculation, CONVERT_OPTION


class BaseElt:  # pylint: disable=R0903
    """Base element"""

    path = "."
    type = "family"


def sorted_func_name(func_name):
    s_func_name = func_name.split("/")
    s_func_name.reverse()
    return "/".join(s_func_name)


class TiramisuReflector:
    """Convert object to tiramisu representation"""

    def __init__(
        self,
        objectspace,
        funcs_paths,
    ):
        self.informations_idx = -1
        self.reflector_objects = {}
        self.text = {
            "header": [],
            "option": [],
        }
        self.objectspace = objectspace
        if self.objectspace.export_with_import:
            if self.objectspace.internal_functions:
                for func in self.objectspace.internal_functions:
                    self.text["header"].append(f"func[func] = func")
            self.text["header"].extend(
                [
                    "from tiramisu import *",
                    "from tiramisu.setting import ALLOWED_LEADER_PROPERTIES",
                    "from re import compile as re_compile",
                ]
            )
        if self.objectspace.export_with_import:
            self.text["header"].extend(
                [
                    "from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription"
                ]
            )
        if funcs_paths:
            for funcs_path in sorted(funcs_paths, key=sorted_func_name):
                if not isfile(funcs_path):
                    continue
                self.text["header"].append(f"load_functions('{funcs_path}')")
        if self.objectspace.export_with_import:
            if objectspace.main_namespace:
                self.text["header"].extend(
                    [
                        "try:",
                        "    groups.namespace",
                        "except:",
                        "    groups.addgroup('namespace')",
                    ]
                )
            for mode in self.objectspace.modes_level:
                self.text["header"].append(f'ALLOWED_LEADER_PROPERTIES.add("{mode}")')
        self.make_tiramisu_objects()
        for key, value in self.objectspace.jinja.items():
            self.add_jinja_to_function(key, value)

    def add_jinja_to_function(
        self,
        variable_name: str,
        jinja: str,
    ) -> None:
        jinja_text = dumps(jinja, ensure_ascii=False)
        self.text["header"].append(f"dict_env['{variable_name}'] = {jinja_text}")

    def make_tiramisu_objects(self) -> None:
        """make tiramisu objects"""
        baseelt = BaseElt()
        self.objectspace.reflector_names[baseelt.path] = (
            f"option_0{self.objectspace.suffix}"
        )
        basefamily = Family(
            baseelt,
            self,
        )
        for elt in self.objectspace.paths.get():
            if elt.path in self.objectspace.families:
                Family(
                    elt,
                    self,
                )
            else:
                Variable(
                    elt,
                    self,
                )
        #        else:
        #            path_prefixes = self.objectspace.paths.get_path_prefixes()
        #            for path_prefix in path_prefixes:
        #                space = self.objectspace.space.variables[path_prefix]
        #                self.set_name(space)
        #                baseprefix = Family(
        #                    space,
        #                    self,
        #                )
        #                basefamily.add(baseprefix)
        #                for elt in self.reorder_family(space):
        #                    self.populate_family(
        #                        baseprefix,
        #                        elt,
        #                    )
        #                if not hasattr(baseprefix.elt, "information"):
        #                    baseprefix.elt.information = self.objectspace.information(
        #                        baseprefix.elt.xmlfiles
        #                    )
        #                for key, value in self.objectspace.paths.get_providers_path(
        #                    path_prefix
        #                ).items():
        #                    setattr(baseprefix.elt.information, key, value)
        #                for key, value in self.objectspace.paths.get_suppliers_path(
        #                    path_prefix
        #                ).items():
        #                    setattr(baseprefix.elt.information, key, value)
        baseelt.name = normalize_family(self.objectspace.base_option_name)
        baseelt.description = self.objectspace.base_option_name
        self.reflector_objects[baseelt.path].get(
            [], baseelt.description
        )  # pylint: disable=E1101

    def set_name(
        self,
        elt,
    ):
        """Set name"""
        if elt.path not in self.objectspace.reflector_names:
            self.objectspace.set_name(elt, "optiondescription_")
        return self.objectspace.reflector_names[elt.path]

    def get_information_name(self):
        self.informations_idx += 1
        return f"information_{self.informations_idx}"

    def get_text(self):
        """Get text"""
        return "\n".join(self.text["header"] + self.text["option"])


class Common:
    """Common function for variable and family"""

    def __init__(
        self,
        elt,
        tiramisu,
    ):
        self.objectspace = tiramisu.objectspace
        self.elt = elt
        self.option_name = None
        self.tiramisu = tiramisu
        tiramisu.reflector_objects[elt.path] = self
        self.object_type = None
        self.informations = []

    def get(self, calls, parent_name):
        """Get tiramisu's object"""
        if self.elt.path in calls:
            msg = f'"{self.elt.path}" will make an infinite loop'
            raise DictConsistencyError(msg, 80, self.elt.xmlfiles)
        self_calls = calls.copy()
        self_calls.append(self.elt.path)
        self.calls = self_calls
        if self.option_name is None:
            self.option_name = self.objectspace.reflector_names[self.elt.path]
            self.populate_attrib()
            if self.informations:
                for information in self.informations:
                    self.tiramisu.text["option"].append(
                        f"{information}.set_option({self.option_name})"
                    )
        return self.option_name

    def populate_attrib(self):
        """Populate attributes"""
        keys = {"name": self.convert_str(self.elt.name)}
        if hasattr(self.elt, "description") and self.elt.description:
            keys["doc"] = self.convert_str(self.elt.description)
        self._populate_attrib(keys)
        if self.elt.path in self.objectspace.properties:
            keys["properties"] = self.properties_to_string(
                self.objectspace.properties[self.elt.path]
            )
        self.populate_informations(keys)
        attrib = ", ".join([f"{key}={value}" for key, value in keys.items()])
        self.tiramisu.text["option"].append(
            f"{self.option_name} = {self.object_type}({attrib})"
        )

    def _populate_attrib(
        self,
        keys: dict,
    ) -> None:  # pragma: no cover
        raise NotImplementedError()

    @staticmethod
    def convert_str(value):
        """convert string"""
        if value is None:
            return "None"
        return dumps(value, ensure_ascii=False)

    def properties_to_string(
        self,
        values: list,
    ) -> None:
        """Change properties to string"""
        properties = []
        calc_properties = []
        for property_, value in values.items():
            if value is True:
                properties.append(self.convert_str(property_))
            elif isinstance(value, list):
                for val in value:
                    calc_properties.append(self.calculation_value(val))
            else:
                calc_properties.append(self.calculation_value(value))
        return "frozenset({" + ", ".join(sorted(properties) + calc_properties) + "})"

    def calc_properties(
        self,
        prop,
        calculation,
    ) -> str:
        """Populate properties"""
        option_name = self.tiramisu.reflector_objects[child.source.path].get(
            self.calls, self.elt.path
        )
        kwargs = (
            f"'condition': ParamOption({option_name}, notraisepropertyerror=True), "
            f"'expected': {self.populate_param(child.expected)}"
        )
        if child.inverse:
            kwargs += ", 'reverse_condition': ParamValue(True)"
        return (
            f"Calculation(func['calc_value'], Params(ParamValue('{child.name}'), "
            f"kwargs={{{kwargs}}}), func['calc_value_property_help'])"
        )

    def populate_informations(self, keys):
        """Populate Tiramisu's informations"""
        informations = self.objectspace.informations.get(self.elt.path)
        if not informations:
            return
        keys["informations"] = informations

    def populate_param(
        self,
        param,
    ):
        """Populate variable parameters"""
        if not isinstance(param, dict):
            if isinstance(param, str):
                value = self.convert_str(param)
            else:
                value = param
            return f"ParamValue({value})"
        if param["type"] == "value":
            return f"ParamValue({param['value']})"
        if param["type"] == "information":
            # default? really?
            if self.elt.multi:
                default = []
            else:
                default = None
            if "variable" in param:
                if param["variable"].path == self.elt.path:
                    return f'ParamSelfInformation("{param["information"]}", {default})'
                information_variable_path = param["variable"].path
                information_variable = self.tiramisu.reflector_objects[
                    information_variable_path
                ]
                if information_variable_path not in self.calls:
                    option_name = information_variable.get(self.calls, self.elt.path)
                    return f'ParamInformation("{param["information"]}", {default}, option={option_name})'
                else:
                    information = (
                        f'ParamInformation("{param["information"]}", {default})'
                    )
                    information_name = self.tiramisu.get_information_name()
                    self.tiramisu.text["option"].append(
                        f"{information_name} = {information}"
                    )
                    information_variable.informations.append(information_name)
                    return information_name
            return f'ParamInformation("{param["information"]}", {default})'
        if param["type"] == "identifier":
            if "identifier" in param and param["identifier"] != None:
                return f"ParamIdentifier(identifier_index={param['identifier']})"
            return "ParamIdentifier()"
        if param["type"] == "index":
            return "ParamIndex()"
        if param["type"] == "variable":
            return self.build_option_param(
                param["variable"],
                param.get("propertyerror", True),
                param.get("identifier"),
                param.get("dynamic"),
                param.get("whole", False),
            )
        if param["type"] == "any":
            if isinstance(param["value"], str):
                value = self.convert_str(param["value"])
            else:
                value = str(param["value"])
            return "ParamValue(" + value + ")"
        raise Exception("pfff")

    def build_option_param(
        self,
        variable,
        propertyerror,
        identifier: Optional[str],
        dynamic,
        whole: bool,
    ) -> str:
        """build variable parameters"""
        if variable.path == self.elt.path:
            return f"ParamSelfOption(whole={whole})"
        if whole:
            msg = f'variable param "{variable.path}" has whole attribute but it\'s not allowed for external variable'
            raise DictConsistencyError(msg, 34, self.elt.xmlfiles)
        option_name = self.tiramisu.reflector_objects[variable.path].get(
            self.calls, self.elt.path
        )
        params = [f"{option_name}"]
        if identifier is not None:
            param_type = "ParamDynOption"
            identifiers = []
            for ident in identifier:
                if isinstance(ident, str):
                    ident = self.convert_str(ident)
                identifiers.append(str(ident))
            params.append("[" + ", ".join(identifiers) + "]")
        else:
            param_type = "ParamOption"
        if not propertyerror:
            params.append("notraisepropertyerror=True")
        return f'{param_type}({", ".join(params)})'

    def calculation_value(
        self,
        function,
    ) -> str:
        """Generate calculated value"""
        child = function.to_function(self.objectspace)
        new_args = []
        kwargs = []
        if "params" in child:
            for key, value in child["params"].items():
                if not key:
                    for val in value:
                        new_args.append(self.populate_param(val))
                else:
                    kwargs.append(f"'{key}': " + self.populate_param(value))
        ret = (
            f"Calculation(func['{child['function']}'], Params(("
            + ", ".join(new_args)
            + ")"
        )
        if kwargs:
            ret += ", kwargs={" + ", ".join(kwargs) + "}"
        ret += ")"
        if hasattr(child, "warnings_only"):
            ret += f", warnings_only={child.warnings_only}"
        if "help" in child:
            ret += f", help_function=func['{child['help']}']"
        ret = ret + ")"
        return ret

    def populate_calculation(
        self,
        datas: Union[Calculation, str, list],
        return_a_tuple: bool = False,
    ) -> str:
        if isinstance(datas, str):
            return self.convert_str(datas)
        if isinstance(datas, Calculation):
            return self.calculation_value(datas)
        if not isinstance(datas, list):
            return datas
        params = []
        for idx, data in enumerate(datas):
            if isinstance(data, Calculation):
                try:
                    params.append(self.calculation_value(data))
                except VariableCalculationDependencyError:
                    pass
            elif isinstance(data, str):
                params.append(self.convert_str(data))
            else:
                params.append(str(data))
        if return_a_tuple:
            ret = "("
        else:
            ret = "["
        ret += ", ".join(params)
        if return_a_tuple:
            if len(params) <= 1:
                ret += ","
            ret += ")"
        else:
            ret += "]"
        return ret


class Variable(Common):
    """Manage variable"""

    def __init__(
        self,
        elt,
        tiramisu,
    ):
        super().__init__(elt, tiramisu)
        if elt.type in self.tiramisu.objectspace.custom_types:
            self.object_type = self.tiramisu.objectspace.custom_types[elt.type].__name__
        else:
            self.object_type = CONVERT_OPTION[elt.type]["opttype"]

    def _populate_attrib(
        self,
        keys: dict,
    ):
        if self.elt.type == "symlink":
            keys["opt"] = self.tiramisu.reflector_objects[self.elt.opt.path].get(
                self.calls, self.elt.path
            )
            return
        if self.elt.type == "choice":
            keys["values"] = self.populate_calculation(
                self.elt.choices, return_a_tuple=True
            )
        if self.elt.type == "regexp":
            self.object_type = "Regexp_" + self.option_name
            self.tiramisu.text["header"].append(
                f"""class {self.object_type}(RegexpOption):
    __slots__ = tuple()
    _type = 'value'
{self.object_type}._regexp = re_compile(r"{self.elt.regexp}")
"""
            )
        if self.elt.path in self.objectspace.multis:
            keys["multi"] = self.objectspace.multis[self.elt.path]
        if hasattr(self.elt, "default") and self.elt.default is not None:
            try:
                keys["default"] = self.populate_calculation(self.elt.default)
            except VariableCalculationDependencyError:
                pass
        if self.elt.path in self.objectspace.default_multi:
            try:
                keys["default_multi"] = self.populate_calculation(
                    self.objectspace.default_multi[self.elt.path]
                )
            except VariableCalculationDependencyError:
                pass
        if self.elt.validators:
            keys["validators"] = self.populate_calculation(self.elt.validators)
        for key, value in (
            CONVERT_OPTION.get(self.elt.type, {}).get("initkwargs", {}).items()
        ):
            if isinstance(value, str):
                value = self.convert_str(value)
            keys[key] = value
        if self.elt.params:
            for param in self.elt.params:
                value = param.value
                if isinstance(value, str):
                    value = self.convert_str(value)
                keys[param.key] = value


class Family(Common):
    """Manage family"""

    def __init__(
        self,
        elt,
        tiramisu,
    ):
        super().__init__(elt, tiramisu)
        if self.elt.type == "dynamic":
            self.tiramisu.objectspace.has_dyn_option = True
            self.object_type = "ConvertDynOptionDescription"
        elif self.elt.type == "leadership":
            self.object_type = "Leadership"
        else:
            self.object_type = "OptionDescription"
        if hasattr(self.elt, "name") and self.elt.name == self.elt.namespace:
            self.group_type = "groups.namespace"
        else:
            self.group_type = None
        self.children = []

    def add(self, child):
        """Add a child"""
        self.children.append(child)

    def _populate_attrib(
        self,
        keys: list,
    ) -> None:
        if self.group_type:
            keys["group_type"] = self.group_type
        if self.elt.type == "dynamic":
            keys["identifiers"] = self.populate_calculation(self.elt.dynamic)
        children = []
        for path in self.objectspace.parents[self.elt.path]:
            children.append(self.objectspace.paths[path])
        keys["children"] = (
            "["
            + ", ".join(
                [
                    self.tiramisu.reflector_objects[child.path].get(
                        self.calls, self.elt.path
                    )
                    for child in children
                ]
            )
            + "]"
        )
