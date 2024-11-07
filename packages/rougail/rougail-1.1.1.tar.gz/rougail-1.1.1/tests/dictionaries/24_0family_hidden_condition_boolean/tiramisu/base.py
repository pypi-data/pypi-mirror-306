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
dict_env['frozen_rougail.family.variable'] = "{% if not rougail.condition %}\ncondition is false\n{% endif %}\n"
dict_env['hidden_rougail.family'] = "{% if not rougail.condition %}\ncondition is false\n{% endif %}\n"
option_2 = BoolOption(name="condition", doc="a conditional variable", default=False, properties=frozenset({"mandatory", "standard"}), informations={'type': 'boolean'})
option_4 = StrOption(name="variable", doc="a variable", properties=frozenset({"force_default_on_freeze", "standard", Calculation(func['jinja_to_property'], Params((ParamValue("frozen")), kwargs={'__internal_jinja': ParamValue("frozen_rougail.family.variable"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/24_0family_hidden_condition_boolean/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("frozen"), '__internal_variable': ParamValue("rougail.family.variable"), 'when': ParamValue(True), 'inverse': ParamValue(False), 'rougail.condition': ParamOption(option_2, notraisepropertyerror=True)}), help_function=func['jinja_to_property_help'])}), informations={'type': 'string'})
optiondescription_3 = OptionDescription(name="family", doc="a family", children=[option_4], properties=frozenset({"standard", Calculation(func['jinja_to_property'], Params((ParamValue("hidden")), kwargs={'__internal_jinja': ParamValue("hidden_rougail.family"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/24_0family_hidden_condition_boolean/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("hidden"), '__internal_variable': ParamValue("rougail.family"), 'when': ParamValue(True), 'inverse': ParamValue(False), 'rougail.condition': ParamOption(option_2, notraisepropertyerror=True)}), help_function=func['jinja_to_property_help'])}))
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_2, optiondescription_3], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
