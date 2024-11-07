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
option_3 = StrOption(name="var", doc="A variable", default="non", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
optiondescription_2 = OptionDescription(name="family", doc="a family", children=[option_3], properties=frozenset({"basic"}))
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_2], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
