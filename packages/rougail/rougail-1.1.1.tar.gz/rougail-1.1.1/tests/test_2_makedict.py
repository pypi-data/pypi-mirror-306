from os.path import isfile, join, isdir
from pytest import fixture
from os import listdir, mkdir, environ
from json import dump, load, dumps, loads
from pathlib import Path

environ['TIRAMISU_LOCALE'] = 'en'

from .custom import CustomOption
from tiramisu import Config
from tiramisu.error import PropertiesOptionError


dico_dirs = 'tests/dictionaries'


test_ok = set()

for test in listdir(dico_dirs):
    if isdir(join(dico_dirs, test)):
        if isdir(join(dico_dirs, test, 'tiramisu')):
            test_ok.add(test)

debug = False
#debug = True
excludes = set([])
#excludes = set([
#    '80leadership_subfamily',
#    '80valid_enum_variables',
#])

# excludes = set(['60_5family_dynamic_variable_outside_sub_suffix'])
test_ok -= excludes
# test_ok = ['04_1default_calculation_hidden']


test_ok = list(test_ok)
test_ok.sort()
no_test_base_multi = False
#no_test_base_multi = True
#no_test_base = True
no_test_base = False
#no_test_multi = True
no_test_multi = False


@fixture(scope="module", params=test_ok)
def test_dir(request):
    return request.param


def option_value(parent, key_is_option=False):
    for option, value in parent.items():
        if option.isoptiondescription():
            if not key_is_option and option.isleadership():
                ret = []
                for idx, datas in enumerate(option_value(value, key_is_option=True)):
                    sub_option, sub_value = datas
                    if not idx:
                        sub_option = sub_option.path()
                        key = sub_option
                        for val in sub_value:
                            ret.append({sub_option: val})
                    else:
                        index = sub_option.index()
                        sub_option = sub_option.path()
                        ret[index][sub_option] = sub_value
                yield key, ret
            else:
                yield from option_value(value, key_is_option)
        elif key_is_option:
            yield option, value
        else:
            yield option.path(), value


def launch_flattener(test_dir,
                     filename,
                     ):
    makedict_dir = join(test_dir, 'makedict')
    makedict_file = join(makedict_dir, 'base.json')
    makedict_before = join(makedict_dir, 'before.json')
    makedict_after = join(makedict_dir, 'after.json')
    informations_file = join(test_dir, 'informations.json')
    mandatory_file = Path(makedict_dir) / 'mandatory.json'

    modulepath = join(test_dir, 'tiramisu', filename + '.py')
    with open(modulepath) as fh:
        optiondescription = {}
        exec(fh.read(), {'CustomOption': CustomOption}, optiondescription)  # pylint: disable=W0122
    config = Config(optiondescription["option_0"])
    # change default rights
    ro_origin = config.property.default('read_only', 'append')
    ro_append = frozenset(ro_origin - {'force_store_value'})
    rw_origin = config.property.default('read_write', 'append')
    rw_append = frozenset(rw_origin - {'force_store_value'})
    config.property.setdefault(ro_append, 'read_only', 'append')
    config.property.setdefault(rw_append, 'read_write', 'append')

    config.information.set('test_information', 'value')
    config.property.read_only()
    config.property.remove('mandatory')
    config.information.set('info', 'value')
    if isfile(informations_file):
        with open(informations_file) as informations:
            for key, value in load(informations).items():
                if filename == 'base':
                    config.option(key).information.set('test_information', value)
                elif filename == 'no_namespace':
                    config.option(key.split('.', 1)[-1]).information.set('test_information', value)
                else:
                    for root in ['1', '2']:
                        config.option(f'{root}.{key}').information.set('test_information', value)
    #
    config_dict = dict(option_value(config.value.get()))
    if filename == 'base':
        if not isdir(makedict_dir):
            mkdir(makedict_dir)
        if not isfile(makedict_file) or debug:
            with open(makedict_file, 'w') as fh:
                dump(config_dict, fh, indent=4)
                fh.write('\n')
    elif filename == 'no_namespace':
        config_dict = {f'rougail.{path}': value for path, value in config_dict.items()}
    else:
        config_dict_prefix = {'1': {}, '2': {}}
        for key, value in config_dict.items():
            prefix, path = key.split('.', 1)
            if value and isinstance(value, list) and isinstance(value[0], dict):
                new_value = []
                for dct in value:
                    new_dct = {}
                    for k, v in dct.items():
                        k = k.split('.', 1)[-1]
                        new_dct[k] = v
                    new_value.append(new_dct)
                value = new_value
            config_dict_prefix[prefix][path] = value
        assert loads(dumps(config_dict_prefix['1'])) == loads(dumps(config_dict_prefix['2']))
        config_dict = config_dict_prefix['1']
    if not isfile(makedict_file):
        raise Exception('dict is not empty')
    with open(makedict_file, 'r') as fh:
        assert load(fh) == loads(dumps(config_dict)), f"error in file {makedict_file}"
    #
    value_owner(makedict_before, config, filename)
    # deploy
    ro = config.property.default('read_only', 'append')
    ro = frozenset(list(ro) + ['force_store_value'])
    config.property.setdefault(ro, 'read_only', 'append')
    rw = config.property.default('read_write', 'append')
    rw = frozenset(list(rw) + ['force_store_value'])
    config.property.setdefault(rw, 'read_write', 'append')
    config.property.add('force_store_value')
    #
    value_owner(makedict_after, config, filename)
    #
    mandatory(mandatory_file, config.value.mandatory(), filename)


