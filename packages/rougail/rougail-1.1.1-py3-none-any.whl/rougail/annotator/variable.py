"""Annotate variable

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

from rougail.i18n import _
from rougail.error import DictConsistencyError
from rougail.object_model import Calculation, VariableCalculation
from tiramisu.error import display_list


class Walk:
    """Walk to objectspace to find variable or family"""

    objectspace = None

    def get_variables(self):
        """Iter all variables from the objectspace"""
        for path in self.objectspace.variables:
            yield self.objectspace.paths[path]

    #        yield from get_variables(self.objectspace)

    def get_families(self):
        """Iter all families from the objectspace"""
        for path in self.objectspace.families:
            yield self.objectspace.paths[path]


class Annotator(Walk):  # pylint: disable=R0903
    """Annotate variable"""

    level = 30

    def __init__(
        self,
        objectspace,
        *args,
    ):
        if not objectspace.paths:
            return
        self.objectspace = objectspace
        if self.objectspace.main_namespace:
            self.forbidden_name = [self.objectspace.main_namespace]
            for extra in self.objectspace.extra_dictionaries:
                self.forbidden_name.append(extra)
        else:
            self.forbidden_name = []
        # default type inference from a default value with :term:`basic types`
        self.basic_types = {
            str: "string",
            int: "number",
            bool: "boolean",
            float: "float",
        }
        self.verify_choices()
        self.convert_variable()
        self.convert_test()
        self.convert_examples()
        self.convert_help()

    def convert_variable(self):
        """convert variable"""
        for variable in self.get_variables():
            if variable.version != "1.0":
                if variable.type == "symlink":
                    continue
                self._convert_variable_inference(variable)
        for variable in self.get_variables():
            if variable.type == "symlink":
                continue
            if variable.version != "1.0":
                self._default_variable_copy_informations(variable)
            if variable.multi is None:
                variable.multi = False
            if variable.type is None:
                variable.type = "string"
            self.objectspace.informations.add(variable.path, "type", variable.type)
            self._convert_variable(variable)

    def _convert_variable_inference(
        self,
        variable,
    ) -> None:
        # variable has no type
        if variable.type is None:
            # choice type inference from the `choices` attribute
            if variable.choices is not None:
                variable.type = "choice"
            elif variable.regexp is not None:
                variable.type = "regexp"
            elif variable.default not in [None, []]:
                if isinstance(variable.default, list):
                    tested_value = variable.default[0]
                else:
                    tested_value = variable.default
                variable.type = self.basic_types.get(type(tested_value), None)
        # variable has no multi attribute
        if variable.multi is None and not (
            variable.type is None and isinstance(variable.default, VariableCalculation)
        ):
            if variable.path in self.objectspace.leaders:
                variable.multi = True
            else:
                variable.multi = isinstance(variable.default, list)

    def _default_variable_copy_informations(
        self,
        variable,
    ) -> None:
        # if a variable has a variable as default value, that means the type/params or multi should has same value
        if variable.type is not None or not isinstance(
            variable.default, VariableCalculation
        ):
            return
        # copy type and params
        calculated_variable_path = variable.default.variable
        calculated_variable, identifier = self.objectspace.paths.get_with_dynamic(
            calculated_variable_path,
            variable.default.path_prefix,
            variable.path,
            variable.version,
            variable.namespace,
            variable.xmlfiles,
        )
        if calculated_variable is None:
            return
        variable.type = calculated_variable.type
        if variable.params is None and calculated_variable.params is not None:
            variable.params = calculated_variable.params
        # copy multi attribut
        if variable.multi is None:
            calculated_path = calculated_variable.path
            if (
                calculated_path in self.objectspace.leaders
                and variable.path in self.objectspace.followers
                and calculated_path.rsplit(".")[0] == variable.path.rsplit(".")[0]
            ):
                variable.multi = False
            else:
                variable.multi = calculated_variable.multi

    def _convert_variable(
        self,
        variable: dict,
    ) -> None:
        # variable without description: description is the name
        if not variable.description:
            variable.description = variable.name
        if variable.path in self.objectspace.followers:
            if not variable.multi:
                self.objectspace.multis[variable.path] = True
            else:
                self.objectspace.multis[variable.path] = "submulti"
        elif variable.multi:
            self.objectspace.multis[variable.path] = True
        if variable.path in self.objectspace.leaders:
            if not self.objectspace.multis.get(variable.path, False):
                variable.multi = self.objectspace.multis[variable.path] = True
            family = self.objectspace.paths[variable.path.rsplit(".", 1)[0]]
            if variable.hidden:
                family.hidden = variable.hidden
            #            elif family.hidden:
            #                variable.hidden = family.hidden
            variable.hidden = None
        if variable.regexp is not None and variable.type != "regexp":
            msg = _(
                'the variable "{0}" has regexp attribut but has not the "regexp" type'
            ).format(variable.path)
            raise DictConsistencyError(msg, 37, variable.xmlfiles)
        if variable.mandatory is None:
            variable.mandatory = True

    def convert_test(self):
        """Convert variable tests value"""
        for variable in self.get_variables():
            if variable.type == "symlink":
                continue
            if variable.test is None:
                continue
            self.objectspace.informations.add(
                variable.path, "test", tuple(variable.test)
            )

    def convert_examples(self):
        """Convert variable tests value"""
        for variable in self.get_variables():
            if variable.type == "symlink":
                continue
            if variable.examples is None:
                continue
            self.objectspace.informations.add(
                variable.path, "examples", tuple(variable.examples)
            )

    def convert_help(self):
        """Convert variable help"""
        for variable in self.get_variables():
            if not hasattr(variable, "help") or not variable.help:
                continue
            self.objectspace.informations.add(variable.path, "help", variable.help)
            del variable.help

    def verify_choices(self):
        for variable in self.get_variables():
            if variable.type is None and variable.choices:
                # choice type inference from the `choices` attribute
                variable.type = "choice"
            if variable.choices is not None and variable.type != "choice":
                msg = _(
                    'the variable "{0}" has choices attribut but has not the "choice" type'
                ).format(variable.path)
                raise DictConsistencyError(msg, 11, variable.xmlfiles)
            if variable.type != "choice":
                continue
            if variable.default is None:
                continue
            if None in variable.choices and variable.mandatory is None:
                variable.mandatory = False
            if not isinstance(variable.choices, list):
                continue
            choices = variable.choices
            has_calculation = False
            for choice in choices:
                if isinstance(choice, Calculation):
                    has_calculation = True
                    break
            if has_calculation:
                continue

            default = variable.default
            if not isinstance(default, list):
                default = [default]
            for value in default:
                if isinstance(value, Calculation):
                    continue
                if value not in choices:
                    msg = _(
                        'the variable "{0}" has an unvalid default value "{1}" should be in {2}'
                    ).format(
                        variable.path,
                        value,
                        display_list(choices, separator="or", add_quote=True),
                    )
                    raise DictConsistencyError(msg, 26, variable.xmlfiles)
