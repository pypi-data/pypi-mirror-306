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
option_3 = StrOption(name="varname", doc="No change", multi=True, default=["a"], default_multi="a", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_2 = OptionDescription(name="general", doc="général", children=[option_3], properties=frozenset({"standard"}))
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_2], properties=frozenset({"standard"}))
option_5 = StrOption(name="var", doc="a varaible", multi=True, default=["a"], default_multi="a", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_7 = StrOption(name="var", doc="var", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
optiondescription_6 = ConvertDynOptionDescription(name="dyn_{{ identifier }}", doc="dyn_{{ identifier }}", identifiers=Calculation(func['calc_value'], Params((ParamOption(option_5)))), children=[option_7], properties=frozenset({"basic"}), informations={'dynamic_variable': 'extra.var'})
optiondescription_4 = OptionDescription(name="extra", doc="extra", group_type=groups.namespace, children=[option_5, optiondescription_6], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_4])
