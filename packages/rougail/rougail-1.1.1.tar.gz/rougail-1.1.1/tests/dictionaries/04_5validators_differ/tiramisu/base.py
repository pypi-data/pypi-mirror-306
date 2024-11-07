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
dict_env['validators_rougail.var1'] = "{% if _.var1 == _.var2 %}\nvar1 must be different than var2\n{% endif %}\n"
option_3 = StrOption(name="var2", doc="A second variable", default="no", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_2 = StrOption(name="var1", doc="a first variable", default="oui", validators=[Calculation(func['valid_with_jinja'], Params((), kwargs={'__internal_jinja': ParamValue("validators_rougail.var1"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/04_5validators_differ/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("validators"), '__internal_variable': ParamValue("rougail.var1"), '_.var2': ParamOption(option_3, notraisepropertyerror=True), '_.var1': ParamSelfOption(whole=False)}))], properties=frozenset({"mandatory", "standard"}), informations={'type': 'string', 'test': ('another_value',)})
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_2, option_3], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
