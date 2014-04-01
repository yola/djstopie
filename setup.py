#!/usr/bin/env python
from setuptools import setup
import djstoppy

setup(
    name=djstoppy.__name__,
    version=djstoppy.__version__,
    description=djstoppy.__doc__,
    author='Yola',
    author_email='engineers@yola.com',
    url=djstoppy.__urls__,
    packages=['djstoppy'],
    test_suite='nose.collector',
    install_requires=[
        'django >= 1.4, <= 1.6',
        'PyYAML==3.10',
        'ua-parser==0.3.5',
        'user-agents==0.2.0',
        'languish==0.0.3',
    ]
)
