****************
Mopidy-Scrobbler
****************

.. image:: https://img.shields.io/pypi/v/Mopidy-Scrobbler
    :target: https://pypi.org/project/Mopidy-Scrobbler/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/github/actions/workflow/status/mopidy/mopidy-scrobbler/ci.yml?branch=main
    :target: https://github.com/mopidy/mopidy-scrobbler/actions
    :alt: CI build status

.. image:: https://img.shields.io/codecov/c/gh/mopidy/mopidy-scrobbler
    :target: https://codecov.io/gh/mopidy/mopidy-scrobbler
    :alt: Test coverage

`Mopidy <https://www.mopidy.com/>`_ extension for scrobbling played tracks to
`Last.fm <https://www.last.fm/>`_.

This extension requires a free user account at Last.fm.


Maintainer wanted
=================

Mopidy-Scrobbler is currently kept on life support by the Mopidy core developers.
It is in need of a more dedicated maintainer.

If you want to be the maintainer of Mopidy-Scrobbler, please:

1. Make 2-3 good pull requests improving any part of the project.

2. Read and get familiar with all of the project's open issues.

3. Send a pull request removing this section and adding yourself as the
   "Current maintainer" in the "Credits" section below. In the pull request
   description, please refer to the previous pull requests and state that
   you've familiarized yourself with the open issues.

   As a maintainer, you'll be given push access to the repo and the authority
   to make releases to PyPI when you see fit.


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
- Current maintainer: None. Maintainer wanted, see section above.
- `Contributors <https://github.com/mopidy/mopidy-scrobbler/graphs/contributors>`_
