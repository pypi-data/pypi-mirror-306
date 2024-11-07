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
dict_env['frozen_1.rougail.family.var1'] = "{% if rougail.condition == \"yes\" %}\ncondition is yes\n{% endif %}\n"
dict_env['hidden_1.rougail.family'] = "{% if rougail.condition == \"yes\" %}\ncondition is yes\n{% endif %}\n"
dict_env['frozen_2.rougail.family.var1'] = "{% if rougail.condition == \"yes\" %}\ncondition is yes\n{% endif %}\n"
dict_env['hidden_2.rougail.family'] = "{% if rougail.condition == \"yes\" %}\ncondition is yes\n{% endif %}\n"
option_3 = StrOption(name="condition", doc="the variable use has condition", default="no", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_5 = StrOption(name="var1", doc="a variable", properties=frozenset({"basic", "force_default_on_freeze", "mandatory", Calculation(func['jinja_to_property'], Params((ParamValue("frozen")), kwargs={'__internal_jinja': ParamValue("frozen_1.rougail.family.var1"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/24_0family_hidden_condition/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("frozen"), '__internal_variable': ParamValue("1.rougail.family.var1"), 'when': ParamValue(True), 'inverse': ParamValue(False), 'rougail.condition': ParamOption(option_3, notraisepropertyerror=True)}), help_function=func['jinja_to_property_help'])}), informations={'type': 'string'})
optiondescription_4 = OptionDescription(name="family", doc="possibly hidden family", children=[option_5], properties=frozenset({"basic", Calculation(func['jinja_to_property'], Params((ParamValue("hidden")), kwargs={'__internal_jinja': ParamValue("hidden_1.rougail.family"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/24_0family_hidden_condition/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("hidden"), '__internal_variable': ParamValue("1.rougail.family"), 'when': ParamValue(True), 'inverse': ParamValue(False), 'rougail.condition': ParamOption(option_3, notraisepropertyerror=True)}), help_function=func['jinja_to_property_help'])}))
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_3, optiondescription_4], properties=frozenset({"basic"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"basic"}))
option_8 = StrOption(name="condition", doc="the variable use has condition", default="no", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_10 = StrOption(name="var1", doc="a variable", properties=frozenset({"basic", "force_default_on_freeze", "mandatory", Calculation(func['jinja_to_property'], Params((ParamValue("frozen")), kwargs={'__internal_jinja': ParamValue("frozen_2.rougail.family.var1"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/24_0family_hidden_condition/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("frozen"), '__internal_variable': ParamValue("2.rougail.family.var1"), 'when': ParamValue(True), 'inverse': ParamValue(False), 'rougail.condition': ParamOption(option_8, notraisepropertyerror=True)}), help_function=func['jinja_to_property_help'])}), informations={'type': 'string'})
optiondescription_9 = OptionDescription(name="family", doc="possibly hidden family", children=[option_10], properties=frozenset({"basic", Calculation(func['jinja_to_property'], Params((ParamValue("hidden")), kwargs={'__internal_jinja': ParamValue("hidden_2.rougail.family"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/24_0family_hidden_condition/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("hidden"), '__internal_variable': ParamValue("2.rougail.family"), 'when': ParamValue(True), 'inverse': ParamValue(False), 'rougail.condition': ParamOption(option_8, notraisepropertyerror=True)}), help_function=func['jinja_to_property_help'])}))
optiondescription_7 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_8, optiondescription_9], properties=frozenset({"basic"}))
optiondescription_6 = OptionDescription(name="2", doc="2", children=[optiondescription_7], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_6])
