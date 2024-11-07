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
dict_env['frozen_1.rougail.dyn{{ identifier }}.vardyn'] = "{% if _.var2 == \"no\" %}\nvar2 is no\n{% endif %}\n"
dict_env['hidden_1.rougail.dyn{{ identifier }}'] = "{% if _.var2 == \"no\" %}\nvar2 is no\n{% endif %}\n"
dict_env['frozen_2.rougail.dyn{{ identifier }}.vardyn'] = "{% if _.var2 == \"no\" %}\nvar2 is no\n{% endif %}\n"
dict_env['hidden_2.rougail.dyn{{ identifier }}'] = "{% if _.var2 == \"no\" %}\nvar2 is no\n{% endif %}\n"
option_3 = StrOption(name="var", doc="A suffix variable", multi=True, default=["val1", "val2"], default_multi="val1", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_4 = StrOption(name="var2", doc="a second variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_6 = StrOption(name="vardyn", doc="a dynamic variable", default="val", properties=frozenset({"force_default_on_freeze", "mandatory", "standard", Calculation(func['jinja_to_property'], Params((ParamValue("frozen")), kwargs={'__internal_jinja': ParamValue("frozen_1.rougail.dyn{{ identifier }}.vardyn"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/60_5family_dynamic_calc2/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("frozen"), '__internal_variable': ParamValue("1.rougail.dyn{{ identifier }}.vardyn"), 'when': ParamValue(True), 'inverse': ParamValue(False), '_.var2': ParamOption(option_4, notraisepropertyerror=True)}), help_function=func['jinja_to_property_help'])}), informations={'type': 'string'})
optiondescription_5 = ConvertDynOptionDescription(name="dyn{{ identifier }}", doc="A dynamic family", identifiers=Calculation(func['calc_value'], Params((ParamOption(option_3)))), children=[option_6], properties=frozenset({"standard", Calculation(func['jinja_to_property'], Params((ParamValue("hidden")), kwargs={'__internal_jinja': ParamValue("hidden_1.rougail.dyn{{ identifier }}"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/60_5family_dynamic_calc2/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("hidden"), '__internal_variable': ParamValue("1.rougail.dyn{{ identifier }}"), 'when': ParamValue(True), 'inverse': ParamValue(False), '_.var2': ParamOption(option_4, notraisepropertyerror=True)}), help_function=func['jinja_to_property_help'])}), informations={'dynamic_variable': '1.rougail.var'})
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_3, option_4, optiondescription_5], properties=frozenset({"basic"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"basic"}))
option_9 = StrOption(name="var", doc="A suffix variable", multi=True, default=["val1", "val2"], default_multi="val1", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_10 = StrOption(name="var2", doc="a second variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_12 = StrOption(name="vardyn", doc="a dynamic variable", default="val", properties=frozenset({"force_default_on_freeze", "mandatory", "standard", Calculation(func['jinja_to_property'], Params((ParamValue("frozen")), kwargs={'__internal_jinja': ParamValue("frozen_2.rougail.dyn{{ identifier }}.vardyn"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/60_5family_dynamic_calc2/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("frozen"), '__internal_variable': ParamValue("2.rougail.dyn{{ identifier }}.vardyn"), 'when': ParamValue(True), 'inverse': ParamValue(False), '_.var2': ParamOption(option_10, notraisepropertyerror=True)}), help_function=func['jinja_to_property_help'])}), informations={'type': 'string'})
optiondescription_11 = ConvertDynOptionDescription(name="dyn{{ identifier }}", doc="A dynamic family", identifiers=Calculation(func['calc_value'], Params((ParamOption(option_9)))), children=[option_12], properties=frozenset({"standard", Calculation(func['jinja_to_property'], Params((ParamValue("hidden")), kwargs={'__internal_jinja': ParamValue("hidden_2.rougail.dyn{{ identifier }}"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/60_5family_dynamic_calc2/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("hidden"), '__internal_variable': ParamValue("2.rougail.dyn{{ identifier }}"), 'when': ParamValue(True), 'inverse': ParamValue(False), '_.var2': ParamOption(option_10, notraisepropertyerror=True)}), help_function=func['jinja_to_property_help'])}), informations={'dynamic_variable': '2.rougail.var'})
optiondescription_8 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_9, option_10, optiondescription_11], properties=frozenset({"basic"}))
optiondescription_7 = OptionDescription(name="2", doc="2", children=[optiondescription_8], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_7])
