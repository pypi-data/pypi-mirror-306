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
option_2 = BoolOption(name="condition", doc="a condition", default=False, properties=frozenset({"mandatory", "standard"}), informations={'type': 'boolean'})
option_3 = StrOption(name="variable", doc="a variable", properties=frozenset({"basic", "mandatory", Calculation(func['variable_to_property'], Params((ParamValue("disabled"), ParamOption(option_2)), kwargs={'when': ParamValue(True), 'inverse': ParamValue(False)}), help_function=func['variable_to_property'])}), informations={'type': 'string'})
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_2, option_3], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
