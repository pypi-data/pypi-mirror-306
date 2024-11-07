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
dict_env['default_1.rougail.multi1'] = "{% if _.bool %}\nTrue\nFalse\n{% else %}\nFalse\n{% endif %}\n"
dict_env['default_1.rougail.multi2'] = "{% if not _.bool %}\nTrue\nFalse\n{% else %}\nFalse\n{% endif %}\n"
dict_env['default_2.rougail.multi1'] = "{% if _.bool %}\nTrue\nFalse\n{% else %}\nFalse\n{% endif %}\n"
dict_env['default_2.rougail.multi2'] = "{% if not _.bool %}\nTrue\nFalse\n{% else %}\nFalse\n{% endif %}\n"
option_3 = BoolOption(name="bool", doc="a boolean variable", default=False, properties=frozenset({"mandatory", "standard"}), informations={'type': 'boolean'})
option_4 = BoolOption(name="multi1", doc="a first multi variable", multi=True, default=Calculation(func['jinja_to_function'], Params((), kwargs={'__internal_jinja': ParamValue("default_1.rougail.multi1"), '__internal_type': ParamValue("boolean"), '__internal_multi': ParamValue(True), '__internal_files': ParamValue(['tests/dictionaries/40_8calculation_boolean/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("default"), '__internal_variable': ParamValue("1.rougail.multi1"), '_.bool': ParamOption(option_3, notraisepropertyerror=True)})), properties=frozenset({"mandatory", "standard"}), informations={'type': 'boolean'})
option_5 = BoolOption(name="multi2", doc="a second multi variable", multi=True, default=Calculation(func['jinja_to_function'], Params((), kwargs={'__internal_jinja': ParamValue("default_1.rougail.multi2"), '__internal_type': ParamValue("boolean"), '__internal_multi': ParamValue(True), '__internal_files': ParamValue(['tests/dictionaries/40_8calculation_boolean/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("default"), '__internal_variable': ParamValue("1.rougail.multi2"), '_.bool': ParamOption(option_3, notraisepropertyerror=True)})), properties=frozenset({"mandatory", "standard"}), informations={'type': 'boolean'})
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_3, option_4, option_5], properties=frozenset({"standard"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"standard"}))
option_8 = BoolOption(name="bool", doc="a boolean variable", default=False, properties=frozenset({"mandatory", "standard"}), informations={'type': 'boolean'})
option_9 = BoolOption(name="multi1", doc="a first multi variable", multi=True, default=Calculation(func['jinja_to_function'], Params((), kwargs={'__internal_jinja': ParamValue("default_2.rougail.multi1"), '__internal_type': ParamValue("boolean"), '__internal_multi': ParamValue(True), '__internal_files': ParamValue(['tests/dictionaries/40_8calculation_boolean/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("default"), '__internal_variable': ParamValue("2.rougail.multi1"), '_.bool': ParamOption(option_8, notraisepropertyerror=True)})), properties=frozenset({"mandatory", "standard"}), informations={'type': 'boolean'})
option_10 = BoolOption(name="multi2", doc="a second multi variable", multi=True, default=Calculation(func['jinja_to_function'], Params((), kwargs={'__internal_jinja': ParamValue("default_2.rougail.multi2"), '__internal_type': ParamValue("boolean"), '__internal_multi': ParamValue(True), '__internal_files': ParamValue(['tests/dictionaries/40_8calculation_boolean/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("default"), '__internal_variable': ParamValue("2.rougail.multi2"), '_.bool': ParamOption(option_8, notraisepropertyerror=True)})), properties=frozenset({"mandatory", "standard"}), informations={'type': 'boolean'})
optiondescription_7 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_8, option_9, option_10], properties=frozenset({"standard"}))
optiondescription_6 = OptionDescription(name="2", doc="2", children=[optiondescription_7], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_6])
