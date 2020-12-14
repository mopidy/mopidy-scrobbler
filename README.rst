****************
Mopidy-Scrobbler
****************

.. image:: https://img.shields.io/pypi/v/Mopidy-Scrobbler
    :target: https://pypi.org/project/Mopidy-Scrobbler/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/circleci/build/gh/mopidy/mopidy-scrobbler
    :target: https://circleci.com/gh/mopidy/mopidy-scrobbler
    :alt: Travis CI build status

.. image:: https://img.shields.io/codecov/c/gh/mopidy/mopidy-scrobbler
    :target: https://codecov.io/gh/mopidy/mopidy-scrobbler
    :alt: Test coverage

`Mopidy <https://www.mopidy.com/>`_ extension for scrobbling played tracks to
`Last.fm <https://www.last.fm/>`_.

This extension requires a free user account at Last.fm.


Installation
============

Install by running::

    sudo python3 -m pip install Mopidy-Scrobbler

See https://mopidy.com/ext/scrobbler/ for alternative installation methods.


Configuration
=============

The extension is enabled by default when it is installed. You just need to add
your Last.fm username and password to your Mopidy configuration file::

    [scrobbler]
    username = alice
    password = secret

The following configuration values are available:

- ``scrobbler/enabled``: If the scrobbler extension should be enabled or not.
  Defaults to enabled.
- ``scrobbler/username``: Your Last.fm username.
- ``scrobbler/password``: Your Last.fm password.


Project resources
=================

- `Source code <https://github.com/mopidy/mopidy-scrobbler>`_
- `Issue tracker <https://github.com/mopidy/mopidy-scrobbler/issues>`_
- `Changelog <https://github.com/mopidy/mopidy-scrobbler/releases>`_


Credits
=======

- Original author: `Stein Magnus Jodal <https://github.com/jodal>`__
- Current maintainer: `Stein Magnus Jodal <https://github.com/jodal>`__
- `Contributors <https://github.com/mopidy/mopidy-scrobbler/graphs/contributors>`_
