from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
option_1 = IntOption(name="int", doc="A limited number", default=10, min_number=0, max_number=100, properties=frozenset({"mandatory", "standard"}), informations={'type': 'number'})
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[option_1])
