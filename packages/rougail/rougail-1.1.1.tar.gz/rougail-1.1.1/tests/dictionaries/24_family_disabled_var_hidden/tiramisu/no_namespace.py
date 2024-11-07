from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
option_2 = BoolOption(name="var1", doc="A description", default=True, properties=frozenset({"mandatory", "standard"}), informations={'type': 'boolean'})
option_3 = StrOption(name="var2", doc="A description", properties=frozenset({"basic", "force_default_on_freeze", "mandatory", Calculation(func['variable_to_property'], Params((ParamValue("hidden"), ParamOption(option_2)), kwargs={'when': ParamValue(True), 'inverse': ParamValue(False)}), help_function=func['variable_to_property']), Calculation(func['variable_to_property'], Params((ParamValue("frozen"), ParamOption(option_2)), kwargs={'when': ParamValue(True), 'inverse': ParamValue(False)}), help_function=func['variable_to_property'])}), informations={'type': 'string'})
optiondescription_1 = OptionDescription(name="family", doc="family", children=[option_2, option_3], properties=frozenset({"basic", "disabled"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
