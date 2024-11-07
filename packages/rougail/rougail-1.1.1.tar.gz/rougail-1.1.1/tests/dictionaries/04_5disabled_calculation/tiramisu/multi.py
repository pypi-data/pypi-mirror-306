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
dict_env['disabled_1.rougail.variable1'] = "{% if _.condition == \"yes\" %}\ncondition is yes\n{% endif %}\n"
dict_env['disabled_1.rougail.variable2'] = "{% if _.condition == \"yes\" %}\ncondition is yes\n{% endif %}\n"
dict_env['disabled_2.rougail.variable1'] = "{% if _.condition == \"yes\" %}\ncondition is yes\n{% endif %}\n"
dict_env['disabled_2.rougail.variable2'] = "{% if _.condition == \"yes\" %}\ncondition is yes\n{% endif %}\n"
option_3 = StrOption(name="condition", doc="a conditional variable", default="no", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_4 = StrOption(name="variable1", doc="a first variable", properties=frozenset({"basic", "mandatory", Calculation(func['jinja_to_property'], Params((ParamValue("disabled")), kwargs={'__internal_jinja': ParamValue("disabled_1.rougail.variable1"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/04_5disabled_calculation/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("disabled"), '__internal_variable': ParamValue("1.rougail.variable1"), 'when': ParamValue(True), 'inverse': ParamValue(False), '_.condition': ParamOption(option_3, notraisepropertyerror=True)}), help_function=func['jinja_to_property_help'])}), informations={'type': 'string'})
option_5 = StrOption(name="variable2", doc="a second variable", properties=frozenset({"basic", "mandatory", Calculation(func['jinja_to_property'], Params((ParamValue("disabled")), kwargs={'__internal_jinja': ParamValue("disabled_1.rougail.variable2"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/04_5disabled_calculation/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("disabled"), '__internal_variable': ParamValue("1.rougail.variable2"), 'when': ParamValue(True), 'inverse': ParamValue(False), '_.condition': ParamOption(option_3, notraisepropertyerror=True)}), help_function=func['jinja_to_property_help'])}), informations={'type': 'string'})
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_3, option_4, option_5], properties=frozenset({"basic"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"basic"}))
option_8 = StrOption(name="condition", doc="a conditional variable", default="no", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_9 = StrOption(name="variable1", doc="a first variable", properties=frozenset({"basic", "mandatory", Calculation(func['jinja_to_property'], Params((ParamValue("disabled")), kwargs={'__internal_jinja': ParamValue("disabled_2.rougail.variable1"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/04_5disabled_calculation/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("disabled"), '__internal_variable': ParamValue("2.rougail.variable1"), 'when': ParamValue(True), 'inverse': ParamValue(False), '_.condition': ParamOption(option_8, notraisepropertyerror=True)}), help_function=func['jinja_to_property_help'])}), informations={'type': 'string'})
option_10 = StrOption(name="variable2", doc="a second variable", properties=frozenset({"basic", "mandatory", Calculation(func['jinja_to_property'], Params((ParamValue("disabled")), kwargs={'__internal_jinja': ParamValue("disabled_2.rougail.variable2"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/04_5disabled_calculation/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("disabled"), '__internal_variable': ParamValue("2.rougail.variable2"), 'when': ParamValue(True), 'inverse': ParamValue(False), '_.condition': ParamOption(option_8, notraisepropertyerror=True)}), help_function=func['jinja_to_property_help'])}), informations={'type': 'string'})
optiondescription_7 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_8, option_9, option_10], properties=frozenset({"basic"}))
optiondescription_6 = OptionDescription(name="2", doc="2", children=[optiondescription_7], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_6])
