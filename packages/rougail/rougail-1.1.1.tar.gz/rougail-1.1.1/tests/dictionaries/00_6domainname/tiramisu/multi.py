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
option_3 = DomainnameOption(name="variable", doc="a domain name variable", default="my.domain.name", type="domainname", allow_ip=False, properties=frozenset({"mandatory", "standard"}), informations={'type': 'domainname'})
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_3], properties=frozenset({"standard"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"standard"}))
option_6 = DomainnameOption(name="variable", doc="a domain name variable", default="my.domain.name", type="domainname", allow_ip=False, properties=frozenset({"mandatory", "standard"}), informations={'type': 'domainname'})
optiondescription_5 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_6], properties=frozenset({"standard"}))
optiondescription_4 = OptionDescription(name="2", doc="2", children=[optiondescription_5], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_4])
