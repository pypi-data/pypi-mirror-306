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
option_5 = StrOption(name="var", doc="a calculated variable", default=Calculation(func['calc_value'], Params((ParamOption(option_3)))), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_4 = OptionDescription(name="fam1", doc="a family", children=[option_5], properties=frozenset({"standard"}))
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_3, optiondescription_4], properties=frozenset({"standard"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"standard"}))
option_8 = StrOption(name="var", doc="a variable", default="no", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_10 = StrOption(name="var", doc="a calculated variable", default=Calculation(func['calc_value'], Params((ParamOption(option_8)))), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_9 = OptionDescription(name="fam1", doc="a family", children=[option_10], properties=frozenset({"standard"}))
optiondescription_7 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_8, optiondescription_9], properties=frozenset({"standard"}))
optiondescription_6 = OptionDescription(name="2", doc="2", children=[optiondescription_7], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_6])
