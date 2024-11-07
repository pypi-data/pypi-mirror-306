"""
Config file for Rougail

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

from pathlib import Path
from tiramisu import Config
from ruamel.yaml import YAML
from .utils import _, load_modules, normalize_family
from .convert import RougailConvert


RENAMED = {
    "dictionaries_dir": "main_dictionaries",
    "variable_namespace": "main_namespace",
    "functions_file": "functions_files",
}
NOT_IN_TIRAMISU = {
    "custom_types": {},
}
SUBMODULES = None


def get_sub_modules():
    global SUBMODULES
    if SUBMODULES is None:
        SUBMODULES = {}
        for submodule in Path(__file__).parent.iterdir():
            if submodule.name.startswith("_") or not submodule.is_dir():
                continue
            config_file = submodule / "config.py"
            if config_file.is_file():
                SUBMODULES[submodule.name] = load_modules(
                    "rougail." + submodule.name + ".config", str(config_file)
                )
    return SUBMODULES


def get_level(module):
    return module["level"]


class _RougailConfig:
    def __init__(self, backward_compatibility: bool, root, extra_vars: dict):
        self.backward_compatibility = backward_compatibility
        self.root = root
        self.config = Config(
            self.root,
        )
        self.config.property.read_only()
        self.extra_vars = extra_vars
        self.not_in_tiramisu = NOT_IN_TIRAMISU | extra_vars
        for variable, default_value in self.not_in_tiramisu.items():
            if not isinstance(default_value, str):
                default_value = default_value.copy()
            setattr(self, variable, default_value)

    def copy(self):
        rougailconfig = _RougailConfig(
            self.backward_compatibility, self.root, self.extra_vars
        )
        rougailconfig.config.value.importation(self.config.value.exportation())
        rougailconfig.config.property.importation(self.config.property.exportation())
        rougailconfig.config.property.read_only()
        for variable in self.not_in_tiramisu:
            value = getattr(self, variable)
            if not isinstance(value, str):
                value = value.copy()
            setattr(rougailconfig, variable, value)
        return rougailconfig

    def __setitem__(
        self,
        key,
        value,
    ) -> None:
        if key in self.not_in_tiramisu:
            setattr(self, key, value)
        else:
            self.config.property.read_write()
            if key == "export_with_import":
                key = "not_export_with_import"
            key = RENAMED.get(key, key)
            option = self.config.option(key)
            if option.isoptiondescription() and option.isleadership():
                leader = list(value)
                option.leader().value.reset()
                option.leader().value.set(leader)
                follower = option.followers()[0]
                for idx, val in enumerate(value.values()):
                    self.config.option(follower.path(), idx).value.set(val)
            elif key == "not_export_with_import":
                option.value.set(not value)
            else:
                option.value.set(value)
            self.config.property.read_only()

    def __getitem__(
        self,
        key,
    ) -> None:
        if key in self.not_in_tiramisu:
            return getattr(self, key)
        if key == "export_with_import":
            key = "not_export_with_import"
        option = self.config.option(key)
        if option.isoptiondescription() and option.isleadership():
            return self.get_leadership(option)
        ret = self.config.option(key).value.get()
        if key == "not_export_with_import":
            return not ret
        return ret

    def get_leadership(self, option) -> dict:
        leader = None
        followers = []
        for opt, value in option.value.get().items():
            if opt.issymlinkoption():
                continue
            if leader is None:
                leader = value
            else:
                followers.append(value)
        return dict(zip(leader, followers))

    def parse(self, config) -> str:
        for option in config:
            if option.isoptiondescription():
                yield from self.parse(option)
            elif not option.issymlinkoption():
                yield f"{option.path()}: {option.value.get()}"

    def __repr__(self):
        self.config.property.read_write()
        try:
            values = "\n".join(self.parse(self.config))
        except Exception as err:
            values = str(err)
        self.config.property.read_only()
        return values


class FakeRougailConvert(RougailConvert):
    def __init__(
        self,
        add_extra_options: bool,
    ) -> None:
        self.add_extra_options = add_extra_options
        super().__init__({})

    def load_config(self) -> None:
        self.sort_dictionaries_all = False
        self.main_namespace = None
        self.suffix = ""
        self.custom_types = {}
        self.functions_files = []
        self.modes_level = []
        self.extra_annotators = []
        self.base_option_name = "baseoption"
        self.export_with_import = True
        self.internal_functions = []
        self.plugins = ["structural_commandline"]
        self.add_extra_options = self.add_extra_options


def get_rougail_config(
    *,
    backward_compatibility: bool = True,
    add_extra_options: bool = True,
) -> _RougailConfig:
    if backward_compatibility:
        main_namespace_default = "rougail"
    else:
        main_namespace_default = "null"
    rougail_options = f"""default_dictionary_format_version:
  description: Dictionary format version by default, if not specified in dictionary file
  alternative_name: v
  choices:
    - '1.0'
    - '1.1'
  mandatory: false

main_dictionaries:
  description: 'Directories where dictionary files are placed'
  type: unix_filename
  alternative_name: m
  params:
     allow_relative: True
     test_existence: True
     types:
       - directory
  multi: true

sort_dictionaries_all:
  description: Sort dictionaries from differents directories
  negative_description: Sort dictionaries directory by directory
  default: false

main_namespace:
  description: Main namespace name
  default: {main_namespace_default}
  alternative_name: s
  mandatory: false

extra_dictionaries:
  description: Extra namespaces
  type: leadership
  disabled:
    variable: main_namespace
    when: null

  names:
    description: 'Extra namespace name'
    alternative_name: xn
    multi: true
    mandatory: false

  directories:
    description: Directories where extra dictionary files are placed
    alternative_name: xd
    type: unix_filename
    params:
      allow_relative: true
      test_existence: true
      types:
        - directory
    multi: true

