import os
import requests

import pytest

# workaroud fixture within parametrize call
from tests.conftest import partners_dict


@pytest.mark.parametrize('partner', partners_dict)
def test_partner_url_and_logo(partner):
    logo_file = partners_dict[partner]
    r = requests.get(partner)
    r.raise_for_status()
    assert os.path.isfile(os.path.join('static/img/logo/', logo_file))
