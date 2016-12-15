__author__ = 'Stefan Schweer'

import json
import logging

import falcon

from gazetteer.models.zone import DnsZone

logger = logging.getLogger(__name__)


class ARecordCollectionResource(object):
    """
    Return list of domains
    """

    def __init__(self, config):
        self.config = config

    def _get_zone(self, name):
        return DnsZone(name, self.config.dns_server)

    def on_get(self, req, resp, name):
        """Handles GET requests"""
        zone = self._get_zone(name)
        resp.body = zone.a_records_as_json()
        logger.debug(zone.a_records_as_json())
        resp.status = falcon.HTTP_200


class ARecordResource(object):
    """
    Handles A-Record objects
    """

    def __init__(self, config):
        self.config = config

    def _get_zone(self, name):
        return DnsZone(name, self.config.dns_server)

    def on_head(self, req, resp, name, record):
        """Handles HEAD requests"""

        try:
            z = self._get_zone(name)
            resp.status = falcon.HTTP_200
            if record in z.a_records_as_dict().keys():
                resp.status = falcon.HTTP_200
            else:
                resp.status = falcon.HTTP_404
        except Exception as e:
            logger.error(e)
            resp.status = falcon.HTTP_500

    def on_put(self):
        pass

    def on_post(self):
        pass

    def on_get(self, req, resp, name, record):
        """
        Handles GET requests
        :returns json domain object
        """
        try:
            z = self._get_zone(name)
            resp.status = falcon.HTTP_200
            entries = z.a_records_as_dict()
            resp.body = json.dumps({record: entries[record]})
        except Exception as e:
            logger.error(e)
            resp.status = falcon.HTTP_404
