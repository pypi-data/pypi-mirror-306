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
dict_env['disabled_1.rougail.leader.follower'] = "{% if rougail.condition == \"yes\" %}\ncondition is yes\n{% endif %}\n"
dict_env['disabled_2.rougail.leader.follower'] = "{% if rougail.condition == \"yes\" %}\ncondition is yes\n{% endif %}\n"
option_3 = BoolOption(name="condition", doc="a condition", default=True, properties=frozenset({"mandatory", "standard"}), informations={'type': 'boolean'})
option_5 = StrOption(name="leader", doc="aleader", multi=True, default=["a"], properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_6 = StrOption(name="follower", doc="a follower", multi=True, properties=frozenset({"basic", "mandatory", Calculation(func['jinja_to_property'], Params((ParamValue("disabled")), kwargs={'__internal_jinja': ParamValue("disabled_1.rougail.leader.follower"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/44_4disabled_calcultion_follower/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("disabled"), '__internal_variable': ParamValue("1.rougail.leader.follower"), 'when': ParamValue(True), 'inverse': ParamValue(False), 'rougail.condition': ParamOption(option_3, notraisepropertyerror=True)}), help_function=func['jinja_to_property_help'])}), informations={'type': 'string'})
optiondescription_4 = Leadership(name="leader", doc="a leadership", children=[option_5, option_6], properties=frozenset({"basic"}))
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_3, optiondescription_4], properties=frozenset({"basic"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"basic"}))
option_9 = BoolOption(name="condition", doc="a condition", default=True, properties=frozenset({"mandatory", "standard"}), informations={'type': 'boolean'})
option_11 = StrOption(name="leader", doc="aleader", multi=True, default=["a"], properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_12 = StrOption(name="follower", doc="a follower", multi=True, properties=frozenset({"basic", "mandatory", Calculation(func['jinja_to_property'], Params((ParamValue("disabled")), kwargs={'__internal_jinja': ParamValue("disabled_2.rougail.leader.follower"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/44_4disabled_calcultion_follower/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("disabled"), '__internal_variable': ParamValue("2.rougail.leader.follower"), 'when': ParamValue(True), 'inverse': ParamValue(False), 'rougail.condition': ParamOption(option_9, notraisepropertyerror=True)}), help_function=func['jinja_to_property_help'])}), informations={'type': 'string'})
optiondescription_10 = Leadership(name="leader", doc="a leadership", children=[option_11, option_12], properties=frozenset({"basic"}))
optiondescription_8 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_9, optiondescription_10], properties=frozenset({"basic"}))
optiondescription_7 = OptionDescription(name="2", doc="2", children=[optiondescription_8], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_7])
