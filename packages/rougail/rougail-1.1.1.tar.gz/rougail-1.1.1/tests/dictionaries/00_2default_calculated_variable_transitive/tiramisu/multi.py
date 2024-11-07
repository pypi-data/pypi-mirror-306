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
option_3 = DomainnameOption(name="var1", doc="a first variable", multi=True, type="domainname", allow_ip=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'domainname'})
option_4 = DomainnameOption(name="var2", doc="a second variable", multi=True, default=Calculation(func['calc_value'], Params((ParamOption(option_3)))), type="domainname", allow_ip=True, properties=frozenset({"mandatory", "standard"}), informations={'type': 'domainname'})
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_3, option_4], properties=frozenset({"basic"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"basic"}))
option_7 = DomainnameOption(name="var1", doc="a first variable", multi=True, type="domainname", allow_ip=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'domainname'})
option_8 = DomainnameOption(name="var2", doc="a second variable", multi=True, default=Calculation(func['calc_value'], Params((ParamOption(option_7)))), type="domainname", allow_ip=True, properties=frozenset({"mandatory", "standard"}), informations={'type': 'domainname'})
optiondescription_6 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_7, option_8], properties=frozenset({"basic"}))
optiondescription_5 = OptionDescription(name="2", doc="2", children=[optiondescription_6], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_5])
