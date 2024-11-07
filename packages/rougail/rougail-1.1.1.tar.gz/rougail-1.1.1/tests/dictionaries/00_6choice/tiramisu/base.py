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
option_2 = ChoiceOption(name="var1", doc="the first variable", values=("a", "b", "c"), properties=frozenset({"basic", "mandatory"}), informations={'type': 'choice'})
option_3 = ChoiceOption(name="var2", doc="the second variable", values=("a", "b", "c"), properties=frozenset({"basic", "mandatory"}), informations={'type': 'choice'})
option_4 = ChoiceOption(name="var3", doc="the third variable", values=("a", "b", "c", None), properties=frozenset({"standard"}), informations={'type': 'choice'})
option_5 = ChoiceOption(name="var4", doc="the forth variable", values=(None, "b", "c"), properties=frozenset({"standard"}), informations={'type': 'choice'})
option_6 = ChoiceOption(name="var5", doc="the fifth variable", values=("a", "b", "c"), default="a", properties=frozenset({"mandatory", "standard"}), informations={'type': 'choice'})
option_7 = ChoiceOption(name="var6", doc="the sixth variable", values=(1, 2, 3), default=1, properties=frozenset({"mandatory", "standard"}), informations={'type': 'choice'})
optiondescription_1 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_2, option_3, option_4, option_5, option_6, option_7], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1])
