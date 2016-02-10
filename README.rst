****************
Mopidy-Scrobbler
****************

.. image:: https://img.shields.io/pypi/v/Mopidy-Scrobbler.svg?style=flat
    :target: https://pypi.python.org/pypi/Mopidy-Scrobbler/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/Mopidy-Scrobbler.svg?style=flat
    :target: https://pypi.python.org/pypi/Mopidy-Scrobbler/
    :alt: Number of PyPI downloads

.. image:: https://img.shields.io/travis/mopidy/mopidy-scrobbler/master.svg?style=flat
    :target: https://travis-ci.org/mopidy/mopidy-scrobbler
    :alt: Travis CI build status

.. image:: https://img.shields.io/coveralls/mopidy/mopidy-scrobbler/master.svg?style=flat
   :target: https://coveralls.io/r/mopidy/mopidy-scrobbler?branch=master
   :alt: Test coverage

`Mopidy <http://www.mopidy.com/>`_ extension for scrobbling played tracks to
`Last.fm <http://www.last.fm/>`_.

This extension requires a free user account at Last.fm.


Installation
============

Install by running::

    pip install Mopidy-Scrobbler

Or, if available, install the Debian/Ubuntu package from `apt.mopidy.com
<http://apt.mopidy.com/>`_.


Configuration
=============

The extension is enabled by default when it is installed. You just need to add
your Last.fm username and password to your Mopidy configuration file, typically
found at ``~/.config/mopidy/mopidy.conf``::

    [scrobbler]
    username = alice
    password = secret

The following configuration values are available:

- ``scrobbler/enabled``: If the scrobbler extension should be enabled or not.
- ``scrobbler/username``: Your Last.fm username.
- ``scrobbler/password``: Your Last.fm password.


Project resources
=================

- `Source code <https://github.com/mopidy/mopidy-scrobbler>`_
- `Issue tracker <https://github.com/mopidy/mopidy-scrobbler/issues>`_


Changelog
=========

v1.2.0 (2015-02-10)
-------------------

- Allow scrobbling to Libre.fm. A session key must be created beforehand.
  This authentication launches the default Web browser to do so. If Mopidy is
  run by a user without a default Web browser or without access to the current
  display session, the URL given in the log output must be opened manually.

- This version introduces configuration changes. ``username`` and ``password``
  are now ``lastfm_username``, ``lastfm_password`` and ``librefm_username``,
  ``librefm_password`` for Last.fm and Libre.fm respectively.

v1.1.2 (2015-01-06)
-------------------

- Scrobble only the first given artist instead of a concatenated string of
  all existing artists to prevent Last.fm from creating bogus artist pages.

v1.1.1 (2014-12-29)
-------------------

- Updated to work with ``None`` as the default value of ``track_no`` in
  Mopidy's ``Track`` model. This was changed in Mopidy 0.19.5. (Fixes: #7)

v1.1.0 (2014-01-20)
-------------------

- Updated extension API to match Mopidy 0.18.

v1.0.0 (2013-10-08)
-------------------

- Moved extension out of the main Mopidy project.

- Added test suite.
