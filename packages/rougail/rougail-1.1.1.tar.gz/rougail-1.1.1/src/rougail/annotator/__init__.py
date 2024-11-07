"""Annotate dictionaries

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

import importlib.resources
from os.path import isfile
from ..utils import load_modules


ANNOTATORS = None


def get_level(module):
    return module.level


def get_annotators(annotators, module_name, file_name=None):
    if file_name is None:
        _module_name = module_name
    else:
        _module_name = module_name + "." + file_name
        full_file_name = f"/{file_name}.py"
    annotators[_module_name] = []
    for pathobj in importlib.resources.files(module_name).iterdir():
        path = str(pathobj)
        if not path.endswith(".py") or path.endswith("__.py"):
            continue
        if file_name is not None and not path.endswith(full_file_name):
            continue
        module = load_modules(module_name, path)
        if "Annotator" not in dir(module):
            continue
        annotators[_module_name].append(module.Annotator)


class SpaceAnnotator:  # pylint: disable=R0903
    """Transformations applied on a object instance"""

    def __init__(
        self,
        objectspace,
    ):
        global ANNOTATORS
        if ANNOTATORS is None:
            ANNOTATORS = {}
            get_annotators(ANNOTATORS, "rougail.annotator")
        for extra_annotator in objectspace.extra_annotators:
            if extra_annotator in ANNOTATORS:
                continue
            get_annotators(ANNOTATORS, extra_annotator)
        for plugin in objectspace.plugins:
            try:
                get_annotators(ANNOTATORS, f"rougail.{plugin}", "annotator")
            except ModuleNotFoundError:
                pass
        annotators = ANNOTATORS["rougail.annotator"].copy()
        for extra_annotator in objectspace.extra_annotators:
            annotators.extend(ANNOTATORS[extra_annotator])
        for plugin in objectspace.plugins:
            annotators.extend(ANNOTATORS[f"rougail.{plugin}.annotator"])
        annotators = sorted(annotators, key=get_level)
        functions = {}
        functions_files = objectspace.functions_files
        for functions_file in functions_files:
            if isfile(functions_file):
                loaded_modules = load_modules("function_file", functions_file)
                for function in dir(loaded_modules):
                    if function.startswith("_"):
                        continue
                    functions[function] = getattr(loaded_modules, function)
        objectspace.functions = functions
        for annotator in annotators:
            annotator(objectspace)


__all__ = ("SpaceAnnotator",)
