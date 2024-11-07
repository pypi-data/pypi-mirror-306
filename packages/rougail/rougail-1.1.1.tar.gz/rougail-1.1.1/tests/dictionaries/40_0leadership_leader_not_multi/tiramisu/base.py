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
option_3 = StrOption(name="mode_conteneur_actif", doc="No change", default="non", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_2 = OptionDescription(name="general", doc="general", children=[option_3], properties=frozenset({"standard"}))
option_6 = StrOption(name="leader", doc="leader", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_7 = StrOption(name="follower1", doc="follower1", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_8 = StrOption(name="follower2", doc="follower2", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
optiondescription_5 = Leadership(name="leader", doc="leader", children=[option_6, option_7, option_8], properties=frozenset({"basic"}))
optiondescription_4 = OptionDescription(name="general1", doc="general1", children=[optiondescription_5], properties=frozenset({"basic"}))
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_2, optiondescription_4], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
