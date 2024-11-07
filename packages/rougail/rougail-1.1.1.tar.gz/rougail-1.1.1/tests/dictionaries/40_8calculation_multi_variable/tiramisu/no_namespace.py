from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
option_2 = StrOption(name="var2", doc="a second variable", default="no", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_3 = StrOption(name="var3", doc="a third variable", default="yes", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_1 = StrOption(name="var", doc="a first variable", multi=True, default=[Calculation(func['calc_value'], Params((ParamOption(option_2)))), Calculation(func['calc_value'], Params((ParamOption(option_3))))], default_multi=Calculation(func['calc_value'], Params((ParamOption(option_2)))), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[option_1, option_2, option_3])
