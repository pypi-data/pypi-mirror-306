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
option_4 = StrOption(name="var1", doc="a first variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
information_0 = ParamInformation("test_information", None)
option_5 = StrOption(name="var2", doc="a second variable", default=Calculation(func['calc_value'], Params((information_0))), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_3 = OptionDescription(name="family", doc="family", children=[option_4, option_5], properties=frozenset({"basic"}))
information_0.set_option(optiondescription_3)
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_3], properties=frozenset({"basic"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"basic"}))
option_9 = StrOption(name="var1", doc="a first variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
information_1 = ParamInformation("test_information", None)
option_10 = StrOption(name="var2", doc="a second variable", default=Calculation(func['calc_value'], Params((information_1))), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_8 = OptionDescription(name="family", doc="family", children=[option_9, option_10], properties=frozenset({"basic"}))
information_1.set_option(optiondescription_8)
optiondescription_7 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_8], properties=frozenset({"basic"}))
optiondescription_6 = OptionDescription(name="2", doc="2", children=[optiondescription_7], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_6])
