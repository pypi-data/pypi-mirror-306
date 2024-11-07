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
option_4 = BoolOption(name="var1", doc="A description", default=True, properties=frozenset({"mandatory", "standard"}), informations={'type': 'boolean'})
option_5 = StrOption(name="var2", doc="A description", properties=frozenset({"basic", "force_default_on_freeze", "mandatory", Calculation(func['variable_to_property'], Params((ParamValue("hidden"), ParamOption(option_4)), kwargs={'when': ParamValue(True), 'inverse': ParamValue(False)}), help_function=func['variable_to_property']), Calculation(func['variable_to_property'], Params((ParamValue("frozen"), ParamOption(option_4)), kwargs={'when': ParamValue(True), 'inverse': ParamValue(False)}), help_function=func['variable_to_property'])}), informations={'type': 'string'})
optiondescription_3 = OptionDescription(name="family", doc="family", children=[option_4, option_5], properties=frozenset({"basic", "disabled"}))
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_3], properties=frozenset({"basic"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"basic"}))
option_9 = BoolOption(name="var1", doc="A description", default=True, properties=frozenset({"mandatory", "standard"}), informations={'type': 'boolean'})
option_10 = StrOption(name="var2", doc="A description", properties=frozenset({"basic", "force_default_on_freeze", "mandatory", Calculation(func['variable_to_property'], Params((ParamValue("hidden"), ParamOption(option_9)), kwargs={'when': ParamValue(True), 'inverse': ParamValue(False)}), help_function=func['variable_to_property']), Calculation(func['variable_to_property'], Params((ParamValue("frozen"), ParamOption(option_9)), kwargs={'when': ParamValue(True), 'inverse': ParamValue(False)}), help_function=func['variable_to_property'])}), informations={'type': 'string'})
optiondescription_8 = OptionDescription(name="family", doc="family", children=[option_9, option_10], properties=frozenset({"basic", "disabled"}))
optiondescription_7 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_8], properties=frozenset({"basic"}))
optiondescription_6 = OptionDescription(name="2", doc="2", children=[optiondescription_7], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_6])
