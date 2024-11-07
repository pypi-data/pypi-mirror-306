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
dict_env['default_1.rougail.var2'] = "{%- for v in var %}\n{{ v }}\n{%- endfor -%}"
dict_env['default_2.rougail.var2'] = "{%- for v in var %}\n{{ v }}\n{%- endfor -%}"
option_3 = StrOption(name="var", doc="a suffix variable", multi=True, default=["val1", "val2"], default_multi="val1", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_5 = StrOption(name="var", doc="a variable inside a dynamic family", default=Calculation(func['calc_value'], Params((ParamIdentifier()))), properties=frozenset({"standard"}), informations={'type': 'string'})
optiondescription_4 = ConvertDynOptionDescription(name="my_dyn_family_{{ identifier }}", doc="a dynamic family", identifiers=Calculation(func['calc_value'], Params((ParamOption(option_3)))), children=[option_5], properties=frozenset({"standard"}), informations={'dynamic_variable': '1.rougail.var'})
option_6 = StrOption(name="var2", doc="a variable", multi=True, default=Calculation(func['jinja_to_function'], Params((), kwargs={'__internal_jinja': ParamValue("default_1.rougail.var2"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(True), '__internal_files': ParamValue(['tests/dictionaries/60_5family_dynamic_variable_outside_jinja/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("default"), '__internal_variable': ParamValue("1.rougail.var2"), 'var': ParamOption(option_5)})), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_3, optiondescription_4, option_6], properties=frozenset({"standard"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"standard"}))
option_9 = StrOption(name="var", doc="a suffix variable", multi=True, default=["val1", "val2"], default_multi="val1", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_11 = StrOption(name="var", doc="a variable inside a dynamic family", default=Calculation(func['calc_value'], Params((ParamIdentifier()))), properties=frozenset({"standard"}), informations={'type': 'string'})
optiondescription_10 = ConvertDynOptionDescription(name="my_dyn_family_{{ identifier }}", doc="a dynamic family", identifiers=Calculation(func['calc_value'], Params((ParamOption(option_9)))), children=[option_11], properties=frozenset({"standard"}), informations={'dynamic_variable': '2.rougail.var'})
option_12 = StrOption(name="var2", doc="a variable", multi=True, default=Calculation(func['jinja_to_function'], Params((), kwargs={'__internal_jinja': ParamValue("default_2.rougail.var2"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(True), '__internal_files': ParamValue(['tests/dictionaries/60_5family_dynamic_variable_outside_jinja/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("default"), '__internal_variable': ParamValue("2.rougail.var2"), 'var': ParamOption(option_11)})), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_8 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_9, optiondescription_10, option_12], properties=frozenset({"standard"}))
optiondescription_7 = OptionDescription(name="2", doc="2", children=[optiondescription_8], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_7])
