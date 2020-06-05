import os
import yaml

import pytest

from pyladies_cz import app, REDIRECTS

cities = {d: (os.path.join('cities', d, 'city.yml'),
              os.path.join('cities', d, 'meetups.yml'),
              os.path.join('cities', d, 'team.yml'))
          for d in os.listdir('cities')
          if os.path.isdir(os.path.join('cities', d))}
feedbacks = {d: os.path.join('cities', d, 'feedbacks.yml')
             for d in os.listdir('cities')
             if os.path.isfile(os.path.join('cities', d, 'feedbacks.yml'))}
simple_urls = [u.rule for u in app.url_map.iter_rules() if not u.arguments]
v1_redirects = ['/v1/{}'.format(r) for r in REDIRECTS]

with open('partners.yml') as f:
    partners = yaml.load(f.read(), Loader=yaml.SafeLoader)


@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


@pytest.fixture
def feedbacks_all():
    return feedbacks


@pytest.fixture(params=feedbacks.items(), ids=feedbacks.keys())
def feedbacks_for_city(request):
    return request.param


@pytest.fixture(params=cities.items(), ids=cities.keys())
def city(request):
    return request.param


@pytest.fixture(params=simple_urls)
def simple_url(request):
    return request.param


@pytest.fixture(params=v1_redirects)
def v1_redirect(request):
    return request.param


@pytest.fixture(params=partners, ids=lambda x: x['url'])
def partner(request):
    return request.param
