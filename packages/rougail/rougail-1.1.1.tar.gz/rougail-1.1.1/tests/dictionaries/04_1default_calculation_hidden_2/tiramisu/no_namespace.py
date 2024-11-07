from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
dict_env['default_var3'] = "{% if _.var2 is propertyerror %}\nvalue\n{% endif %}\n"
option_1 = StrOption(name="var1", doc="a first variable", default="value", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_2 = StrOption(name="var2", doc="a second variable", properties=frozenset({"basic", "mandatory", Calculation(func['variable_to_property'], Params((ParamValue("disabled"), ParamOption(option_1)), kwargs={'when': ParamValue("value"), 'inverse': ParamValue(False)}), help_function=func['variable_to_property'])}), informations={'type': 'string'})
option_3 = StrOption(name="var3", doc="a third variable", default=Calculation(func['jinja_to_function'], Params((), kwargs={'__internal_jinja': ParamValue("default_var3"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/04_1default_calculation_hidden_2/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("default"), '__internal_variable': ParamValue("var3"), '_.var2': ParamOption(option_2, notraisepropertyerror=True)})), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[option_1, option_2, option_3])
