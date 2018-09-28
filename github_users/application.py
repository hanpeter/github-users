# -*- coding: utf-8 -*-

from __future__ import absolute_import
import csv
import sys
import json
from pprint import pformat
from github3 import login, GitHub


class Application(object):
    DEFAULT_FIELD_NAMES = ['name', 'login']

    def __init__(self, github_token):
        """
        Log in to GitHub using the given token and grabs the user object of the logged in user

        .. seealso:: https://github.com/settings/tokens

        :param github_token: GitHub authentication token. If you don't have one, create one with `read:org` permission
                             from here: https://github.com/settings/tokens
        """
        # Login to github using the given token
        self._github = login(token=github_token)

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
        org = next(org for org in self._github.organizations() if org.login == org_name)

        for user in org.members():
            # For every user, grab the whole user object and yield
            # This will cause extra requests and slow things down, but performance for this application
            # is not that important and extra data is always nice
            user = self._github.user(username=user.login)

            user_dict = {}
            for field in field_names:
                value = getattr(user, field, '')
                if value is None:
                    value = ''
                user_dict[field] = value.encode('utf-8')

            yield user_dict

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
