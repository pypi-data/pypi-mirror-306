from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
option_1 = BoolOption(name="var1", doc="the first variable", default=True, properties=frozenset({"mandatory", "standard"}), informations={'type': 'boolean'})
option_2 = BoolOption(name="var2", doc="the second variable", default=True, properties=frozenset({"mandatory", "standard"}), informations={'type': 'boolean'})
option_3 = BoolOption(name="var3", doc="the third variable", default=True, properties=frozenset({"mandatory", "standard"}), informations={'type': 'boolean'})
option_4 = BoolOption(name="var4", doc="the forth variable", default=False, properties=frozenset({"mandatory", "standard"}), informations={'type': 'boolean'})
option_5 = BoolOption(name="var5", doc="the fifth variable", default=False, properties=frozenset({"mandatory", "standard"}), informations={'type': 'boolean'})
option_6 = BoolOption(name="var6", doc="the sixth variable", default=False, properties=frozenset({"mandatory", "standard"}), informations={'type': 'boolean'})
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[option_1, option_2, option_3, option_4, option_5, option_6])
