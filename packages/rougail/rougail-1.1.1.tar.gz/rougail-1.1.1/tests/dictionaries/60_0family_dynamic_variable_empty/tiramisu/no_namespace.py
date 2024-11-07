from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
option_1 = StrOption(name="var", doc="a suffix variable", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_3 = StrOption(name="var", doc="a variable inside dynamic family", default="val", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_2 = ConvertDynOptionDescription(name="dyn{{ identifier }}", doc="a dynamic family", identifiers=Calculation(func['calc_value'], Params((ParamOption(option_1)))), children=[option_3], properties=frozenset({"standard"}), informations={'dynamic_variable': 'var'})
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[option_1, optiondescription_2])
