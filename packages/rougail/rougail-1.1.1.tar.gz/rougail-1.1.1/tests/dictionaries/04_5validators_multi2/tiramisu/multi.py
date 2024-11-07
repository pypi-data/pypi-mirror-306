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
dict_env['validators_1.rougail.var1'] = "{% if values | length > 2 %}\nlength must be less than 3\n{% endif %}\n"
dict_env['validators_2.rougail.var1'] = "{% if values | length > 2 %}\nlength must be less than 3\n{% endif %}\n"
option_3 = StrOption(name="var1", doc="a second variable", multi=True, default=["no", "yes"], default_multi="no", validators=[Calculation(func['valid_with_jinja'], Params((), kwargs={'__internal_jinja': ParamValue("validators_1.rougail.var1"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/04_5validators_multi2/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("validators"), '__internal_variable': ParamValue("1.rougail.var1"), 'values': ParamSelfOption(whole=True)}))], properties=frozenset({"mandatory", "standard"}), informations={'type': 'string', 'test': ('val1', 'val2')})
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_3], properties=frozenset({"standard"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"standard"}))
option_6 = StrOption(name="var1", doc="a second variable", multi=True, default=["no", "yes"], default_multi="no", validators=[Calculation(func['valid_with_jinja'], Params((), kwargs={'__internal_jinja': ParamValue("validators_2.rougail.var1"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/04_5validators_multi2/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("validators"), '__internal_variable': ParamValue("2.rougail.var1"), 'values': ParamSelfOption(whole=True)}))], properties=frozenset({"mandatory", "standard"}), informations={'type': 'string', 'test': ('val1', 'val2')})
optiondescription_5 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_6], properties=frozenset({"standard"}))
optiondescription_4 = OptionDescription(name="2", doc="2", children=[optiondescription_5], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_4])
