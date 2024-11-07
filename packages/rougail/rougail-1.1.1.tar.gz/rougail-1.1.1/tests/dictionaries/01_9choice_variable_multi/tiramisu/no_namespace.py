from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
option_1 = StrOption(name="variable1", doc="a first variable", multi=True, default=["a", "b", "c"], default_multi="a", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_2 = ChoiceOption(name="variable2", doc="a second variable", values=Calculation(func['calc_value'], Params((ParamOption(option_1)))), properties=frozenset({"basic", "mandatory"}), informations={'type': 'choice'})
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[option_1, option_2])
