Development
===========

Automated Testing
-----------------

All pull requests and merges are tested in `Travis CI <https://travis-ci.org/>`_
based on the ``.travis.yml`` file.

Usually, a link to your specific travis build appears in pull requests, but if
not, you can find it on the
`pull requests page <https://travis-ci.org/pytest-dev/pytest-selenium/pull_requests>`_

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
