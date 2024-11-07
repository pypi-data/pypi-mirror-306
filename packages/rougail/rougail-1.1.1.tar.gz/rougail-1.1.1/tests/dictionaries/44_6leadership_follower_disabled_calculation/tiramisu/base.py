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
dict_env['disabled_rougail.leader.follower'] = "{% if __.condition == \"yes\" %}\ndisabled\n{% endif %}\n"
option_2 = StrOption(name="condition", doc="a condition", default="yes", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_4 = StrOption(name="leader", doc="a leader", multi=True, properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_5 = StrOption(name="follower", doc="a follower", multi=True, properties=frozenset({"basic", "mandatory", Calculation(func['jinja_to_property'], Params((ParamValue("disabled")), kwargs={'__internal_jinja': ParamValue("disabled_rougail.leader.follower"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/44_6leadership_follower_disabled_calculation/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("disabled"), '__internal_variable': ParamValue("rougail.leader.follower"), 'when': ParamValue(True), 'inverse': ParamValue(False), '__.condition': ParamOption(option_2, notraisepropertyerror=True)}), help_function=func['jinja_to_property_help'])}), informations={'type': 'string'})
optiondescription_3 = Leadership(name="leader", doc="a leadership", children=[option_4, option_5], properties=frozenset({"basic"}))
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_2, optiondescription_3], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
