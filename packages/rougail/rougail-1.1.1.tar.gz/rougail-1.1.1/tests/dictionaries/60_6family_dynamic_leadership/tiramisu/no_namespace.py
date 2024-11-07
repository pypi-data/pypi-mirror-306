from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
option_1 = StrOption(name="var", doc="a suffix variable", multi=True, default=["val1", "val2"], default_multi="val1", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_4 = StrOption(name="leader", doc="a leader", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_5 = StrOption(name="follower1", doc="a follower1", multi=True, properties=frozenset({"standard"}), informations={'type': 'string'})
option_6 = StrOption(name="follower2", doc="a follower2", multi=True, properties=frozenset({"standard"}), informations={'type': 'string'})
optiondescription_3 = Leadership(name="leadership", doc="a leadership", children=[option_4, option_5, option_6], properties=frozenset({"basic"}))
optiondescription_2 = ConvertDynOptionDescription(name="dyn{{ identifier }}", doc="a dynamic family", identifiers=Calculation(func['calc_value'], Params((ParamOption(option_1)))), children=[optiondescription_3], properties=frozenset({"basic"}), informations={'dynamic_variable': 'var'})
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[option_1, optiondescription_2])
