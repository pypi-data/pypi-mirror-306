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
option_4 = StrOption(name="my_variable", doc="my_variable", properties=frozenset({"force_default_on_freeze", "frozen", "standard"}), informations={'type': 'string'})
optiondescription_3 = OptionDescription(name="type", doc="a type family", children=[option_4], properties=frozenset({"standard"}))
option_6 = StrOption(name="my_variable", doc="my_variable", properties=frozenset({"force_default_on_freeze", "frozen", "standard"}), informations={'type': 'string'})
optiondescription_5 = OptionDescription(name="description", doc="This is a other great family", children=[option_6], properties=frozenset({"standard"}))
option_8 = StrOption(name="my_variable", doc="my_variable", properties=frozenset({"force_default_on_freeze", "frozen", "standard"}), informations={'type': 'string'})
optiondescription_7 = OptionDescription(name="help", doc="a help family", children=[option_8], properties=frozenset({"standard"}), informations={'help': 'This is a other great family'})
option_10 = StrOption(name="my_variable", doc="my_variable", properties=frozenset({"advanced", "force_default_on_freeze", "frozen"}), informations={'type': 'string'})
optiondescription_9 = OptionDescription(name="mode", doc="a mode family", children=[option_10], properties=frozenset({"advanced"}))
option_12 = StrOption(name="my_variable", doc="my_variable", properties=frozenset({"force_default_on_freeze", "frozen", "standard"}), informations={'type': 'string'})
optiondescription_11 = OptionDescription(name="hidden", doc="an hidden family", children=[option_12], properties=frozenset({"hidden", "standard"}))
option_14 = StrOption(name="my_variable", doc="my_variable", properties=frozenset({"force_default_on_freeze", "frozen", "standard"}), informations={'type': 'string'})
optiondescription_13 = OptionDescription(name="disabled", doc="an disabled family", children=[option_14], properties=frozenset({"disabled", "standard"}))
optiondescription_2 = OptionDescription(name="my_family", doc="This is a great family", children=[optiondescription_3, optiondescription_5, optiondescription_7, optiondescription_9, optiondescription_11, optiondescription_13], properties=frozenset({"disabled", "hidden", "standard"}), informations={'help': 'This is a great family'})
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_2], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
