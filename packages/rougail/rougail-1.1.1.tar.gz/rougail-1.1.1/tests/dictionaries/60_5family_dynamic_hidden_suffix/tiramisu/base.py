from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
try:
    groups.namespace
except:
    groups.addgroup('namespace')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
dict_env['frozen_rougail.dyn{{ identifier }}.var'] = "{% if suffix == 'val2' %}\ndisabled\n{% endif %}\n"
dict_env['frozen_rougail.dyn{{ identifier }}.family.var'] = "{% if suffix == 'val2' %}\ndisabled\n{% endif %}\n"
dict_env['hidden_rougail.dyn{{ identifier }}'] = "{% if suffix == 'val2' %}\ndisabled\n{% endif %}\n"
option_3 = StrOption(name="var", doc="a variable", properties=frozenset({"force_default_on_freeze", "standard", Calculation(func['jinja_to_property'], Params((ParamValue("frozen")), kwargs={'__internal_jinja': ParamValue("frozen_rougail.dyn{{ identifier }}.var"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/60_5family_dynamic_hidden_suffix/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("frozen"), '__internal_variable': ParamValue("rougail.dyn{{ identifier }}.var"), 'suffix': ParamIdentifier(), 'when': ParamValue(True), 'inverse': ParamValue(False)}), help_function=func['jinja_to_property_help'])}), informations={'type': 'string'})
option_5 = StrOption(name="var", doc="a new variable", properties=frozenset({"force_default_on_freeze", "standard", Calculation(func['jinja_to_property'], Params((ParamValue("frozen")), kwargs={'__internal_jinja': ParamValue("frozen_rougail.dyn{{ identifier }}.family.var"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/60_5family_dynamic_hidden_suffix/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("frozen"), '__internal_variable': ParamValue("rougail.dyn{{ identifier }}.family.var"), 'suffix': ParamIdentifier(), 'when': ParamValue(True), 'inverse': ParamValue(False)}), help_function=func['jinja_to_property_help'])}), informations={'type': 'string'})
optiondescription_4 = OptionDescription(name="family", doc="a family", children=[option_5], properties=frozenset({"standard"}))
optiondescription_2 = ConvertDynOptionDescription(name="dyn{{ identifier }}", doc="a dynamic family", identifiers=["val1", "val2"], children=[option_3, optiondescription_4], properties=frozenset({"standard", Calculation(func['jinja_to_property'], Params((ParamValue("hidden")), kwargs={'__internal_jinja': ParamValue("hidden_rougail.dyn{{ identifier }}"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/60_5family_dynamic_hidden_suffix/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("hidden"), '__internal_variable': ParamValue("rougail.dyn{{ identifier }}"), 'suffix': ParamIdentifier(), 'when': ParamValue(True), 'inverse': ParamValue(False)}), help_function=func['jinja_to_property_help'])}))
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_2], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
