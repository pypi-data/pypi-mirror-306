from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
option_1 = BoolOption(name="condition", doc="a condition", default=True, properties=frozenset({"mandatory", "standard"}), informations={'type': 'boolean'})
option_2 = StrOption(name="var", doc="a variable", properties=frozenset({"standard", Calculation(func['variable_to_property'], Params((ParamValue("mandatory"), ParamOption(option_1)), kwargs={'when': ParamValue(True), 'inverse': ParamValue(False)}), help_function=func['variable_to_property'])}), informations={'type': 'string'})
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[option_1, option_2])
