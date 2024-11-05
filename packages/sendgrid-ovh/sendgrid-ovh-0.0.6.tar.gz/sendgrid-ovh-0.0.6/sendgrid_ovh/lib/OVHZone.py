from sendgrid_ovh.lib.OVHClientFactory import OVHClientFactory
import json


class OVHZone():

    def __init__(self):
        self.client = OVHClientFactory().build()

    def get_all_zones(self):
        return self.client.get('/domain/zone/')

    def has(self, domain):
        return domain in self.get_all_zones()

    def get_zone(self, domain):
        return self.client.get('/domain/zone/{}'.format(domain))

    def export(self, domain):
        return self.client.get('/domain/zone/{}/export'.format(domain))

    def get_records(self, domain):
        return self.client.get('/domain/zone/{}/record'.format(domain))

    def get_records_details(self, domain, sub_domain=None):
        records = []
        if sub_domain is not None:
            record_ids = self.client.get('/domain/zone/{}/record'.format(domain), subDomain=None)
        else:
            record_ids = self.client.get('/domain/zone/{}/record'.format(domain))
        for record_id in record_ids:
            records.append(self.get_record(domain, record_id))
        return records

    def get_record(self, domain, record_id):
        return self.client.get('/domain/zone/{}/record/{}'.format(domain, record_id))

    def delete_record(self, domain, record_id):
        return self.client.delete('/domain/zone/{}/record/{}'.format(domain, record_id))

    def create_record(self, domain, field_type, sub_domain, value, ttl=0):
        return self.client.post('/domain/zone/{}/record/'.format(domain),
                                    fieldType=field_type,
                                    subDomain=sub_domain,
                                    target=value,
                                    ttl=ttl)

    def update_record(self, domain, record_id, sub_domain, value, ttl=0):
        original_record = self.get_record(domain, record_id)
        return self.client.put('/domain/zone/{}/record/{}'.format(domain, record_id),
                                    subDomain=sub_domain if sub_domain is not None else original_record['subDomain'],
                                    target=value if value is not None else original_record['target'],
                                    ttl=int(ttl) if ttl is not None else original_record['ttl']
                               )

    def refresh(self, domain):
        return self.client.post('/domain/zone/{}/refresh'.format(domain))