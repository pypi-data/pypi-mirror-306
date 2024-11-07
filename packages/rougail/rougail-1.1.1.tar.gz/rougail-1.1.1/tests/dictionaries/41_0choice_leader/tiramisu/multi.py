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
option_4 = StrOption(name="leader", doc="The leader", multi=True, properties=frozenset({"standard"}), informations={'type': 'string'})
option_5 = ChoiceOption(name="follower1", doc="A follower", values=("a", "b", "c"), multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'choice'})
optiondescription_3 = Leadership(name="leader", doc="The leadership", children=[option_4, option_5], properties=frozenset({"basic"}))
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_3], properties=frozenset({"basic"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"basic"}))
option_9 = StrOption(name="leader", doc="The leader", multi=True, properties=frozenset({"standard"}), informations={'type': 'string'})
option_10 = ChoiceOption(name="follower1", doc="A follower", values=("a", "b", "c"), multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'choice'})
optiondescription_8 = Leadership(name="leader", doc="The leadership", children=[option_9, option_10], properties=frozenset({"basic"}))
optiondescription_7 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_8], properties=frozenset({"basic"}))
optiondescription_6 = OptionDescription(name="2", doc="2", children=[optiondescription_7], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_6])
