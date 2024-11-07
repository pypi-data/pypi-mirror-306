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
dict_env['default_rougail.dyn{{ identifier }}.var'] = "{% for val in __.var %}\nt{{ val }}\n{% endfor %}\n"
dict_env['default_rougail.dyn{{ identifier }}.dyn_{{ identifier }}.var_identifiers'] = "{{ s1 }}-{{ s2 }}\n"
option_2 = StrOption(name="var", doc="A identifier variable", multi=True, default=["val1", "val2"], default_multi="val1", properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_4 = StrOption(name="var", doc="A dynamic variable", multi=True, default=Calculation(func['jinja_to_function'], Params((), kwargs={'__internal_jinja': ParamValue("default_rougail.dyn{{ identifier }}.var"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(True), '__internal_files': ParamValue(['tests/dictionaries/60_6family_dynamic_sub_dynamic/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("default"), '__internal_variable': ParamValue("rougail.dyn{{ identifier }}.var"), '__.var': ParamOption(option_2, notraisepropertyerror=True)})), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_6 = StrOption(name="var", doc="A variable dynamic", default=Calculation(func['calc_value'], Params((ParamIdentifier()))), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_7 = StrOption(name="var_identifier", doc="identifier from first family", default=Calculation(func['calc_value'], Params((ParamIdentifier(identifier_index=0)))), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
option_8 = StrOption(name="var_identifiers", doc="merge identifiers", default=Calculation(func['jinja_to_function'], Params((), kwargs={'__internal_jinja': ParamValue("default_rougail.dyn{{ identifier }}.dyn_{{ identifier }}.var_identifiers"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/60_6family_dynamic_sub_dynamic/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("default"), '__internal_variable': ParamValue("rougail.dyn{{ identifier }}.dyn_{{ identifier }}.var_identifiers"), 's1': ParamIdentifier(identifier_index=0), 's2': ParamIdentifier(identifier_index=1)})), properties=frozenset({"mandatory", "standard"}), informations={'type': 'string'})
optiondescription_5 = ConvertDynOptionDescription(name="dyn_{{ identifier }}", doc="a Second dynamic variable", identifiers=Calculation(func['calc_value'], Params((ParamOption(option_4)))), children=[option_6, option_7, option_8], properties=frozenset({"standard"}), informations={'dynamic_variable': 'rougail.dyn{{ identifier }}.var'})
optiondescription_3 = ConvertDynOptionDescription(name="dyn{{ identifier }}", doc="A dynamic family", identifiers=Calculation(func['calc_value'], Params((ParamOption(option_2)))), children=[option_4, optiondescription_5], properties=frozenset({"standard"}), informations={'dynamic_variable': 'rougail.var'})
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_2, optiondescription_3], properties=frozenset({"standard"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
