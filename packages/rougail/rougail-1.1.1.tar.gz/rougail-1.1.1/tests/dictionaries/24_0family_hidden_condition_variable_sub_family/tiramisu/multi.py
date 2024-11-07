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
option_3 = BoolOption(name="condition", doc="the variable use has condition", default=True, properties=frozenset({"mandatory", "standard"}), informations={'type': 'boolean'})
option_6 = StrOption(name="var1", doc="a variable", properties=frozenset({"force_default_on_freeze", "standard", Calculation(func['variable_to_property'], Params((ParamValue("frozen"), ParamOption(option_3)), kwargs={'when': ParamValue(True), 'inverse': ParamValue(False)}), help_function=func['variable_to_property'])}), informations={'type': 'string'})
optiondescription_5 = OptionDescription(name="subfamily", doc="a subfamily", children=[option_6], properties=frozenset({"standard"}))
optiondescription_4 = OptionDescription(name="family", doc="possibly hidden family", children=[optiondescription_5], properties=frozenset({"standard", Calculation(func['variable_to_property'], Params((ParamValue("hidden"), ParamOption(option_3)), kwargs={'when': ParamValue(True), 'inverse': ParamValue(False)}), help_function=func['variable_to_property'])}))
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_3, optiondescription_4], properties=frozenset({"standard"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"standard"}))
option_9 = BoolOption(name="condition", doc="the variable use has condition", default=True, properties=frozenset({"mandatory", "standard"}), informations={'type': 'boolean'})
option_12 = StrOption(name="var1", doc="a variable", properties=frozenset({"force_default_on_freeze", "standard", Calculation(func['variable_to_property'], Params((ParamValue("frozen"), ParamOption(option_9)), kwargs={'when': ParamValue(True), 'inverse': ParamValue(False)}), help_function=func['variable_to_property'])}), informations={'type': 'string'})
optiondescription_11 = OptionDescription(name="subfamily", doc="a subfamily", children=[option_12], properties=frozenset({"standard"}))
optiondescription_10 = OptionDescription(name="family", doc="possibly hidden family", children=[optiondescription_11], properties=frozenset({"standard", Calculation(func['variable_to_property'], Params((ParamValue("hidden"), ParamOption(option_9)), kwargs={'when': ParamValue(True), 'inverse': ParamValue(False)}), help_function=func['variable_to_property'])}))
optiondescription_8 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_9, optiondescription_10], properties=frozenset({"standard"}))
optiondescription_7 = OptionDescription(name="2", doc="2", children=[optiondescription_8], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_7])
