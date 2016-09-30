# -*- coding: utf-8 -*-

from __future__ import absolute_import
import csv
import sys
from logging import getLogger
import click
from github3 import login


# To allow click to display help on '-h' as well
CONTEXT_SETTINGS = {
    'help_option_names': ['-h', '--help']
}


class Application(object):
    def __init__(self, github_token):
        """
        Log in to GitHub using the given token and grabs the user object of the logged in user

        .. seealso:: https://github.com/settings/tokens

        :param github_token: GitHub authentication token. If you don't have one, create one with `read:org` permission
                             from here: https://github.com/settings/tokens
        """
        # Login to github using the given token
        self._github = login(token=github_token)
        # Grabs the current user
        self._me = self._github.user()

    def _get_users(self, org_name):
        """
        Finds one organization with the given name then yields users within the organization.
        Assumes the given name is exact and there is only 1 organization with the given name.

        :param org_name: Name of the organization to look for.
        :type org_name: str
        :return: List of users in the given organization
        """
        # Find the organization with the given name
        # GOTCHA: Assumes the given name is exact and looks for a perfect match
        # GOTCHA: Assumes there is only 1 organization with the given name
        org = [org for org in self._github.iter_orgs(login=self._me.login) if org.login == org_name][0]

        for user in org.iter_members():
            # For every user, grab the whole user object and yield
            # This will cause extra requests and slow things down, but performance for this application
            # is not that important and extra data is always nice
            yield self._github.user(login=user.login)

    def csv(self, org_name, output=None, field_names=['name', 'login']):
        """
        Creates a csv file containing all the users in the given organization and write it to output

        .. seealso:: https://developer.github.com/v3/users/#response-1

        :param org_name: Name of the GitHub organization whose users will be printed.
        :type org_name: str
        :param output: Path to the file that will be written. If the file exists, it will be overwritten, not appended.
                       If the file does not exist, it will be created.
                       If set to None, the users will be printed to stdout.
        :type output: str
        :param field_names: List of fields to be written. Refer to https://developer.github.com/v3/users/#response-1 on
                            the names of the fields. If invalid field is listed, the values will be all empty string.
        :type field_names: list[str]
        """
        # GOTCHA: Because stdout is not a file, context manager cannot be used
        if output is not None:
            out_stream = open(output, 'w+')
        else:
            out_stream = sys.stdout

        writer = csv.DictWriter(out_stream, fieldnames=field_names, quoting=csv.QUOTE_ALL)

        # The first row is always headers, which are the names of the fields as they are provided
        writer.writeheader()

        for user in self._get_users(org_name=org_name):
            # Create a dictionary of only requested fields for DictWriter
            user_dict = dict((field, getattr(user, field, '')) for field in field_names)
            writer.writerow(user_dict)

        out_stream.close()


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument(
    'github_token',
    # help=(
    #     "GitHub authentication token. If you don't have one, create one "
    #     "with `read:org` permission from here: https://github.com/settings/tokens"
    # ),
)
@click.argument('org_name')
@click.option(
    '--output-format',
    type=click.Choice(['csv', 'json', 'pprint']),
    default='pprint',
    help='The format in which you want the output.',
)
@click.option(
    '--output-file',
    type=click.Path(),
    default=None,
    help=(
        'Path to the file in which the output will be written. '
        'If the file exists, it will be overwritten, not appended. If the file does not exist, it will be created. '
        'If not set, the output will be printed to stdout.'
    )
)
def main(github_token, org_name, output_format, output_file):
    app = Application(github_token=github_token)
    app.csv(org_name=org_name, output=output_file)
