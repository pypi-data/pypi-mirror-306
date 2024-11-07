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
class Regexp_option_3(RegexpOption):
    __slots__ = tuple()
    _type = 'value'
Regexp_option_3._regexp = re_compile(r"^#(?:[0-9a-f]{3}){1,2}$")

class Regexp_option_6(RegexpOption):
    __slots__ = tuple()
    _type = 'value'
Regexp_option_6._regexp = re_compile(r"^#(?:[0-9a-f]{3}){1,2}$")

option_3 = Regexp_option_3(name="var", doc="a first variable", default="#a1a1a1", properties=frozenset({"mandatory", "standard"}), informations={'type': 'regexp', 'test': ('#b1b1b1', '#b2b2b2')})
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_3], properties=frozenset({"standard"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"standard"}))
option_6 = Regexp_option_6(name="var", doc="a first variable", default="#a1a1a1", properties=frozenset({"mandatory", "standard"}), informations={'type': 'regexp', 'test': ('#b1b1b1', '#b2b2b2')})
optiondescription_5 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_6], properties=frozenset({"standard"}))
optiondescription_4 = OptionDescription(name="2", doc="2", children=[optiondescription_5], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_4])
