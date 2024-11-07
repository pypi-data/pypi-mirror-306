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
option_3 = StrOption(name="var1", doc="the first variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string', 'test': ('test',)})
option_4 = StrOption(name="var2", doc="the second variable", default="value", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string', 'test': ('test',)})
option_5 = StrOption(name="var3", doc="the third variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string', 'test': ('test1', 'test2')})
option_6 = StrOption(name="var4", doc="the forth variable", properties=frozenset({"standard"}), informations={'type': 'string', 'test': (None, 'test1', 'test2')})
option_7 = BoolOption(name="var5", doc="the fifth variable", default=True, properties=frozenset({"mandatory", "standard"}), informations={'type': 'boolean', 'test': (False,)})
option_8 = StrOption(name="var6", doc="the sixth variable", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'string', 'test': ('test1', 'test2')})
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_3, option_4, option_5, option_6, option_7, option_8], properties=frozenset({"basic"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"basic"}))
option_11 = StrOption(name="var1", doc="the first variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string', 'test': ('test',)})
option_12 = StrOption(name="var2", doc="the second variable", default="value", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string', 'test': ('test',)})
option_13 = StrOption(name="var3", doc="the third variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string', 'test': ('test1', 'test2')})
option_14 = StrOption(name="var4", doc="the forth variable", properties=frozenset({"standard"}), informations={'type': 'string', 'test': (None, 'test1', 'test2')})
option_15 = BoolOption(name="var5", doc="the fifth variable", default=True, properties=frozenset({"mandatory", "standard"}), informations={'type': 'boolean', 'test': (False,)})
option_16 = StrOption(name="var6", doc="the sixth variable", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'string', 'test': ('test1', 'test2')})
optiondescription_10 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_11, option_12, option_13, option_14, option_15, option_16], properties=frozenset({"basic"}))
optiondescription_9 = OptionDescription(name="2", doc="2", children=[optiondescription_10], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_9])
