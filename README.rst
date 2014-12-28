****************
Mopidy-Scrobbler
****************

.. image:: https://img.shields.io/pypi/v/Mopidy-Scrobbler.svg?style=flat
    :target: https://pypi.python.org/pypi/Mopidy-Scrobbler/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/Mopidy-Scrobbler.svg?style=flat
    :target: https://pypi.python.org/pypi/Mopidy-Scrobbler/
    :alt: Number of PyPI downloads

.. image:: https://img.shields.io/travis/mopidy/mopidy-scrobbler/master?style=flat
    :target: https://travis-ci.org/mopidy/mopidy-scrobbler
    :alt: Travis CI build status

.. image:: https://img.shields.io/coveralls/mopidy/mopidy-scrobbler/master?style=flat
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
- `Download development snapshot <https://github.com/mopidy/mopidy-scrobbler/tarball/master#egg=Mopidy-Scrobbler-dev>`_


Changelog
=========

v1.1.1 (UNRELEASED)
-------------------

- Updated to work with ``None`` as the default value of ``track_no`` in
  Mopidy's ``Track`` model. This was changed in Mopidy 0.20.

v1.1.0 (2014-01-20)
-------------------

- Updated extension API to match Mopidy 0.18.

v1.0.0 (2013-10-08)
-------------------

- Moved extension out of the main Mopidy project.

- Added test suite.
