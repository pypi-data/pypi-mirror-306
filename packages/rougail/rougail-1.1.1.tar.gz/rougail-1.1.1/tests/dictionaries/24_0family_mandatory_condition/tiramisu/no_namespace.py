from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
dict_env['mandatory_var'] = "{% if _.condition == \"yes\" %}\ncondition is yes\n{% endif %}\n"
option_1 = StrOption(name="condition", doc="a condition", default="no", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_2 = StrOption(name="var", doc="a variable", properties=frozenset({"standard", Calculation(func['jinja_to_property'], Params((ParamValue("mandatory")), kwargs={'__internal_jinja': ParamValue("mandatory_var"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/24_0family_mandatory_condition/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("mandatory"), '__internal_variable': ParamValue("var"), 'when': ParamValue(True), 'inverse': ParamValue(False), '_.condition': ParamOption(option_1, notraisepropertyerror=True)}), help_function=func['jinja_to_property_help'])}), informations={'type': 'string'})
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[option_1, option_2])
