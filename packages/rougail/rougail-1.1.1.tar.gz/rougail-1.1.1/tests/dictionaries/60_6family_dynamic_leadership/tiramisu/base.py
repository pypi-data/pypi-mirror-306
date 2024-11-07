from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
try:
    groups.namespace
except:
    groups.addgroup('namespace')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
option_2 = StrOption(name="var", doc="a suffix variable", multi=True, default=["val1", "val2"], default_multi="val1", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_5 = StrOption(name="leader", doc="a leader", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_6 = StrOption(name="follower1", doc="a follower1", multi=True, properties=frozenset({"standard"}), informations={'type': 'string'})
option_7 = StrOption(name="follower2", doc="a follower2", multi=True, properties=frozenset({"standard"}), informations={'type': 'string'})
optiondescription_4 = Leadership(name="leadership", doc="a leadership", children=[option_5, option_6, option_7], properties=frozenset({"basic"}))
optiondescription_3 = ConvertDynOptionDescription(name="dyn{{ identifier }}", doc="a dynamic family", identifiers=Calculation(func['calc_value'], Params((ParamOption(option_2)))), children=[optiondescription_4], properties=frozenset({"basic"}), informations={'dynamic_variable': 'rougail.var'})
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_2, optiondescription_3], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
