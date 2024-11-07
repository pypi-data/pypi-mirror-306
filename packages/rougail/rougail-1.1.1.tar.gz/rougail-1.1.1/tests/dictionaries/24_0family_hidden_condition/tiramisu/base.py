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
dict_env['frozen_rougail.family.var1'] = "{% if rougail.condition == \"yes\" %}\ncondition is yes\n{% endif %}\n"
dict_env['hidden_rougail.family'] = "{% if rougail.condition == \"yes\" %}\ncondition is yes\n{% endif %}\n"
option_2 = StrOption(name="condition", doc="the variable use has condition", default="no", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_4 = StrOption(name="var1", doc="a variable", properties=frozenset({"basic", "force_default_on_freeze", "mandatory", Calculation(func['jinja_to_property'], Params((ParamValue("frozen")), kwargs={'__internal_jinja': ParamValue("frozen_rougail.family.var1"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/24_0family_hidden_condition/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("frozen"), '__internal_variable': ParamValue("rougail.family.var1"), 'when': ParamValue(True), 'inverse': ParamValue(False), 'rougail.condition': ParamOption(option_2, notraisepropertyerror=True)}), help_function=func['jinja_to_property_help'])}), informations={'type': 'string'})
optiondescription_3 = OptionDescription(name="family", doc="possibly hidden family", children=[option_4], properties=frozenset({"basic", Calculation(func['jinja_to_property'], Params((ParamValue("hidden")), kwargs={'__internal_jinja': ParamValue("hidden_rougail.family"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/24_0family_hidden_condition/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("hidden"), '__internal_variable': ParamValue("rougail.family"), 'when': ParamValue(True), 'inverse': ParamValue(False), 'rougail.condition': ParamOption(option_2, notraisepropertyerror=True)}), help_function=func['jinja_to_property_help'])}))
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_2, optiondescription_3], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
