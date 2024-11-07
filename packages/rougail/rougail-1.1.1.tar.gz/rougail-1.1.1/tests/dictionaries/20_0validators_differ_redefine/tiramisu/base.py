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
dict_env['validators_rougail.var3'] = "{% if _.var3 == _.var2 %}\nvar3 must be different than var2\n{% endif %}\n"
option_2 = StrOption(name="var1", doc="a first variable", default="no", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_3 = StrOption(name="var2", doc="a second variable", default="no", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_4 = StrOption(name="var3", doc="a third variable", default="yes", validators=[Calculation(func['valid_with_jinja'], Params((), kwargs={'__internal_jinja': ParamValue("validators_rougail.var3"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/20_0validators_differ_redefine/dictionaries/rougail/01-base.yml']), '__internal_attribute': ParamValue("validators"), '__internal_variable': ParamValue("rougail.var3"), '_.var3': ParamSelfOption(whole=False), '_.var2': ParamOption(option_3, notraisepropertyerror=True)}))], properties=frozenset({"mandatory", "standard"}), informations={'type': 'string', 'test': ('yes',)})
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_2, option_3, option_4], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
