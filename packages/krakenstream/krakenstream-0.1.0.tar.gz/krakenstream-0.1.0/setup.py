"""
setup.py

This script is used to package and distribute the KrakenStream module.
It uses setuptools to define the package, its dependencies, and entry points.

To install the package locally, run:
    python setup.py install

For development purposes, use:
    python setup.py develop
"""

from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as file:
    long_description = file.read()

setup(
    name='krakenstream',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    entry_points={},
    author='gahfy',
    author_email='g.herfray@gahfy.io',
    description='A simple Python client to interact with the Kraken cryptocurrency exchange API.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gahfy/krakenstream',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5',
)
