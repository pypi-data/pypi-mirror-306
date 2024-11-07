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
dict_env['default_1.extra.variable'] = "no"
dict_env['default_2.extra.variable'] = "no"
option_3 = StrOption(name="variable", doc="a variable", default="rougail", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_3], properties=frozenset({"standard"}))
option_5 = StrOption(name="variable", doc="a variable", default=Calculation(func['jinja_to_function'], Params((), kwargs={'__internal_jinja': ParamValue("default_1.extra.variable"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/00_9extra/dictionaries/extra/00-base.yml']), '__internal_attribute': ParamValue("default"), '__internal_variable': ParamValue("1.extra.variable")})), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_4 = OptionDescription(name="extra", doc="extra", group_type=groups.namespace, children=[option_5], properties=frozenset({"standard"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2, optiondescription_4], properties=frozenset({"standard"}))
option_8 = StrOption(name="variable", doc="a variable", default="rougail", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_7 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_8], properties=frozenset({"standard"}))
option_10 = StrOption(name="variable", doc="a variable", default=Calculation(func['jinja_to_function'], Params((), kwargs={'__internal_jinja': ParamValue("default_2.extra.variable"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/00_9extra/dictionaries/extra/00-base.yml']), '__internal_attribute': ParamValue("default"), '__internal_variable': ParamValue("2.extra.variable")})), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_9 = OptionDescription(name="extra", doc="extra", group_type=groups.namespace, children=[option_10], properties=frozenset({"standard"}))
optiondescription_6 = OptionDescription(name="2", doc="2", children=[optiondescription_7, optiondescription_9], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_6])