upgrade:
  description: Update dictionaries to newest Rougail format version
  negative_description: Do not update dictionaries to newest Rougail format version
  default: false

upgrade_options:
  description: Update informations
  disabled:
    variable: upgrade
    when: false

  main_dictionaries:
    description: 'Directories where dictionary files will be placed'
    default:
      variable: __.main_dictionaries

  extra_dictionary:
    description: 'Directories where extra files will be placed'
    type: unix_filename
    params:
      allow_relative: true
      test_existence: true
      types:
        - directory
    disabled:
      variable: __.main_namespace
      when: null

functions_files:
  description: File with functions
  alternative_name: c
  type: unix_filename
  params:
    allow_relative: true
    test_existence: true
    types:
      - file
  multi: true
  mandatory: false

modes_level:
  description: All modes level available
  multi: true
  mandatory: false
"""
    if backward_compatibility:
        rougail_options += """
  default:
    - basic
    - standard
    - advanced
"""
    rougail_options += """
default_family_mode:
  description: Default mode for a family
  default:
    jinja: |
      {% if modes_level %}
      {{ modes_level[0] }}
      {% endif %}
  disabled:
    jinja: |
      {% if not modes_level %}
      No mode
      {% endif %}
  validators:
    - type: jinja
      jinja: |
        {% if default_family_mode not in modes_level %}
        not in modes_level ({modes_level})
        {% endif %}
  commandline: false

default_variable_mode:
  description: Default mode for a variable
  default:
    jinja: |
      {% if modes_level %}
        {% if modes_level | length == 1 %}
      {{ modes_level[0] }}
        {% else %}
      {{ modes_level[1] }}
        {% endif %}
      {% endif %}
  disabled:
    jinja: |
      {% if not modes_level %}
      No mode
      {% endif %}
  validators:
    - type: jinja
      jinja: |
        {% if default_variable_mode not in modes_level %}
        not in modes_level ({modes_level})
        {% endif %}
  commandline: false

base_option_name:
  description: Option name for the base option
  default: baseoption
  commandline: false

not_export_with_import:
  description: In cache file, do not importation of Tiramisu and other dependencies
  default: false
  commandline: false

tiramisu_cache:
  description: Tiramisu cache filename
  alternative_name: t
  type: unix_filename
  mandatory: false
  params:
    allow_relative: true

internal_functions:
  description: Name of internal functions that we can use as a function
  multi: true
  mandatory: false
  commandline: false

extra_annotators:
  description: Name of extra annotators
  multi: true
  mandatory: false
  commandline: false

plugins:
  description: Name of Rougail plugins
  multi: true
  mandatory: false
  commandline: false

suffix:
  description: Suffix add to generated option name
  default: ''
  mandatory: false
  commandline: false
"""
    processes = {
        "structural": [],
        "output": [],
        "user data": [],
    }
    for module in get_sub_modules().values():
        data = module.get_rougail_config()
        processes[data["process"]].append(data)
    # reorder
    for process in processes:
        processes[process] = list(sorted(processes[process], key=get_level))
    rougail_process = """step:  # Load and exporter steps
  disabled:
    variable: upgrade"""
    for process in processes:
        if processes[process]:
            objects = processes[process]
            rougail_process += """
  {NAME}:
    description: Select for {NAME}
    alternative_name: {NAME[0]}
    choices:
""".format(
                NAME=normalize_family(process),
            )
            for obj in objects:
                rougail_process += f"      - {obj['name']}\n"
            if process == "structural":
                rougail_process += "    commandline: false"
            elif process == "user data":
                rougail_process += """    multi: true
    mandatory: false
"""
                hidden_outputs = [
                    process["name"]
                    for process in processes["output"]
                    if not process.get("allow_user_data", True)
                ]
                if hidden_outputs:
                    rougail_process += """    hidden:
      type: jinja
      jinja: |
"""
                    for hidden_output in hidden_outputs:
                        rougail_process += """        {% if _.output == 'NAME' %}
        Cannot load user data for NAME output
        {% endif %}
""".replace(
                            "NAME", hidden_output
                        )
            elif objects:
                rougail_process += "    default: {DEFAULT}".format(
                    DEFAULT=objects[0]["name"]
                )
        else:
            if process == 'output':
                prop = 'hidden'
            else:
                prop = 'disabled'
            rougail_process += """
  {NAME}:
    description: Select for {NAME}
    mandatory: false
    {PROP}: true
    multi: true
    default: ["You haven't installed \\\"{NAME}\\\" package for rougail"]
    validators:
      - jinja: Please install a rougail-{NAME}-* package.
""".format(
                NAME=normalize_family(process),
                PROP=prop,
            )
    rougail_options += rougail_process
    convert = FakeRougailConvert(add_extra_options)
    convert._init()
    convert.namespace = None
    convert.parse_root_file(
        "rougail.config",
        "",
        "1.1",
        YAML().load(rougail_options),
    )
    extra_vars = {}
    for process in processes:
        for obj in processes[process]:
            if "extra_vars" in obj:
                extra_vars |= obj["extra_vars"]
            if not "options" in obj:
                continue
            convert.parse_root_file(
                f'rougail.config.{obj["name"]}',
                "",
                "1.1",
                YAML().load(obj["options"]),
            )

    tiram_obj = convert.save(None)
    optiondescription = {}
    exec(tiram_obj, {}, optiondescription)  # pylint: disable=W0122
    return _RougailConfig(
        backward_compatibility,
        optiondescription["option_0"],
        extra_vars=extra_vars,
    )


RougailConfig = get_rougail_config()
