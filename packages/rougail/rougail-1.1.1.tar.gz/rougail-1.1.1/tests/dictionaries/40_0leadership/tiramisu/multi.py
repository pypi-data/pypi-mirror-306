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
option_4 = StrOption(name="leader", doc="a leader", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_5 = StrOption(name="follower1", doc="a follower", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_6 = StrOption(name="follower2", doc="an other follower", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
optiondescription_3 = Leadership(name="leader", doc="a leadership", children=[option_4, option_5, option_6], properties=frozenset({"basic"}))
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_3], properties=frozenset({"basic"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"basic"}))
option_10 = StrOption(name="leader", doc="a leader", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_11 = StrOption(name="follower1", doc="a follower", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_12 = StrOption(name="follower2", doc="an other follower", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
optiondescription_9 = Leadership(name="leader", doc="a leadership", children=[option_10, option_11, option_12], properties=frozenset({"basic"}))
optiondescription_8 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_9], properties=frozenset({"basic"}))
optiondescription_7 = OptionDescription(name="2", doc="2", children=[optiondescription_8], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_7])
