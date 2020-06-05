import os
import requests


def test_partner_url_and_logo(partner):
    r = requests.get(partner['url'])
    r.raise_for_status()
    assert os.path.isfile(os.path.join('static/img/logo/', partner['logo-file']))
