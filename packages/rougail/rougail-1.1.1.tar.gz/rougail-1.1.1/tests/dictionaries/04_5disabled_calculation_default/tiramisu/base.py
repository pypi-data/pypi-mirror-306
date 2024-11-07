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
dict_env['default_rougail.var1'] = "{{ _.condition }}\n"
dict_env['disabled_rougail.var1'] = "{% if _.condition == \"yes\" %}\ncondition is yes\n{% endif %}\n"
dict_env['default_rougail.var2'] = "{{ rougail.condition }}\n"
dict_env['disabled_rougail.var2'] = "{% if rougail.condition == \"yes\" %}\ncondition is yes\n{% endif %}\n"
option_2 = StrOption(name="condition", doc="a condition", default="no", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_3 = StrOption(name="var1", doc="a first variable", default=Calculation(func['jinja_to_function'], Params((), kwargs={'__internal_jinja': ParamValue("default_rougail.var1"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/04_5disabled_calculation_default/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("default"), '__internal_variable': ParamValue("rougail.var1"), '_.condition': ParamOption(option_2, notraisepropertyerror=True)})), properties=frozenset({"mandatory", "standard", Calculation(func['jinja_to_property'], Params((ParamValue("disabled")), kwargs={'__internal_jinja': ParamValue("disabled_rougail.var1"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/04_5disabled_calculation_default/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("disabled"), '__internal_variable': ParamValue("rougail.var1"), 'when': ParamValue(True), 'inverse': ParamValue(False), '_.condition': ParamOption(option_2, notraisepropertyerror=True)}), help_function=func['jinja_to_property_help'])}), informations={'type': 'string'})
option_4 = StrOption(name="var2", doc="a second variable", default=Calculation(func['jinja_to_function'], Params((), kwargs={'__internal_jinja': ParamValue("default_rougail.var2"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/04_5disabled_calculation_default/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("default"), '__internal_variable': ParamValue("rougail.var2"), 'rougail.condition': ParamOption(option_2, notraisepropertyerror=True)})), properties=frozenset({"mandatory", "standard", Calculation(func['jinja_to_property'], Params((ParamValue("disabled")), kwargs={'__internal_jinja': ParamValue("disabled_rougail.var2"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/04_5disabled_calculation_default/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("disabled"), '__internal_variable': ParamValue("rougail.var2"), 'when': ParamValue(True), 'inverse': ParamValue(False), 'rougail.condition': ParamOption(option_2, notraisepropertyerror=True)}), help_function=func['jinja_to_property_help'])}), informations={'type': 'string'})
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_2, option_3, option_4], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
