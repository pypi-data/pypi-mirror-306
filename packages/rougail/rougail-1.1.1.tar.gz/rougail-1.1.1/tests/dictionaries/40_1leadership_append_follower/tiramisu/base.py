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
option_3 = StrOption(name="leader", doc="the leader", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_4 = StrOption(name="follower1", doc="the follower1", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_5 = StrOption(name="follower2", doc="the follower2", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_6 = StrOption(name="follower3", doc="the follower3", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
optiondescription_2 = Leadership(name="leader", doc="a leadership", children=[option_3, option_4, option_5, option_6], properties=frozenset({"basic"}))
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_2], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
