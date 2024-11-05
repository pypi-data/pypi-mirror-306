import sendgrid
import os
from sendgrid_ovh.lib.OnePasswordCli import OnePasswordCli


class SendGridClientFactory:

    def __init__(self):
        self.onepassword = OnePasswordCli()

    def build(self):
        if os.environ.get('SENDGRID_API_KEY'):
            return sendgrid.SendGridAPIClient().client
        elif self.onepassword.has_proper_sendgrid_env_variables():
            return sendgrid.SendGridAPIClient(
                api_key=self.onepassword.get_sendgrid_secret('api_key')
            ).client
        else:
            raise Exception('Unable to find Sendgrid API key in environment')
