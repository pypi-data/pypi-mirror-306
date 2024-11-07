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
option_4 = StrOption(name="variable", doc="a variable", properties=frozenset({"advanced"}), informations={'type': 'string'})
optiondescription_3 = OptionDescription(name="subfamily", doc="a sub family", children=[option_4], properties=frozenset({"advanced"}))
optiondescription_2 = OptionDescription(name="family", doc="a family", children=[optiondescription_3], properties=frozenset({"advanced"}))
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_2], properties=frozenset({"advanced"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
