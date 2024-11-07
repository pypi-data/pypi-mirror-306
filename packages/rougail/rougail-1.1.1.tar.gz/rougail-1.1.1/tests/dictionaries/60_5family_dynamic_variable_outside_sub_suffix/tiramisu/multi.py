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
option_3 = StrOption(name="var", doc="a suffix variable", multi=True, default=["val1", "val2"], default_multi="val1", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_6 = StrOption(name="var", doc="a variable inside a sub dynamic family", default=Calculation(func['calc_value'], Params((ParamIdentifier()))), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_5 = ConvertDynOptionDescription(name="subdyn_{{ identifier }}", doc="a sub dynamic family", identifiers=Calculation(func['calc_value'], Params((ParamOption(option_3)))), children=[option_6], properties=frozenset({"standard"}), informations={'dynamic_variable': '1.var'})
optiondescription_4 = ConvertDynOptionDescription(name="my_dyn_family_{{ identifier }}", doc="a dynamic family", identifiers=Calculation(func['calc_value'], Params((ParamOption(option_3, notraisepropertyerror=True)))), children=[optiondescription_5], properties=frozenset({"standard"}), informations={'dynamic_variable': '1.rougail.var'})
option_7 = StrOption(name="var2", doc="a variable", multi=True, default=Calculation(func['calc_value'], Params((ParamDynOption(option_6, ["val1", None])))), properties=frozenset({"standard"}), informations={'type': 'string'})
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_3, optiondescription_4, option_7], properties=frozenset({"standard"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"standard"}))
option_10 = StrOption(name="var", doc="a suffix variable", multi=True, default=["val1", "val2"], default_multi="val1", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_13 = StrOption(name="var", doc="a variable inside a sub dynamic family", default=Calculation(func['calc_value'], Params((ParamIdentifier()))), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_12 = ConvertDynOptionDescription(name="subdyn_{{ identifier }}", doc="a sub dynamic family", identifiers=Calculation(func['calc_value'], Params((ParamOption(option_10)))), children=[option_13], properties=frozenset({"standard"}), informations={'dynamic_variable': '2.var'})
optiondescription_11 = ConvertDynOptionDescription(name="my_dyn_family_{{ identifier }}", doc="a dynamic family", identifiers=Calculation(func['calc_value'], Params((ParamOption(option_10, notraisepropertyerror=True)))), children=[optiondescription_12], properties=frozenset({"standard"}), informations={'dynamic_variable': '2.rougail.var'})
option_14 = StrOption(name="var2", doc="a variable", multi=True, default=Calculation(func['calc_value'], Params((ParamDynOption(option_13, ["val1", None])))), properties=frozenset({"standard"}), informations={'type': 'string'})
optiondescription_9 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_10, optiondescription_11, option_14], properties=frozenset({"standard"}))
optiondescription_8 = OptionDescription(name="2", doc="2", children=[optiondescription_9], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_8])
