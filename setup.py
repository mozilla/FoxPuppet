# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from setuptools import setup

setup(name='FoxPuppet',
      use_scm_version=True,
      description='Firefox user interface testing model for use with Selenium',
      long_description=open('README.rst').read(),
      author='Firefox Test Engineering',
      author_email='firefox-test-engineering@mozilla.com',
      url='https://github.com/mozilla/FoxPuppet',
      license='MPL2',
      packages=['foxpuppet'],
      install_requires=['selenium>=3.0.1'],
      setup_requires=['setuptools_scm'])
