from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
option_1 = CustomOption(name="custom1", doc="a first custom variable", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'custom'})
option_2 = CustomOption(name="custom2", doc="a second custom variable", multi=True, default=["value"], default_multi="value", properties=frozenset({"mandatory", "standard"}), informations={'type': 'custom'})
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[option_1, option_2])
