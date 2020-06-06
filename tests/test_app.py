import requests

from lxml.html import fromstring


def test_simple_url(client, simple_url):
    rv = client.get(simple_url)
    assert rv.status_code == 200


def test_about_section_content(client):
    rv = client.get('/ostatni/')
    assert 'Jak založit Pyladies ve tvém městě?' in rv.data.decode('utf-8')


def test_city_urls(client, city):
    rv = client.get(f'/{city[0]}/')
    rv_course = client.get(f'/{city[0]}_course/')
    rv_info = client.get(f'/{city[0]}_info/')
    assert rv.status_code == 200
    assert rv_course.status_code == 200
    assert rv_info.status_code == 200


def test_materials_dropdown_menu_urls(client):
    rv = client.get('/')
    a_elements = fromstring(rv.data).cssselect('ul.navbar-other li.materials-dropdown ul li a')
    assert len(a_elements)
    for a in a_elements:
        r = requests.get(a.get('href'))
        r.raise_for_status()
