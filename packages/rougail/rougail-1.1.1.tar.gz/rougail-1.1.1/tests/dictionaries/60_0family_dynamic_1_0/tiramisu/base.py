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
option_2 = StrOption(name="var", doc="A suffix variable", multi=True, default=["val1", "val2"], default_multi="val1", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_4 = StrOption(name="vardyn", doc="Dynamic variable", properties=frozenset({"standard"}), informations={'type': 'string'})
optiondescription_3 = ConvertDynOptionDescription(name="dyn{{ identifier }}", doc="dyn{{ identifier }}", identifiers=Calculation(func['calc_value'], Params((ParamOption(option_2, notraisepropertyerror=True)), kwargs={'allow_none': ParamValue(True)})), children=[option_4], properties=frozenset({"standard"}), informations={'dynamic_variable': 'rougail.var'})
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_2, optiondescription_3], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
