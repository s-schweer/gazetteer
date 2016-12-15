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
    doc = '{foo: bar}\n'

    result = client.simulate_get('/config')
    assert result.text == doc