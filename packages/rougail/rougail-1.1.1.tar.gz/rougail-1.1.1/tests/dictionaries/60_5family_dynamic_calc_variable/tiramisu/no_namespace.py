from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
option_1 = StrOption(name="var1", doc="A suffix variable", multi=True, default=["val1", "val2"], default_multi="val1", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_3 = StrOption(name="var", doc="A dynamic variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
optiondescription_2 = ConvertDynOptionDescription(name="dyn{{ identifier }}", doc="dyn{{ identifier }}", identifiers=Calculation(func['calc_value'], Params((ParamOption(option_1, notraisepropertyerror=True)))), children=[option_3], properties=frozenset({"basic"}), informations={'dynamic_variable': 'var1'})
option_4 = StrOption(name="var2", doc="A variable calculated", default=Calculation(func['calc_value'], Params((ParamDynOption(option_3, ["val1"])))), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[option_1, optiondescription_2, option_4])
