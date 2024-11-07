# -*- coding: utf-8 -*-
from json import loads, dumps, dump
from os import listdir
from os.path import dirname, abspath, join, normpath, splitext, isfile
import sys
import warnings
import pytest

from tiramisu import OptionDescription, Config
from tiramisu.error import ValueWarning
from tests.dict.data.unicode1_leadership_value import get_description as get_description_unicode1_leadership_value, \
                                                      get_values as get_values_unicode1_leadership_value


warnings.simplefilter("always", ValueWarning)


def datapath():
    path_ = join(normpath(dirname(abspath(__file__))), 'data')
    if path_ not in sys.path:
        sys.path.insert(1, path_)
    return path_


def list_data(ext='.py'):
#    if ext == '.py':
#        return ['unicode1_leadership_requires.py']
    datadir = datapath()
    filenames = listdir(datadir)
    filenames.sort()
    ret = []
    for filename in filenames:
        # if filename.endswith(ext) and not filename.startswith('__'):
        if filename.endswith(ext) and not filename.startswith('__') and not 'not_equal' in filename and not 'callback' in filename and not filename == 'unicode2_copy.py' and not filename == 'unicode2_multi_copy.py':
#            if 'leadership' in filename:
#                print('FIXME')
#                continue
            ret.append(filename)
    return ret


def load_config(filename,
                add_extra_od=False,
                remote='minimum',
                clearable='minimum',
                root=None,
                ):
    modulepath = splitext(filename)[0]
    mod = __import__(modulepath)
    descr = mod.get_description()
    if add_extra_od:
        descr = OptionDescription('root', '', [descr])
    config = Config(descr)
    config.property.add('demoting_error_warning')
    if 'get_values' in dir(mod):
        mod.get_values(config, add_extra_od)

    form = [{'title': 'Configurer',
             'type': 'submit'}]
    if 'get_form' in dir(mod):
        form.extend(mod.get_form(add_extra_od))
    config.property.read_write()
    if root is None:
        values = loads(dumps(config.dict(remotable=remote, clearable=clearable, form=form)))
    else:
        values = loads(dumps(config.option(root).dict(remotable=remote, clearable=clearable, form=form)))
    return values


def parse_expected(schema, all_options):
    for key, value in schema['properties'].items():
        if 'properties' in value:
            parse_expected(value, all_options)
        elif value.get('type') != 'symlink':
            all_options.append(key)


def del_property(expected, prop):
    new_form = {}
    for key, form in expected['form'].items():
        if prop in form:
            del form[prop]
        if form:
            new_form[key] = form
    return new_form


def del_value_property(schema, form):
    all_options = []
    for key, root in schema.items():
        if 'properties' in root:
            del_value_property(root['properties'], form)
        else:
            is_remote = form.get(key) and form[key].get('remote', False)
            if 'value' in root and is_remote:
                del root['value']


def add_property(expected, prop, prop_value):
    all_options = []
    all_descroptions = []
    for key, root in expected['schema'].items():
        if 'properties' in root:
            parse_expected(root, all_options)
            all_descroptions.append(key)
        else:
            all_options.append(key)

    all_options.extend(all_descroptions)
    ordered_options = all_options.copy()
    new_form = {}
    buttons = []
    for key, form in expected['form'].items():
        if key == 'null':
            # for button
            buttons = form
        else:
            if 'collapse' not in form.keys():
                form[prop] = prop_value
            all_options.remove(key)
            new_form[key] = form
    for option in all_options:
        if option not in all_descroptions:
            new_form[option] = {prop: prop_value}
    ordered_form = {}
    for key in ordered_options:
        if key in new_form:
            ordered_form[key] = new_form[key]
    ordered_form['null'] = buttons
    return ordered_form



LISTDATA = list_data()


LISTDATA_MOD = []
idx = 0
while True:
    idx += 1
    list_files = list_data('.mod{}'.format(idx))
    if not list_files:
        break
    LISTDATA_MOD.extend(list_files)


@pytest.fixture(params=LISTDATA)
def filename(request):
    return request.param


@pytest.fixture(params=LISTDATA_MOD)
def filename_mod(request):
    return request.param


