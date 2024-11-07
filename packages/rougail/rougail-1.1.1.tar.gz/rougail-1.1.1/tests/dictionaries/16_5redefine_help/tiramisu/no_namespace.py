from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
option_2 = StrOption(name="variable", doc="redefine help", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string', 'help': 'redefine help ok'})
optiondescription_1 = OptionDescription(name="family", doc="a family", children=[option_2], properties=frozenset({"basic"}), informations={'help': 'redefine help family ok'})
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
