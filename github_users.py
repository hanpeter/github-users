# -*- coding: utf-8 -*-

from __future__ import absolute_import
import csv
from os.path import expanduser
from logging import getLogger
import click
from github3 import login


# To allow click to display help on '-h' as well
CONTEXT_SETTINGS = {
    'help_option_names': ['-h', '--help']
}


class Application(object):
    def __init__(self, github_token):
        # Login to github using the given token
        self._github = login(token=github_token)
        # Grabs the current user
        self._me = self._github.user()

    def get_users(self, org_name):
        # Find the organization with the given name
        # XXX: Assumes the given name is exact and looks for a perfect match
        # XXX: Assumes there is only 1 organization with the given name
        org = [org for org in self._github.iter_orgs(login=self._me.login) if org.login == org_name][0]

        for user in org.iter_members():
            yield self._github.user(login=user.login)

    def csv(self, org_name, file_name=expanduser('~/tmp/github_users.csv'), field_names=['name', 'login']):
        with open(file_name, 'w+') as csv_file:
            writer = csv.writer(csv_file, quoting=csv.QUOTE_ALL)

            writer.writerow(field_names)

            for user in self.get_users(org_name=org_name):
                values = [getattr(user, field, '') for field in field_names]
                writer.writerow(values)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('github_token')
@click.argument('org_name')
@click.argument('format', type=click.Choice(['csv']))
@click.option('--output-file', type=click.Path(), default=expanduser('~/tmp/github_users.csv'))
def main(github_token, org_name, format, output_file):
    app = Application(github_token=github_token)
    app.csv(org_name=org_name, file_name=output_file)
