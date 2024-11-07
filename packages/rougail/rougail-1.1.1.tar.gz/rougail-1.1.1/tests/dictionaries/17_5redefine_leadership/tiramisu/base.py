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
option_3 = StrOption(name="leader", doc="a leader", multi=True, properties=frozenset({"force_default_on_freeze", "frozen", "standard"}), informations={'type': 'string'})
option_4 = StrOption(name="follower", doc="a follower", multi=True, properties=frozenset({"force_default_on_freeze", "frozen", "standard"}), informations={'type': 'string'})
optiondescription_2 = Leadership(name="leader", doc="leader", children=[option_3, option_4], properties=frozenset({"hidden", "standard"}))
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_2], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
