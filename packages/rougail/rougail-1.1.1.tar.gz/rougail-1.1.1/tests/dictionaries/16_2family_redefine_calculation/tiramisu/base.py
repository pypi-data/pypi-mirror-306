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
dict_env['disabled_rougail.family'] = "true\n"
option_3 = StrOption(name="var1", doc="var1", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
optiondescription_2 = OptionDescription(name="family", doc="family", children=[option_3], properties=frozenset({"basic", Calculation(func['jinja_to_property'], Params((ParamValue("disabled")), kwargs={'__internal_jinja': ParamValue("disabled_rougail.family"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/16_2family_redefine_calculation/dictionaries/rougail/01-base.yml']), '__internal_attribute': ParamValue("disabled"), '__internal_variable': ParamValue("rougail.family"), 'when': ParamValue(True), 'inverse': ParamValue(False)}), help_function=func['jinja_to_property_help'])}))
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_2], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
