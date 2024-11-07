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
option_3 = StrOption(name="var", doc="a suffix variable", multi=True, default=["val1", "val2"], default_multi="val1", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_6 = StrOption(name="leader", doc="a leader", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_7 = StrOption(name="follower1", doc="a follower1", multi=True, properties=frozenset({"standard"}), informations={'type': 'string'})
option_8 = StrOption(name="follower2", doc="a follower2", multi=True, properties=frozenset({"standard"}), informations={'type': 'string'})
optiondescription_5 = Leadership(name="leadership", doc="a leadership", children=[option_6, option_7, option_8], properties=frozenset({"basic"}))
optiondescription_4 = ConvertDynOptionDescription(name="dyn{{ identifier }}", doc="a dynamic family", identifiers=Calculation(func['calc_value'], Params((ParamOption(option_3)))), children=[optiondescription_5], properties=frozenset({"basic"}), informations={'dynamic_variable': '1.rougail.var'})
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_3, optiondescription_4], properties=frozenset({"basic"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"basic"}))
option_11 = StrOption(name="var", doc="a suffix variable", multi=True, default=["val1", "val2"], default_multi="val1", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_14 = StrOption(name="leader", doc="a leader", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_15 = StrOption(name="follower1", doc="a follower1", multi=True, properties=frozenset({"standard"}), informations={'type': 'string'})
option_16 = StrOption(name="follower2", doc="a follower2", multi=True, properties=frozenset({"standard"}), informations={'type': 'string'})
optiondescription_13 = Leadership(name="leadership", doc="a leadership", children=[option_14, option_15, option_16], properties=frozenset({"basic"}))
optiondescription_12 = ConvertDynOptionDescription(name="dyn{{ identifier }}", doc="a dynamic family", identifiers=Calculation(func['calc_value'], Params((ParamOption(option_11)))), children=[optiondescription_13], properties=frozenset({"basic"}), informations={'dynamic_variable': '2.rougail.var'})
optiondescription_10 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_11, optiondescription_12], properties=frozenset({"basic"}))
optiondescription_9 = OptionDescription(name="2", doc="2", children=[optiondescription_10], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_9])
