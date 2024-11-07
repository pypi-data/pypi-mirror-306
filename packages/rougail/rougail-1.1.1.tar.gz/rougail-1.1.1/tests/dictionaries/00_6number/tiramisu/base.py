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
option_2 = IntOption(name="var1", doc="the first variable", default=0, properties=frozenset({"mandatory", "standard"}), informations={'type': 'number'})
option_3 = IntOption(name="var2", doc="the second variable", default=0, properties=frozenset({"mandatory", "standard"}), informations={'type': 'number'})
option_4 = IntOption(name="var3", doc="the third variable", default=0, properties=frozenset({"mandatory", "standard"}), informations={'type': 'number'})
option_5 = IntOption(name="var4", doc="this forth variable", default=10, properties=frozenset({"mandatory", "standard"}), informations={'type': 'number'})
option_6 = IntOption(name="var5", doc="the fifth variable", default=10, properties=frozenset({"mandatory", "standard"}), informations={'type': 'number'})
option_7 = IntOption(name="var6", doc="the sixth variable", default=10, properties=frozenset({"mandatory", "standard"}), informations={'type': 'number'})
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_2, option_3, option_4, option_5, option_6, option_7], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
