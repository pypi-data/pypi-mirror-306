from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
class Regexp_option_1(RegexpOption):
    __slots__ = tuple()
    _type = 'value'
Regexp_option_1._regexp = re_compile(r"^#(?:[0-9a-f]{3}){1,2}$")

option_1 = Regexp_option_1(name="var", doc="a first variable", default="#a1a1a1", properties=frozenset({"mandatory", "standard"}), informations={'type': 'regexp', 'test': ('#b1b1b1', '#b2b2b2')})
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[option_1])
