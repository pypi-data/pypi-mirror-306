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
dict_env['default_rougail.var1'] = "{% if var2 is defined %} {{ var2 }} {% elif var3 is defined %} {{ var3 }} {% elif var4 is defined %} {{ var4 }} {% else %} {{ _.var2 }} {% endif %} "
option_3 = StrOption(name="var2", doc="a second variable", default="no", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_2 = StrOption(name="var1", doc="a first variable", default=Calculation(func['jinja_to_function'], Params((), kwargs={'__internal_jinja': ParamValue("default_rougail.var1"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/00_9default_calculation_param_optional/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("default"), '__internal_variable': ParamValue("rougail.var1"), 'var2': ParamOption(option_3), '_.var2': ParamOption(option_3, notraisepropertyerror=True)})), properties=frozenset({"standard"}), informations={'type': 'string'})
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_2, option_3], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
