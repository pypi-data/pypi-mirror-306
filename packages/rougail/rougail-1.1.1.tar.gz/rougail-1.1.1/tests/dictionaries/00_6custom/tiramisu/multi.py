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
option_3 = CustomOption(name="custom1", doc="the first variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'custom'})
option_4 = CustomOption(name="custom2", doc="the seconf variable", default="value", properties=frozenset({"mandatory", "standard"}), informations={'type': 'custom'})
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_3, option_4], properties=frozenset({"basic"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"basic"}))
option_7 = CustomOption(name="custom1", doc="the first variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'custom'})
option_8 = CustomOption(name="custom2", doc="the seconf variable", default="value", properties=frozenset({"mandatory", "standard"}), informations={'type': 'custom'})
optiondescription_6 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_7, option_8], properties=frozenset({"basic"}))
optiondescription_5 = OptionDescription(name="2", doc="2", children=[optiondescription_6], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_5])
