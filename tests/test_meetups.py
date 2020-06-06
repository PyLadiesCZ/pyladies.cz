import requests

import pytest

from pyladies_cz import read_meetups_yaml


def test_materials_urls_for_recent_meetups(city):
    _, meetups_yml, _ = city[1]
    meetups = read_meetups_yaml(meetups_yml)
    current_meetups = [m for m in meetups if m['current']]
    past_meetups = [m for m in meetups if not m['current']][:3]
    recent_meetups = current_meetups + past_meetups
    missing_materials_urls = []
    for m in recent_meetups:
        if 'materials' not in m:
            missing_materials_urls.append(m['name'])
            continue
        r = requests.get(m['materials'])
        r.raise_for_status()
    if missing_materials_urls:
        pytest.skip("Missing materials url for: {} / {}".format(city[0],
                                                                ", ".join(missing_materials_urls)))
