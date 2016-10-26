# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from setuptools import setup


setup(
    name='FoxPuppet',
    version='0.1.0',
    description='Firefox user interface testing model for use with Selenium',
    long_description=open('README.rst').read(),
    url='https://github.com/mozilla/FoxPuppet',
    license='MPL2',
    packages=['foxpuppet'],
    install_requires=[
        'selenium>=3.0.1'
    ]
)
