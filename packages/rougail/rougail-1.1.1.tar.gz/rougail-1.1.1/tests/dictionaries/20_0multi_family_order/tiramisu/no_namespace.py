from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
option_1 = StrOption(name="variable", doc="a variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_3 = StrOption(name="variable1", doc="a first variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_5 = StrOption(name="variable", doc="a variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
optiondescription_4 = OptionDescription(name="subfamily", doc="a sub family", children=[option_5], properties=frozenset({"basic"}))
option_6 = StrOption(name="variable2", doc="a second variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
optiondescription_2 = OptionDescription(name="family", doc="a family", children=[option_3, optiondescription_4, option_6], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[option_1, optiondescription_2])
