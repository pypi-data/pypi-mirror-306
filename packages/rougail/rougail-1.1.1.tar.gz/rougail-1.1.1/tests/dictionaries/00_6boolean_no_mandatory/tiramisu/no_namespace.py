from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
option_1 = BoolOption(name="variable", doc="a variable", default=True, properties=frozenset({"standard"}), informations={'type': 'boolean'})
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[option_1])
