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
dict_env['default_1.rougail.var2'] = "{{ information }}\n"
dict_env['default_2.rougail.var2'] = "{{ information }}\n"
option_3 = StrOption(name="var1", doc="a first variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_4 = StrOption(name="var2", doc="a second variable", default=Calculation(func['jinja_to_function'], Params((), kwargs={'__internal_jinja': ParamValue("default_1.rougail.var2"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/00_9default_calculation_information_other_variable/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("default"), '__internal_variable': ParamValue("1.rougail.var2"), 'information': ParamInformation("test_information", None, option=option_3)})), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_3, option_4], properties=frozenset({"basic"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"basic"}))
option_7 = StrOption(name="var1", doc="a first variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
option_8 = StrOption(name="var2", doc="a second variable", default=Calculation(func['jinja_to_function'], Params((), kwargs={'__internal_jinja': ParamValue("default_2.rougail.var2"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/00_9default_calculation_information_other_variable/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("default"), '__internal_variable': ParamValue("2.rougail.var2"), 'information': ParamInformation("test_information", None, option=option_7)})), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_6 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_7, option_8], properties=frozenset({"basic"}))
optiondescription_5 = OptionDescription(name="2", doc="2", children=[optiondescription_6], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_5])
