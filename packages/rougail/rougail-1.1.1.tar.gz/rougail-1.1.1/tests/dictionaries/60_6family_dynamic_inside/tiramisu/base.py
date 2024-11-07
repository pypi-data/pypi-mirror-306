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
option_4 = StrOption(name="var1", doc="value is suffix", default=Calculation(func['calc_value'], Params((ParamIdentifier()))), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_5 = StrOption(name="var2", doc="value is first variable", default=Calculation(func['calc_value'], Params((ParamOption(option_4)))), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_6 = StrOption(name="var3", doc="value is relative first variable", default=Calculation(func['calc_value'], Params((ParamOption(option_4)))), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_7 = StrOption(name="var4", doc="value is first variable of val1", default=Calculation(func['calc_value'], Params((ParamDynOption(option_4, ["val1"])))), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_3 = ConvertDynOptionDescription(name="{{ identifier }}_dyn", doc="a dynamic family", identifiers=Calculation(func['calc_value'], Params((ParamOption(option_2)))), children=[option_4, option_5, option_6, option_7], properties=frozenset({"standard"}), informations={'dynamic_variable': 'rougail.var'})
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_2, optiondescription_3], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
