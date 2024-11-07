"""Annotate to add specify attribute for tiramisu-cmdline

Silique (https://www.silique.fr)
Copyright (C) 2024

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
from rougail.utils import _
from rougail.error import DictConsistencyError


class Annotator(Walk):
    """Annotate value"""

    level = 80

    def __init__(self, objectspace, *args) -> None:
        if not objectspace.paths:
            return
        self.alternative_names = {}
        self.objectspace = objectspace
        not_for_commandlines = []
        for family in self.get_families():
            if family.commandline:
                continue
            self.not_for_commandline(family)
            not_for_commandlines.append(family.path + ".")
        for variable in self.get_variables():
            if variable.type == "symlink":
                continue
            variable_path = variable.path
            for family_path in not_for_commandlines:
                if variable_path.startswith(family_path):
                    break
            else:
                if not variable.commandline:
                    self.not_for_commandline(variable)
                else:
                    self.manage_alternative_name(variable)
                    self.manage_negative_description(variable)

    def not_for_commandline(self, variable) -> None:
        self.objectspace.properties.add(variable.path, "not_for_commandline", True)

    def manage_alternative_name(self, variable) -> None:
        if not variable.alternative_name:
            return
        alternative_name = variable.alternative_name
        variable_path = variable.path
        all_letters = ""
        for letter in alternative_name:
            all_letters += letter
            if all_letters == "h":
                msg = _('alternative_name "{0}" conflict with "--help"').format(
                    alternative_name
                )
                raise DictConsistencyError(msg, 202, variable.xmlfiles)
            if all_letters in self.alternative_names:
                msg = _('conflict alternative_name "{0}": "{1}" and "{2}"').format(
                    alternative_name, variable_path, self.alternative_names[all_letters]
                )
                raise DictConsistencyError(msg, 202, variable.xmlfiles)

        self.alternative_names[alternative_name] = variable_path
        if "." not in variable_path:
            path = alternative_name
        else:
            path = variable_path.rsplit(".", 1)[0] + "." + alternative_name
        self.objectspace.add_variable(
            alternative_name,
            {"type": "symlink", "path": path, "opt": variable},
            variable.xmlfiles,
            False,
            False,
            variable.version,
        )

    def manage_negative_description(self, variable) -> None:
        if not variable.negative_description:
            if variable.type == "boolean" and not self.objectspace.add_extra_options:
                raise DictConsistencyError(
                    _(
                        'negative_description is mandatory for boolean variable, but "{0}" hasn\'t'
                    ).format(variable.path),
                    200,
                    variable.xmlfiles,
                )
            return
        if variable.type != "boolean":
            raise DictConsistencyError(
                _(
                    'negative_description is only available for boolean variable, but "{0}" is "{1}"'
                ).format(variable.path, variable.type),
                201,
                variable.xmlfiles,
            )
        self.objectspace.informations.add(
            variable.path, "negative_description", variable.negative_description
        )
