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
option_3 = ChoiceOption(name="var1", doc="the first variable", values=("a", "b", "c"), properties=frozenset({"basic", "mandatory"}), informations={'type': 'choice'})
option_4 = ChoiceOption(name="var2", doc="the second variable", values=("a", "b", "c"), properties=frozenset({"basic", "mandatory"}), informations={'type': 'choice'})
option_5 = ChoiceOption(name="var3", doc="the third variable", values=("a", "b", "c", None), properties=frozenset({"standard"}), informations={'type': 'choice'})
option_6 = ChoiceOption(name="var4", doc="the forth variable", values=(None, "b", "c"), properties=frozenset({"standard"}), informations={'type': 'choice'})
option_7 = ChoiceOption(name="var5", doc="the fifth variable", values=("a", "b", "c"), default="a", properties=frozenset({"mandatory", "standard"}), informations={'type': 'choice'})
option_8 = ChoiceOption(name="var6", doc="the sixth variable", values=(1, 2, 3), default=1, properties=frozenset({"mandatory", "standard"}), informations={'type': 'choice'})
optiondescription_2 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_3, option_4, option_5, option_6, option_7, option_8], properties=frozenset({"basic"}))
optiondescription_1 = OptionDescription(name="1", doc="1", children=[optiondescription_2], properties=frozenset({"basic"}))
option_11 = ChoiceOption(name="var1", doc="the first variable", values=("a", "b", "c"), properties=frozenset({"basic", "mandatory"}), informations={'type': 'choice'})
option_12 = ChoiceOption(name="var2", doc="the second variable", values=("a", "b", "c"), properties=frozenset({"basic", "mandatory"}), informations={'type': 'choice'})
option_13 = ChoiceOption(name="var3", doc="the third variable", values=("a", "b", "c", None), properties=frozenset({"standard"}), informations={'type': 'choice'})
option_14 = ChoiceOption(name="var4", doc="the forth variable", values=(None, "b", "c"), properties=frozenset({"standard"}), informations={'type': 'choice'})
option_15 = ChoiceOption(name="var5", doc="the fifth variable", values=("a", "b", "c"), default="a", properties=frozenset({"mandatory", "standard"}), informations={'type': 'choice'})
option_16 = ChoiceOption(name="var6", doc="the sixth variable", values=(1, 2, 3), default=1, properties=frozenset({"mandatory", "standard"}), informations={'type': 'choice'})
optiondescription_10 = OptionDescription(name="rougail", doc="Rougail", group_type=groups.namespace, children=[option_11, option_12, option_13, option_14, option_15, option_16], properties=frozenset({"basic"}))
optiondescription_9 = OptionDescription(name="2", doc="2", children=[optiondescription_10], properties=frozenset({"basic"}))
option_0 = OptionDescription(name="baseoption", doc="baseoption", children=[optiondescription_1, optiondescription_9])
