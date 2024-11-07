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
option_3 = StrOption(name="leader", doc="the leader", multi=True, default=["leader"], properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_4 = StrOption(name="follower1", doc="the follower1", multi=submulti, default_multi=["value"], properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_5 = StrOption(name="follower2", doc="the follower2", multi=submulti, default=Calculation(func['calc_value'], Params((ParamOption(option_4)))), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_2 = Leadership(name="leader", doc="a leadership", children=[option_3, option_4, option_5], properties=frozenset({"standard"}))
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_2], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
