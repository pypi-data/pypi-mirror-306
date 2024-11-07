from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
option_1 = StrOption(name="var1", doc="a first variable", default="yes", properties=frozenset({"force_default_on_freeze", "frozen", "hidden", "standard"}), informations={'type': 'string'})
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[option_1])
