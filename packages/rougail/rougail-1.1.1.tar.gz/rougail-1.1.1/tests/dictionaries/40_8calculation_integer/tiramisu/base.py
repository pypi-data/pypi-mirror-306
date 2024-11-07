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
dict_env['default_rougail.int1'] = "{% if rougail.bool %}1{% else %}2{% endif %}\n"
dict_env['default_rougail.int2'] = "{% if not rougail.bool %}3{% else %}4{% endif %}\n"
option_2 = BoolOption(name="bool", doc="a boolean variable", default=False, properties=frozenset({"mandatory", "standard"}), informations={'type': 'boolean'})
option_3 = IntOption(name="int1", doc="first integer variable", default=Calculation(func['jinja_to_function'], Params((), kwargs={'__internal_jinja': ParamValue("default_rougail.int1"), '__internal_type': ParamValue("number"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/40_8calculation_integer/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("default"), '__internal_variable': ParamValue("rougail.int1"), 'rougail.bool': ParamOption(option_2, notraisepropertyerror=True)})), properties=frozenset({"mandatory", "standard"}), informations={'type': 'number'})
option_4 = IntOption(name="int2", doc="second integer variable", default=Calculation(func['jinja_to_function'], Params((), kwargs={'__internal_jinja': ParamValue("default_rougail.int2"), '__internal_type': ParamValue("number"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/40_8calculation_integer/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("default"), '__internal_variable': ParamValue("rougail.int2"), 'rougail.bool': ParamOption(option_2, notraisepropertyerror=True)})), properties=frozenset({"mandatory", "standard"}), informations={'type': 'number'})
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_2, option_3, option_4], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
