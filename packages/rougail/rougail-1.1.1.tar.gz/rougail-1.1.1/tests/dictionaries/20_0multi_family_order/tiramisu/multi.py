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
option_3 = StrOption(name="variable", doc="a variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_5 = StrOption(name="variable1", doc="a first variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_7 = StrOption(name="variable", doc="a variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
optiondescription_6 = OptionDescription(name="subfamily", doc="a sub family", children=[option_7], properties=frozenset({"basic"}))
option_8 = StrOption(name="variable2", doc="a second variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
optiondescription_4 = OptionDescription(name="family", doc="a family", children=[option_5, optiondescription_6, option_8], properties=frozenset({"basic"}))
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_3, optiondescription_4], properties=frozenset({"basic"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"basic"}))
option_11 = StrOption(name="variable", doc="a variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_13 = StrOption(name="variable1", doc="a first variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_15 = StrOption(name="variable", doc="a variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
optiondescription_14 = OptionDescription(name="subfamily", doc="a sub family", children=[option_15], properties=frozenset({"basic"}))
option_16 = StrOption(name="variable2", doc="a second variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
optiondescription_12 = OptionDescription(name="family", doc="a family", children=[option_13, optiondescription_14, option_16], properties=frozenset({"basic"}))
optiondescription_10 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_11, optiondescription_12], properties=frozenset({"basic"}))
optiondescription_9 = OptionDescription(name="2", doc="2", children=[optiondescription_10], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_9])
