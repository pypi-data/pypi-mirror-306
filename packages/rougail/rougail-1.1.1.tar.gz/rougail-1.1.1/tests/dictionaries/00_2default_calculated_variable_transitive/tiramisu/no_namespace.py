from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
option_1 = DomainnameOption(name="var1", doc="a first variable", multi=True, type="domainname", allow_ip=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'domainname'})
option_2 = DomainnameOption(name="var2", doc="a second variable", multi=True, default=Calculation(func['calc_value'], Params((ParamOption(option_1)))), type="domainname", allow_ip=True, properties=frozenset({"mandatory", "standard"}), informations={'type': 'domainname'})
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[option_1, option_2])
