from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
option_1 = StrOption(name="source_variable_1", doc="the first source variable", default="val1", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_2 = StrOption(name="source_variable_2", doc="the second source variable", default="val2", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_3 = ChoiceOption(name="my_variable", doc="a variable", values=(Calculation(func['calc_value'], Params((ParamOption(option_1)))), Calculation(func['calc_value'], Params((ParamOption(option_2))))), default="val1", properties=frozenset({"mandatory", "standard"}), informations={'type': 'choice'})
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[option_1, option_2, option_3])
