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
dict_env['default_rougail.var2'] = "{{ _.dynval1.family.var }}\n"
option_2 = StrOption(name="var1", doc="a suffix variable", multi=True, default=["val1", "val2"], default_multi="val1", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_5 = StrOption(name="var", doc="with a variable", properties=frozenset({"basic", "mandatory"}), informations={'type': 'string'})
optiondescription_4 = OptionDescription(name="family", doc="a family", children=[option_5], properties=frozenset({"basic"}))
optiondescription_3 = ConvertDynOptionDescription(name="dyn{{ identifier }}", doc="a dynamic family", identifiers=Calculation(func['calc_value'], Params((ParamOption(option_2)))), children=[optiondescription_4], properties=frozenset({"basic"}), informations={'dynamic_variable': 'rougail.var1'})
option_6 = StrOption(name="var2", doc="a second variable", default=Calculation(func['jinja_to_function'], Params((), kwargs={'__internal_jinja': ParamValue("default_rougail.var2"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/60_2family_dynamic_jinja_fill_sub_group/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("default"), '__internal_variable': ParamValue("rougail.var2"), '_.dynval1.family.var': ParamDynOption(option_5, ["val1"], notraisepropertyerror=True)})), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_2, optiondescription_3, option_6], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
