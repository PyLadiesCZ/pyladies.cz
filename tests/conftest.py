import os
import yaml

import pytest

from pyladies_cz import app, REDIRECTS

cities_yamls_dict = {d: (os.path.join('cities', d, 'city.yml'),
                         os.path.join('cities', d, 'meetups.yml'),
                         os.path.join('cities', d, 'team.yml'))
                     for d in os.listdir('cities')
                     if os.path.isdir(os.path.join('cities', d))}
feedbacks_yamls_dict = {d: os.path.join('cities', d, 'feedbacks.yml')
                        for d in os.listdir('cities')
                        if os.path.isfile(os.path.join('cities', d, 'feedbacks.yml'))}
simple_urls_list = [u.rule for u in app.url_map.iter_rules() if not u.arguments]
redirects_dict = REDIRECTS


with open('partners.yml') as f:
    partners_dict = {i['url']: i['logo-file']
                     for i in yaml.load(f.read(), Loader=yaml.SafeLoader)}


@pytest.fixture
def flask_app():
    return app


@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


@pytest.fixture
def feedbacks():
    feedbacks = list()
    for yml in feedbacks_yamls_dict.values():
        with open(yml) as f:
            feedbacks.extend(yaml.load(f.read(), Loader=yaml.SafeLoader))
    return feedbacks


@pytest.fixture
def cities_yamls():
    return cities_yamls_dict
