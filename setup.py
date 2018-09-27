# -*- coding: utf-8 -*-

from __future__ import absolute_import
from setuptools import setup, find_packages
from github_users import __version__


# URL to the repository on Github.
REPO_URL = 'https://github.com/hanpeter/github-users'

# Github will generate a tarball as long as you tag your releases, so don't
# forget to tag!
DOWNLOAD_URL = ''.join((REPO_URL, '/tarball/release/', __version__))


setup(
    name='github-users',
    version=__version__,
    author='Peter Han',
    author_email='git@peterhan.me',
    description='CLI that returns a list of users in a GitHub organization',
    url=REPO_URL,
    download_url=DOWNLOAD_URL,
    packages=find_packages(exclude=['tests']),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development',
        'Topic :: Software Development :: Documentation',
        'Topic :: Utilities',
    ],
    install_requires=[
        'click',
        'github3.py',
    ],
    entry_points={
        'console_scripts': [
            'github-users=github_users:main',
        ],
    },
)
