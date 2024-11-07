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
option_2 = StrOption(name="var1", doc="the first variable", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_3 = StrOption(name="var2", doc="the second variable", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_4 = StrOption(name="var3", doc="the third variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_5 = StrOption(name="var4", doc="the forth variable", multi=True, default=["value"], default_multi="value", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_6 = StrOption(name="var5", doc="the fifth variable", multi=True, default=["value"], default_multi="value", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_7 = StrOption(name="var6", doc="the sixth variable", multi=True, default=["value"], default_multi="value", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_8 = StrOption(name="var7", doc="the seventh variable", multi=True, default=["value"], default_multi="value", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_9 = StrOption(name="var8", doc="the eighth variable", multi=True, default=["value"], default_multi="value", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_2, option_3, option_4, option_5, option_6, option_7, option_8, option_9], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
