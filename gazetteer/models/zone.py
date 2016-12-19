import json
import logging

import dns.query
import dns.zone
import dns.update
import dns.rdatatype

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class DnsZone(object):
    def __init__(self, name=None, dns_server=None):
        self.name = name
        self.zone = self._domain_xfer(name, dns_server)
        self.a_records = self._parse_a_records(self.zone)
        self.dns_server = dns_server

    def _domain_xfer(self, name, dns_server):
        try:
            return dns.zone.from_xfr(dns.query.xfr(dns_server, name))
        except Exception as e:
            raise Exception(e)

    def _parse_a_records(self, zone):
        a_records = []
        for (name, ttl, rdata) in zone.iterate_rdatas('A'):
            a_records.append(ARecord(str(name), str(ttl), str(rdata)))
        return a_records

    def a_records_as_dict(self):
        records = []
        for record in self.a_records:
            records.append(dict(name=record.name, ttl=record.ttl, address=record.address))
        return records

    def a_records_as_json(self):
        return json.dumps(self.a_records_as_dict())

    def add_a_record(self, doc):
        name = doc.get('name')
        ttl = doc.get('ttl')
        address = doc.get('address')
        try:
            a_record = ARecord(name, ttl, address)
            update = dns.update.Update(self.name)
            update.absent(name)
            update.add(name, ttl, dns.rdatatype.A, address)
            result = dns.query.tcp(update, self.dns_server)
            logger.info('creating a record for {} returned: {}'.format(name, result))
            self.a_records.append(a_record)
        except Exception as e:
            logger.error('adding record for {} failed: {}'.format(name, str(e)))
            raise Exception(e)
        return name

    def a_record_exists(self, name):
        for a_record in self.a_records:
            if a_record.name == name:
                return True
        return False

    def get_a_record(self, name):
        if self.a_record_exists(name):
            for record in self.a_records:
                if record.name == name:
                    return record.as_json()
        else:
            return None


class ARecord(object):
    def __init__(self, name, ttl, address):
        self.name = name
        self.ttl = ttl
        self.address = address

    def as_dict(self):
        return dict(name=self.name, ttl=self.ttl, address=self.address)

    def as_json(self):
        return json.dumps(self.as_dict())



