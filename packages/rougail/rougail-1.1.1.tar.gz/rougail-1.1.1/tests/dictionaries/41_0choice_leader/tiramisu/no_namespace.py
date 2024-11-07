from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
option_2 = StrOption(name="leader", doc="The leader", multi=True, properties=frozenset({"standard"}), informations={'type': 'string'})
option_3 = ChoiceOption(name="follower1", doc="A follower", values=("a", "b", "c"), multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'choice'})
optiondescription_1 = Leadership(name="leader", doc="The leadership", children=[option_2, option_3], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
