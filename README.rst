****************
Mopidy-Scrobbler
****************

.. image:: https://img.shields.io/pypi/v/Mopidy-Scrobbler.svg?style=flat
    :target: https://pypi.python.org/pypi/Mopidy-Scrobbler/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/travis/mopidy/mopidy-scrobbler/master.svg?style=flat
    :target: https://travis-ci.org/mopidy/mopidy-scrobbler
    :alt: Travis CI build status

.. image:: https://img.shields.io/coveralls/mopidy/mopidy-scrobbler/master.svg?style=flat
   :target: https://coveralls.io/r/mopidy/mopidy-scrobbler?branch=master
   :alt: Test coverage

`Mopidy <https://www.mopidy.com/>`_ extension for scrobbling played tracks to
`Last.fm <https://www.last.fm/>`_.

This extension requires a free user account at Last.fm.


Installation
============

Install by running::

    pip install Mopidy-Scrobbler

Or, if available, install the Debian/Ubuntu package from `apt.mopidy.com
<https://apt.mopidy.com/>`_.


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


Credits
=======

- Original author: `Stein Magnus Jodal <https://github.com/jodal>`__
- Current maintainer: `Stein Magnus Jodal <https://github.com/jodal>`__
- `Contributors <https://github.com/mopidy/mopidy-scrobbler/graphs/contributors>`_


Changelog
=========

v1.2.1 (2019-03-10)
-------------------

- Require pylast < 3, as that version removed support for Python 2.7. (Fixes:
  #30)

v1.2.0 (2018-04-01)
-------------------

- Require pylast >= 1.6.0, which is the version packed in Debian stable.

- Fix compatability with pylast >= 2, which has removed the ``ScrobblingError``
  exception type.

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
