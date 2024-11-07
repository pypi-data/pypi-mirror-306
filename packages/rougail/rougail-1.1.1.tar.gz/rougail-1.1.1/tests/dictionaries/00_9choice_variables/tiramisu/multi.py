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
option_3 = StrOption(name="source_variable_1", doc="the first source variable", default="val1", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_4 = StrOption(name="source_variable_2", doc="the second source variable", default="val2", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_5 = ChoiceOption(name="my_variable", doc="a variable", values=(Calculation(func['calc_value'], Params((ParamOption(option_3)))), Calculation(func['calc_value'], Params((ParamOption(option_4))))), default="val1", properties=frozenset({"mandatory", "standard"}), informations={'type': 'choice'})
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_3, option_4, option_5], properties=frozenset({"standard"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"standard"}))
option_8 = StrOption(name="source_variable_1", doc="the first source variable", default="val1", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_9 = StrOption(name="source_variable_2", doc="the second source variable", default="val2", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_10 = ChoiceOption(name="my_variable", doc="a variable", values=(Calculation(func['calc_value'], Params((ParamOption(option_8)))), Calculation(func['calc_value'], Params((ParamOption(option_9))))), default="val1", properties=frozenset({"mandatory", "standard"}), informations={'type': 'choice'})
optiondescription_7 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_8, option_9, option_10], properties=frozenset({"standard"}))
optiondescription_6 = OptionDescription(name="2", doc="2", children=[optiondescription_7], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_6])
