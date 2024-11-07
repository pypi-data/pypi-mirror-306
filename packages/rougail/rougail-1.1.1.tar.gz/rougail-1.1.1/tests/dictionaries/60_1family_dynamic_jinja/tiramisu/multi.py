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
dict_env['dynamic_1.rougail.dyn{{ identifier }}'] = "{% for val in _.var %}\n{{ loop.index }}\n{% endfor %}\n"
dict_env['dynamic_2.rougail.dyn{{ identifier }}'] = "{% for val in _.var %}\n{{ loop.index }}\n{% endfor %}\n"
option_3 = StrOption(name="var", doc="a suffix variable", multi=True, default=["val1", "val2"], default_multi="val1", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_5 = StrOption(name="var", doc="a dynamic variable", default="val", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_4 = ConvertDynOptionDescription(name="dyn{{ identifier }}", doc="A dynamic family", identifiers=Calculation(func['jinja_to_function'], Params((), kwargs={'__internal_jinja': ParamValue("dynamic_1.rougail.dyn{{ identifier }}"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(True), '__internal_files': ParamValue(['tests/dictionaries/60_1family_dynamic_jinja/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("dynamic"), '__internal_variable': ParamValue("1.rougail.dyn{{ identifier }}"), '_.var': ParamOption(option_3, notraisepropertyerror=True)})), children=[option_5], properties=frozenset({"standard"}))
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_3, optiondescription_4], properties=frozenset({"standard"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"standard"}))
option_8 = StrOption(name="var", doc="a suffix variable", multi=True, default=["val1", "val2"], default_multi="val1", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_10 = StrOption(name="var", doc="a dynamic variable", default="val", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_9 = ConvertDynOptionDescription(name="dyn{{ identifier }}", doc="A dynamic family", identifiers=Calculation(func['jinja_to_function'], Params((), kwargs={'__internal_jinja': ParamValue("dynamic_2.rougail.dyn{{ identifier }}"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(True), '__internal_files': ParamValue(['tests/dictionaries/60_1family_dynamic_jinja/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("dynamic"), '__internal_variable': ParamValue("2.rougail.dyn{{ identifier }}"), '_.var': ParamOption(option_8, notraisepropertyerror=True)})), children=[option_10], properties=frozenset({"standard"}))
optiondescription_7 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_8, optiondescription_9], properties=frozenset({"standard"}))
optiondescription_6 = OptionDescription(name="2", doc="2", children=[optiondescription_7], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_6])
