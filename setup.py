# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
"""FoxPuppet setup file for packaging."""

from setuptools import setup

setup(
    name="FoxPuppet",
    use_scm_version=True,
    description="Firefox user interface testing model for use with Selenium",
    long_description=open("README.rst").read(),
    author="Firefox Test Engineering",
    author_email="firefox-test-engineering@mozilla.com",
    url="https://github.com/mozilla/FoxPuppet",
    packages=[
        "foxpuppet",
        "foxpuppet.windows",
        "foxpuppet.windows.browser",
        "foxpuppet.windows.browser.notifications",
    ],
    install_requires=["selenium>=3.0.2"],
    setup_requires=["setuptools_scm"],
    license="Mozilla Public License 2.0 (MPL 2.0)",
    keywords="firefox ui testing mozilla selenium",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS :: MacOS X",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
        "Topic :: Utilities",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
    ],
)
