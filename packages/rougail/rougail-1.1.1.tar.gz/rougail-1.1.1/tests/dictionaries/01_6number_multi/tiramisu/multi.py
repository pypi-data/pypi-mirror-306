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
option_3 = IntOption(name="var1", doc="the first variable", multi=True, default=[0], default_multi=0, properties=frozenset({"mandatory", "standard"}), informations={'type': 'number'})
option_4 = IntOption(name="var2", doc="the second variable", multi=True, default=[0], default_multi=0, properties=frozenset({"mandatory", "standard"}), informations={'type': 'number'})
option_5 = IntOption(name="var3", doc="the third variable", multi=True, default=[0], default_multi=0, properties=frozenset({"mandatory", "standard"}), informations={'type': 'number'})
option_6 = IntOption(name="var4", doc="the forth variable", multi=True, default=[10], default_multi=10, properties=frozenset({"mandatory", "standard"}), informations={'type': 'number'})
option_7 = IntOption(name="var5", doc="the fifth variable", multi=True, default=[10], default_multi=10, properties=frozenset({"mandatory", "standard"}), informations={'type': 'number'})
option_8 = IntOption(name="var6", doc="the sixth variable", multi=True, default=[10], default_multi=10, properties=frozenset({"mandatory", "standard"}), informations={'type': 'number'})
option_9 = IntOption(name="var7", doc="the seventh variable", multi=True, default=[0], default_multi=0, properties=frozenset({"mandatory", "standard"}), informations={'type': 'number'})
option_10 = IntOption(name="var8", doc="the eighth variable", multi=True, default=[0], default_multi=0, properties=frozenset({"mandatory", "standard"}), informations={'type': 'number'})
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_3, option_4, option_5, option_6, option_7, option_8, option_9, option_10], properties=frozenset({"standard"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"standard"}))
option_13 = IntOption(name="var1", doc="the first variable", multi=True, default=[0], default_multi=0, properties=frozenset({"mandatory", "standard"}), informations={'type': 'number'})
option_14 = IntOption(name="var2", doc="the second variable", multi=True, default=[0], default_multi=0, properties=frozenset({"mandatory", "standard"}), informations={'type': 'number'})
option_15 = IntOption(name="var3", doc="the third variable", multi=True, default=[0], default_multi=0, properties=frozenset({"mandatory", "standard"}), informations={'type': 'number'})
option_16 = IntOption(name="var4", doc="the forth variable", multi=True, default=[10], default_multi=10, properties=frozenset({"mandatory", "standard"}), informations={'type': 'number'})
option_17 = IntOption(name="var5", doc="the fifth variable", multi=True, default=[10], default_multi=10, properties=frozenset({"mandatory", "standard"}), informations={'type': 'number'})
option_18 = IntOption(name="var6", doc="the sixth variable", multi=True, default=[10], default_multi=10, properties=frozenset({"mandatory", "standard"}), informations={'type': 'number'})
option_19 = IntOption(name="var7", doc="the seventh variable", multi=True, default=[0], default_multi=0, properties=frozenset({"mandatory", "standard"}), informations={'type': 'number'})
option_20 = IntOption(name="var8", doc="the eighth variable", multi=True, default=[0], default_multi=0, properties=frozenset({"mandatory", "standard"}), informations={'type': 'number'})
optiondescription_12 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_13, option_14, option_15, option_16, option_17, option_18, option_19, option_20], properties=frozenset({"standard"}))
optiondescription_11 = OptionDescription(name="2", doc="2", children=[optiondescription_12], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_11])
