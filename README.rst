****************
Mopidy-Scrobbler
****************

.. image:: https://pypip.in/v/Mopidy-Scrobbler/badge.png
    :target: https://crate.io/packages/Mopidy-Scrobbler/
    :alt: Latest PyPI version

.. image:: https://pypip.in/d/Mopidy-Scrobbler/badge.png
    :target: https://crate.io/packages/Mopidy-Scrobbler/
    :alt: Number of PyPI downloads

.. image:: https://travis-ci.org/mopidy/mopidy-scrobbler.png?branch=master
    :target: https://travis-ci.org/mopidy/mopidy-scrobbler
    :alt: Travis CI build status

.. image:: https://coveralls.io/repos/mopidy/mopidy-scrobbler/badge.png?branch=master
   :target: https://coveralls.io/r/mopidy/mopidy-scrobbler?branch=master
   :alt: Test coverage

`Mopidy <http://www.mopidy.com/>`_ extension for scrobbling played tracks to
`Last.fm <http://www.last.fm/>`_.


Installation
============

Install by running::

    pip install Mopidy-Scrobbler

Or, if available, install the Debian/Ubuntu package from `apt.mopidy.com
<http://apt.mopidy.com/>`_.


Configuration
=============

Before starting Mopidy, you must add your Last.fm username and password to your
Mopidy configuration file::

    [scrobbler]
    username = alice
    password = secret


Project resources
=================

- `Source code <https://github.com/mopidy/mopidy-scrobbler>`_
- `Issue tracker <https://github.com/mopidy/mopidy-scrobbler/issues>`_
- `Download development snapshot <https://github.com/mopidy/mopidy-scrobbler/tarball/master#egg=Mopidy-Scrobbler-dev>`_


Changelog
=========

v0.1.0 (UNRELEASED)
-------------------

- Moved extension out of the main Mopidy project.
