from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
dict_env['choices_var'] = "{% for item in trange(0, 10) %}\n{{ item }}\n{%- endfor %}\n"
option_1 = ChoiceOption(name="var", doc="a variable", values=Calculation(func['jinja_to_function'], Params((), kwargs={'__internal_jinja': ParamValue("choices_var"), '__internal_type': ParamValue("number"), '__internal_multi': ParamValue(True), '__internal_files': ParamValue(['tests/dictionaries/00_9default_integer/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("choices"), '__internal_variable': ParamValue("var")})), default=9, properties=frozenset({"mandatory", "standard"}), informations={'type': 'choice'})
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[option_1])
