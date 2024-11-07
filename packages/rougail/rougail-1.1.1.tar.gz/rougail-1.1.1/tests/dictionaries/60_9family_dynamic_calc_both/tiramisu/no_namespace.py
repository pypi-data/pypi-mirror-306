from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
option_1 = StrOption(name="var", doc="a suffix variable", default="val2", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_3 = StrOption(name="vardyn", doc="a dynamic variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
optiondescription_2 = ConvertDynOptionDescription(name="dyn{{ identifier }}", doc="a dynamic family", identifiers=["val1", Calculation(func['calc_value'], Params((ParamOption(option_1))))], children=[option_3], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[option_1, optiondescription_2])
