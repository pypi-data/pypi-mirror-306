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
dict_env['disabled_1.rougail.{{ identifier }}_dyn.var4'] = "{% if 'val4' not in __.var %}\nval4 is not a valid value\n{% endif %}\n"
dict_env['disabled_2.rougail.{{ identifier }}_dyn.var4'] = "{% if 'val4' not in __.var %}\nval4 is not a valid value\n{% endif %}\n"
option_3 = StrOption(name="var", doc="a suffix variable", multi=True, default=["val1", "val2"], default_multi="val1", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string', 'test': ('val1', 'val2', 'val3', 'val4')})
option_5 = StrOption(name="var1", doc="a variable 1", default=Calculation(func['calc_value'], Params((ParamIdentifier()))), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_6 = StrOption(name="var2", doc="a variable 2", default=Calculation(func['calc_value'], Params((ParamOption(option_5)))), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_7 = StrOption(name="var3", doc="a variable 3", default=Calculation(func['calc_value'], Params((ParamOption(option_5)))), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_8 = StrOption(name="var4", doc="a variable 4", default=Calculation(func['calc_value'], Params((ParamDynOption(option_5, ["val4"])))), properties=frozenset({"mandatory", "standard", Calculation(func['jinja_to_property'], Params((ParamValue("disabled")), kwargs={'__internal_jinja': ParamValue("disabled_1.rougail.{{ identifier }}_dyn.var4"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/60_5family_dynamic_unknown_suffix/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("disabled"), '__internal_variable': ParamValue("1.rougail.{{ identifier }}_dyn.var4"), 'when': ParamValue(True), 'inverse': ParamValue(False), '__.var': ParamOption(option_3, notraisepropertyerror=True)}), help_function=func['jinja_to_property_help'])}), informations={'type': 'string'})
optiondescription_4 = ConvertDynOptionDescription(name="{{ identifier }}_dyn", doc="a dynamic family", identifiers=Calculation(func['calc_value'], Params((ParamOption(option_3)))), children=[option_5, option_6, option_7, option_8], properties=frozenset({"standard"}), informations={'dynamic_variable': '1.rougail.var'})
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_3, optiondescription_4], properties=frozenset({"standard"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"standard"}))
option_11 = StrOption(name="var", doc="a suffix variable", multi=True, default=["val1", "val2"], default_multi="val1", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string', 'test': ('val1', 'val2', 'val3', 'val4')})
option_13 = StrOption(name="var1", doc="a variable 1", default=Calculation(func['calc_value'], Params((ParamIdentifier()))), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_14 = StrOption(name="var2", doc="a variable 2", default=Calculation(func['calc_value'], Params((ParamOption(option_13)))), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_15 = StrOption(name="var3", doc="a variable 3", default=Calculation(func['calc_value'], Params((ParamOption(option_13)))), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_16 = StrOption(name="var4", doc="a variable 4", default=Calculation(func['calc_value'], Params((ParamDynOption(option_13, ["val4"])))), properties=frozenset({"mandatory", "standard", Calculation(func['jinja_to_property'], Params((ParamValue("disabled")), kwargs={'__internal_jinja': ParamValue("disabled_2.rougail.{{ identifier }}_dyn.var4"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/60_5family_dynamic_unknown_suffix/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("disabled"), '__internal_variable': ParamValue("2.rougail.{{ identifier }}_dyn.var4"), 'when': ParamValue(True), 'inverse': ParamValue(False), '__.var': ParamOption(option_11, notraisepropertyerror=True)}), help_function=func['jinja_to_property_help'])}), informations={'type': 'string'})
optiondescription_12 = ConvertDynOptionDescription(name="{{ identifier }}_dyn", doc="a dynamic family", identifiers=Calculation(func['calc_value'], Params((ParamOption(option_11)))), children=[option_13, option_14, option_15, option_16], properties=frozenset({"standard"}), informations={'dynamic_variable': '2.rougail.var'})
optiondescription_10 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_11, optiondescription_12], properties=frozenset({"standard"}))
optiondescription_9 = OptionDescription(name="2", doc="2", children=[optiondescription_10], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_9])
