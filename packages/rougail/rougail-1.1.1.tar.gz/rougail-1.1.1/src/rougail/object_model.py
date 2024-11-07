"""Rougail object model

Silique (https://www.silique.fr)
Copyright (C) 2023-2024

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

from typing import Optional, Union, get_type_hints, Any, Literal, List, Dict, Iterator
from pydantic import (
    BaseModel,
    StrictBool,
    StrictInt,
    StrictFloat,
    StrictStr,
    ConfigDict,
)
from tiramisu import undefined
from .utils import get_jinja_variable_to_param, get_realpath
from .error import DictConsistencyError, VariableCalculationDependencyError

BASETYPE = Union[StrictBool, StrictInt, StrictFloat, StrictStr, None]
PROPERTY_ATTRIBUTE = ["frozen", "hidden", "disabled", "mandatory"]


def convert_boolean(value: str) -> bool:
    """Boolean coercion. The Rougail XML may contain srings like `True` or `False`"""
    if isinstance(value, bool):
        return value
    value = value.lower()
    if value == "true":
        return True
    elif value == "false":
        return False
    elif value in ["", None]:
        return None
    raise Exception(f'unknown boolean value "{value}"')


CONVERT_OPTION = {
    "string": dict(opttype="StrOption", example="example"),
    "number": dict(opttype="IntOption", func=int, example=42),
    "float": dict(opttype="FloatOption", func=float, example=1.42),
    "boolean": dict(opttype="BoolOption", func=convert_boolean),
    "secret": dict(opttype="PasswordOption", example="secrets"),
    "mail": dict(opttype="EmailOption", example="user@example.net"),
    "unix_filename": dict(opttype="FilenameOption", example="/tmp/myfile.txt"),
    "date": dict(opttype="DateOption", example="2000-01-01"),
    "unix_user": dict(opttype="UsernameOption", example="username"),
    "ip": dict(
        opttype="IPOption", initkwargs={"allow_reserved": True}, example="1.1.1.1"
    ),
    "cidr": dict(opttype="IPOption", initkwargs={"cidr": True}, example="1.1.1.0/24"),
    "netmask": dict(opttype="NetmaskOption", example="255.255.255.0"),
    "network": dict(opttype="NetworkOption", example="1.1.1.0"),
    "network_cidr": dict(
        opttype="NetworkOption", initkwargs={"cidr": True}, example="1.1.1.0/24"
    ),
    "broadcast": dict(opttype="BroadcastOption", example="1.1.1.255"),
    "netbios": dict(
        opttype="DomainnameOption",
        initkwargs={"type": "netbios", "warnings_only": True},
        example="example",
    ),
    "domainname": dict(
        opttype="DomainnameOption",
        initkwargs={"type": "domainname", "allow_ip": False},
        example="example.net",
    ),
    "hostname": dict(
        opttype="DomainnameOption",
        initkwargs={"type": "hostname", "allow_ip": False},
        example="example",
    ),
    "web_address": dict(
        opttype="URLOption",
        initkwargs={"allow_ip": False, "allow_without_dot": True},
        example="https://example.net",
    ),
    "port": dict(
        opttype="PortOption", initkwargs={"allow_private": True}, example="111"
    ),
    "mac": dict(opttype="MACOption", example="00:00:00:00:00"),
    "unix_permissions": dict(
        opttype="PermissionsOption",
        initkwargs={"warnings_only": True},
        func=int,
        example="644",
    ),
    "choice": dict(opttype="ChoiceOption", example="a_choice"),
    "regexp": dict(opttype="RegexpOption"),
    #
    "symlink": dict(opttype="SymLinkOption"),
}


class Param(BaseModel):
    key: str
    model_config = ConfigDict(extra="forbid")

    def __init__(
        self,
        path,
        attribute,
        family_is_dynamic,
        is_follower,
        xmlfiles,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)


class AnyParam(Param):
    type: str
    value: Union[BASETYPE, List[BASETYPE]]


class VariableParam(Param):
    type: str
    variable: str
    propertyerror: bool = True
    whole: bool = False
    optional: bool = False


class IdentifierParam(Param):
    type: str
    identifier: Optional[int] = None

    def __init__(
        self,
        **kwargs,
    ) -> None:
        if not kwargs["family_is_dynamic"]:
            msg = f'identifier parameter for "{kwargs["attribute"]}" in "{kwargs["path"]}" cannot be set none dynamic family'
            raise DictConsistencyError(msg, 10, kwargs["xmlfiles"])
        super().__init__(**kwargs)


class InformationParam(Param):
    type: str
    information: str
    variable: Optional[str] = None


class IndexParam(Param):
    type: str

    def __init__(
        self,
        **kwargs,
    ) -> None:

        if not kwargs["is_follower"]:
            msg = f'the variable "{kwargs["path"]}" is not a follower, so cannot have index type for param in "{kwargs["attribute"]}"'
            raise DictConsistencyError(msg, 25, kwargs["xmlfiles"])
        super().__init__(**kwargs)


PARAM_TYPES = {
    "any": AnyParam,
    "variable": VariableParam,
    "identifier": IdentifierParam,
    "information": InformationParam,
    "index": IndexParam,
}


class Calculation(BaseModel):
    path_prefix: Optional[str]
    path: str
    inside_list: bool
    version: str
    ori_path: Optional[str] = None
    default_values: Any = None
    namespace: Optional[str]
    xmlfiles: List[str]

    model_config = ConfigDict(extra="forbid")

    def get_realpath(
        self,
        path: str,
    ) -> str:
        return get_realpath(path, self.path_prefix)

    def get_params(self, objectspace):
        if not self.params:
            return {}
        params = {}
        for param_obj in self.params:
            param = param_obj.model_dump()
            if param.get("type") == "variable":
                if self.ori_path is None:
                    path = self.path
                else:
                    path = self.ori_path
                variable, identifier = objectspace.paths.get_with_dynamic(
                    param["variable"],
                    self.path_prefix,
                    path,
                    self.version,
                    self.namespace,
                    self.xmlfiles,
                )
                if not variable:
                    if not param.get("optional"):
                        msg = f'cannot find variable "{param["variable"]}" defined attribute in "{self.attribute_name}" for "{self.path}"'
                        raise DictConsistencyError(msg, 22, self.xmlfiles)
                    continue
                if not isinstance(variable, objectspace.variable):
                    raise Exception("pfff it's a family")
                param["variable"] = variable
                if identifier:
                    param["identifier"] = identifier
            if param.get("type") == "information":
                if param["variable"]:
                    if self.ori_path is None:
                        path = self.path
                    else:
                        path = self.ori_path
                    variable, identifier = objectspace.paths.get_with_dynamic(
                        param["variable"],
                        self.path_prefix,
                        path,
                        self.version,
                        self.namespace,
                        self.xmlfiles,
                    )
                    if not variable:
                        msg = f'cannot find variable "{param["variable"]}" defined in "{self.attribute_name}" for "{self.path}"'
                        raise DictConsistencyError(msg, 14, self.xmlfiles)
                    param["variable"] = variable
                    if identifier:
                        msg = f'variable "{param["variable"]}" defined in "{self.attribute_name}" for "{self.path}" is a dynamic variable'
                        raise DictConsistencyError(msg, 15, self.xmlfiles)
                else:
                    del param["variable"]
            params[param.pop("key")] = param
        return params


class JinjaCalculation(Calculation):
    attribute_name: Literal[
        "frozen",
        "hidden",
        "mandatory",
        "empty",
        "disabled",
        "default",
        "validators",
        "choices",
        "dynamic",
    ]
    jinja: StrictStr
    params: Optional[List[Param]] = None
    return_type: BASETYPE = None
    description: Optional[StrictStr] = None

    def _jinja_to_function(
        self,
        function,
        return_type,
        multi,
        objectspace,
        *,
        add_help=False,
        params: Optional[dict] = None,
    ):
        variable = objectspace.paths[self.path]
        jinja_path = f"{self.attribute_name}_{self.path}"
        idx = 0
        while jinja_path in objectspace.jinja:
            jinja_path = f"{self.attribute_name}_{self.path}_{idx}"
            idx += 1
        objectspace.jinja[jinja_path] = self.jinja
        default = {
            "function": function,
            "params": {
                "__internal_jinja": jinja_path,
                "__internal_type": return_type,
                "__internal_multi": multi,
                "__internal_files": self.xmlfiles,
                "__internal_attribute": self.attribute_name,
                "__internal_variable": self.path,
            },
        }
        if self.default_values:
            default["params"]["__default_value"] = self.default_values
        if add_help:
            default["help"] = function + "_help"
        if self.params:
            default["params"] |= self.get_params(objectspace)
        if params:
            default["params"] |= params
        if self.ori_path is None:
            path = self.path
        else:
            path = self.ori_path
        for sub_variable, identifier, true_path in get_jinja_variable_to_param(
            path,
            self.jinja,
            objectspace,
            variable.xmlfiles,
            objectspace.functions,
            self.path_prefix,
            self.version,
            self.namespace,
        ):
            if true_path in default["params"]:
                continue
            if isinstance(sub_variable, dict):
                default["params"][true_path] = {
                    "type": "value",
                    "value": sub_variable,
                }
            else:
                default["params"][true_path] = {
                    "type": "variable",
                    "variable": sub_variable,
                }
                if self.version != "1.0":
                    default["params"][true_path]["propertyerror"] = False
                if identifier:
                    default["params"][true_path]["identifier"] = identifier
        return default

    def to_function(
        self,
        objectspace,
    ) -> dict:
        if self.attribute_name == "default":
            if self.return_type:
                raise Exception("return_type not allowed!")
            variable = objectspace.paths[self.path]
            return_type = variable.type
            if self.inside_list:
                multi = False
            elif self.path in objectspace.followers:
                multi = objectspace.multis[self.path] == "submulti"
            else:
                multi = self.path in objectspace.multis
            return self._jinja_to_function(
                "jinja_to_function",
                return_type,
                multi,
                objectspace,
            )
        elif self.attribute_name == "validators":
            if self.return_type:
                raise Exception("pfff")
            return self._jinja_to_function(
                "valid_with_jinja",
                "string",
                False,
                objectspace,
            )
        elif self.attribute_name in PROPERTY_ATTRIBUTE:
            if self.return_type:
                raise Exception("return_type not allowed!")
            return self._jinja_to_function(
                "jinja_to_property",
                "string",
                False,
                objectspace,
                add_help=True,
                params={None: [self.attribute_name], "when": True, "inverse": False},
            )
        elif self.attribute_name == "choices":
            return_type = self.return_type
            if return_type is None:
                return_type = "string"
            return self._jinja_to_function(
                "jinja_to_function",
                return_type,
                not self.inside_list,
                objectspace,
            )
        elif self.attribute_name == "dynamic":
            return self._jinja_to_function(
                "jinja_to_function",
                "string",
                True,
                objectspace,
            )
        raise Exception("hu?")


class _VariableCalculation(Calculation):
    variable: StrictStr
    propertyerror: bool = True
    allow_none: bool = False

    def get_variable(
        self,
        objectspace,
    ) -> "Variable":
        if self.ori_path is None:
            path = self.path
        else:
            path = self.ori_path
        variable, identifier = objectspace.paths.get_with_dynamic(
            self.variable,
            self.path_prefix,
            path,
            self.version,
            self.namespace,
            self.xmlfiles,
        )
        if variable and not isinstance(variable, objectspace.variable):
            # FIXME remove the pfff
            raise Exception("pfff it's a family")
        return variable, identifier

    def get_params(
        self,
        objectspace,
        variable: "Variable",
        identifier: Optional[str],
        *,
        needs_multi: Optional[bool] = None,
    ):
        if not variable:
            msg = f'Variable not found "{self.variable}" for attribut "{self.attribute_name}" for variable "{self.path}"'
            raise DictConsistencyError(msg, 88, self.xmlfiles)
        param = {
            "type": "variable",
            "variable": variable,
            "propertyerror": self.propertyerror,
        }
        if identifier:
            param["identifier"] = identifier
        params = {None: [param]}
        if self.default_values:
            params["__default_value"] = self.default_values
        if self.allow_none:
            params["allow_none"] = True
        if needs_multi is None:
            if self.attribute_name != "default":
                needs_multi = True
            else:
                needs_multi = self.path in objectspace.multis
        calc_variable_is_multi = variable.path in objectspace.multis
        if not calc_variable_is_multi:
            if variable.path in objectspace.paths._dynamics and (
                identifier is None or identifier[-1] is None
            ):
                self_dyn_path = objectspace.paths._dynamics.get(self.path)
                if self_dyn_path is not None:
                    var_dyn_path = objectspace.paths._dynamics[variable.path]
                    if self_dyn_path != var_dyn_path and not self_dyn_path.startswith(
                        f"{var_dyn_path}."
                    ):
                        calc_variable_is_multi = True
                else:
                    calc_variable_is_multi = True
            elif identifier and "{{ identifier }}" in identifier:
                calc_variable_is_multi = True
        if needs_multi:
            if calc_variable_is_multi:
                if self.inside_list:
                    msg = f'the variable "{self.path}" has an invalid attribute "{self.attribute_name}", the variable "{variable.path}" is multi but is inside a list'
                    raise DictConsistencyError(msg, 18, self.xmlfiles)
            elif not self.inside_list:
                msg = f'the variable "{self.path}" has an invalid attribute "{self.attribute_name}", the variable "{variable.path}" is not multi but is not inside a list'
                raise DictConsistencyError(msg, 20, self.xmlfiles)
        elif self.inside_list:
            msg = f'the variable "{self.path}" has an invalid attribute "{self.attribute_name}", it\'s a list'
            raise DictConsistencyError(msg, 23, self.xmlfiles)
        elif calc_variable_is_multi:
            if (
                variable.multi
                or variable.path.rsplit(".", 1)[0] != self.path.rsplit(".", 1)[0]
            ):
                # it's not a follower or not in same leadership
                msg = f'the variable "{self.path}" has an invalid attribute "{self.attribute_name}", the variable "{variable.path}" is a multi'
                raise DictConsistencyError(msg, 21, self.xmlfiles)
            else:
                params[None][0]["index"] = {"index": {"type": "index"}}
        return params


class VariableCalculation(_VariableCalculation):
    attribute_name: Literal["default", "choices", "dynamic"]
    optional: bool = False

    def to_function(
        self,
        objectspace,
    ) -> dict:
        if self.attribute_name != "default" and self.optional:
            msg = f'"{self.attribute_name}" variable shall not have an "optional" attribute for variable "{self.variable}"'
            raise DictConsistencyError(msg, 33, self.xmlfiles)
        variable, identifier = self.get_variable(objectspace)
        if not variable and self.optional:
            raise VariableCalculationDependencyError()
        params = self.get_params(
            objectspace,
            variable,
            identifier,
        )
        return {
            "function": "calc_value",
            "params": params,
        }


class VariablePropertyCalculation(_VariableCalculation):
    attribute_name: Literal[*PROPERTY_ATTRIBUTE]
    when: Any = undefined
    when_not: Any = undefined

    def to_function(
        self,
        objectspace,
    ) -> dict:
        variable, identifier = self.get_variable(objectspace)
        params = self.get_params(
            objectspace,
            variable,
            identifier,
            needs_multi=False,
        )
        variable = params[None][0]["variable"]
        if self.when is not undefined:
            if self.version == "1.0":
                msg = f'when is not allowed in format version 1.0 for attribute "{self.attribute_name}" for variable "{self.path}"'
                raise DictConsistencyError(msg, 103, variable.xmlfiles)
            if self.when_not is not undefined:
                msg = f'the variable "{self.path}" has an invalid attribute "{self.attribute_name}", when and when_not cannot set together'
                raise DictConsistencyError(msg, 31, variable.xmlfiles)
            when = self.when
            inverse = False
        elif self.when_not is not undefined:
            if self.version == "1.0":
                msg = f'when_not is not allowed in format version 1.0 for attribute "{self.attribute_name}" for variable "{self.path}"'
                raise DictConsistencyError(msg, 104, variable.xmlfiles)
            when = self.when_not
            inverse = True
        else:
            if variable.type != "boolean":
                raise Exception("only boolean!")
            when = True
            inverse = False
        params[None].insert(0, self.attribute_name)
        params["when"] = when
        params["inverse"] = inverse
        return {
            "function": "variable_to_property",
            "params": params,
            "help": "variable_to_property",
        }


class InformationCalculation(Calculation):
    attribute_name: Literal["default", "choice", "dynamic"]
    information: StrictStr
    variable: Optional[StrictStr]

    def to_function(
        self,
        objectspace,
    ) -> dict:
        params = {
            None: [
                {
                    "type": "information",
                    "information": self.information,
                }
            ]
        }
        if self.variable:
            if self.ori_path is None:
                path = self.path
            else:
                path = self.ori_path
            variable, identifier = objectspace.paths.get_with_dynamic(
                self.variable,
                self.path_prefix,
                path,
                self.version,
                self.namespace,
                self.xmlfiles,
            )
            if variable is None or identifier is not None:
                raise Exception("pfff")
            params[None][0]["variable"] = variable
        if self.default_values:
            params["__default_value"] = self.default_values
        return {
            "function": "calc_value",
            "params": params,
        }


class _IdentifierCalculation(Calculation):
    identifier: Optional[int] = None

    def get_identifier(self) -> dict:
        identifier = {"type": "identifier"}
        if self.identifier is not None:
            identifier["identifier"] = self.identifier
        return identifier


class IdentifierCalculation(_IdentifierCalculation):
    attribute_name: Literal["default", "choice", "dynamic"]

    def to_function(
        self,
        objectspace,
    ) -> dict:
        identifier = {"type": "identifier"}
        if self.identifier is not None:
            identifier["identifier"] = self.identifier
        return {
            "function": "calc_value",
            "params": {None: [self.get_identifier()]},
        }


class IdentifierPropertyCalculation(_IdentifierCalculation):
    attribute_name: Literal[*PROPERTY_ATTRIBUTE]
    when: Any = undefined
    when_not: Any = undefined

    def to_function(
        self,
        objectspace,
    ) -> dict:
        if self.version == "1.0":
            msg = f'when is not allowed in format version 1.0 for attribute "{self.attribute_name}"'
            raise DictConsistencyError(msg, 105, variable.xmlfiles)
        if self.when is not undefined:
            if self.when_not is not undefined:
                msg = f'the identifier has an invalid attribute "{self.attribute_name}", when and when_not cannot set together'
                raise DictConsistencyError(msg, 35, variable.xmlfiles)
            when = self.when
            inverse = False
        elif self.when_not is not undefined:
            when = self.when_not
            inverse = True
        else:
            msg = f'the identifier has an invalid attribute "{self.attribute_name}", when and when_not cannot set together'
            raise DictConsistencyError
        params = {
            None: [self.attribute_name, self.get_identifier()],
            "when": when,
            "inverse": inverse,
        }
        return {
            "function": "variable_to_property",
            "params": params,
            "help": "variable_to_property",
        }


class IndexCalculation(Calculation):
    attribute_name: Literal["default", "choice", "dynamic"]

    def to_function(
        self,
        objectspace,
    ) -> dict:
        if self.path not in objectspace.followers:
            msg = f'the variable "{self.path}" is not a follower, so cannot have index type for "{self.attribute_name}"'
            raise DictConsistencyError(msg, 60, self.xmlfiles)
        return {
            "function": "calc_value",
            "params": {None: [{"type": "index"}]},
        }


CALCULATION_TYPES = {
    "jinja": JinjaCalculation,
    "variable": VariableCalculation,
    "information": InformationCalculation,
    "identifier": IdentifierCalculation,
    "suffix": IdentifierCalculation,
    "index": IndexCalculation,
}
CALCULATION_PROPERTY_TYPES = {
    "jinja": JinjaCalculation,
    "variable": VariablePropertyCalculation,
    "information": InformationCalculation,
    "identifier": IdentifierPropertyCalculation,
    "index": IndexCalculation,
}
BASETYPE_CALC = Union[StrictBool, StrictInt, StrictFloat, StrictStr, Calculation, None]


class Family(BaseModel):
    name: str
    description: Optional[str] = None
    type: Literal["family", "leadership", "dynamic"] = "family"
    path: str
    help: Optional[str] = None
    mode: Optional[str] = None
    hidden: Union[bool, Calculation] = False
    disabled: Union[bool, Calculation] = False
    namespace: Optional[str]
    version: str
    xmlfiles: List[str] = []

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)


class Dynamic(Family):
    # None only for format 1.0
    variable: str = None
    dynamic: Union[List[Union[StrictStr, Calculation]], Calculation]


class Variable(BaseModel):
    # type will be set dynamically in `annotator/value.py`, default is None
    type: str = None
    name: str
    description: Optional[str] = None
    default: Union[List[BASETYPE_CALC], BASETYPE_CALC] = None
    choices: Optional[Union[List[BASETYPE_CALC], Calculation]] = None
    regexp: Optional[str] = None
    params: Optional[List[Param]] = None
    validators: Optional[List[Calculation]] = None
    multi: Optional[bool] = None
    unique: Optional[bool] = None
    help: Optional[str] = None
    hidden: Union[bool, Calculation] = False
    disabled: Union[bool, Calculation] = False
    mandatory: Union[None, bool, Calculation] = None
    empty: Union[None, bool, Calculation] = True
    auto_save: bool = False
    mode: Optional[str] = None
    test: Optional[list] = None
    examples: Optional[list] = None
    path: str
    namespace: Optional[str]
    version: str
    path_prefix: Optional[str]
    xmlfiles: List[str] = []

    model_config = ConfigDict(extra="forbid", arbitrary_types_allowed=True)


class SymLink(BaseModel):
    type: Literal["symlink"] = "symlink"
    name: str
    path: str
    opt: Variable
    namespace: Optional[str]
    version: str
    path_prefix: Optional[str]
    xmlfiles: List[str] = []

    model_config = ConfigDict(extra="forbid")
