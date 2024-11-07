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
dict_env['choices_rougail.var'] = "{% for n in trange(0, 10) %}\n{{ n }}\n{% endfor %}\n"
option_2 = ChoiceOption(name="var", doc="a variable", values=Calculation(func['jinja_to_function'], Params((), kwargs={'__internal_jinja': ParamValue("choices_rougail.var"), '__internal_type': ParamValue("number"), '__internal_multi': ParamValue(True), '__internal_files': ParamValue(['tests/dictionaries/00_6choice_calculation/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("choices"), '__internal_variable': ParamValue("rougail.var")})), default=9, properties=frozenset({"mandatory", "standard"}), informations={'type': 'choice'})
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_2], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
