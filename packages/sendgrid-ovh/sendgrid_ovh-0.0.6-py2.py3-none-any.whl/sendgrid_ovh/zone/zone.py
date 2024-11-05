from sendgrid_ovh.lib.OVHZone import OVHZone
from sendgrid_ovh.lib.Output import Output
import click
from rich import print
import tldextract


@click.group(name='get')
def command_get():
    pass


@click.group(name='search')
def command_search():
    pass


@click.command(name='refresh')
@click.argument('domain', required=True)
def command_refresh(domain):
    Zone().refresh(domain)


@click.command(name='list')
def command_list():
    Zone().list()


@click.command(name='has')
@click.argument('domain', required=True)
def command_has(domain):
    Zone().has(domain)


@click.command(name='export')
@click.argument('domain', required=True)
def command_export(domain):
    Zone().export(domain)


@click.command(name='records')
@click.argument('domain', required=True)
def command_get_records(domain):
    Zone().get_records(domain)


@click.command(name='zone')
@click.argument('domain', required=True)
def command_get_zone(domain):
    Zone().get_zone(domain)


@click.command(name='record')
@click.argument('domain', required=True)
@click.argument('record_id', required=True)
def command_get_record(domain, record_id):
    Zone().get_record(domain, record_id)


@click.command(name='records')
@click.argument('domain', required=True)
@click.argument('search', required=True)
def command_search_records(domain, search):
    Zone().search_records(domain, search)


@click.group(name='create')
def command_create():
    pass


@click.command(name='record')
@click.argument('full_domain', required=True)
@click.argument('value', required=True)
@click.option('--field-type', required=True, default="TXT")
@click.option('--ttl', required=False, default=0)
def command_create_record(full_domain, value, field_type, ttl):
    Zone().create_record(full_domain, value, field_type, ttl)


@click.group(name='update')
def command_update():
    pass


@click.command(name='record')
@click.argument('domain', required=True)
@click.argument('record_id', required=True)
@click.argument('value', required=False)
@click.option('--subdomain', required=False)
@click.option('--ttl', required=False, default=0)
@click.option('--refresh', required=False, default=False, is_flag=True)
def command_update_record(domain, record_id, value, subdomain, ttl, refresh):
    Zone().update_record(domain, record_id, subdomain, value, ttl, refresh)


@click.group(name='delete')
def command_delete():
    pass


@click.command(name='record')
@click.argument('domain', required=True)
@click.argument('record_id', required=True)
def command_delete_record(domain, record_id):
    Zone().delete_record(domain, record_id)


command_get.add_command(command_get_records)
command_get.add_command(command_get_record)
command_get.add_command(command_get_zone)
command_create.add_command(command_create_record)
command_search.add_command(command_search_records)
command_delete.add_command(command_delete_record)
command_update.add_command(command_update_record)


class Zone:

    def __init__(self):
        self.client = OVHZone()
        self.output = Output()
        pass

    def list(self):
        for zone in self.client.get_all_zones():
            print(zone)
        exit(0)

    def has(self, domain):
        if self.client.has(domain):
            print("[bold green][SUCCESS][/bold green] Zone [italic]{}[/italic] is manageable".format(domain))
            exit(0)
        else:
            print("[bold red][ERROR][/bold red] Zone [italic]{}[/italic] is [bold]NOT[/bold] manageable".format(domain))
            exit(1)

    def export(self, domain):
        zone = self.client.export(domain)
        print(zone)

    def get_records(self, domain):
        records = self.client.get_records_details(domain)
        self.output.ovh_zone_records(domain, records)

    def search_records(self, domain, search):
        records = self.client.get_records_details(domain, search)
        self.output.ovh_zone_records(domain, records)

    def get_zone(self, domain):
        zone = self.client.get_zone(domain)
        self.output.ovh_zone(zone)

    def get_record(self, domain, record_id):
        record = self.client.get_record(domain, record_id)
        self.output.ovh_zone_records(domain, [record])

    def create_record(self, full_domain, value, field_type, ttl=0):
        parsed_domain = tldextract.extract(full_domain)
        result = self.client.create_record(parsed_domain.registered_domain, field_type, parsed_domain.subdomain, value, ttl)
        self.output.ovh_zone_records(parsed_domain.registered_domain, [result])
        self.output.success("Record ({}) has been created".format(result['id']))

    def delete_record(self, domain, record_id):
        result = self.client.delete_record(domain, record_id)
        if result is None:
            self.output.success("Record ({}) of domain ({}) has been deleted".format(record_id, domain))

    def refresh(self, domain):
        result = self.client.refresh(domain)
        if result is None:
            self.output.success("Zone of domain ({}) has been refreshed".format(domain))

    def update_record(self, domain, record_id, sub_domain, value, ttl, refresh):
        refreshed = False
        result = self.client.update_record(domain, record_id, sub_domain, value, ttl)
        if refresh:
            refreshed = self.client.refresh(domain)
        if result is None:
            self.output.success("Record ({}) of domain ({}) has been updated".format(record_id, domain))
        if refresh and refreshed is None:
            self.output.success("Zone of domain ({}) has been refreshed".format(domain))

    def create_sendgrid_records(self, records):
        for record in records:
            self.create_record(record['host'], record['data'] + '.', record['type'].upper())




