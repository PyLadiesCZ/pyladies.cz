import os
import requests

import pytest

from pyladies_cz import read_meetups_yaml

# workaroud fixture within parametrize call
from tests.conftest import cities_yamls_dict


@pytest.mark.parametrize('city', cities_yamls_dict)
def test_materials_urls_for_recent_meetups(city):
    meetups = read_meetups_yaml(os.path.join('cities', city, 'meetups.yml'))
    current_meetups = [m for m in meetups if m['current']]
    past_meetups = [m for m in meetups if not m['current']][:3]
    recent_meetups = current_meetups + past_meetups
    missing_materials_url = False
    for m in recent_meetups:
        if 'materials' not in m:
            missing_materials_url = True
            continue
        r = requests.get(m['materials'])
        r.raise_for_status()
    if missing_materials_url:
        pytest.skip("at least one missing materials url")
