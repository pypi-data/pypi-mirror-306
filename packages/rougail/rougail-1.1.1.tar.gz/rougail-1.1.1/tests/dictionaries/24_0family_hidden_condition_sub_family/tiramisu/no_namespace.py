from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
dict_env['frozen_family.subfamily.var1'] = "{% if _.condition == \"yes\" %}\ncondition is yes\n{% endif %}\n"
dict_env['hidden_family'] = "{% if _.condition == \"yes\" %}\ncondition is yes\n{% endif %}\n"
option_1 = StrOption(name="condition", doc="the variable use has condition", default="no", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_4 = StrOption(name="var1", doc="a variable", properties=frozenset({"basic", "force_default_on_freeze", "mandatory", Calculation(func['jinja_to_property'], Params((ParamValue("frozen")), kwargs={'__internal_jinja': ParamValue("frozen_family.subfamily.var1"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/24_0family_hidden_condition_sub_family/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("frozen"), '__internal_variable': ParamValue("family.subfamily.var1"), 'when': ParamValue(True), 'inverse': ParamValue(False), '_.condition': ParamOption(option_1, notraisepropertyerror=True)}), help_function=func['jinja_to_property_help'])}), informations={'type': 'string'})
optiondescription_3 = OptionDescription(name="subfamily", doc="subfamily", children=[option_4], properties=frozenset({"basic"}))
optiondescription_2 = OptionDescription(name="family", doc="possibly hidden family", children=[optiondescription_3], properties=frozenset({"basic", Calculation(func['jinja_to_property'], Params((ParamValue("hidden")), kwargs={'__internal_jinja': ParamValue("hidden_family"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/24_0family_hidden_condition_sub_family/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("hidden"), '__internal_variable': ParamValue("family"), 'when': ParamValue(True), 'inverse': ParamValue(False), '_.condition': ParamOption(option_1, notraisepropertyerror=True)}), help_function=func['jinja_to_property_help'])}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[option_1, optiondescription_2])
