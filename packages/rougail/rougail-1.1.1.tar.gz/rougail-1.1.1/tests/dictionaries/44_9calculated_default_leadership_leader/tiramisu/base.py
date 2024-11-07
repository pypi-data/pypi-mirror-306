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
dict_env['disabled_rougail.leader.follower'] = "{% if _.leader == \"a\" %}\nthe value of \"leader\" is \"a\"\n{% endif %}\n"
option_3 = StrOption(name="leader", doc="a leader", multi=True, default=["a", "b"], properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_4 = StrOption(name="follower", doc="a follower", multi=True, default=Calculation(func['calc_value'], Params((ParamOption(option_3)))), properties=frozenset({"mandatory", "standard", Calculation(func['jinja_to_property'], Params((ParamValue("disabled")), kwargs={'__internal_jinja': ParamValue("disabled_rougail.leader.follower"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/44_9calculated_default_leadership_leader/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("disabled"), '__internal_variable': ParamValue("rougail.leader.follower"), 'when': ParamValue(True), 'inverse': ParamValue(False), '_.leader': ParamOption(option_3, notraisepropertyerror=True)}), help_function=func['jinja_to_property_help'])}), informations={'type': 'string'})
optiondescription_2 = Leadership(name="leader", doc="leader", children=[option_3, option_4], properties=frozenset({"standard"}))
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_2], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
