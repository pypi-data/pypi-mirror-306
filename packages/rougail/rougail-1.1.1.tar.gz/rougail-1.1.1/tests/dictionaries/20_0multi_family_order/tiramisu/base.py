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
option_2 = StrOption(name="variable", doc="a variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_4 = StrOption(name="variable1", doc="a first variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_6 = StrOption(name="variable", doc="a variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
optiondescription_5 = OptionDescription(name="subfamily", doc="a sub family", children=[option_6], properties=frozenset({"basic"}))
option_7 = StrOption(name="variable2", doc="a second variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
optiondescription_3 = OptionDescription(name="family", doc="a family", children=[option_4, optiondescription_5, option_7], properties=frozenset({"basic"}))
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_2, optiondescription_3], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
