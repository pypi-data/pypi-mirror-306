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
option_5 = StrOption(name="variable", doc="a variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
optiondescription_4 = OptionDescription(name="subfamily", doc="a sub family", children=[option_5], properties=frozenset({"basic"}))
optiondescription_3 = OptionDescription(name="family", doc="a family", children=[optiondescription_4], properties=frozenset({"basic"}))
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_3], properties=frozenset({"basic"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"basic"}))
option_10 = StrOption(name="variable", doc="a variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
optiondescription_9 = OptionDescription(name="subfamily", doc="a sub family", children=[option_10], properties=frozenset({"basic"}))
optiondescription_8 = OptionDescription(name="family", doc="a family", children=[optiondescription_9], properties=frozenset({"basic"}))
optiondescription_7 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_8], properties=frozenset({"basic"}))
optiondescription_6 = OptionDescription(name="2", doc="2", children=[optiondescription_7], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_6])
