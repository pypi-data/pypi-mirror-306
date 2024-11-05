from sendgrid_ovh.lib.SendGridWhiteLabel import SendGridWhiteLabel
from sendgrid_ovh.lib.Output import Output
from sendgrid_ovh.zone.zone import Zone
import click
from rich.prompt import Confirm
from python_http_client import NotFoundError


@click.group('sendgrid')
def command_sendgrid():
    pass


@click.group('authenticated-domains')
def command_authenticated_domains():
    pass


@click.command(name='create')
@click.argument('domain', required=True)
@click.option('--zone-handler')
def command_domain_authenticate(domain, zone_handler):
    SendGrid().authenticate_a_domain(domain, zone_handler)


@click.command(name='list')
@click.option('--only-not-validated', help='Ouput only domains not validated', is_flag=True)
def command_list_all_authenticated_domains(only_not_validated):
    SendGrid().list_authenticated_domains(only_not_validated)


@click.command(name='get')
@click.argument('domain_id', required=True, type=int)
def command_get_authenticated_domain_id(domain_id):
    SendGrid().get_authenticated_domain_id(domain_id)


@click.command(name='search')
@click.argument('domain', required=True)
@click.option('--only-ids', help='Ouput only matching ids', is_flag=True)
def command_search_authenticated_domain(domain, only_ids):
    SendGrid().search_authenticated_domain(domain, only_ids)


@click.command(name='delete')
@click.argument('domain_id', required=True, type=int)
def command_delete_authenticated_domain_id(domain_id):
    SendGrid().delete_authenticated_domain_id(domain_id)


@click.command(name='validate')
@click.argument('domain_id', required=True, type=int)
def command_validate_authenticated_domain_id(domain_id):
    SendGrid().valite_authenticated_domain_id(domain_id)


command_sendgrid.add_command(command_authenticated_domains)
command_authenticated_domains.add_command(command_list_all_authenticated_domains)
command_authenticated_domains.add_command(command_domain_authenticate)
command_authenticated_domains.add_command(command_search_authenticated_domain)
command_authenticated_domains.add_command(command_get_authenticated_domain_id)
command_authenticated_domains.add_command(command_delete_authenticated_domain_id)
command_authenticated_domains.add_command(command_validate_authenticated_domain_id)


class SendGrid:

    def __init__(self):
        self.client = SendGridWhiteLabel()
        self.output = Output()
        self.ovh = Zone()

    def authenticate_a_domain(self, domain, zone_handler):
        result = self.client.create_domain_authentication(domain)
        records = result['dns']
        records['_dmarc'] = {
            'type': 'txt',
            'host': '_dmarc.' + domain,
            'data': 'v=DMARC1; p=none;',
            'valid': 'Not validated'
        }
        self.output.sendgrid_records(records.values())
        self.output.success("Domain ({}) has been created with id ({})".format(domain, result['id']))
        if zone_handler and zone_handler.lower() == 'ovh':
            self.ovh.create_sendgrid_records(records.values())
            self.ovh.refresh(domain)

    def list_authenticated_domains(self, only_not_validated):
        domains = self.client.list_all_authenticated_domains()
        if only_not_validated:
            domains = [ domain for domain in domains if not domain['valid']]
        self.output.sendgrid_domains(domains)

    def search_authenticated_domain(self, domain, only_ids):
        domains = self.client.search_authenticated_domains(domain)
        if only_ids:
            for domain in domains:
                print(domain['id'])
        else:
            self.output.sendgrid_domains(domains)

    def get_authenticated_domain_id(self, domain_id):
        domain = self.client.get_authenticated_domain_id(domain_id)
        self.output.sendgrid_records(domain['dns'].values())

    def delete_authenticated_domain_id(self, domain_id):
        if self._is_valid(domain_id):
            self.output.error("Valid domains can't be deleted by this app.Delete them manually")
            self.get_authenticated_domain_id(domain_id)
            exit(1)
        result = self.client.delete_authenticated_domain_id(domain_id)
        if result == "deleted":
            self.output.success("domain_id ({}) successfully deleted.".format(domain_id))
        else:
            self.output.error(result)
            exit(1)

    def valite_authenticated_domain_id(self, domain_id):
        result = self.client.validate_authenticated_domain_id(domain_id)
        if result['valid']:
            self.output.success("Domain_id ({}) is valid.".format(domain_id))
        else:
            self.output.error("Domain_id ({}) is NOT valid.".format(domain_id))
            self.get_authenticated_domain_id(domain_id)

    def _is_valid(self, domain_id):
        try:
            domain = self.client.get_authenticated_domain_id(domain_id)
        except NotFoundError as e:
            self.output.error("domain_id ({}) not found".format(domain_id))
            exit(2)
        return domain['valid']






