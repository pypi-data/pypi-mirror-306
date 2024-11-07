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
option_3 = StrOption(name="var1", doc="a first variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
information_0 = ParamInformation("test_information", None)
option_4 = StrOption(name="var2", doc="a second variable", default=Calculation(func['calc_value'], Params((information_0))), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_2 = OptionDescription(name="family", doc="family", children=[option_3, option_4], properties=frozenset({"basic"}))
information_0.set_option(optiondescription_2)
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_2], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
