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
option_2 = BoolOption(name="condition", doc="the variable use has condition", default=True, properties=frozenset({"mandatory", "standard"}), informations={'type': 'boolean'})
option_5 = StrOption(name="var1", doc="a variable", properties=frozenset({"force_default_on_freeze", "standard", Calculation(func['variable_to_property'], Params((ParamValue("frozen"), ParamOption(option_2)), kwargs={'when': ParamValue(True), 'inverse': ParamValue(False)}), help_function=func['variable_to_property'])}), informations={'type': 'string'})
optiondescription_4 = OptionDescription(name="subfamily", doc="a subfamily", children=[option_5], properties=frozenset({"standard"}))
optiondescription_3 = OptionDescription(name="family", doc="possibly hidden family", children=[optiondescription_4], properties=frozenset({"standard", Calculation(func['variable_to_property'], Params((ParamValue("hidden"), ParamOption(option_2)), kwargs={'when': ParamValue(True), 'inverse': ParamValue(False)}), help_function=func['variable_to_property'])}))
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_2, optiondescription_3], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
