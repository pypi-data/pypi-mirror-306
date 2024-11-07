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
dict_env['default_1.rougail.leader.follower1'] = "{{ index }}"
dict_env['default_2.rougail.leader.follower1'] = "{{ index }}"
option_4 = StrOption(name="leader", doc="a leader", multi=True, default=["a", "b", "c"], properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_5 = IntOption(name="follower1", doc="a follower", multi=True, default=Calculation(func['jinja_to_function'], Params((), kwargs={'__internal_jinja': ParamValue("default_1.rougail.leader.follower1"), '__internal_type': ParamValue("number"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/40_2leadership_calculation_param_index/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("default"), '__internal_variable': ParamValue("1.rougail.leader.follower1"), 'index': ParamIndex()})), properties=frozenset({"mandatory", "standard"}), informations={'type': 'number'})
optiondescription_3 = Leadership(name="leader", doc="leadership", children=[option_4, option_5], properties=frozenset({"standard"}))
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_3], properties=frozenset({"standard"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"standard"}))
option_9 = StrOption(name="leader", doc="a leader", multi=True, default=["a", "b", "c"], properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_10 = IntOption(name="follower1", doc="a follower", multi=True, default=Calculation(func['jinja_to_function'], Params((), kwargs={'__internal_jinja': ParamValue("default_2.rougail.leader.follower1"), '__internal_type': ParamValue("number"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/40_2leadership_calculation_param_index/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("default"), '__internal_variable': ParamValue("2.rougail.leader.follower1"), 'index': ParamIndex()})), properties=frozenset({"mandatory", "standard"}), informations={'type': 'number'})
optiondescription_8 = Leadership(name="leader", doc="leadership", children=[option_9, option_10], properties=frozenset({"standard"}))
optiondescription_7 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_8], properties=frozenset({"standard"}))
optiondescription_6 = OptionDescription(name="2", doc="2", children=[optiondescription_7], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_6])
