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
dict_env['choices_1.rougail.var'] = "{% for n in trange(0, 10) %}\n{{ n }}\n{% endfor %}\n"
dict_env['choices_2.rougail.var'] = "{% for n in trange(0, 10) %}\n{{ n }}\n{% endfor %}\n"
option_3 = ChoiceOption(name="var", doc="a variable", values=Calculation(func['jinja_to_function'], Params((), kwargs={'__internal_jinja': ParamValue("choices_1.rougail.var"), '__internal_type': ParamValue("number"), '__internal_multi': ParamValue(True), '__internal_files': ParamValue(['tests/dictionaries/00_6choice_calculation/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("choices"), '__internal_variable': ParamValue("1.rougail.var")})), default=9, properties=frozenset({"mandatory", "standard"}), informations={'type': 'choice'})
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_3], properties=frozenset({"standard"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"standard"}))
option_6 = ChoiceOption(name="var", doc="a variable", values=Calculation(func['jinja_to_function'], Params((), kwargs={'__internal_jinja': ParamValue("choices_2.rougail.var"), '__internal_type': ParamValue("number"), '__internal_multi': ParamValue(True), '__internal_files': ParamValue(['tests/dictionaries/00_6choice_calculation/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("choices"), '__internal_variable': ParamValue("2.rougail.var")})), default=9, properties=frozenset({"mandatory", "standard"}), informations={'type': 'choice'})
optiondescription_5 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_6], properties=frozenset({"standard"}))
optiondescription_4 = OptionDescription(name="2", doc="2", children=[optiondescription_5], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_4])
