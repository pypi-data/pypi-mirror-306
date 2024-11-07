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
option_4 = StrOption(name="variable", doc="redefine help", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string', 'help': 'redefine help ok'})
optiondescription_3 = OptionDescription(name="family", doc="a family", children=[option_4], properties=frozenset({"basic"}), informations={'help': 'redefine help family ok'})
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_3], properties=frozenset({"basic"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"basic"}))
option_8 = StrOption(name="variable", doc="redefine help", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string', 'help': 'redefine help ok'})
optiondescription_7 = OptionDescription(name="family", doc="a family", children=[option_8], properties=frozenset({"basic"}), informations={'help': 'redefine help family ok'})
optiondescription_6 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_7], properties=frozenset({"basic"}))
optiondescription_5 = OptionDescription(name="2", doc="2", children=[optiondescription_6], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_5])