def value_owner(makedict_value_owner, config, filename):
    ret = {}
    for key, value in option_value(config.value.get(), True):
        path = key.path()
        if not key.issymlinkoption() and key.isfollower():
            if path in ret:
                continue
            ret[path] = {'owner': [],
                         'value': [],
                         }
            for idx in range(0, key.value.len()):
                try:
                    option = config.option(path, idx)
                    ret[path]['value'].append(option.value.get())
                    ret[path]['owner'].append(option.owner.get())
                except PropertiesOptionError as err:
                    ret[path]['value'].append(str(err))
                    ret[path]['owner'].append('error')
        else:
            owner = key.owner.get()
            ret[path] = {'owner': owner,
                         'value': value,
                         }
    if filename == 'base':
        if not isfile(makedict_value_owner) or debug:
            with open(makedict_value_owner, 'w') as fh:
                dump(ret, fh, indent=4)
                fh.write('\n')
    elif filename == 'no_namespace':
        ret = {f'rougail.{path}': value for path, value in ret.items()}
    else:
        ret_prefix = {'1': {}, '2': {}}
        for key, value in ret.items():
            prefix, path = key.split('.', 1)
            ret_prefix[prefix][path] = value
        assert loads(dumps(ret_prefix['1'])) == loads(dumps(ret_prefix['2']))
        ret = ret_prefix['1']
    with open(makedict_value_owner, 'r') as fh:
        assert load(fh) == loads(dumps(ret)), f"error in file {makedict_value_owner}"


def mandatory(mandatory_file, mandatories, filename):
    ret = [opt.path() for opt in mandatories]
    if not mandatory_file.is_file():
        with mandatory_file.open('w') as fh:
            dump(ret, fh)
    if filename == 'no_namespace':
        ret = [f'rougail.{path}' for path in ret]
    elif filename == 'multi':
        ret_prefix = {'1': [], '2': []}
        for key in ret:
            prefix, path = key.split('.', 1)
            ret_prefix[prefix].append(path)
        assert ret_prefix['1'] == ret_prefix['2']
        ret = ret_prefix['1']
    with mandatory_file.open() as fh:
        assert ret == load(fh), f"error in file {mandatory_file}"


def test_dictionary(test_dir):
    if no_test_base:
        print('FIXME')
        return
    test_dir = join(dico_dirs, test_dir)
    launch_flattener(test_dir, 'base')


def test_dictionary_no_namespace(test_dir):
    test_dir = join(dico_dirs, test_dir)
    if isfile(join(test_dir, 'force_namespace')):
        return
    launch_flattener(test_dir, 'no_namespace')


def test_dictionary_multi(test_dir):
    if no_test_base_multi:
        print('FIXME')
        return
    test_dir = join(dico_dirs, test_dir)
    launch_flattener(test_dir, 'multi')
