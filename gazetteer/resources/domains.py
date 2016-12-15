__author__ = 'Stefan Schweer'
import dns.query
import dns.zone
import json
import falcon
import logging

logger = logging.getLogger(__name__)

class DomainCollectionResource(object):

    def __init__(self, config):
        self.config = config

    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.body = json.dumps(self.config.domains)
        resp.status = falcon.HTTP_200

class DomainResource(object):

    def __init__(self, config):
        self.config = config

    def on_head(self, req, resp, name):
        """Handles HEAD requests"""

        try:
            if name in self.config.domains:
                dns.zone.from_xfr(dns.query.xfr(self.config.dns_server, name))
                resp.status = falcon.HTTP_200
            else:
                raise Exception('not configured for domain {}'.format(name))
        except:
            resp.status = falcon.HTTP_404

    def on_get(self, req, resp, name):
        """Handles GET requests"""
        try:
            z = dns.zone.from_xfr(dns.query.xfr(self.config.dns_server, name))
            resp.status = falcon.HTTP_200
            entries = {}
            for n in sorted(z.nodes.keys()):
                entries[str(n)] = z[n].to_text(n).replace('\n', '; ')
            resp.body = json.dumps(entries)
        except Exception as e:
            logger.error(e)
            resp.status = falcon.HTTP_404

