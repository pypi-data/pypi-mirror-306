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
option_3 = FloatOption(name="var1", doc="the first variable", default=0.0, properties=frozenset({"mandatory", "standard"}), informations={'type': 'float'})
option_4 = FloatOption(name="var2", doc="the second variable", default=0.0, properties=frozenset({"mandatory", "standard"}), informations={'type': 'float'})
option_5 = FloatOption(name="var3", doc="the third variable", default=0.0, properties=frozenset({"mandatory", "standard"}), informations={'type': 'float'})
option_6 = FloatOption(name="var4", doc="the forth variable", default=10.1, properties=frozenset({"mandatory", "standard"}), informations={'type': 'float'})
option_7 = FloatOption(name="var5", doc="the fifth variable", default=10.1, properties=frozenset({"mandatory", "standard"}), informations={'type': 'float'})
option_8 = FloatOption(name="var6", doc="the sixth variable", default=10.1, properties=frozenset({"mandatory", "standard"}), informations={'type': 'float'})
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_3, option_4, option_5, option_6, option_7, option_8], properties=frozenset({"standard"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"standard"}))
option_11 = FloatOption(name="var1", doc="the first variable", default=0.0, properties=frozenset({"mandatory", "standard"}), informations={'type': 'float'})
option_12 = FloatOption(name="var2", doc="the second variable", default=0.0, properties=frozenset({"mandatory", "standard"}), informations={'type': 'float'})
option_13 = FloatOption(name="var3", doc="the third variable", default=0.0, properties=frozenset({"mandatory", "standard"}), informations={'type': 'float'})
option_14 = FloatOption(name="var4", doc="the forth variable", default=10.1, properties=frozenset({"mandatory", "standard"}), informations={'type': 'float'})
option_15 = FloatOption(name="var5", doc="the fifth variable", default=10.1, properties=frozenset({"mandatory", "standard"}), informations={'type': 'float'})
option_16 = FloatOption(name="var6", doc="the sixth variable", default=10.1, properties=frozenset({"mandatory", "standard"}), informations={'type': 'float'})
optiondescription_10 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_11, option_12, option_13, option_14, option_15, option_16], properties=frozenset({"standard"}))
optiondescription_9 = OptionDescription(name="2", doc="2", children=[optiondescription_10], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_9])
