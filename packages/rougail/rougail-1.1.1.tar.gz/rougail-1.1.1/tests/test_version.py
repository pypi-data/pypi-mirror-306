from shutil import rmtree  # , copyfile, copytree
from os import getcwd, makedirs
from os.path import isfile, join, isdir
from pytest import fixture, raises
from os import listdir

from rougail import Rougail, RougailConfig
from rougail.error import DictConsistencyError

from ruamel.yaml import YAML

# dico_dirs = 'tests/data'
# test_ok = set()
# for test in listdir(dico_dirs):
#    if isdir(join(dico_dirs, test)):
#        test_ok.add(test)
# excludes = set([])
# test_ok -= excludes

# ORI_DIR = getcwd()

# test_ok = list(test_ok)
# test_ok.sort()
##print(test_ok)

# @fixture(scope="module", params=test_ok)
# def test_dir(request):
#    return request.param

"""
the kinematics are as follows:
- if no version attribute is defined in the yaml file, then the default version attribute of rougailconfig is taken
- if a version attribute is defined in the yaml file, this is the one that is taken
"""


def test_validate_default_version():
    "retrieves the default_dictionary_format_version if no version in the yaml file"

    RougailConfig["dictionaries_dir"] = ["tests/data/dict1"]
    RougailConfig["default_dictionary_format_version"] = "1.1"
    rougail = Rougail()
    config = rougail.get_config()

    filename = "tests/data/dict1/dict.yml"
    with open(filename, encoding="utf8") as file_fh:
        objects = YAML(typ="safe").load(file_fh)
    version = rougail.converted.validate_file_version(objects, filename)
    assert version == RougailConfig["default_dictionary_format_version"]


def test_validate_file_version_from_yml():
    "retrives the yaml file version defined in the yaml file"

    RougailConfig["dictionaries_dir"] = ["tests/data/dict2"]
    RougailConfig["default_dictionary_format_version"] = "1.1"
    rougail = Rougail()
    config = rougail.get_config()

    filename = "tests/data/dict2/dict.yml"
    with open(filename, encoding="utf8") as file_fh:
        objects = YAML(typ="safe").load(file_fh)
    version = rougail.converted.validate_file_version(objects, filename)
    assert version == "1.0"


def test_retrieve_version_from_config():

    RougailConfig["dictionaries_dir"] = ["tests/data/dict2"]
    RougailConfig["default_dictionary_format_version"] = "1.1"
    rougail = Rougail()
    # FIXME replace with rougail.annotator()
    # rougail.converted.annotator()
    rougail.get_config()
    assert rougail.converted.paths._data["rougail.hello"].version == "1.0"


# def test_dictionary(test_dir):
#    assert getcwd() == ORI_DIR
#    test_dir = join(dico_dirs, test_dir)
#    launch_test(test_dir, 'dict')
#    assert getcwd() == ORI_DIR
