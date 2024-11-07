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
dict_env['dynamic_rougail.dyn{{ identifier }}'] = "{% for val in _.var %}\n{{ loop.index }}\n{% endfor %}\n"
option_2 = StrOption(name="var", doc="a suffix variable", multi=True, default=["val1", "val2"], default_multi="val1", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_4 = StrOption(name="var", doc="a dynamic variable", default="val", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_3 = ConvertDynOptionDescription(name="dyn{{ identifier }}", doc="A dynamic family", identifiers=Calculation(func['jinja_to_function'], Params((), kwargs={'__internal_jinja': ParamValue("dynamic_rougail.dyn{{ identifier }}"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(True), '__internal_files': ParamValue(['tests/dictionaries/60_1family_dynamic_jinja/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("dynamic"), '__internal_variable': ParamValue("rougail.dyn{{ identifier }}"), '_.var': ParamOption(option_2, notraisepropertyerror=True)})), children=[option_4], properties=frozenset({"standard"}))
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_2, optiondescription_3], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
