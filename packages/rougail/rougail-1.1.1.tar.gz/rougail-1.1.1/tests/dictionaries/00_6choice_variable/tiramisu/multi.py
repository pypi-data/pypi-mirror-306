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
option_3 = StrOption(name="var1", doc="a second variable", multi=True, default=["a", "b", "c"], default_multi="a", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_4 = ChoiceOption(name="var2", doc="a first variable", values=Calculation(func['calc_value'], Params((ParamOption(option_3)))), default="a", properties=frozenset({"mandatory", "standard"}), informations={'type': 'choice'})
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_3, option_4], properties=frozenset({"standard"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"standard"}))
option_7 = StrOption(name="var1", doc="a second variable", multi=True, default=["a", "b", "c"], default_multi="a", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_8 = ChoiceOption(name="var2", doc="a first variable", values=Calculation(func['calc_value'], Params((ParamOption(option_7)))), default="a", properties=frozenset({"mandatory", "standard"}), informations={'type': 'choice'})
optiondescription_6 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_7, option_8], properties=frozenset({"standard"}))
optiondescription_5 = OptionDescription(name="2", doc="2", children=[optiondescription_6], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_5])
