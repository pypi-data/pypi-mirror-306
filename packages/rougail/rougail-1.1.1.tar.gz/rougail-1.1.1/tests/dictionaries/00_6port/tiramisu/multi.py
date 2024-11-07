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
option_3 = PortOption(name="variable1", doc="a port variable", allow_private=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'port'})
option_4 = PortOption(name="variable2", doc="a port variable with default value", default="8080", allow_private=True, properties=frozenset({"mandatory", "standard"}), informations={'type': 'port'})
option_5 = PortOption(name="variable3", doc="a port variable with integer default value", default="8080", allow_private=True, properties=frozenset({"mandatory", "standard"}), informations={'type': 'port'})
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_3, option_4, option_5], properties=frozenset({"basic"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"basic"}))
option_8 = PortOption(name="variable1", doc="a port variable", allow_private=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'port'})
option_9 = PortOption(name="variable2", doc="a port variable with default value", default="8080", allow_private=True, properties=frozenset({"mandatory", "standard"}), informations={'type': 'port'})
option_10 = PortOption(name="variable3", doc="a port variable with integer default value", default="8080", allow_private=True, properties=frozenset({"mandatory", "standard"}), informations={'type': 'port'})
optiondescription_7 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_8, option_9, option_10], properties=frozenset({"basic"}))
optiondescription_6 = OptionDescription(name="2", doc="2", children=[optiondescription_7], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_6])
