# -*- coding: utf-8 -*-

from __future__ import absolute_import
import csv
import sys
import json
from pprint import pformat
import click
from github3 import login


# To allow click to display help on '-h' as well
CONTEXT_SETTINGS = {
    'help_option_names': ['-h', '--help']
}


class Application(object):
    DEFAULT_FIELD_NAMES = ['name', 'login']
    VERSION = '0.0.2'

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

    def _get_users(self, org_name, field_names=DEFAULT_FIELD_NAMES):
        """
        Finds one organization with the given name then yields the given fields of each users in the organization
        as a list of dictionaries.
        Assumes the given name is exact and there is only 1 organization with the given name.

        :param org_name: Name of the organization to look for.
        :type org_name: str
        :param field_names: List of fields to be written. Refer to https://developer.github.com/v3/users/#response-1 on
                            the names of the fields. If invalid field is listed, the values will be all empty string.
        :type field_names: list[str]
        :return: List of users in the given organization
        """
        # Find the organization with the given name
        # GOTCHA: Assumes the given name is exact and looks for a perfect match
        # GOTCHA: Assumes there is only 1 organization with the given name
        org = [org for org in self._github.iter_orgs() if org.login == org_name][0]

        for user in org.iter_members():
            # For every user, grab the whole user object and yield
            # This will cause extra requests and slow things down, but performance for this application
            # is not that important and extra data is always nice
            user = self._github.user(login=user.login)
            yield dict((field, getattr(user, field, '').encode('utf-8')) for field in field_names)

    def csv(self, org_name, output=None, field_names=DEFAULT_FIELD_NAMES, *args, **kwargs):
        """
        Creates a csv file containing all the users in the given organization

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

        for user in self._get_users(org_name=org_name, field_names=field_names):
            writer.writerow(user)

        out_stream.close()

    def json(self, org_name, output=None, field_names=DEFAULT_FIELD_NAMES, *args, **kwargs):
        """
        Creates a json file containing all the users in the given organization

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

        json.dump(list(self._get_users(org_name=org_name, field_names=field_names)), out_stream)
        # json.dump() does not create an empty line at the end of the file. Make one manually.
        out_stream.write('\n')

        out_stream.close()

    def pprint(self, org_name, output=None, field_names=DEFAULT_FIELD_NAMES, *args, **kwargs):
        """
        Creates a text file containing all the users in the given organization

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

        out_stream.write(pformat(list(self._get_users(org_name=org_name, field_names=field_names))))
        # json.dump() does not create an empty line at the end of the file. Make one manually.
        out_stream.write('\n')

        out_stream.close()


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('org-name')
@click.option(
    '-t', '--github-token',
    envvar='GITHUB_TOKEN',
    required=True,
    help=(
        "GitHub authentication token. If you don't have one, create one "
        "with `read:org` permission from here: https://github.com/settings/tokens. "
        "Can be also set as `GITHUB_TOKEN` environment variable."
    ),
)
@click.option(
    '-f', '--output-format',
    # GOTCHA: Because getattr is used, it is very important for the user input to match the function name
    type=click.Choice(['csv', 'json', 'pprint']),
    default='pprint',
    help='The format in which you want the output. (default: pprint)',
)
@click.option(
    '-o', '--output',
    type=click.Path(),
    default=None,
    help=(
        'Path to the file in which the output will be written. '
        'If the file exists, it will be overwritten, not appended. If the file does not exist, it will be created. '
        'If not set, the output will be printed to stdout.'
    )
)
@click.option(
    '-n', '--field-names',
    type=str,
    multiple=True,
    default=Application.DEFAULT_FIELD_NAMES,
    help=(
        'List of fields to be written. Refer to https://developer.github.com/v3/users/#response-1 on '
        'the names of the fields. If invalid field is listed, the values will be all empty string.'
        '(default: ' + str(Application.DEFAULT_FIELD_NAMES) + ')'
    )
)
@click.version_option(
    version=Application.VERSION,
)
def main(org_name, github_token, output_format, output, field_names):
    """
    Prints out a list of users in the given GitHub organization.

    \b
    If you want a quick list:
        github-users krux
    If you want it in CSV:
        github-users krux -f csv
    If you want it in a CSV file:
        github-users krux -f csv -o ~/tmp/users.csv
    If you want the user's location also:
        github-users krux -n name -n login -n location
    """
    app = Application(github_token=github_token)
    # Figure out which function to call based on the user input.
    getattr(app, output_format)(org_name=org_name, output=output, field_names=field_names)
