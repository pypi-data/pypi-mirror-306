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
option_4 = StrOption(name="leader", doc="a leader", multi=True, properties=frozenset({"force_default_on_freeze", "frozen", "standard"}), informations={'type': 'string'})
option_5 = StrOption(name="follower1", doc="the follower1", multi=True, properties=frozenset({"force_default_on_freeze", "frozen", "standard"}), informations={'type': 'string'})
option_6 = StrOption(name="follower2", doc="the follower2", multi=True, properties=frozenset({"force_default_on_freeze", "frozen", "standard"}), informations={'type': 'string'})
option_7 = StrOption(name="follower3", doc="follower3", multi=True, properties=frozenset({"force_default_on_freeze", "frozen", "standard"}), informations={'type': 'string'})
optiondescription_3 = Leadership(name="leader", doc="a leadership", children=[option_4, option_5, option_6, option_7], properties=frozenset({"hidden", "standard"}))
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_3], properties=frozenset({"standard"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"standard"}))
option_11 = StrOption(name="leader", doc="a leader", multi=True, properties=frozenset({"force_default_on_freeze", "frozen", "standard"}), informations={'type': 'string'})
option_12 = StrOption(name="follower1", doc="the follower1", multi=True, properties=frozenset({"force_default_on_freeze", "frozen", "standard"}), informations={'type': 'string'})
option_13 = StrOption(name="follower2", doc="the follower2", multi=True, properties=frozenset({"force_default_on_freeze", "frozen", "standard"}), informations={'type': 'string'})
option_14 = StrOption(name="follower3", doc="follower3", multi=True, properties=frozenset({"force_default_on_freeze", "frozen", "standard"}), informations={'type': 'string'})
optiondescription_10 = Leadership(name="leader", doc="a leadership", children=[option_11, option_12, option_13, option_14], properties=frozenset({"hidden", "standard"}))
optiondescription_9 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_10], properties=frozenset({"standard"}))
optiondescription_8 = OptionDescription(name="2", doc="2", children=[optiondescription_9], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_8])
