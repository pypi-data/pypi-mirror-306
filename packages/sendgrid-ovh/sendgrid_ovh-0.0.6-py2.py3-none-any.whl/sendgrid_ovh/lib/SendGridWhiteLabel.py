from sendgrid_ovh.lib.SendGridClientFactory import SendGridClientFactory
import json


class SendGridWhiteLabel():

    def __init__(self):
        self.client = SendGridClientFactory().build()

    def create_domain_authentication(self, domain):
        data = {
            "domain": domain,
            "subdomain": "",
            "username": "",
            "ips": [],
            "custom_spf": True,
            "default": False,
            "automatic_security": True
        }
        response = self.client.whitelabel.domains.post(
            request_body=data
        )
        return json.loads(response.body.decode('utf-8'))

    def list_all_authenticated_domains(self):
        response = self.client.whitelabel.domains.get(query_params={
            'limit': 1000,
        })
        body = json.loads(response.body.decode('utf-8'))
        return body

    def search_authenticated_domains(self, domain):
        response = self.client.whitelabel.domains.get(query_params={
            'domain': domain
        })
        body = json.loads(response.body.decode('utf-8'))
        return body

    def get_authenticated_domain_id(self, domain_id):
        response = self.client.whitelabel.domains._(domain_id).get()
        body = json.loads(response.body.decode('utf-8'))
        return body

    def delete_authenticated_domain_id(self, domain_id):
        response = self.client.whitelabel.domains._(domain_id).delete()
        if response.status_code == 204:
            return "deleted"
        else:
            body = json.loads(response.body.decode('utf-8'))
            return body

    def validate_authenticated_domain_id(self, domain_id):
        response = self.client.whitelabel.domains._(domain_id).validate.post()
        body = json.loads(response.body.decode('utf-8'))
        return body

