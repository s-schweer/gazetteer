__author__ = 'Stefan Schweer'
import pytest
from falcon import testing

from gazetteer import app


@pytest.fixture(scope='module')
def client():
    # Assume the hypothetical `myapp` package has a
    # function called `create()` to initialize and
    # return a `falcon.API` instance.
    return testing.TestClient(app.create())


def test_get_config(client):
    doc = dict(foo='bar',
               dns_server='172.17.0.2',
               domains=['example.net'])

    result = client.simulate_get('/config')
    assert result.json == doc

def test_get_domains(client):
    result = client.simulate_get('/domains')
    domains = ['example.net']
    assert result.json == domains

def test_head_domain_exists(client):
    result = client.simulate_head('/domains/example.net')
    assert result.status == '200 OK'

def test_head_domain_not_exists(client):
    result = client.simulate_head('/domains/example.com')
    assert result.status == '404 Not Found'

def test_get_domain(client):
    doc = {"ftp": "ftp 86400 IN CNAME www", "www": "www 86400 IN A 192.168.0.2", "@": "@ 86400 IN SOA ns1 hostmaster 2002022401 10800 15 604800 10800; @ 86400 IN NS ns1; @ 86400 IN MX 10 mail.another.com.", "ns1": "ns1 86400 IN A 192.168.0.1", "bill": "bill 86400 IN A 192.168.0.3", "fred": "fred 86400 IN A 192.168.0.4"}

    result = client.simulate_get('/domains/example.net')
    assert result.json == doc