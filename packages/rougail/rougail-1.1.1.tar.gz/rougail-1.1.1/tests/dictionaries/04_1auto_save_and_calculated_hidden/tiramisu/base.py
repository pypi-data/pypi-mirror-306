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
dict_env['default_rougail.var2'] = "yes"
dict_env['hidden_rougail.var2'] = "{% if _.var1 == \"yes\" %}\n_.var1 is yes\n{% endif %}\n"
dict_env['frozen_rougail.var2'] = "{% if _.var1 == \"yes\" %}\n_.var1 is yes\n{% endif %}\n"
option_2 = StrOption(name="var1", doc="a first variable", default="no", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_3 = StrOption(name="var2", doc="a second variable", default=Calculation(func['jinja_to_function'], Params((), kwargs={'__internal_jinja': ParamValue("default_rougail.var2"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/04_1auto_save_and_calculated_hidden/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("default"), '__internal_variable': ParamValue("rougail.var2")})), properties=frozenset({"basic", "force_store_value", "mandatory", Calculation(func['jinja_to_property'], Params((ParamValue("hidden")), kwargs={'__internal_jinja': ParamValue("hidden_rougail.var2"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/04_1auto_save_and_calculated_hidden/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("hidden"), '__internal_variable': ParamValue("rougail.var2"), 'when': ParamValue(True), 'inverse': ParamValue(False), '_.var1': ParamOption(option_2, notraisepropertyerror=True)}), help_function=func['jinja_to_property_help']), Calculation(func['jinja_to_property'], Params((ParamValue("frozen")), kwargs={'__internal_jinja': ParamValue("frozen_rougail.var2"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/04_1auto_save_and_calculated_hidden/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("frozen"), '__internal_variable': ParamValue("rougail.var2"), 'when': ParamValue(True), 'inverse': ParamValue(False), '_.var1': ParamOption(option_2, notraisepropertyerror=True)}), help_function=func['jinja_to_property_help'])}), informations={'type': 'string'})
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_2, option_3], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
