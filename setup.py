#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
setup(name='huedefaultbrightness',
    version = '1.0.0',
    url = 'https://github.com/dabear/huedefaultbrightness.git',
    author = 'Bjorn Berg',
    author_email = 'bjorninges.spam@gmail.com',
    description = 'Sets up a philips hue to with a a brightnes similar to last time it was on',
    packages = find_packages(),
    install_requires=[
        'phue',
        'pytz'
    ],
    
)
