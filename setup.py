#!/usr/bin/env python
from setuptools import setup
import djstopie

setup(
    name=djstopie.__name__,
    version=djstopie.__version__,
    description=djstopie.__doc__,
    author='Yola',
    author_email='engineers@yola.com',
    url=djstopie.__url__,
    packages=['djstopie'],
    test_suite='nose.collector',
    install_requires=[
        'django >= 1.4, <= 1.6',
        'PyYAML==3.10',
        'ua-parser==0.3.5',
        'user-agents==0.2.0'
    ]
)
