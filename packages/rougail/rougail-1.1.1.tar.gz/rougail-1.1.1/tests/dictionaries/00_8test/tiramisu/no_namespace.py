from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
option_1 = StrOption(name="var1", doc="the first variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string', 'test': ('test',)})
option_2 = StrOption(name="var2", doc="the second variable", default="value", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string', 'test': ('test',)})
option_3 = StrOption(name="var3", doc="the third variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string', 'test': ('test1', 'test2')})
option_4 = StrOption(name="var4", doc="the forth variable", properties=frozenset({"standard"}), informations={'type': 'string', 'test': (None, 'test1', 'test2')})
option_5 = BoolOption(name="var5", doc="the fifth variable", default=True, properties=frozenset({"mandatory", "standard"}), informations={'type': 'boolean', 'test': (False,)})
option_6 = StrOption(name="var6", doc="the sixth variable", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'string', 'test': ('test1', 'test2')})
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[option_1, option_2, option_3, option_4, option_5, option_6])
