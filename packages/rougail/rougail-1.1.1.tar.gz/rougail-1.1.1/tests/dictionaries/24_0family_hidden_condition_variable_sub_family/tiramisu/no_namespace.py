from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
option_1 = BoolOption(name="condition", doc="the variable use has condition", default=True, properties=frozenset({"mandatory", "standard"}), informations={'type': 'boolean'})
option_4 = StrOption(name="var1", doc="a variable", properties=frozenset({"force_default_on_freeze", "standard", Calculation(func['variable_to_property'], Params((ParamValue("frozen"), ParamOption(option_1)), kwargs={'when': ParamValue(True), 'inverse': ParamValue(False)}), help_function=func['variable_to_property'])}), informations={'type': 'string'})
optiondescription_3 = OptionDescription(name="subfamily", doc="a subfamily", children=[option_4], properties=frozenset({"standard"}))
optiondescription_2 = OptionDescription(name="family", doc="possibly hidden family", children=[optiondescription_3], properties=frozenset({"standard", Calculation(func['variable_to_property'], Params((ParamValue("hidden"), ParamOption(option_1)), kwargs={'when': ParamValue(True), 'inverse': ParamValue(False)}), help_function=func['variable_to_property'])}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[option_1, optiondescription_2])
