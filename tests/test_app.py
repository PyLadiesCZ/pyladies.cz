import pytest

# workaroud fixture within parametrize call
from tests.conftest import simple_urls_list, cities_yamls_dict


@pytest.mark.parametrize('simple_url', simple_urls_list)
def test_simple_urls(client, simple_url):
    rv = client.get(simple_url)
    assert rv.status_code == 200


def test_about_section_content(client):
    rv = client.get('/ostatni/')
    assert 'Jak založit Pyladies ve tvém městě?' in rv.data.decode('utf-8')


@pytest.mark.parametrize('city', cities_yamls_dict)
def test_cities_urls(client, city):
    rv = client.get(f'/{city}/')
    rv_course = client.get(f'/{city}_course/')
    rv_info = client.get(f'/{city}_info/')
    assert rv.status_code == 200
    assert rv_course.status_code == 200
    assert rv_info.status_code == 200
