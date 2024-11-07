from .custom import CustomOption

from pathlib import Path
from pytest import fixture
from json import load, dump
from ruamel.yaml import YAML

from rougail import Rougail
from rougail.config import get_rougail_config
from rougail.user_data_file import RougailUserDataFile

EXT = "yml"
dico_dirs = Path('../rougail/tests/dictionaries')

# path configuration
ROUGAILCONFIG = get_rougail_config(backward_compatibility=False, add_extra_options=False)

test_ok = set()
excludes = set()
test_ok -= excludes

for test in dico_dirs.iterdir():
    if (test / 'tiramisu').is_dir() and test.name not in excludes:
        test_ok.add(test.name)
# test_ok = ['24_family_disabled_var_hidden']

test_ok = list(test_ok)
test_ok.sort()


@fixture(scope="module", params=test_ok)
def test_dir(request):
    return request.param


def test_dictionaries_all(test_dir):
    "tests the output"
    _test_dictionaries(test_dir, 'all')


def test_dictionaries_all_exclude(test_dir):
    "tests the output"
    _test_dictionaries(test_dir, 'all', True)


def test_dictionaries_mandatories(test_dir):
    "tests the output"
    _test_dictionaries(test_dir, 'mandatories')


def _get_rougailconfig(test_dir):
    "rougail config settings"
    rougailconfig = ROUGAILCONFIG.copy()
    rougailconfig['step.user_data'] = ['file']
    rougailconfig['main_namespace'] = 'rougail'
    dirs = [str(dico_dirs / test_dir / 'dictionaries' / 'rougail')]
    rougailconfig['custom_types']['custom'] = CustomOption
    rougailconfig['main_dictionaries'] = dirs
    rougailconfig['functions_files'] = ['../rougail/tests/eosfunc/test.py']
    return rougailconfig


def _test_dictionaries(test_dir, level, need_exclude=False):
    rougailconfig = _get_rougailconfig(test_dir)
    # populate tests if not already exists
    dest_dir = Path('tests') / 'results' / test_dir
    populate(dest_dir, rougailconfig, level, need_exclude)
    # loads the config in the tiramisu's meaning
    rougail = Rougail(rougailconfig)
    config = rougail.run()
    # loading the file
    if need_exclude:
        filename = dest_dir / 'file' / f'{level}_exclude.{EXT}'
    else:
        filename = dest_dir / 'file' / f'{level}.{EXT}'
    rougailconfig['file.filename'] = [str(filename)]
    # loads variables in the tiramisu config
    user_data = RougailUserDataFile(config,
                                    rougailconfig=rougailconfig,
                                    ).run()
    errors = rougail.user_datas(user_data)
    #expected output
    with open(Path('tests') / 'results' / test_dir /  'makedict' / f'{level}.json') as json_file:
        expected = load(json_file)
    # here is the effective test
    config.property.read_only()
    config_dict = dict(option_value(config.value.get()))
    errors_file = Path('tests') / 'results' / test_dir /  'errors' / f'{level}.json'
    if not errors_file.is_file():
        errors_file.parent.mkdir(parents=True, exist_ok=True)
        with open(errors_file, 'a') as json_file:
            dump(errors, json_file, indent=4)
    with open(errors_file) as json_file:
        expected_errors = load(json_file)
    assert  expected_errors == errors
    assert  expected == config_dict


def populate(dest_dir, rougailconfig, level, need_exclude):
    if need_exclude:
        filename = dest_dir / 'file' / f'{level}_exclude.{EXT}'
    else:
        filename = dest_dir / 'file' / f'{level}.{EXT}'
    makedict_file = dest_dir / 'makedict' / f'{level}.json'
    excludes = []
    if not filename.is_file() or not makedict_file.is_file():
        config = Rougail(rougailconfig).run()
        config.property.read_only()
        root_config = config.unrestraint
        if level == 'all':
            only = False
        else:
            only = True
        values = {}
        get_variables(root_config, values, only, excludes)
        if need_exclude:
            for exclude in excludes:
                _values = values
                *s_exclude, name = exclude.split('.')
                for _name in s_exclude:
                    if _name not in _values:
                        break
                    _values = _values[_name]
                else:
                    if name in _values:
                        del _values[name]
    if not filename.is_file():
        filename.parent.mkdir(parents=True, exist_ok=True)
        yaml = YAML()
        with filename.open('w') as fh:
            yaml.dump(values, fh)
    if  not makedict_file.is_file():
        makedict_file.parent.mkdir(parents=True, exist_ok=True)
        config.property.read_only()
        config_dict = dict(option_value(config.value.get()))
        with makedict_file.open('w') as fh:
            dump(config_dict, fh, indent=4)
            fh.write('\n')


def get_value(variable):
    if 'force_store_value' in variable.property.get():
        return variable.value.get()
    tests = variable.information.get('test', None)
    if tests:
        tests = list(tests)
    else:
        if variable.type() == 'integer':
            tests = [1, 2, 3]
        elif variable.type() == 'float':
            tests = [1.1, 2.2, 3.3]
        elif variable.type() == 'port':
            tests = ['80', '443']
        elif variable.type() == 'boolean':
            tests = [True]
        elif variable.type() == 'domain name':
            tests = ['domain1.lan', 'domain2.lan']
        elif variable.type() == 'choice':
            tests = variable.value.list()
        elif variable.type() == 'network address':
            if variable.extra('_cidr'):
                tests = ['192.168.1.0/24', '10.0.0.0/24']
            else:
                tests = ['192.168.1.0', '10.0.0.0']
        elif variable.type() == 'netmask address':
            tests = ['255.255.255.0', '255.255.0.0']
        elif variable.type() == 'IP':
            if variable.extra('_cidr'):
                tests = ['192.168.1.6/32', '10.0.10.0/24']
            else:
                tests = ['192.168.1.6', '10.0.10.10']
        else:
            tests = ['string1', 'string2', 'string3']
    if not variable.ismulti() or (variable.isfollower() and variable.issubmulti() is False):
        tests = tests[0]
    variable.value.set(tests)
    return tests


def get_variables(config, values, only, excludes, *, index=None):
    for idx, key in enumerate(config):
        if key.isoptiondescription():
            if key.isleadership():
                value = []
                leader = key.leader()
                if only and not leader.property.mandatory():
                    set_leader = False
                    leader_value = leader.value.get()
                else:
                    set_leader = True
                    leader_value = get_value(leader)
                for idx_, val in enumerate(leader_value):
                    if set_leader:
                        value.append({leader.name(): val})
                    else:
                        value.append({})
                    get_variables(key, value[-1], only, excludes, index=idx_)
                if value:
                    values[key.name()] = value
            else:
                value = {}
                get_variables(key, value, only, excludes)
                if value:
                    values[key.name()] = value
                if key.isdynamic(only_self=True):
                    identifier = key.identifiers(only_self=True, uncalculated=True)
                    exclude = key.information.get('dynamic_variable',
                                                               None,
                                                               )
                    if exclude:
                        identifiers = key.identifiers()[:-1]
                        if identifiers:
                            identifiers.reverse()
                            for identifier in identifiers:
                                exclude = exclude.replace('{{ identifier }}', str(identifier), 1)
                        excludes.append(exclude)
        else:
            if only:
                try:
                    mandatory = key.property.mandatory()
                except:
                    mandatory = False
            if not only or mandatory:
                if idx == 0 and index is not None:
                    continue
                if idx and index is not None and index != key.index():
                    continue
                value = get_value(key)
                values[key.name()] = value


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
