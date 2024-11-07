# from json import dumps, loads
import asyncio
from os import environ
try:
    from tiramisu_api import Config
    class TestConfig(Config):
        def __init__(self,
                     config):
            self.test_option = config.option
            json = self.test_option.dict()
            # assert json == loads(dumps(json))
            super().__init__(json)

        def send_data(self,
                      updates):
            return self.updates_data(self.test_option.updates(updates))
    PARAMS = ['tiramisu', 'tiramisu-api']
except:
    PARAMS = ['tiramisu']

import pytest


def get_config(config, type, error=False):
    if type == 'tiramisu':
        return config
    if error:
        config.property.add('demoting_error_warning')
    return TestConfig(config)


def value_list(values):
    if values[0] == '':
        del values[0]
    return tuple(values)


def global_owner(config, config_type):
    return config.owner.get()


@pytest.fixture(params=PARAMS)
def config_type(request):
    return request.param


def parse_od_get(dico):
    ret = {}
    for k, v in dico.items():
        if k.isoptiondescription():
            if k.isleadership():
                leader_path = k.leader().path()
                ret_leadership = []
                for variable, value in v.items():
                    if variable.path() == leader_path:
                        for val in value:
                            ret_leadership.append({leader_path: val})
                    else:
                        ret_leadership[variable.index()][variable.path()] = value
                ret[leader_path] = ret_leadership
            else:
                ret.update(parse_od_get(v))
        else:
            ret[k.path()] = v
    return ret
