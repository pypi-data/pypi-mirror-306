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
dict_env['default_extra.variable2'] = "{{ rougail.variable }}\n"
dict_env['default_extra.variable3'] = "{{ variable }}\n"
option_2 = StrOption(name="variable", doc="a variable", default="value", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_2], properties=frozenset({"standard"}))
option_4 = StrOption(name="variable1", doc="a first variable", default=Calculation(func['calc_value'], Params((ParamOption(option_2)))), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_5 = StrOption(name="variable2", doc="a second variable", default=Calculation(func['jinja_to_function'], Params((), kwargs={'__internal_jinja': ParamValue("default_extra.variable2"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/00_9extra_calculation/dictionaries/extra/00-base.yml']), '__internal_attribute': ParamValue("default"), '__internal_variable': ParamValue("extra.variable2"), 'rougail.variable': ParamOption(option_2, notraisepropertyerror=True)})), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_6 = StrOption(name="variable3", doc="a third variable", default=Calculation(func['jinja_to_function'], Params((), kwargs={'__internal_jinja': ParamValue("default_extra.variable3"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/00_9extra_calculation/dictionaries/extra/00-base.yml']), '__internal_attribute': ParamValue("default"), '__internal_variable': ParamValue("extra.variable3"), 'variable': ParamOption(option_2)})), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_3 = OptionDescription(name="extra", doc="extra", group_type=groups.namespace, children=[option_4, option_5, option_6], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_3])
