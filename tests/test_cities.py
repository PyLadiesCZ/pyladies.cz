import os
import yaml

import pytest


def test_mandatory_yml_files(city):
    city_yml, meetups_yml, _ = city[1]
    assert os.path.isfile(city_yml)
    assert os.path.isfile(meetups_yml)


def test_mandatory_city_yml_loading(city):
    city_yml, _, _ = city[1]
    with open(city_yml) as f:
        yaml.load(f.read(), Loader=yaml.SafeLoader)


def test_mandatory_meetups_yml_loading(city):
    _, meetups_yml, _ = city[1]
    with open(meetups_yml) as f:
        yaml.load(f.read(), Loader=yaml.SafeLoader)


def test_team_yml_loading(city):
    _, _, team_yml = city[1]
    if not os.path.isfile(team_yml):
        pytest.skip("missing team.yml")
    with open(team_yml) as f:
        yaml.load(f.read(), Loader=yaml.SafeLoader)
