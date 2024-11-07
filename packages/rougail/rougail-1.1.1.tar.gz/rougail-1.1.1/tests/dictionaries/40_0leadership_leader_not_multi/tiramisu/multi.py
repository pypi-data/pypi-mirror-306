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
option_4 = StrOption(name="mode_conteneur_actif", doc="No change", default="non", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_3 = OptionDescription(name="general", doc="general", children=[option_4], properties=frozenset({"standard"}))
option_7 = StrOption(name="leader", doc="leader", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_8 = StrOption(name="follower1", doc="follower1", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_9 = StrOption(name="follower2", doc="follower2", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
optiondescription_6 = Leadership(name="leader", doc="leader", children=[option_7, option_8, option_9], properties=frozenset({"basic"}))
optiondescription_5 = OptionDescription(name="general1", doc="general1", children=[optiondescription_6], properties=frozenset({"basic"}))
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_3, optiondescription_5], properties=frozenset({"basic"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"basic"}))
option_13 = StrOption(name="mode_conteneur_actif", doc="No change", default="non", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_12 = OptionDescription(name="general", doc="general", children=[option_13], properties=frozenset({"standard"}))
option_16 = StrOption(name="leader", doc="leader", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_17 = StrOption(name="follower1", doc="follower1", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_18 = StrOption(name="follower2", doc="follower2", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
optiondescription_15 = Leadership(name="leader", doc="leader", children=[option_16, option_17, option_18], properties=frozenset({"basic"}))
optiondescription_14 = OptionDescription(name="general1", doc="general1", children=[optiondescription_15], properties=frozenset({"basic"}))
optiondescription_11 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_12, optiondescription_14], properties=frozenset({"basic"}))
optiondescription_10 = OptionDescription(name="2", doc="2", children=[optiondescription_11], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_10])
