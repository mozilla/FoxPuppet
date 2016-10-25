# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from setuptools import setup, find_packages


setup(
    name='FoxPuppet',
    version='0.1.0',
    description='Foxpuppet for Firefox UI testing',
    long_description='See http://foxpuppet.readthedocs.org/',
    url='https://github.com/mozilla/FoxPuppet',
    license='MPL',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pytest',
        'selenium>=3.0.1'
    ]
)
