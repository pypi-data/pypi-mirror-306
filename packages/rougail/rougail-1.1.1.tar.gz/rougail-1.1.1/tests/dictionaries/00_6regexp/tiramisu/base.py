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
class Regexp_option_2(RegexpOption):
    __slots__ = tuple()
    _type = 'value'
Regexp_option_2._regexp = re_compile(r"^#(?:[0-9a-f]{3}){1,2}$")

option_2 = Regexp_option_2(name="var", doc="a first variable", default="#a1a1a1", properties=frozenset({"mandatory", "standard"}), informations={'type': 'regexp', 'test': ('#b1b1b1', '#b2b2b2')})
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_2], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
