import pytest
import requests

from lxml.html import fromstring

# workaroud fixture within parametrize call
from tests.conftest import redirects_dict


@pytest.mark.parametrize('redirect', redirects_dict)
def test_redirects(client, redirect):
    rv = client.get(f'/v1/{redirect}')
    redir_element = fromstring(rv.data).cssselect('a.meta-redirect')[0]
    r = requests.get(redir_element.get('href'))
    print(redir_element.get('href'))
    assert r.status_code == 200
