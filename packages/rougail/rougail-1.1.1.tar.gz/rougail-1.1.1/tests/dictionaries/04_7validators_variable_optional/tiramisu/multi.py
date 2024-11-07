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
dict_env['validators_1.rougail.general.int'] = "{% if _.int == int2 %}\nint and int2 must be different\n{% endif %}\n"
dict_env['validators_1.rougail.general.int_0'] = "{% if int3 is defined and _.int == int3 %}\nint and int3 must be different\n{% endif %}\n"
dict_env['validators_2.rougail.general.int'] = "{% if _.int == int2 %}\nint and int2 must be different\n{% endif %}\n"
dict_env['validators_2.rougail.general.int_0'] = "{% if int3 is defined and _.int == int3 %}\nint and int3 must be different\n{% endif %}\n"
option_5 = IntOption(name="int2", doc="a second number", default=1, properties=frozenset({"mandatory", "standard"}), informations={'type': 'number'})
option_4 = IntOption(name="int", doc="a first number", validators=[Calculation(func['valid_with_jinja'], Params((), kwargs={'__internal_jinja': ParamValue("validators_1.rougail.general.int"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/04_7validators_variable_optional/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("validators"), '__internal_variable': ParamValue("1.rougail.general.int"), 'int2': ParamOption(option_5), '_.int': ParamSelfOption(whole=False)})), Calculation(func['valid_with_jinja'], Params((), kwargs={'__internal_jinja': ParamValue("validators_1.rougail.general.int_0"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/04_7validators_variable_optional/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("validators"), '__internal_variable': ParamValue("1.rougail.general.int"), '_.int': ParamSelfOption(whole=False)}))], properties=frozenset({"basic", "mandatory"}), informations={'type': 'number', 'test': (5,)})
optiondescription_3 = OptionDescription(name="general", doc="a family", children=[option_4, option_5], properties=frozenset({"basic"}))
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_3], properties=frozenset({"basic"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"basic"}))
option_10 = IntOption(name="int2", doc="a second number", default=1, properties=frozenset({"mandatory", "standard"}), informations={'type': 'number'})
option_9 = IntOption(name="int", doc="a first number", validators=[Calculation(func['valid_with_jinja'], Params((), kwargs={'__internal_jinja': ParamValue("validators_2.rougail.general.int"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/04_7validators_variable_optional/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("validators"), '__internal_variable': ParamValue("2.rougail.general.int"), 'int2': ParamOption(option_10), '_.int': ParamSelfOption(whole=False)})), Calculation(func['valid_with_jinja'], Params((), kwargs={'__internal_jinja': ParamValue("validators_2.rougail.general.int_0"), '__internal_type': ParamValue("string"), '__internal_multi': ParamValue(False), '__internal_files': ParamValue(['tests/dictionaries/04_7validators_variable_optional/dictionaries/rougail/00-base.yml']), '__internal_attribute': ParamValue("validators"), '__internal_variable': ParamValue("2.rougail.general.int"), '_.int': ParamSelfOption(whole=False)}))], properties=frozenset({"basic", "mandatory"}), informations={'type': 'number', 'test': (5,)})
optiondescription_8 = OptionDescription(name="general", doc="a family", children=[option_9, option_10], properties=frozenset({"basic"}))
optiondescription_7 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[optiondescription_8], properties=frozenset({"basic"}))
optiondescription_6 = OptionDescription(name="2", doc="2", children=[optiondescription_7], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_6])
