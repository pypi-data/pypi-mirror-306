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
option_4 = StrOption(name="varname", doc="No change", multi=True, default=["a"], default_multi="a", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_3 = OptionDescription(name="general", doc="général", children=[option_4], properties=frozenset({"standard"}))
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_3], properties=frozenset({"standard"}))
option_6 = StrOption(name="var", doc="a varaible", multi=True, default=["a"], default_multi="a", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_8 = StrOption(name="var", doc="var", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
optiondescription_7 = ConvertDynOptionDescription(name="dyn_{{ identifier }}", doc="dyn_{{ identifier }}", identifiers=Calculation(func['calc_value'], Params((ParamOption(option_6)))), children=[option_8], properties=frozenset({"basic"}), informations={'dynamic_variable': '1.extra.var'})
optiondescription_5 = OptionDescription(name="extra", doc="extra", group_type=groups.namespace, children=[option_6, optiondescription_7], properties=frozenset({"basic"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2, optiondescription_5], properties=frozenset({"basic"}))
option_12 = StrOption(name="varname", doc="No change", multi=True, default=["a"], default_multi="a", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_11 = OptionDescription(name="general", doc="général", children=[option_12], properties=frozenset({"standard"}))
optiondescription_10 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_11], properties=frozenset({"standard"}))
option_14 = StrOption(name="var", doc="a varaible", multi=True, default=["a"], default_multi="a", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_16 = StrOption(name="var", doc="var", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
optiondescription_15 = ConvertDynOptionDescription(name="dyn_{{ identifier }}", doc="dyn_{{ identifier }}", identifiers=Calculation(func['calc_value'], Params((ParamOption(option_14)))), children=[option_16], properties=frozenset({"basic"}), informations={'dynamic_variable': '2.extra.var'})
optiondescription_13 = OptionDescription(name="extra", doc="extra", group_type=groups.namespace, children=[option_14, optiondescription_15], properties=frozenset({"basic"}))
optiondescription_9 = OptionDescription(name="2", doc="2", children=[optiondescription_10, optiondescription_13], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_9])
