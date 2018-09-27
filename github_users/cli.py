# -*- coding: utf-8 -*-

from __future__ import absolute_import
import click
from github_users.__version__ import __version__
from github_users.application import Application


# To allow click to display help on '-h' as well
CONTEXT_SETTINGS = {
    'help_option_names': ['-h', '--help']
}


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
    version=__version__,
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
