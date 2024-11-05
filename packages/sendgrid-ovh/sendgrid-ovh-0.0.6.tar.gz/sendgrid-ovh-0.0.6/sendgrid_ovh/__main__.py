#!/usr/bin/env python3
import click
from sendgrid_ovh.sendgrid import sendgrid
from sendgrid_ovh.zone import zone


@click.group()
def cli():
    pass


cli.add_command(sendgrid.command_sendgrid)
cli.add_command(zone.command_get)
cli.add_command(zone.command_create)
cli.add_command(zone.command_search)
cli.add_command(zone.command_export)
cli.add_command(zone.command_list)
cli.add_command(zone.command_has)
cli.add_command(zone.command_delete)
cli.add_command(zone.command_update)
cli.add_command(zone.command_refresh)

if __name__ == '__main__':
    cli()
