__author__ = 'Stefan Schweer'

# Let's get this party started!
import json
from wsgiref import simple_server

import falcon

from gazetteer.config import YamlConfig
from gazetteer.resources import domains


# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class ConfigResource(object):
    def __init__(self, config):
        self.config = config

    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200  # This is the default status
        resp.body = json.dumps(self.config.entries)


def create(config_file=None):
    config = YamlConfig(config_file)
    # falcon.API instances are callable WSGI apps
    app = falcon.API()

    # Resources are represented by long-lived class instances
    config_resource = ConfigResource(config)

    # things will handle all requests to the '/things' URL path
    app.add_route('/config', config_resource)
    app.add_route('/domains', domains.DomainCollectionResource(config))
    app.add_route('/domains/{name}', domains.DomainResource(config))
    return app


app = create()

if __name__ == '__main__':
    httpd = simple_server.make_server('127.0.0.1', 8000, app)
    httpd.serve_forever()
