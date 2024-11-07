"""Annotate value

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

from rougail.annotator.variable import Walk

from rougail.i18n import _
from rougail.error import DictConsistencyError
from rougail.object_model import Calculation


class Annotator(Walk):  # pylint: disable=R0903
    """Annotate value"""

    level = 70

    def __init__(
        self,
        objectspace,
        *args,
    ) -> None:
        if not objectspace.paths:
            return
        self.objectspace = objectspace
        self.convert_value()
        self.valid_choices()

    def convert_value(self) -> None:
        """convert value"""
        for variable in self.get_variables():
            if variable.type == "symlink":
                continue
            if variable.version != "1.0" and variable.type == "port":
                self._convert_port(variable)
            self._convert_value(variable)

    def _convert_value(
        self,
        variable: dict,
    ) -> None:
        multi = self.objectspace.multis.get(variable.path, False)
        # a boolean must have value, the default value is "True"
        if variable.type == "boolean" and multi is False and variable.default is None:
            variable.default = True

        if variable.default is None or isinstance(variable.default, Calculation):
            return

        if isinstance(variable.default, list):
            if not multi:
                msg = f'The variable "{variable.path}" with a list as default value must have "multi" attribute'
                raise DictConsistencyError(msg, 68, variable.xmlfiles)
            if variable.path in self.objectspace.followers and multi != "submulti":
                msg = _(
                    'the follower "{0}" without multi attribute can only have one value'
                ).format(variable.name)
                raise DictConsistencyError(msg, 87, variable.xmlfiles)
            if not variable.default:
                variable.default = None
            else:
                if variable.path not in self.objectspace.leaders:
                    if multi == "submulti":
                        self.objectspace.default_multi[variable.path] = variable.default
                        variable.default = None
                    else:
                        self.objectspace.default_multi[variable.path] = (
                            variable.default[0]
                        )
        elif variable.multi:
            msg = _(
                'the variable "{0}" is multi but has a non list default value'
            ).format(variable.name)
            raise DictConsistencyError(msg, 12, variable.xmlfiles)
        elif variable.path in self.objectspace.followers:
            self.objectspace.default_multi[variable.path] = variable.default
            variable.default = None

    def _convert_port(self, variable) -> None:
        if variable.multi is False and isinstance(variable.default, int):
            variable.default = str(variable.default)
        elif variable.multi is True and isinstance(variable.default, list):
            for idx, value in enumerate(variable.default):
                if isinstance(value, int):
                    variable.default[idx] = str(value)

    def valid_choices(self) -> None:
        """A variable with type "Choice" that is not mandatory must has "nil" value"""
        for variable in self.get_variables():
            if variable.type != "choice":
                continue
            if isinstance(variable.choices, Calculation):
                continue
            if variable.choices is None:
                msg = f'the variable "{variable.path}" is a "choice" variable but don\'t have any choice'
                raise DictConsistencyError(msg, 19, variable.xmlfiles)
            if not variable.mandatory and not variable.multi:
                self.add_choice_nil(variable)

    def add_choice_nil(self, variable) -> None:
        """A variable with type "Choice" that is not mandatory must has "nil" value"""
        for choice in variable.choices:
            if choice is None:
                return
        variable.choices.append(None)
