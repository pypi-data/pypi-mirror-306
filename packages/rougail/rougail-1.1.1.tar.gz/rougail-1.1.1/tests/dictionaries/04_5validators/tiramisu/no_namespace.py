from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
dict_env['validators_int'] = "{% if _.int > 100 %}\nvalue is too high\n{% endif %}\n"
option_1 = IntOption(name="int", doc="A number", validators=[Calculation(func['valid_with_jinja'], Params((), kwargs={'__internal_jinja': ParamValue("validators_int"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/04_5validators/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("validators"), '__internal_variable': ParamValue("int"), '_.int': ParamSelfOption(whole=False)}))], properties=frozenset({"basic", "mandatory"}), informations={'type': 'number'})
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[option_1])
