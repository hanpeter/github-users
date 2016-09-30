# -*- coding: utf-8 -*-

from __future__ import absolute_import
from setuptools import setup, find_packages


# We use the version to construct the DOWNLOAD_URL.
VERSION = '0.0.1'

# URL to the repository on Github.
REPO_URL = 'https://github.com/hanpeter/github-users'

# Github will generate a tarball as long as you tag your releases, so don't
# forget to tag!
DOWNLOAD_URL = ''.join((REPO_URL, '/tarball/release/', VERSION))


setup(
    name='github-users',
    version=VERSION,
    author='@hanpeter',
    description='Returns a list of users in a GitHub orgs as a csv file',
    url=REPO_URL,
    download_url=DOWNLOAD_URL,
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    py_modules=['github_users'],
    install_requires=[
        'click',
        'github3.py'
    ],
    entry_points={
        'console_scripts': [

        ],
    },
)
