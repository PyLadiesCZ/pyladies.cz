import os
import yaml

import pytest

# workaroud fixture within parametrize call
from tests.conftest import cities_yamls_dict


def test_mandatory_yml_files(cities_yamls):
    for city_yml, meetups_yml, _ in cities_yamls.values():
        assert os.path.isfile(city_yml)
        assert os.path.isfile(meetups_yml)


@pytest.mark.parametrize('city', cities_yamls_dict)
def test_mandatory_city_yml_loading(city):
    city_yml, _, _ = cities_yamls_dict[city]
    with open(city_yml) as f:
        yaml.load(f.read(), Loader=yaml.SafeLoader)


@pytest.mark.parametrize('city', cities_yamls_dict)
def test_mandatory_meetups_yml_loading(city):
    _, meetups_yml, _ = cities_yamls_dict[city]
    with open(meetups_yml) as f:
        yaml.load(f.read(), Loader=yaml.SafeLoader)


@pytest.mark.parametrize('city', cities_yamls_dict)
def test_team_yml_loading(city):
    _, _, team_yml = cities_yamls_dict[city]
    if not os.path.isfile(team_yml):
        pytest.skip("missing team.yml")
    with open(team_yml) as f:
        yaml.load(f.read(), Loader=yaml.SafeLoader)