def test_jsons(filename):
    debug = False
    # debug = True
    datadir = datapath()
    if debug:
        print()
    # for clearable in ['minimum']:
    for clearable in ['minimum', 'none', 'all']:
        if debug:
            print('==> clearable', clearable)
        # for remote in ['all']:
        for remote in ['minimum', 'none', 'all']:
            if debug:
                print('  ==> remotable', remote)
            modulepath = splitext(filename)[0]
            if debug:
                print("    {} (remote: {}, clearable: {})".format(filename, remote, clearable))
            values = load_config(filename,
                                 remote=remote,
                                 clearable=clearable,
                                 )
            #
            if not isfile(join(datadir, modulepath + '.json')) and \
                    clearable == 'minimum' and \
                    remote == 'minimum':
                with open(join(datadir, modulepath + '.json'), 'w') as fh:
                    dump(values, fh, indent=2)
            with open(join(datadir, modulepath + '.json'), 'r') as fh:
                expected = loads(fh.read())
            if clearable == 'none':
                expected['form'] = del_property(expected, 'clearable')
            if remote == 'all':
                if 'tiramisu' in expected:
                    del expected['tiramisu']
                expected['form'] = del_property(expected, 'pattern')
            if clearable == 'all':
                expected['form'] = add_property(expected, 'clearable', True)
            if remote == 'all':
                expected['form'] = add_property(expected, 'remote', True)
            new_expected = {}
            for key, form in expected['form'].items():
                if key != 'null' and form.get('remote', False):
                    if 'dependencies' in form:
                        del form['dependencies']
                    if 'copy' in form:
                        del form['copy']
                    if 'not_equal' in form:
                        del form['not_equal']
                new_expected[key] = form
            expected['form'] = new_expected

            # properties are unordered
            for model in expected['model']:
                if 'properties' in model:
                    model['properties'] = set(model['properties'])
            for model in values['model']:
                if 'properties' in model:
                    model['properties'] = set(model['properties'])
            del_value_property(expected['schema'], expected['form'])
            if debug:
                from pprint import pprint
                pprint(values)
                print('----------------')
                pprint(expected)
            assert values == expected, "error in file {}".format(filename)


def loads_yml(fh, issub, modulepath):
    dico = loads(fh.read())
    if issub:
        new_dico_ori = {}
        for key, value in dico.items():
            key = modulepath + '.' + key
            if isinstance(value, list):
                new_value = []
                for val in value:
                    if isinstance(val, dict):
                        new_val = {}
                        for k, v in val.items():
                            new_val[modulepath + '.' + k] = v
                        val = new_val
                    new_value.append(val)
                value = new_value
            new_dico_ori[key] = value
            dico = new_dico_ori
        return dico


def test_jsons_subconfig(filename):
    debug = False
    # debug = True
    datadir = datapath()
    if debug:
        print()
    modulepath = splitext(filename)[0]
    if debug:
        print("    ", filename)
    values = load_config(filename, add_extra_od=True, root=modulepath)
    #
    with open(join(datadir, modulepath + '.json'), 'r') as fh:
        expected = loads(fh.read())
    # properties are unordered
    for model in expected['model'].values():
        if 'properties' in model:
            model['properties'] = set(model['properties'])
    for model in values['model'].values():
        if 'properties' in model:
            model['properties'] = set(model['properties'])
    # add root

    def change_key(schema):
        new_schema = {}
        for key_schema, val_schema in schema.items():
            key = modulepath + '.' + key_schema
            # val_schema['name'] = key
            if 'opt_path' in val_schema:
                val_schema['opt_path'] = modulepath + '.' + val_schema['opt_path']
            if 'properties' in val_schema:
                val_schema['properties'] = change_key(val_schema['properties'])
            new_schema[key] = val_schema
        return new_schema

    expected['schema'] = change_key(expected['schema'])
    new_form_all = {}
    for key, form in expected['form'].items():
        if key != 'null':
            key = modulepath + '.' + key
        new_form_all[key] = form
        if 'copy' in form:
            for idx, noteq in enumerate(form['copy']):
                form['copy'][idx] = modulepath + '.' + noteq
        if 'not_equal' in form:
            new_form = []
            for idx, not_equal in enumerate(form['not_equal']):
                for noteq in not_equal['options']:
                    new_form.append(modulepath + '.' + noteq)
                form['not_equal'][idx]['options'] = new_form
        if 'dependencies' in form:
            for dependency in form['dependencies'].values():
                for val1 in dependency.values():
                    if isinstance(val1, list):
                        for idx, lst in enumerate(val1):
                            val1[idx] = modulepath + '.' + lst
                    else:
                        for val2 in val1.values():
                            if isinstance(val2, list):
                                for idx, lst in enumerate(val2):
                                    val2[idx] = modulepath + '.' + lst

    expected['form'] = new_form_all
    new_model = {}
    for key, model in expected['model'].items():
        new_model[modulepath + '.' + key] = model
    expected['model'] = new_model
    if debug:
        from pprint import pprint
        pprint(values)
        print('----------------')
        pprint(expected)
    assert values == expected, "error in file {}".format(filename)


