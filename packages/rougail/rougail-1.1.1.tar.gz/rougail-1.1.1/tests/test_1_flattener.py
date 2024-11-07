from pytest import fixture, raises
from os import getcwd, listdir, environ, makedirs
from os.path import isfile, join, isdir, dirname
from shutil import rmtree, copyfile
import logging

environ['TIRAMISU_LOCALE'] = 'en'

from rougail import Rougail, RougailConfig
from rougail.error import DictConsistencyError
from .custom import CustomOption


logger = logging.getLogger()
logger.setLevel(logging.INFO)


dico_dirs = 'tests/dictionaries'

# if test_3_template.py failed, this temporary directory must be removed
tmp_dir = join(dico_dirs, 'tmp')
if isdir(tmp_dir):
    rmtree(tmp_dir)


test_ok = set()
test_raise = set()

for test in listdir(dico_dirs):
    if isdir(join(dico_dirs, test)):
        if isdir(join(dico_dirs, test, 'tiramisu')):
            test_ok.add(test)
        elif test != '__pycache__':
            test_raise.add(test)

excludes = set([
    '80family_several',
])
test_ok -= excludes
test_raise -= excludes
# test_ok = ['60_5family_dynamic_variable_outside_sub_suffix']
#test_ok = []
#test_raise = ['88valid_enum_invalid_default']
#test_raise = []
test_multi = True
#test_multi = False
test_base = test_multi
#test_base = True
#test_base = False
test_no_namespace = test_multi
#test_no_namespace = True
#test_no_namespace = False

ORI_DIR = getcwd()

debug = False
#debug = True

test_ok = list(test_ok)
test_raise = list(test_raise)
test_ok.sort()
test_raise.sort()

@fixture(scope="module", params=test_ok)
def test_dir(request):
    return request.param


@fixture(scope="module", params=test_raise)
def test_dir_error(request):
    return request.param


def get_tiramisu_filename(test_dir, subdir, multi, namespace):
    if not namespace and not multi:
        filename = 'no_namespace.py'
    elif not multi:
        filename = 'base.py'
    else:
        filename = 'multi.py'
    return join(test_dir, subdir, filename)


def load_rougail_object(test_dir, rougailconfig, multi=False, namespace=False):
    rougailconfig['functions_file'] = [join(dico_dirs, '../eosfunc/test.py')]
    dirs = [join(test_dir, 'dictionaries', 'rougail')]
    subfolder = join(test_dir, 'dictionaries', 'rougail2')
    if isdir(subfolder):
        dirs.append(subfolder)
    rougailconfig['dictionaries_dir'] = dirs
    extra_dictionaries = {}
    extras = listdir(join(test_dir, 'dictionaries'))
    extras.sort()
    for extra in extras:
        if extra in ['rougail', 'rougail2']:
            continue
        subfolder = join(test_dir, 'dictionaries', extra)
        if isdir(subfolder):
            extra_dictionaries[extra] = [subfolder]
    if extra_dictionaries:
        rougailconfig['extra_dictionaries'] = extra_dictionaries
    rougailconfig['tiramisu_cache'] = get_tiramisu_filename(test_dir, 'tmp', multi, namespace)
    rougailconfig['custom_types']['custom'] = CustomOption
    return Rougail(rougailconfig)


def save(test_dir, eolobj, multi=False, namespace=False, error=False):
    tiramisu_tmp = get_tiramisu_filename(test_dir, 'tmp', multi, namespace)
    tiramisu_tmp_dir = dirname(tiramisu_tmp)
    if isdir(tiramisu_tmp_dir):
        rmtree(tiramisu_tmp_dir)
    makedirs(tiramisu_tmp_dir)
    tiramisu_objects = eolobj.get_config()
    tiramisu_file = get_tiramisu_filename(test_dir, 'tiramisu', multi, namespace)
    tiramisu_dir = dirname(tiramisu_file)
    if not error:
        if not isdir(tiramisu_dir):
            raise Exception(f'creates {tiramisu_dir}')
        if not isfile(tiramisu_file) or debug:
            copyfile(tiramisu_tmp, tiramisu_file)
        with open(tiramisu_tmp, 'r') as fh:
            tiramisu_objects = fh.read()
        with open(tiramisu_file, 'r') as fh:
            tiramisu_objects_ori = fh.read()
        assert tiramisu_objects == tiramisu_objects_ori
        if isdir(tiramisu_tmp_dir):
            rmtree(tiramisu_tmp_dir)


def test_dictionary(test_dir):
    if not test_no_namespace:
        print('NAMESPACE!')
        return
    assert getcwd() == ORI_DIR
    test_dir_ = join(dico_dirs, test_dir)
    rougailconfig = RougailConfig.copy()
    rougailconfig['main_namespace'] = None
    if isfile(join(test_dir_, 'force_namespace')):
        return
    eolobj = load_rougail_object(test_dir_, rougailconfig)
    if not eolobj:
        return
    save(test_dir_, eolobj)
    assert getcwd() == ORI_DIR


def test_dictionary_namespace(test_dir):
    if not test_base:
        print('BASE!')
        return
    assert getcwd() == ORI_DIR
    test_dir_ = join(dico_dirs, test_dir)
    rougailconfig = RougailConfig.copy()
    rougailconfig['main_namespace'] = 'Rougail'
    eolobj = load_rougail_object(test_dir_, rougailconfig, namespace=True)
    if not eolobj:
        return
    save(test_dir_, eolobj, namespace=True)
    assert getcwd() == ORI_DIR


def test_dictionary_multi(test_dir):
    if not test_multi:
        print('MULTI!')
        return
    assert getcwd() == ORI_DIR
    test_dir_ = join(dico_dirs, test_dir)
    rougailconfig = RougailConfig.copy()
    rougailconfig['main_namespace'] = 'Rougail'
    eolobj = load_rougail_object(test_dir_, rougailconfig, multi=True)
    if not eolobj:
        return
    eolobj.add_path_prefix('1')
    eolobj.add_path_prefix('2')
    save(test_dir_, eolobj, multi=True)
    assert getcwd() == ORI_DIR


def test_error_dictionary(test_dir_error):
    assert getcwd() == ORI_DIR
    test_dir_ = join(dico_dirs, test_dir_error)
    errno = []
    rougailconfig = RougailConfig.copy()
    rougailconfig['main_namespace'] = 'Rougail'
    eolobj = load_rougail_object(test_dir_, rougailconfig, namespace=True)
    if eolobj is None:
        return
    for i in listdir(test_dir_):
        if i.startswith('errno_'):
            errno.append(int(i.split('_')[1]))
    if not errno:
        errno.append(0)
    with raises(DictConsistencyError) as err:
        save(test_dir_, eolobj, error=True)
    assert err.value.errno in errno, f'expected errno: {errno}, errno: {err.value.errno}, msg: {err}'
    tiramisu_tmp_dir = dirname(get_tiramisu_filename(test_dir_, 'tmp', False, True))
    if isdir(tiramisu_tmp_dir):
        rmtree(tiramisu_tmp_dir)
    assert getcwd() == ORI_DIR
