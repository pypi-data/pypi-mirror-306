from rich.table import Table
from rich.console import Console
from rich import print
from datetime import datetime


class Output:
    @staticmethod
    def error(message):
        print("[bold red]ERROR[/bold red] {}".format(message))

    @staticmethod
    def success(message):
        print("[bold green]SUCCESS[/bold green] {}".format(message))

    @staticmethod
    def _print_table(table):
        console = Console()
        console.print(table)

    @staticmethod
    def _true_green_false_red(boolean):
        if boolean:
            return "[green]True[/green]"
        else:
            return "[red]False[/red]"

    def sendgrid_domains(self, domains, title=None):
        table = Table(title=None)
        table.add_column('id')
        table.add_column('subdomain')
        table.add_column('domain')
        table.add_column('Valid')

        for domain in domains:
            table.add_row(str(domain['id']),
                          domain['subdomain'],
                          domain['domain'],
                          self._true_green_false_red(domain['valid'])
                          )

        self._print_table(table)

    def sendgrid_records(self, records, title=None):
        table = Table(title=title)
        table.add_column('Subdomain')
        table.add_column('Type')
        table.add_column('Value')
        table.add_column('Valid')

        for record in records:
            table.add_row(record['host'],
                          record['type'],
                          record['data'],
                          self._true_green_false_red(record['valid']))

        self._print_table(table)

    def ovh_zone_records(self, domain, records):
        table = Table(title="Records of {}".format(domain))
        table.add_column('ID')
        table.add_column('Subdomain')
        table.add_column('TTL')
        table.add_column('Type')
        table.add_column('Value')

        for record in records:
            table.add_row(str(record['id']), record['subDomain'], str(record['ttl']), record['fieldType'], record['target'])

        self._print_table(table)

    def ovh_zone(self, zone):
        table = Table(title="Details of zone of {}".format(zone['name']),
                      show_header=False,
                      show_lines=True)
        table.add_column('Key')
        table.add_column('Value')

        table.add_row('dnssecSupported', str(zone['dnssecSupported']))
        table.add_row('hasDnsAnycast', str(zone['hasDnsAnycast']))
        table.add_row('lastUpdate', datetime.fromisoformat(zone['lastUpdate']).strftime("%d/%m/%Y %H:%M:%S"))
        table.add_row('nameServers', "\n".join(zone['nameServers']))

        self._print_table(table)