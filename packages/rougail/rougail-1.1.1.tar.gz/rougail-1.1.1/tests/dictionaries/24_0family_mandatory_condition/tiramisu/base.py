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
dict_env['mandatory_rougail.var'] = "{% if _.condition == \"yes\" %}\ncondition is yes\n{% endif %}\n"
option_2 = StrOption(name="condition", doc="a condition", default="no", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_3 = StrOption(name="var", doc="a variable", properties=frozenset({"standard", Calculation(func['jinja_to_property'], Params((ParamValue("mandatory")), kwargs={'__internal_jinja': ParamValue("mandatory_rougail.var"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/24_0family_mandatory_condition/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("mandatory"), '__internal_variable': ParamValue("rougail.var"), 'when': ParamValue(True), 'inverse': ParamValue(False), '_.condition': ParamOption(option_2, notraisepropertyerror=True)}), help_function=func['jinja_to_property_help'])}), informations={'type': 'string'})
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_2, option_3], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