def test_updates(filename_mod):
    debug = False
    # debug = True
    datadir = datapath()
    if debug:
        print("test/data/" + filename_mod)
    for issub in [False, True]:
        idx = int(filename_mod[-1])
        modulepath = splitext(filename_mod)[0]
        mod = __import__(modulepath)
        descr = mod.get_description()
        if issub:
            descr = OptionDescription('root', '', [descr])
            root = modulepath
        else:
            root = None
        # dict before modification
        if not isfile(join(datadir, modulepath + '.dict')):
            dico_ori = None
        else:
            with open(join(datadir, modulepath + '.dict'), 'r') as fh:
                dico_ori = loads_yml(fh, issub, modulepath)
        # modify config
        with open(join(datadir, modulepath + '.mod{}'.format(idx)), 'r') as fh:
            body = loads(fh.read())['body']
            if issub:
                for value in body['updates']:
                    value['name'] = modulepath + '.' + value['name']
        # returns of set_updates
        if not isfile(join(datadir, modulepath + '.updates{}'.format(idx))):
            values = None
        else:
            with open(join(datadir, modulepath + '.updates{}'.format(idx)), 'r') as fh:
                values = loads(fh.read())
                if issub:
                    for lidx, key in enumerate(values['updates']):
                        values['updates'][lidx] = modulepath + '.' + key
                    if 'model' in values:
                        new_model = {}
                        for key, value in values['model'].items():
                            new_model[modulepath + '.' + key] = value
                        values['model'] = new_model
        # dict after modification
        if not isfile(join(datadir, modulepath + '.dict{}'.format(idx))):
            dico_mod = None
        else:
            with open(join(datadir, modulepath + '.dict{}'.format(idx)), 'r') as fh:
                dico_mod = loads_yml(fh, issub, modulepath)
        if root is None:
            root_path = ''
        else:
            root_path = '{}.'.format(root)
        for clearable in ['none', 'minimum', 'all']:
            for remote in ['none', 'minimum', 'all']:
                if debug:
                    print("  (remote: {}, clearable: {}, issub {}, root {}, root_path {})".format(remote, clearable, issub, root, root_path))
                for with_model in [False, True]:
                    config = Config(descr)
                    config.property.add('demoting_error_warning')
                    if 'get_values' in dir(mod):
                        mod.get_values(config, issub)
                    if isfile(join(datadir, modulepath + '.mod')):
                        with open(join(datadir, modulepath + '.mod'), 'r') as fh:
                            eval(fh.read())
                    if dico_ori is None:
                        if clearable == 'minimum' and remote == 'minimum':
                            with open(join(datadir, modulepath + '.dict'), 'w') as fh:
                                pouet
                                dump(config.value.get(), fh, indent=2)
                    else:
                        assert config.value.get() == dico_ori, "clearable {}, remote: {}, filename: {}".format(clearable, remote, filename_mod)
                    if root is None:
                        suboption = config
                    else:
                        suboption = config.option(root)
                    if with_model:
                        bodym = body.copy()
                        bodym['model'] = loads(dumps(suboption.dict(remotable=remote, clearable=clearable)))['model']
                    else:
                        suboption.dict(remotable=remote, clearable=clearable)
                        bodym = body
                    if with_model:
                        cal_values = suboption.updates(bodym)
                        if values is None:
                            if clearable == 'minimum' and remote == 'minimum':
                                with open(join(datadir, modulepath + '.updates{}'.format(idx)), 'w') as fh:
                                    dump(cal_values, fh, indent=2)
                        else:
                            if debug:
                                from pprint import pprint
                                pprint(cal_values)
                                print('------------')
                                pprint(values)
                            assert cal_values == values
                    else:
                        assert suboption.updates(bodym) == {}
                    if dico_mod is None:
                        if clearable == 'minimum' and remote == 'minimum':
                            with open(join(datadir, modulepath + '.dict{}'.format(idx)), 'w') as fh:
                                dump(config.value.dict(), fh, indent=2)
                    else:
                        assert config.value.dict() == dico_mod
