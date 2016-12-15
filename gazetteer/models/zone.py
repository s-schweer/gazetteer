__author__ = 'Stefan Schweer'

import dns.query
import dns.zone
import json

class DnsZone(object):

    def __init__(self, name=None, dns_server=None):
        self.name = name
        self.zone = self._domain_xfer(name, dns_server)
        self.a_records = self._parse_a_records(self.zone)


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
        records = {}
        for record in self.a_records:
            records[record.name] = dict(ttl=record.ttl, address=record.address)
        return records

    def a_records_as_json(self):
        return json.dumps(self.a_records_as_dict())

class ARecord(object):

    def __init__(self, name, ttl, address):
        self.name = name
        self.ttl = ttl
        self.address = address

    def as_dict(self):
        return {self.name: dict(ttl=self.ttl, address=self.address)}

    def as_json(self):
        return json.dumps(self.as_dict())
