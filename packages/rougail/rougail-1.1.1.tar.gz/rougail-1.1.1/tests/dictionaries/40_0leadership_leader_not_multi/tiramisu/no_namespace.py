from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
option_2 = StrOption(name="mode_conteneur_actif", doc="No change", default="non", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_1 = OptionDescription(name="general", doc="general", children=[option_2], properties=frozenset({"standard"}))
option_5 = StrOption(name="leader", doc="leader", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_6 = StrOption(name="follower1", doc="follower1", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_7 = StrOption(name="follower2", doc="follower2", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
optiondescription_4 = Leadership(name="leader", doc="leader", children=[option_5, option_6, option_7], properties=frozenset({"basic"}))
optiondescription_3 = OptionDescription(name="general1", doc="general1", children=[optiondescription_4], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_3])
