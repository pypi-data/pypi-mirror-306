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
option_2 = StrOption(name="var", doc="a variable", multi=True, default=["a"], default_multi="a", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_2], properties=frozenset({"standard"}))
option_5 = StrOption(name="var", doc="var", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
optiondescription_4 = ConvertDynOptionDescription(name="dyn_{{ identifier }}", doc="dyn_{{ identifier }}", identifiers=Calculation(func['calc_value'], Params((ParamOption(option_2)))), children=[option_5], properties=frozenset({"basic"}), informations={'dynamic_variable': 'extra.var'})
optiondescription_3 = OptionDescription(name="extra", doc="extra", group_type=groups.namespace, children=[optiondescription_4], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_3])
