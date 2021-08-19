# -*- coding: utf-8 -*-

from __future__ import absolute_import
from setuptools import setup, find_packages
from github_users import __version__


# URL to the repository on Github.
REPO_URL = 'https://github.com/hanpeter/github-users'

# Github will generate a tarball as long as you tag your releases, so don't
# forget to tag!
DOWNLOAD_URL = ''.join((REPO_URL, '/tarball/release/', __version__))

try:
    with open(path.join(path.dirname(__file__), 'README.md')) as f:
        long_description = f.read()
except Exception as e:
    # XXX: Intentional pokemon catch to prevent this read from breaking setup.py
    long_description = None


setup(
    name='github-users',
    version=__version__,
    author='Peter Han',
    author_email='git@peterhan.ca',
    description='CLI that returns a list of users in a GitHub organization',
    long_description=long_description,
    url=REPO_URL,
    download_url=DOWNLOAD_URL,
    packages=find_packages(exclude=['tests']),
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development',
        'Topic :: Software Development :: Documentation',
        'Topic :: Utilities',
    ],
    python_requires='~=3.9',
    # Make sure the license file is packaged up too
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'github-users=github_users:main',
        ],
    },
)
