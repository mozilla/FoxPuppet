Development
===========

Automated Testing
-----------------

All pull requests and merges are tested in `Travis CI <https://travis-ci.org/>`_
based on the ``.travis.yml`` file.

Usually, a link to your specific travis build appears in pull requests, but if
not, you can find it on the
`pull requests page <https://travis-ci.org/mozilla/FoxPuppet/pull_requests>`_

The only way to trigger Travis CI to run again for a pull request, is to submit
another change to the pull branch.

Test coverage is done by `Coveralls <https://coveralls.io/>`_.

Running Tests
-------------

You will need `Tox <http://tox.testrun.org/>`_ installed to run the tests
against the supported Python versions.

You also need to have `Geckodriver <https://github.com/mozilla/geckodriver>`_ installed so the tests can run Firefox.

.. code-block:: bash

  $ pip install tox
  $ tox

Keeping up with Firefox
-----------------------

As Firefox evolves, it will be necessary for FoxPuppet to keep up. This will likely
present itself as a test failure introduces in Firefox nightly. FoxPuppet's tests are
configures to run on Travis CI `every day <https://travis-ci.org/mozilla/FoxPuppet/builds>`_,
which alerts us of regressions or more likely changes in Firefox that we need to adapt
to.

When such failures occur, the following guide may help to determine the change that
introduced the failure, and the fix that may be needed.

Replicate the failure
~~~~~~~~~~~~~~~~~~~~~

To run the tests against a specific Firefox version (you'll typically want Nightly)
make sure the ``PATH`` environment variable is front-loaded with the path to the target
binary. Note that you want the path that *contains* the binary, and not the path of the
binary itself. Although this part should run fine in Python 3, it's worth targeting
2.7 using ``-e py27`` as the following steps currently require it. It's also a good idea to narrow the tests being run using ``-k`` as shown in this example:

.. code-block:: bash

  $ export MOZ_HEADLESS=1
  $ export PATH=/Applications/FirefoxNightly.app/Contents/MacOS:$PATH
  $ tox -e py27 -- -k test_tracking_protection_shield

Determine the regression range
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run ``mozregression`` to determine the change that introduced the failure. Create a
temporary virtual environment using Python 2.7 and install both ``tox`` and
``mozregression``. You can then use ``mozregression`` providing the last time the test
was known to pass, and the first time it was known to fail. This can be determined by
the dates in the Travis CI results. Modify the following to suit your needs:

.. code-block:: bash

  $ mozregression -b 2018-08-12 -g 2018-08-11 -c "tox -e py27 -- -k test_tracking_protection_shield"

This will identify the builds within the range, and systematically download and execute
the tests against the builds to identify the change that caused the failure. You don't
need to worry about ``PATH`` as the FoxPuppet tests use the ``MOZREGRESSION_BINARY``
environment variable if it's set.

Assuming everything goes as expected, mozregression will report the last good revision,
first bad revision, and provide a pushlog URL showing the change(s) that caused the
regression. From this, it should be possible to determine if the failure is expected
due to changes in Firefox, or if a bug has been introduced.

Supporting latest Firefox versions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If behaviour changes in Firefox and FoxPuppet needs to be updated, it is sometimes
necessary to change the behaviour in FoxPuppet based on the Firefox version.
