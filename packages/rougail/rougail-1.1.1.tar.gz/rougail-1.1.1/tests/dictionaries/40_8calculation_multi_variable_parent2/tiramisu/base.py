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
option_3 = StrOption(name="var", doc="a variable", default="no", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_2 = OptionDescription(name="fam1", doc="first family", children=[option_3], properties=frozenset({"standard"}))
option_5 = StrOption(name="var", doc="a varaible", default=Calculation(func['calc_value'], Params((ParamOption(option_3)))), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_4 = OptionDescription(name="fam2", doc="second family", children=[option_5], properties=frozenset({"standard"}))
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_2, optiondescription_4], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
