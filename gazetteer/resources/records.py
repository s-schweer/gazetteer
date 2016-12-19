import json
import logging

import falcon

from gazetteer.models.zone import DnsZone

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def max_body(limit):

    def hook(req, resp, resource, params):
        length = req.content_length
        if length is not None and length > limit:
            msg = ('The size of the request is too large. The body must not '
                   'exceed ' + str(limit) + ' bytes in length.')

            raise falcon.HTTPRequestEntityTooLarge(
                'Request body is too large', msg)

    return hook

class ARecordCollectionResource(object):
    """
    Return list of domains
    """

    def __init__(self, config):
        self.config = config

    def _get_zone(self, name):
        return DnsZone(name, self.config.dns_server)

    def on_get(self, req, resp, zone):
        """Handles GET requests"""
        z = self._get_zone(zone)
        resp.body = z.a_records_as_json()
        logger.debug(z.a_records_as_json())
        resp.status = falcon.HTTP_200

    @falcon.before(max_body(64 * 1024))
    def on_put(self, req, resp, zone):
        try:
            a_record = req.context['doc']
            z = self._get_zone(zone)
            record_name = z.add_a_record(a_record)
            logger.info('adding a record for {} succeeded'.format(record_name))
        except KeyError:
            raise falcon.HTTPBadRequest(
                'Missing A-record',
                'An A-record must be submitted in the request body.')
        except Exception as e:
            logger.error(e)
            raise falcon.HTTPBadRequest(str(e))

        resp.status = falcon.HTTP_201
        resp.location = '/zones/%s/a_records/%s' % (zone, record_name)


class ARecordResource(object):
    """
    Handles A-Record objects
    """

    def __init__(self, config):
        self.config = config

    def _get_zone(self, name):
        return DnsZone(name, self.config.dns_server)

    def on_head(self, req, resp, zone, record):
        """Handles HEAD requests"""

        try:
            z = self._get_zone(zone)
            if z.a_record_exists(record):
                resp.status = falcon.HTTP_200
            else:
                resp.status = falcon.HTTP_404
        except Exception as e:
            logger.error(e)
            resp.status = falcon.HTTP_500


    def on_post(self):
        pass

    def on_get(self, req, resp, zone, record):
        """
        Handles GET requests
        :returns json domain object
        """
        try:
            z = self._get_zone(zone)
            entry = z.get_a_record(record)
            if entry is not None:
                resp.status = falcon.HTTP_200
                resp.body = entry
            else:
                resp.status = falcon.HTTP_404
        except Exception as e:
            logger.error(e)
            resp.status = falcon.HTTP_404
