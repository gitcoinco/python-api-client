# -*- coding: utf-8 -*-
"""Define the gitcoin python api client setup configuration."""
from codecs import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='gitcoin',
    version='0.0.1',
    description='The Gitcoin.co python API client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gitcoinco/python-api-client',
    author='Gitcoin',
    author_email='team@gitcoin.co',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Natural Language :: English',
    ],
    keywords='gitcoin api client bounties bounty rest',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=['requests'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-isort', 'pytest-cov', 'coverage', 'isort'],
    extras_require={
        'deploy': ['twine', 'wheel'],
    },
    project_urls={
        'Bug Reports': 'https://github.com/gitcoinco/python-api-client/issues',
        'Homepage': 'https://gitcoin.co',
        'Source': 'https://github.com/gitcoinco/python-api-client/',
        'API Project': 'https://github.com/gitcoinco/web',
    },
)
