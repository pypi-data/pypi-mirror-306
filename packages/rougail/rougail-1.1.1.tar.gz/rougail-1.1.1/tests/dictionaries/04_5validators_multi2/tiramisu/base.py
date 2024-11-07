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
dict_env['validators_rougail.var1'] = "{% if values | length > 2 %}\nlength must be less than 3\n{% endif %}\n"
option_2 = StrOption(name="var1", doc="a second variable", multi=True, default=["no", "yes"], default_multi="no", validators=[Calculation(func['valid_with_jinja'], Params((), kwargs={'__internal_jinja': ParamValue("validators_rougail.var1"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/04_5validators_multi2/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("validators"), '__internal_variable': ParamValue("rougail.var1"), 'values': ParamSelfOption(whole=True)}))], properties=frozenset({"mandatory", "standard"}), informations={'type': 'string', 'test': ('val1', 'val2')})
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_2], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
