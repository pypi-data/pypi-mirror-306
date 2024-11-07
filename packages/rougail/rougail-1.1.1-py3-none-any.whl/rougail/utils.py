"""Rougail's tools

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

from typing import List, Union
from unicodedata import normalize, combining
import re
from itertools import chain

from importlib.machinery import SourceFileLoader
from importlib.util import spec_from_loader, module_from_spec

from jinja2 import DictLoader, TemplateSyntaxError
from jinja2.sandbox import SandboxedEnvironment
from jinja2.parser import Parser
from jinja2.nodes import Name, Getattr

from tiramisu.config import get_common_path

from .i18n import _
from .error import DictConsistencyError

NAME_REGEXP = re.compile(r"^[a-z0-9_]*$")


def valid_variable_family_name(
    name: str,
    xmlfiles: List[str],
) -> None:
    match = NAME_REGEXP.search(name)
    if not match:
        msg = _(
            'invalid variable or family name "{0}" must only contains lowercase ascii character, number or _'
        ).format(name)
        raise DictConsistencyError(msg, 76, xmlfiles)


def normalize_family(family_name: str) -> str:
    """replace space, accent, uppercase, ... by valid character"""
    if not family_name:
        return
    family_name = family_name.lower()
    family_name = family_name.replace("-", "_").replace(" ", "_").replace(".", "_")
    nfkd_form = normalize("NFKD", family_name)
    family_name = "".join([c for c in nfkd_form if not combining(c)])
    return family_name.lower()


def load_modules(name, module) -> List[str]:
    """list all functions in a module"""
    loader = SourceFileLoader(name, module)
    spec = spec_from_loader(loader.name, loader)
    eosfunc = module_from_spec(spec)
    loader.exec_module(eosfunc)
    return eosfunc


def get_realpath(
    path: str,
    path_prefix: str,
) -> str:
    if path_prefix:
        return f"{path_prefix}.{path}"
    return path


def get_jinja_variable_to_param(
    current_path: str,
    jinja_text,
    objectspace,
    xmlfiles,
    functions,
    path_prefix,
    version,
    namespace,
):
    try:
        env = SandboxedEnvironment(loader=DictLoader({"tmpl": jinja_text}))
        env.filters = functions
        parsed_content = Parser(env, jinja_text, "", "").parse()

        def recurse_getattr(g: Getattr):
            if isinstance(g.node, Getattr):
                return recurse_getattr(g.node) + "." + g.attr
            return g.node.name + "." + g.attr

        variables = set()
        if objectspace.namespace is None:
            for n in parsed_content.find_all(Name):
                variables.add(n.name)
        for g in parsed_content.find_all(Getattr):
            variables.add(recurse_getattr(g))
    except TemplateSyntaxError as err:
        msg = _('error in jinja "{0}" for the variable "{1}": {2}').format(
            jinja_text, current_path, err
        )
        raise DictConsistencyError(msg, 39, xmlfiles) from err
    variables = list(variables)
    variables.sort(reverse=True)
    founded_variables = {}
    unknown_variables = []
    for variable_path in variables:
        variable, identifier = objectspace.paths.get_with_dynamic(
            variable_path,
            path_prefix,
            current_path,
            version,
            namespace,
            xmlfiles,
        )
        if variable and variable.path in objectspace.variables:
            founded_variables[variable_path] = (identifier, variable)
        else:
            sub_family = variable_path + "."
            for founded_variable in chain(founded_variables, unknown_variables):
                if founded_variable.startswith(sub_family):
                    break
            else:
                unknown_variables.append(variable_path)

    for variable_path in unknown_variables:
        for v in founded_variables:
            if get_common_path(v, variable_path) == v:
                break
        else:
            root_path = None
            vpath = variable_path
            while "." in vpath:
                vpath = vpath.rsplit(".", 1)[0]
                variable, identifier = objectspace.paths.get_with_dynamic(
                    vpath,
                    path_prefix,
                    current_path,
                    version,
                    namespace,
                    xmlfiles,
                )
                if variable and variable.path in objectspace.families:
                    root_path = vpath
                    break
            if root_path:
                yield {}, None, root_path
    for variable_path, data in founded_variables.items():
        yield data[1], data[0], variable_path
