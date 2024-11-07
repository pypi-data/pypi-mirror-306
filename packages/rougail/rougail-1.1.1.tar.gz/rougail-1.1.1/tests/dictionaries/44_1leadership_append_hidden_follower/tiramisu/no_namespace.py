from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
option_2 = StrOption(name="leader", doc="a leader", multi=True, properties=frozenset({"force_default_on_freeze", "frozen", "standard"}), informations={'type': 'string'})
option_3 = StrOption(name="follower1", doc="the follower1", multi=True, properties=frozenset({"force_default_on_freeze", "frozen", "standard"}), informations={'type': 'string'})
option_4 = StrOption(name="follower2", doc="the follower2", multi=True, properties=frozenset({"force_default_on_freeze", "frozen", "standard"}), informations={'type': 'string'})
option_5 = StrOption(name="follower3", doc="follower3", multi=True, properties=frozenset({"force_default_on_freeze", "frozen", "standard"}), informations={'type': 'string'})
optiondescription_1 = Leadership(name="leader", doc="a leadership", children=[option_2, option_3, option_4, option_5], properties=frozenset({"hidden", "standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
