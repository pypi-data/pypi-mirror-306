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
option_3 = StrOption(name="var", doc="a variable", multi=True, default=["a"], default_multi="a", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_3], properties=frozenset({"standard"}))
option_6 = StrOption(name="var", doc="var", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
optiondescription_5 = ConvertDynOptionDescription(name="dyn_{{ identifier }}", doc="dyn_{{ identifier }}", identifiers=Calculation(func['calc_value'], Params((ParamOption(option_3)))), children=[option_6], properties=frozenset({"basic"}), informations={'dynamic_variable': '1.var'})
optiondescription_4 = OptionDescription(name="extra", doc="extra", group_type=groups.namespace, children=[optiondescription_5], properties=frozenset({"basic"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2, optiondescription_4], properties=frozenset({"basic"}))
option_9 = StrOption(name="var", doc="a variable", multi=True, default=["a"], default_multi="a", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_8 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_9], properties=frozenset({"standard"}))
option_12 = StrOption(name="var", doc="var", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
optiondescription_11 = ConvertDynOptionDescription(name="dyn_{{ identifier }}", doc="dyn_{{ identifier }}", identifiers=Calculation(func['calc_value'], Params((ParamOption(option_9)))), children=[option_12], properties=frozenset({"basic"}), informations={'dynamic_variable': '2.var'})
optiondescription_10 = OptionDescription(name="extra", doc="extra", group_type=groups.namespace, children=[optiondescription_11], properties=frozenset({"basic"}))
optiondescription_7 = OptionDescription(name="2", doc="2", children=[optiondescription_8, optiondescription_10], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_7])
