import pytest
import json
from falcon import testing

from gazetteer import api


@pytest.fixture(scope='module')
def client():
    # Assume the hypothetical `myapp` package has a
    # function called `create()` to initialize and
    # return a `falcon.API` instance.
    config = dict(foo='bar',
               dns_server='172.17.0.2',
               domains=['example.net'])
    return testing.TestClient(api.create(config=config))


def test_get_config(client):
    doc = dict(foo='bar',
               dns_server='172.17.0.2',
               domains=['example.net'])

    result = client.simulate_get('/config')
    assert result.json == doc


def test_get_domains(client):
    result = client.simulate_get('/zones')
    domains = ['example.net']
    assert result.json == domains


def test_head_domain_exists(client):
    result = client.simulate_head('/zones/example.net')
    assert result.status == '200 OK'


def test_head_domain_not_exists(client):
    result = client.simulate_head('/zones/example.com')
    assert result.status == '404 Not Found'


def test_get_domain(client):
    doc = {"ftp": "ftp 86400 IN CNAME www", "www": "www 86400 IN A 192.168.0.2",
           "@": "@ 86400 IN SOA ns1 hostmaster 2002022401 10800 15 604800 10800; @ 86400 IN NS ns1; @ 86400 IN MX 10 mail.another.com.",
           "ns1": "ns1 86400 IN A 192.168.0.1", "bill": "bill 86400 IN A 192.168.0.3",
           "fred": "fred 86400 IN A 192.168.0.4"}

    result = client.simulate_get('/zones/example.net')
    assert result.json == doc


def test_get_a_records(client):
    doc = [{u'name': u'bill', u'address': u'192.168.0.3', u'ttl': u'86400'}, {u'name': u'fred', u'address': u'192.168.0.4', u'ttl': u'86400'},
           {u'name': u'ns1', u'address': u'192.168.0.1', u'ttl': u'86400'}, {u'name': u'www', u'address': u'192.168.0.2', u'ttl': u'86400'}]
    result = client.simulate_get('/zones/example.net/a_records')
    assert result.json == doc


def test_head_existing_a_record(client):
    result = client.simulate_head('/zones/example.net/a_records/bill')
    assert result.status == '200 OK'


def test_head_non_existing_a_record(client):
    result = client.simulate_head('/zones/example.net/a_records/alter')
    assert result.status == '404 Not Found'


def test_get_existing_a_record(client):
    doc = {u'address': u'192.168.0.3', u'name': u'bill', u'ttl': u'86400'}
    result = client.simulate_get('/zones/example.net/a_records/bill')
    assert result.json == doc

def test_put_a_record(client):
    a_record = json.dumps({'name': 'horst', 'address': '192.168.0.15', 'ttl': 86400})
    headers = {'Content-Type': 'application/json'}
    result = client.simulate_put('/zones/example.net/a_records', body=a_record, headers=headers)
    assert result.headers.get('location') == '/zones/example.net/a_records/horst'