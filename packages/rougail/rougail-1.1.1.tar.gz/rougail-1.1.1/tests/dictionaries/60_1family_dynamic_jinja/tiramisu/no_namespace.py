from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
dict_env['dynamic_dyn{{ identifier }}'] = "{% for val in _.var %}\n{{ loop.index }}\n{% endfor %}\n"
option_1 = StrOption(name="var", doc="a suffix variable", multi=True, default=["val1", "val2"], default_multi="val1", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_3 = StrOption(name="var", doc="a dynamic variable", default="val", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_2 = ConvertDynOptionDescription(name="dyn{{ identifier }}", doc="A dynamic family", identifiers=Calculation(func['jinja_to_function'], Params((), kwargs={'__internal_jinja': ParamValue("dynamic_dyn{{ identifier }}"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(True), '__internal_files': ParamValue(['tests/dictionaries/60_1family_dynamic_jinja/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("dynamic"), '__internal_variable': ParamValue("dyn{{ identifier }}"), '_.var': ParamOption(option_1, notraisepropertyerror=True)})), children=[option_3], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[option_1, optiondescription_2])
