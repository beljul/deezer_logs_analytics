# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='parser',
    version='0.0.1',
    description='Logs parser for Deezer providers',
    long_description=readme,
    author='Jullian Bellino',
    author_email='jullian.bellino@gmail.com',
    url='https://github.com/beljul/deezer_logs_analytics',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

