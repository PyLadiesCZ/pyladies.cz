import requests

from lxml.html import fromstring


def test_v1_redirect(client, v1_redirect):
    rv = client.get(v1_redirect)
    redir_element = fromstring(rv.data).cssselect('a.meta-redirect')[0]
    r = requests.get(redir_element.get('href'))
    assert r.status_code == 200
