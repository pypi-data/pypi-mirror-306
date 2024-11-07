from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
option_3 = StrOption(name="my_variable", doc="my_variable", properties=frozenset({"force_default_on_freeze", "frozen", "standard"}), informations={'type': 'string'})
optiondescription_2 = OptionDescription(name="type", doc="a type family", children=[option_3], properties=frozenset({"standard"}))
option_5 = StrOption(name="my_variable", doc="my_variable", properties=frozenset({"force_default_on_freeze", "frozen", "standard"}), informations={'type': 'string'})
optiondescription_4 = OptionDescription(name="description", doc="This is a other great family", children=[option_5], properties=frozenset({"standard"}))
option_7 = StrOption(name="my_variable", doc="my_variable", properties=frozenset({"force_default_on_freeze", "frozen", "standard"}), informations={'type': 'string'})
optiondescription_6 = OptionDescription(name="help", doc="a help family", children=[option_7], properties=frozenset({"standard"}), informations={'help': 'This is a other great family'})
option_9 = StrOption(name="my_variable", doc="my_variable", properties=frozenset({"advanced", "force_default_on_freeze", "frozen"}), informations={'type': 'string'})
optiondescription_8 = OptionDescription(name="mode", doc="a mode family", children=[option_9], properties=frozenset({"advanced"}))
option_11 = StrOption(name="my_variable", doc="my_variable", properties=frozenset({"force_default_on_freeze", "frozen", "standard"}), informations={'type': 'string'})
optiondescription_10 = OptionDescription(name="hidden", doc="an hidden family", children=[option_11], properties=frozenset({"hidden", "standard"}))
option_13 = StrOption(name="my_variable", doc="my_variable", properties=frozenset({"force_default_on_freeze", "frozen", "standard"}), informations={'type': 'string'})
optiondescription_12 = OptionDescription(name="disabled", doc="an disabled family", children=[option_13], properties=frozenset({"disabled", "standard"}))
optiondescription_1 = OptionDescription(name="my_family", doc="This is a great family", children=[optiondescription_2, optiondescription_4, optiondescription_6, optiondescription_8, optiondescription_10, optiondescription_12], properties=frozenset({"disabled", "hidden", "standard"}), informations={'help': 'This is a great family'})
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
