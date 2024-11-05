import ovh
import os
import subprocess
from sendgrid_ovh.lib.OnePasswordCli import OnePasswordCli


class OVHClientFactory:
    # https://api.ovh.com/createToken/?GET=/domain/zone/*&POST=/domain/zone/*&PUT=/domain/zone/*&DELETE=/domain/zone/*

    def __init__(self):
        self.onepassword = OnePasswordCli()

    def build(self):
        if self.onepassword.has_proper_ovh_env_variables():
            return ovh.Client(
                endpoint='ovh-eu',
                application_key=self.onepassword.get_ovh_secret('application_key'),
                application_secret=self.onepassword.get_ovh_secret('application_secret'),
                consumer_key=self.onepassword.get_ovh_secret('consumer_key'),
            )
        else:
            raise Exception('Only auth method supported is 1Password. Create the mandatory env variables')

