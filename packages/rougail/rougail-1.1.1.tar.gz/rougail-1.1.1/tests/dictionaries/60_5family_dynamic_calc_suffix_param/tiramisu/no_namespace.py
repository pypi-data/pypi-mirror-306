from tiramisu import *
from tiramisu.setting import ALLOWED_LEADER_PROPERTIES
from re import compile as re_compile
from rougail.tiramisu import func, dict_env, load_functions, ConvertDynOptionDescription
load_functions('tests/dictionaries/../eosfunc/test.py')
ALLOWED_LEADER_PROPERTIES.add("basic")
ALLOWED_LEADER_PROPERTIES.add("standard")
ALLOWED_LEADER_PROPERTIES.add("advanced")
dict_env['default_dyn{{ identifier }}.var'] = "{{ identifier }}\n"
option_1 = StrOption(name="var", doc="A identifier variable", multi=True, default=["val1", "val2"], default_multi="val1", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_3 = StrOption(name="var", doc="A dynamic variable", default=Calculation(func['jinja_to_function'], Params((), kwargs={'__internal_jinja': ParamValue("default_dyn{{ identifier }}.var"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/60_5family_dynamic_calc_suffix_param/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("default"), '__internal_variable': ParamValue("dyn{{ identifier }}.var"), 'identifier': ParamIdentifier()})), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_2 = ConvertDynOptionDescription(name="dyn{{ identifier }}", doc="A dynamic family", identifiers=Calculation(func['calc_value'], Params((ParamOption(option_1)))), children=[option_3], properties=frozenset({"standard"}), informations={'dynamic_variable': 'var'})
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[option_1, optiondescription_2])
