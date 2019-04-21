#! usr/bin/env python3
from setuptools import setup

setup(name='message_server',
    version='0.1',
    description='Simple message server',
    author='Rob Thomas',
    packages=['message_server'],
    install_requires=[
    ],
    tests_require=[
        'pytest',
        'pytest-cov'],
    zip_safe=False)
