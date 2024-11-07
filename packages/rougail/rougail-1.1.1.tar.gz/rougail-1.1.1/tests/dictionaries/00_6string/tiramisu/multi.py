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
option_3 = StrOption(name="var1", doc="the first variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_4 = StrOption(name="var2", doc="the second variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_5 = StrOption(name="var3", doc="the third variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_6 = StrOption(name="var4", doc="the forth variable", default="value", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_7 = StrOption(name="var5", doc="the fifth variable", default="value", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_8 = StrOption(name="var6", doc="the sixth variable", default="value", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_3, option_4, option_5, option_6, option_7, option_8], properties=frozenset({"basic"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"basic"}))
option_11 = StrOption(name="var1", doc="the first variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_12 = StrOption(name="var2", doc="the second variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_13 = StrOption(name="var3", doc="the third variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_14 = StrOption(name="var4", doc="the forth variable", default="value", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_15 = StrOption(name="var5", doc="the fifth variable", default="value", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_16 = StrOption(name="var6", doc="the sixth variable", default="value", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_10 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_11, option_12, option_13, option_14, option_15, option_16], properties=frozenset({"basic"}))
optiondescription_9 = OptionDescription(name="2", doc="2", children=[optiondescription_10], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_9])
