from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
dict_env['frozen_dyn{{ identifier }}.var'] = "{% if suffix == 'val2' %}\ndisabled\n{% endif %}\n"
dict_env['frozen_dyn{{ identifier }}.family.var'] = "{% if suffix == 'val2' %}\ndisabled\n{% endif %}\n"
dict_env['hidden_dyn{{ identifier }}'] = "{% if suffix == 'val2' %}\ndisabled\n{% endif %}\n"
option_2 = StrOption(name="var", doc="a variable", properties=frozenset({"force_default_on_freeze", "standard", Calculation(func['jinja_to_property'], Params((ParamValue("frozen")), kwargs={'__internal_jinja': ParamValue("frozen_dyn{{ identifier }}.var"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/60_5family_dynamic_hidden_suffix/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("frozen"), '__internal_variable': ParamValue("dyn{{ identifier }}.var"), 'suffix': ParamIdentifier(), 'when': ParamValue(True), 'inverse': ParamValue(False)}), help_function=func['jinja_to_property_help'])}), informations={'type': 'string'})
option_4 = StrOption(name="var", doc="a new variable", properties=frozenset({"force_default_on_freeze", "standard", Calculation(func['jinja_to_property'], Params((ParamValue("frozen")), kwargs={'__internal_jinja': ParamValue("frozen_dyn{{ identifier }}.family.var"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/60_5family_dynamic_hidden_suffix/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("frozen"), '__internal_variable': ParamValue("dyn{{ identifier }}.family.var"), 'suffix': ParamIdentifier(), 'when': ParamValue(True), 'inverse': ParamValue(False)}), help_function=func['jinja_to_property_help'])}), informations={'type': 'string'})
optiondescription_3 = OptionDescription(name="family", doc="a family", children=[option_4], properties=frozenset({"standard"}))
optiondescription_1 = ConvertDynOptionDescription(name="dyn{{ identifier }}", doc="a dynamic family", identifiers=["val1", "val2"], children=[option_2, optiondescription_3], properties=frozenset({"standard", Calculation(func['jinja_to_property'], Params((ParamValue("hidden")), kwargs={'__internal_jinja': ParamValue("hidden_dyn{{ identifier }}"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/60_5family_dynamic_hidden_suffix/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("hidden"), '__internal_variable': ParamValue("dyn{{ identifier }}"), 'suffix': ParamIdentifier(), 'when': ParamValue(True), 'inverse': ParamValue(False)}), help_function=func['jinja_to_property_help'])}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
